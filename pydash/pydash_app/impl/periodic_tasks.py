"""
Allows for the running of tasks in the background.

Still to be done:

- documentation

Example code with default scheduler:


    >>> import pydash_app.impl.periodic_tasks as pt
    >>> import datetime
    >>> pt.start_default_scheduler()
    >>> pt.add_periodic_task('foo', datetime.timedelta(seconds=3), pt.foo)
    >>> pt.add_periodic_task('bar', datetime.timedelta(seconds=5), pt.bar)
    >>> pt.add_periodic_task('bar', datetime.timedelta(seconds=1), pt.bar)
    >>> pt.add_background_task('baz', pt.baz)
    >>> pt.remove_task('bar')

Example code with custom scheduler:

    >>> import pydash_app.impl.periodic_tasks as pt
    >>> ts = pt.TaskScheduler()
    >>> import datetime
    >>> ts.start()
    >>> ts.add_periodic_task('foo', datetime.timedelta(seconds=1), pt.foo)
    >>> ts.add_periodic_task('bar', datetime.timedelta(seconds=5), pt.bar)
"""

import datetime
from time import sleep
import multiprocessing
import queue
from pqdict import pqdict

class _Task:
    def __init__(self, name, target):
        """
        :name: An identifier to find this task again later (and e.g. remove or alter it). Can be any hashable (using a string or a tuple of strings/integers is common.)
        :target: A function (or other callable) that will perform this task's functionality.
        :run_at_start: If true, runs task right after it was added to the scheduler, rather than only after the first interval has passed.
        """
        if not callable(target) and target is not None:
            raise ValueError(f"`target` passed to _Task constructor should be callable (or None), but `{target}` is not.")

        self.name = name
        self.target = target

        self.next_run_dt = datetime.datetime.now()

    def __call__(self, *args, **kwargs):
        self.target(*args, **kwargs)

    def __hash__(self):
        return hash(self.name)

    def __eq__(self, other):
        return isinstance(other, _Task) and other.name == self.name

    def __repr__(self):
        return f"<{self.__class__.__name__} name={self.name}, target={self.target}, next_run_dt={self.next_run_dt}>"

class _TaskRemoval(_Task):
    """
    A placeholder '_Task' that will indicate to the scheduler
    that the existing task that has `name` should be removed from the schedule.
    """
    def __init__(self, name):
        super().__init__(name, None, None)

class _BackgroundTask(_Task):
    """
    A task that is run only once, right after it is added to the scheduler.
    """
    def __init__(self, name, task):
        """
        :name: An identifier to find this task again later (and e.g. remove or alter it). Can be any hashable (using a string or a tuple of strings/integers is common.)
        :target: A function (or other callable) that will perform this task's functionality.
        """
        super().__init__(name, task)

class _PeriodicTask(_Task):
    """
    A task that is run many times periodically.
    """
    def __init__(self, name, task, interval, run_at_start=False):
        """
        :name: An identifier to find this task again later (and e.g. remove or alter it). Can be any hashable (using a string or a tuple of strings/integers is common.)
        :target: A function (or other callable) that will perform this task's functionality.
        :interval: A datetime.timedelta representing how frequently to run the given target.
        :run_at_start: If true, runs task right after it was added to the scheduler, rather than only after the first interval has passed.
        """
        super().__init__(name, task)

        if not isinstance(interval, datetime.timedelta):
            raise ValueError(f"`interval` is expected to be a `datetime.timedelta` instance, but `{interval}` is not.")

        self.interval = interval
        if not run_at_start:
            self.next_run_dt += interval

    def update_for_next_run(self):
        """
        Makes the Task ready to be re-run once the next period has passed.
        """
        # A conscious choice has been made to always update next_run_dt w.r.t the current time.
        # This means that even if a task's `next_run_dt` would lag behind,
        # the task would not be run multiple times right after another.
        self.next_run_dt = datetime.datetime.now() + self.interval
        return self.next_run_dt

    def __repr__(self):
        """
        Overrides superclass to show `interval` and `next_run_dt` in the string representation.
        """
        return f"<{self.__class__.__name__} name={self.name}, target={self.target}, interval={self.interval}, next_run_dt={self.next_run_dt}>"

