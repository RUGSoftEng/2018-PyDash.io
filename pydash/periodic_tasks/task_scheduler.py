"""
Contains the meat of the task scheduling: The TaskScheduler class,
and a couple of classes that it uses under the hood.

"""

import os
import signal
import multiprocessing
import atexit
import datetime
from time import sleep
from pqdict import pqdict
logger = multiprocessing.log_to_stderr()
from .pqdict_iter_upto_priority import pqdict_iter_upto_priority
from .queue_nonblocking_iter import queue_nonblocking_iter

from pytest_cov.embed import cleanup

# import os
# if "TESTING" in os.environ:
#     multiprocessing.Process = threading.Thread

class _Task:
    """
    A task that can be run using the TaskScheduler.

    Usually you'd want to use one of the more concrete instances of this class.

    >>> def awesome_fun():
    ...   print("Awesome!")
    >>> task = _Task("mytask", awesome_fun)

    >>>
    >>> task = _Task("error_task", 10)
    Traceback (most recent call last):
      ...
    ValueError

    """

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
        """
        It is possible to manually call this task using arguments, but usually the functions do not contain extra arguments

        >>> def awesome_fun(text):
        ...   print(text)
        >>> task = _Task("mytask", awesome_fun)
        >>> task("Awesome!")
        Awesome!

        """
        if "TESTING" in os.environ:
            signal.signal(signal.SIGTERM, cleanup)

        try:
            return self.target(*args, **kwargs)
        except Exception as exception:
            import traceback
            logger.error(f"""---
            Task execution failed.
            Task: {self}
            Exception: {exception}
            Traceback:
            {traceback.format_exc()}
            ---
            """
            )


    def __hash__(self):
        """
        All tasks are hashed, such that two tasks with the same name are considered equal.
        This is to ensure that new instances of tasks with the same name replace old instances of these tasks inside the scheduler.


        >>> def awesome_fun1():
        ...   print("foo")
        >>> def awesome_fun2():
        ...   print("bar")
        >>> task = _Task("mytask", awesome_fun1)
        >>> task2 = _Task("mytask", awesome_fun1)
        >>> task == task2
        True
        >>> hash(task) == hash(task2)
        True
        """
        return hash(self.name)

    def __eq__(self, other):
        return isinstance(other, _Task) and other.name == self.name

    def __repr__(self):
        """
        Tasks have a special string representation for easy introspection.

        >>> def awesome_fun():
        ...   print("Awesome!")
        >>> task = _Task("mytask", awesome_fun)
        >>> f"{task}".startswith("<_Task name=mytask")
        True
        """
        return f"<{self.__class__.__name__} name={self.name}, target={self.target}, next_run_dt={self.next_run_dt}>"


