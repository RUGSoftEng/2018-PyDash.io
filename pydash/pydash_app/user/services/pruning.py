"""
Provides functionality to periodically remove all users that have not verified their account.
"""

from datetime import timedelta

import periodic_tasks
import pydash_app.user.repository
import pydash_logger

logger = pydash_logger.Logger(__name__)


def schedule_periodic_pruning_task(
        interval=timedelta(days=1),
        scheduler=periodic_tasks.default_task_scheduler):
    """
    Schedules the periodic user pruning task, such that all unverified users are deleted from the user repository.
    :param interval: A timedelta instance indicating the interval with which this task should be run. Defaults to one day.
    :param scheduler: The TaskScheduler instance that should schedule this user pruning task and execute it.
      Defaults to the default task scheduler of pydash.periodic_tasks.
    """
    periodic_tasks.add_periodic_task(
        name=('users', 'pruning'),
        task=_prune_unverified_users,
        interval=interval,
        scheduler=scheduler)


def _prune_unverified_users():
    users_to_remove = []

    for user in pydash_app.user.repository.all_unverified():
        if user.has_verification_code_expired():
            users_to_remove.append(user)

    for user in users_to_remove:
        try:
            pydash_app.user.repository.delete_by_id(user.id)
        except KeyError:
            logger.info(f'Tried to prune already deleted user {user}')
            pass
