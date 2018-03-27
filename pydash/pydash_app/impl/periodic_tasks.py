"""
Allows for the running of tasks in the background.

Still to be done:

- wrapping default scheduler as 'global', which can be used as default for function decorators.
- said function decorators.
- background tasks besides the periodic tasks that only run once (partial support already exists, but no public calls to add them yet).
- refactoring :D

Example code:

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
# import heapq
# import heapy
from pqdict import pqdict

class Task:
    """
    :name: An identifier to find this task again later (and e.g. remove or alter it)
    :target: A function (or other callable) that will perform this task's functionality.
    :interval: None for one-off (background) tasks, should otherwise a datetime.timedelta value.
    :run_at_start: If true, runs task right after it was added to the scheduler, rather than only after the first interval has passed.

    """
    def __init__(self, name, target, interval=None, run_at_start=False):
        self.name = name
        self.interval = interval
        self.target = target
        self.run_at_start = run_at_start

        self.next_run_dt = datetime.datetime.now()
        if self.interval is not None and not self.run_at_start:
            self.next_run_dt += interval

    # def __lt__(self, other):
    #     return self.next_run_dt.__le__(other.next_run_dt)

    def __call__(self, *args, **kwargs):
        self.target(*args, **kwargs)

    def __hash__(self):
        return hash(self.name)

    def __eq__(self, other):
        return isinstance(other, Task) and other.name == self.name


class TaskScheduler:
    def __init__(self, granularity=1.0):
        """

        :granularity: How often the scheduler should check if a periodic task's timeout has passed, in seconds. Defaults to `1.0`.
        """
        self._task_queue = pqdict()
        self._pool = None
        self._granularity = granularity
        self._tasks_to_be_scheduled = multiprocessing.Queue()

    def add_periodic_task(self, name, interval, task):
        """
        Altering an already-existing task can be done
        by calling this function with the new information but use the same name.
        """
        # TODO input checking:
        # name: string
        # interval: timedelta
        self._add_task(name, interval, task)

    def add_background_task(self, name, task):
        self._add_task(name, None, task)

    def remove_task(self, name):
        self._add_task(name, None, None)

    def start(self):
        if hasattr(self, '_scheduler_process'):
            raise Exception("TaskScheduler.start() called multiple times.")
        import atexit
        self._scheduler_process = multiprocessing.Process(target=self._start, daemon=False)
        # Ensure scheduler quits alongside main program
        atexit.register(self.stop)

        self._scheduler_process.start()

    def stop(self):
        if not hasattr(self, '_scheduler_process'):
            raise Exception("`TaskScheduler.stop()` called before calling `TaskScheduler.start()`")
        self._scheduler_process.terminate()

    def _add_task(self, name, interval, task):
        self._tasks_to_be_scheduled.put(Task(name, task, interval=interval))

    def _add_tasks_to_be_scheduled(self):
        try:
            while True:
                task = self._tasks_to_be_scheduled.get_nowait()
                if task.target == None:
                    print(f"Removing task {task.name} from internal pqueue")
                    self._task_queue.pop(task, default=None)
                else:
                    print(f"Adding task {task.name} to internal pqueue")
                    # heapq.heappush(self._task_queue, task)
                    self._task_queue[task] = task.next_run_dt
        except queue.Empty:
            # Thrown by self._tasks_to_be_scheduled.get_nowait()
            # when this cross-process queue happens to be empty.
            pass

    def _start(self):
        with multiprocessing.Pool() as pool:
            while True:
                self._add_tasks_to_be_scheduled()
                current_time = datetime.datetime.now()
                self._run_tasks_that_should_have_start(pool, current_time)
                sleep(self._granularity)

    def _run_tasks_that_should_have_start(self, pool, current_time):
        # Otherwise, iterate while tasks are before current time.
        # TODO restructure into for-comprehension?
        while True:
            # print(f"task queue: {self._task_queue}")

            # Do nothing if empty
            if not self._task_queue:
                return

            task = self._task_queue.top()
            # print(f"Looking at task {task.name} which should be run at {task.next_run_dt}, every {task.interval}")
            if task.next_run_dt < current_time:
                print(f"Running task {task.name} at {current_time}, every {task.interval}...")
                # heapq.heappop(self._task_queue)
                self._task_queue.pop()
                self._run_task(pool, task)
                if task.interval is not None:
                    # self._add_periodic_task(task.name, task.interval, tasktask)
                    task.next_run_dt = datetime.datetime.now() + task.interval
                    # heapq.heappush(self._task_queue, task)
                    self._task_queue[task] = task.next_run_dt
            else:
                break

    def _run_task(self, pool, task):
        res = pool.apply_async(task, ())
        res.get()


default_task_scheduler = TaskScheduler()

def add_periodic_task(name, interval, task, scheduler = default_task_scheduler):
    scheduler.add_periodic_task(name, interval, task)

def add_background_task(name, task, scheduler = default_task_scheduler):
    scheduler.add_background_task(name, task)

def remove_task(name, scheduler = default_task_scheduler):
    scheduler.remove_task(name)

def periodic_task(name, interval, scheduler = default_task_scheduler):
    def task_decor(task_function):
        add_periodic_task(name, interval, task_function, scheduler)
        return task_function

    return task_decor

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


