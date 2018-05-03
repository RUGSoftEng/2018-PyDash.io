

class pqdict_iter_upto_priority():
    # TODO Anyone know a better name for this iterator? :-)
    """
    Wrapper around `pqdict` to implement an iterator
    that returns items up to the given `priority` (exclusive).
    The rest of the pqdict is kept unchanged.

    :pqueue: An instance of the `pqdict.pqdict` class.
    :priority: The threshold priority.

    The comparison function that the pqueue itself uses is used to cutoff this iterator,
    so it will automatically work with both min-queues as wel as max-queues.
    """
    def __init__(self, pqueue, priority):
        self.priority = priority
        self._pqueue = pqueue

    def __iter__(self):
        return self

    def __next__(self):
        if not self._pqueue:
            raise StopIteration
        item, item_priority = self._pqueue.topitem()
        if not self._pqueue.precedes(item_priority, self.priority):
            raise StopIteration
        return self._pqueue.pop()