class TaskScheduler:
    """
    Runs tasks in a process pool of subprocesses (See `multiprocessing.Pool`).
    The task scheduler itself, which passes tasks on to this process pool, runs its scheduling loop in a separate subprocess as well.
    This means that there is no computational overhead for the main process.
    """
    def __init__(self, granularity=1.0):
        """
        :granularity: How often the scheduler should check if a periodic task's timeout has passed, in seconds. Defaults to `1.0`.
        """
        self._task_queue = pqdict()
        self._pool = None
        self._granularity = granularity
        self._tasks_to_be_scheduled = multiprocessing.Queue()

    def add_periodic_task(self, name, interval, task, run_at_start=False):
        """
        Adds a task to be run periodically to the scheduler.

        :name: An identifier to find this task again later (and e.g. remove or alter it). Can be any hashable (using a string or a tuple of strings/integers is common.)
        (Calling this function again with the same name will override the earlier task).
        :target: A function (or other callable) that will perform this task's functionality.
        :interval: A datetime.timedelta representing how frequently to run the given target.
        :run_at_start: If true, runs task right after it was added to the scheduler, rather than only after the first interval has passed.

        """
        self._add_task(_PeriodicTask(name, task, interval=interval, run_at_start=run_at_start))

    def add_background_task(self, name, task):
        """
        Adds a task to be run only once (and as soon as possible) to the scheduler.

        :name: An identifier to find this task again later (and e.g. remove or alter it). Can be any hashable (using a string or a tuple of strings/integers is common.)
        (Calling this function again with the same name will override the earlier task).
        :target: A function (or other callable) that will perform this task's functionality.
        """
        self._add_task(_BackgroundTask(name, task))

    def remove_task(self, name):
        """
        Removes a task that was previously added from the scheduler.
        Will do nothing if there is no task with the given name.

        :name: The task with this name will be removed.
        """
        self._add_task(_TaskRemoval(name))

    def _add_task(self, task):
        self._tasks_to_be_scheduled.put(task)

    def start(self):
        """
        Starts the scheduler scheduling loop on a separate process.

        Should only be called once per scheduler.
        """
        if hasattr(self, '_scheduler_process'):
            raise Exception("TaskScheduler.start() called multiple times.")
        import atexit
        self._scheduler_process = multiprocessing.Process(target=self._scheduling_loop, daemon=False)
        # Ensure scheduler quits alongside main program
        atexit.register(self.stop)

        self._scheduler_process.start()

    def stop(self):
        """
        Stops the scheduler scheduling loop.

        Should only be called once per scheduler, and only after `start()` was called.
        When the program exits suddenly, this function will (in most cases) automatically be called
        to clean up the scheduling process.
        """
        if not hasattr(self, '_scheduler_process'):
            raise Exception("`TaskScheduler.stop()` called before calling `TaskScheduler.start()`")
        self._scheduler_process.terminate()

    def _scheduling_loop(self):
        with multiprocessing.Pool() as pool:
            while True:
                self._add_tasks_to_be_scheduled()
                current_time = datetime.datetime.now()
                self._run_waiting_tasks(pool, current_time)
                sleep(self._granularity)

    def _add_tasks_to_be_scheduled(self):
        try:
            while True:
                task = self._tasks_to_be_scheduled.get_nowait()
                if task.target == None:
                    print(f"Removing task {task.name} from internal pqueue")
                    self._task_queue.pop(task, default=None)
                else:
                    print(f"Adding task {task.name} to internal pqueue")
                    # Remove old task with same name if it existed
                    self._task_queue.pop(task, default=None)
                    # And then add new task with new priority
                    self._task_queue[task] = task.next_run_dt
        except queue.Empty:
            # Thrown by self._tasks_to_be_scheduled.get_nowait()
            # when this cross-process queue happens to be empty.
            pass

    def _run_waiting_tasks(self, pool, current_time):
        # TODO restructure into for-comprehension?
        while True:
            # Do nothing if empty
            if not self._task_queue:
                break

            task = self._task_queue.top()
            if task.next_run_dt <= current_time:
                print(f"Running task {task} at {current_time}...")
                self._task_queue.pop()
                self._run_task(pool, task)
                if isinstance(task, _PeriodicTask):
                    task.update_for_next_run()
                    self._task_queue[task] = task.next_run_dt
            else:
                break

    def _run_task(self, pool, task):
        res = pool.apply_async(task, ())
        res.get()


default_task_scheduler = TaskScheduler()

def add_periodic_task(name, interval, task, run_at_start=False, scheduler = default_task_scheduler):
    scheduler.add_periodic_task(name, interval, task)

def add_background_task(name, task, scheduler = default_task_scheduler):
    scheduler.add_background_task(name, task)

def remove_task(name, scheduler = default_task_scheduler):
    scheduler.remove_task(name)

def periodic_task(name, interval, run_at_start=False, scheduler = default_task_scheduler):
    """
    Function decorator to specify that the following function
    should be called periodically.

    Usage:

        @periodic_task('qux', datetime.timedelta(seconds=2))
        def qux():
            print('qux')


        @periodic_task('qux', datetime.timedelta(seconds=2), run_at_start=True, scheduler = your_scheduler)
        def qux():
            print('qux')

    """
    def task_decorator(task_function):
        add_periodic_task(name, interval, task_function, scheduler)
        return task_function

    return task_decorator

def start_default_scheduler():
    default_task_scheduler.start()

def foo():
    print('foo')

def bar():
    print('bar')

def baz():
    print('baz')

@periodic_task('qux', datetime.timedelta(seconds=2))
def qux():
    print('qux')
