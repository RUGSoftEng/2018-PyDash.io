import datetime
from time import sleep
import multiprocessing
# from queue import PriorityQueue
import heapq

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
        if not self.run_at_start:
            self.next_run_dt += interval

    def __lt__(self, other):
        return self.next_run_dt.__le__(other.next_run_dt)

    def __call__(self, *args, **kwargs):
        self.target(*args, **kwargs)



class TaskScheduler:
    def __init__(self, granularity=1.0):
        """

        :granularity: How often the scheduler should check if a periodic task's timeout has passed, in seconds. Defaults to `1.0`.
        """
        self._task_queue = []
        self._pool = None
        self._granularity = granularity

    def add_periodic_task(self, name, interval, task):
        # TODO input checking:
        # name: string
        # interval: timedelta
        self._add_periodic_task(name, interval, task)

    def run(self):
        import atexit
        self._scheduler_process = multiprocessing.Process(target=self._run, daemon=False)
        # Ensure scheduler quits alongside main program
        atexit.register(self._scheduler_process.terminate)

        self._scheduler_process.start()

    def stop(self):
        if not hasattr(self, _scheduler_process):
            raise Exception("`TaskScheduler.stop()` called before calling `TaskScheduler.start()`")
        proc.terminate()

    def _add_periodic_task(self, name, interval, task):
        # TODO use inter-process abstraction
        next_run_dt = datetime.datetime.now() + interval
        # heapq.heappush(self._task_queue, (next_run_dt, interval, name, task))
        heapq.heappush(self._task_queue, Task(name, task, interval=interval))

    def _run(self):
        with multiprocessing.Pool() as pool:
            while True:
                current_time = datetime.datetime.now()
                print(f"current time is: {current_time}")
                self._run_tasks_that_should_have_run(pool, current_time)
                sleep(self._granularity)

    def _run_tasks_that_should_have_run(self, pool, current_time):
        # Do nothing if empty
        if not self._task_queue:
            return
        # Otherwise, iterate while tasks are before current time.
        # TODO restructure into for-comprehension?
        while True:
            task =  self._task_queue[0]
            print(f"Looking at task {task.name} which should be run at {task.next_run_dt}, every {task.interval}")
            if task.next_run_dt < current_time:
                print(f"Running task {task.name}...")
                heapq.heappop(self._task_queue)
                self._run_task(pool, task)
                if task.interval != None:
                    # self._add_periodic_task(task.name, task.interval, tasktask)
                    task.next_run_dt = datetime.datetime.now() + task.interval
                    heapq.heappush(self._task_queue, task)
            else:
                break

    def _run_task(self, pool, task):
        res = pool.apply_async(task.target, ())
        res.get()


_default_task_scheduler = TaskScheduler()

def add_periodic_task(name, interval, task, scheduler = _default_task_scheduler):
    scheduler.add_periodic_task(name, interval, task)


def foo():
    print('foo')

def bar():
    print('bar')
