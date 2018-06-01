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
