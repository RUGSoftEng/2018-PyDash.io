import datetime
from time import sleep
import multiprocessing
# from queue import PriorityQueue
import heapq

class Task:
    def __init__(self, name, target, interval=None, run_at_start=False):
        self._name = name
        self._interval = interval
        self._target = target
        self._run_at_start = run_at_start

        self._next_run_dt = datetime.datetime.now()
        if not self._run_at_start:
            self._next_run_dt += interval

    def __le__(self, other):
        return self._next_run_dt.__le__(other._next_run_dt)



class TaskScheduler:
    def __init__(self):
        self._task_queue = []
        self._pool = multiprocessing.Pool()

    def add_periodic_task(self, name, interval, task):
        # TODO input checking:
        # name: string
        # interval: timedelta 
        self._add_periodic_task(name, interval, task)

    def run(self):
        multiprocessing.Process(target=self._run, daemon=True).start()

    def _add_periodic_task(self, name, interval, task):
        # TODO use inter-process abstraction
        next_run_dt = datetime.datetime.now() + interval
        heapq.heappush(self._task_queue, (next_run_dt, interval, name, task))

    def _run(self):
        while True:
            current_time = datetime.datetime.now()
            print(f"current time is: {current_time}")
            self._run_tasks_that_should_have_run(current_time)
            sleep(1)

    def _run_tasks_that_should_have_run(self, current_time):
            while True:
                next_run_dt, interval, name, task =  self._task_queue[0]
                print(f"Looking at task {name} which should be run at {next_run_dt}, every {interval}")
                if next_run_dt < current_time:
                    print(f"Running task {name}...")
                    heapq.heappop(self._task_queue)
                    self._run_task(task)
                    if interval != None:
                        self._add_periodic_task(name, interval, task)
                else:
                    break

    def _run_task(self, task):
        self._pool.apply_async(task)


_default_task_scheduler = TaskScheduler()

def add_periodic_task(name, interval, task, scheduler = _default_task_scheduler):
    scheduler.add_periodic_task(name, interval, task)