class _TaskRemoval(_Task):
    """
    A placeholder '_Task' that will indicate to the scheduler
    that the existing task that has `name` should be removed from the schedule.
    """

    def __init__(self, name):
        super().__init__(name, None)


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

        It is expected that `interval` is a datetime.timedelta.

        >>> import periodic_tasks as pt
        >>> def awesome_fun():
        ...   print("Awesome!")
        >>> _PeriodicTask("foo", awesome_fun, 42)
        Traceback (most recent call last):
           ...
        ValueError

        """
        super().__init__(name, task)

        if not isinstance(interval, datetime.timedelta):
            raise ValueError(
                f"`interval` is expected to be a `datetime.timedelta` instance, but `{interval}` is not."
            )

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
    This means that there is no computational overhead for the main process at runtime.

    Internally, an indexable priority queue (c.f. the `pqdict` package) is used to keep track of the next tasks to run.
    This makes the scheduling loop quite efficient, because tasks are already ordered (so only the oldest task's desired execution moment needs to be compared to the current timestamp).
    Because the priority queue is indexed, adding and removing a task is also done in `O(log(n))`.

    Adding/updating/removing tasks is possible by using the same name as used previously for the task.
    Names can be strings, but also any other hashable object, so referring to a task based on a tuple of strings + integers is also possible.

    Tasks can be added/updated/removed at any time, including before the scheduler is started.

    The scheduler will be started by calling the `start()` function. It will stop scheduling and tear down the spawned processes when calling the `stop()` function.
    This function will also (in most cases) be automatically called when the main process finishes execution.
    """

    def __init__(self, granularity=0.1, pool_settings={}):
        """
        :granularity: How often the scheduler should check if a periodic task's timeout has passed, in seconds. Defaults to `1.0`.
        :pool_settings: A dictionary of keyword-arguments to pass to the initialization of the multiprocessing.Pool that will be used to run the tasks on.
        """
        self._task_queue = pqdict()
        self._pool = None
        self._granularity = granularity
        self._tasks_to_be_scheduled = multiprocessing.Queue()
        self._graceful_shutdown = multiprocessing.Value('i', 0)
        self.pool_settings = pool_settings

    def add_periodic_task(self, name, interval, task, run_at_start=False):
        """
        Adds a task to be run periodically to the scheduler.

        :name: An identifier to find this task again later (and e.g. remove or alter it). Can be any hashable (using a string or a tuple of strings/integers is common.)
        (Calling this function again with the same name will override the earlier task).
        :target: A function (or other callable) that will perform this task's functionality.
        :interval: A datetime.timedelta representing how frequently to run the given target.
        :run_at_start: If true, runs task right after it was added to the scheduler, rather than only after the first interval has passed.

        """
        self._add_task(
            _PeriodicTask(name, task, interval=interval, run_at_start=run_at_start))

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


        >>> import periodic_tasks as pt
        >>> ts = pt.TaskScheduler()
        >>> ts.start()
        >>> ts.start()
        Traceback (most recent call last):
           ...
        Exception


        """
        if hasattr(self, '_scheduler_process'):
            raise Exception("TaskScheduler.start() called multiple times.")

        self._scheduler_process = multiprocessing.Process(target=self._scheduling_loop, daemon=False)
        # Ensure scheduler quits alongside main program:
        atexit.register(self.stop)

        self._scheduler_process.start()

    def stop(self):
        """
        Stops the scheduler scheduling loop.

        Should only be called once per scheduler, and only after `start()` was called.
        When the program exits suddenly, this function will (in most cases) automatically be called
        to clean up the scheduling process.


        >>> import periodic_tasks as pt
        >>> ts = pt.TaskScheduler()
        >>> ts.stop()
        Traceback (most recent call last):
           ...
        Exception

        """
        if not hasattr(self, '_scheduler_process'):
            raise Exception("`TaskScheduler.stop()` called before calling `TaskScheduler.start()`")

        self._graceful_shutdown = 1
        self._scheduler_process.join(self._granularity)
        self._scheduler_process.terminate()

    def _scheduling_loop(self):
        """
        Executed in the separate process.
        It makes sure all tasks are run whenever their time has come.
        """
        if "TESTING" in os.environ:
            signal.signal(signal.SIGTERM, cleanup)
        with multiprocessing.Pool(**self.pool_settings) as pool:
            while self._graceful_shutdown != 1:
                self._add_tasks_to_be_scheduled()
                current_time = datetime.datetime.now()
                self._run_waiting_tasks(pool, current_time)
                sleep(self._granularity)

    def _add_tasks_to_be_scheduled(self):
        """
        Adds tasks that were added to the multiprocessing.Queue to the internal scheduling priority queue.
        (old tasks with the same name as the new task are replaced; and if the new task does not have a terget function, it is removed alltogether.)
        """

        for task in queue_nonblocking_iter(self._tasks_to_be_scheduled):
            if task.target == None:
                print(f"Removing task {task.name} from internal pqueue")
                self._task_queue.pop(task, default=None)
            else:
                print(f"Adding task {task.name} to internal pqueue")
                # Remove old task with same name if it existed
                self._task_queue.pop(task, default=None)
                # And then add new task with new priority
                self._task_queue[task] = task.next_run_dt

    def _run_waiting_tasks(self, pool, current_time):
        """
        Runs all tasks whose `next_run_dt` has passed since last time.
        """
        for task in pqdict_iter_upto_priority(self._task_queue, current_time):
            print(f"====Running task {task} at {current_time}...")
            self._run_task(pool, task)
            print(f"====Finished running task {task}.")
            if isinstance(task, _PeriodicTask):
                task.update_for_next_run()
                self._task_queue[task] = task.next_run_dt

    def _run_task(self, pool, task):
        """
        Executes a single task in one of the pool's processes
        """
        res = pool.apply_async(task, ())
        # res.get() # <- Uncomment this line to debug tasks in an easy way. Serializes task execution however!
