import queue


class queue_nonblocking_iter():
    """
    This iterator wraps the queue.Queue/multiprocessing.Queue objects,
    which provide both a blocking API and a non-blocking API
    that raises errors when attempting to retrieve an item while it is empty.

    Since these queues exist on multiple threads/processes,
    checking for (non)emptyness before attempting an action is not good enough,
    because its state might change in-between.

    So instead, we handle the `queue.Empty` that is raised
    when attempting to retrieve the next item from an emtpy queue.
    """
    def __init__(self, queue):
        self._queue = queue

    def __iter__(self):
        return self

    def __next__(self):
        try:
            return self._queue.get_nowait()
        except queue.Empty:
            raise StopIteration
