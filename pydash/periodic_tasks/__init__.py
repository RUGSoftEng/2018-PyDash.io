"""
Allows for the running of tasks in the background, as well as periodically.
Tasks can either be added to the `default_task_scheduler`, or multiple schedulers can be created.


Tasks are run in a process pool of subprocesses (See `multiprocessing.Pool`).
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


Example code with custom scheduler:

    >>> import periodic_tasks as pt
    >>> ts = pt.TaskScheduler()
    >>> import datetime
    >>> ts.start()
    >>> ts.add_periodic_task('foo', datetime.timedelta(seconds=1), pt.foo)
    >>> ts.add_periodic_task('bar', datetime.timedelta(seconds=5), pt.bar)


Example code with default scheduler:


    >>> import periodic_tasks as pt
    >>> import datetime
    >>> pt.start_default_scheduler()
    >>> pt.add_periodic_task('foo', datetime.timedelta(seconds=3), pt.foo)
    >>> pt.add_periodic_task('bar', datetime.timedelta(seconds=5), pt.bar)
    >>> pt.add_background_task('baz', pt.baz)
    >>> pt.add_periodic_task('bar', datetime.timedelta(seconds=1), pt.bar) # overrides previous `bar` task with new settings
    >>> pt.remove_task('foo')
"""

from .task_scheduler import TaskScheduler
import datetime
default_task_scheduler = TaskScheduler()


def add_periodic_task(name,
                      interval,
                      task,
                      run_at_start=False,
                      scheduler=default_task_scheduler):
    """
    Adds a task to be run periodically to the given `scheduler`, which defaults to the global `default_task_scheduler` that this module provides.

    :name: An identifier to find this task again later (and e.g. remove or alter it). Can be any hashable (using a string or a tuple of strings/integers is common.)
    (Calling this function again with the same name will override the earlier task).
    :target: A function (or other callable) that will perform this task's functionality.
    :interval: A datetime.timedelta representing how frequently to run the given target.
    :run_at_start: If true, runs task right after it was added to the scheduler, rather than only after the first interval has passed.
    :scheduler: Which TaskScheduler to run the task on. It defaults to the global `default_task_scheduler` that this module provides.
    """
    scheduler.add_periodic_task(name, interval, task)


def add_background_task(name, task, scheduler=default_task_scheduler):
    """
    Adds a task to be run only once (and as soon as possible) to the given `scheduler`, which defaults to the global `default_task_scheduler` that this module provides.

    :name: An identifier to find this task again later (and e.g. remove or alter it). Can be any hashable (using a string or a tuple of strings/integers is common.)
    (Calling this function again with the same name will override the earlier task).
    :target: A function (or other callable) that will perform this task's functionality.
    :scheduler: Which TaskScheduler to run the task on. It defaults to the global `default_task_scheduler` that this module provides.
    """
    scheduler.add_background_task(name, task)


def remove_task(name, scheduler=default_task_scheduler):
    """
    Removes a task that was previously added from the given `scheduler`, which defaults to the global `default_task_scheduler` that this module provides..
    Will do nothing if there is no task with the given name.

    :name: The task with this name will be removed.
    :scheduler: Which TaskScheduler to remove the task from. It defaults to the global `default_task_scheduler` that this module provides.
    """
    scheduler.remove_task(name)


def periodic_task(name,
                  interval,
                  run_at_start=False,
                  scheduler=default_task_scheduler):
    """
    Function decorator to specify that the following function
    should be called periodically;
    It accepts the same arguments as `add_periodic_task` (with the `target` argument filled in by the function being decorated.)

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
    """
    Starts the default (global) scheduler that this module provides.
    """
    default_task_scheduler.start()


# Some example test functions.
# Should be removed once the scheduler is really stable
def foo():
    print('foo')


def bar():
    print('bar')


def baz():
    print('baz')


# @periodic_task('qux', datetime.timedelta(seconds=2))
def qux():
    print('qux')
