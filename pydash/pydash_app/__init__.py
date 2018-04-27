"""
The `pydash_app` package contains all business domain logic of the PyDash application: Everything that is not part of rendering a set of webpages.
"""

import periodic_tasks

import pydash_app.user.services.seeding
import pydash_app.user as user

import pydash_app.dashboard.services.fetching
import pydash_app.dashboard.services.seeding
import pydash_app.dashboard as dashboard


def start_task_scheduler():
    periodic_tasks.default_task_scheduler.start()


def stop_task_scheduler():
    periodic_tasks.default_task_scheduler.stop()


def schedule_periodic_tasks():
    import datetime  # <- remove this line when custom interval no longer necessary for testing.
    dashboard.services.fetching.schedule_all_periodic_dashboards_tasks(
        interval=datetime.timedelta(minutes=1)
    )


def seed_datastructures():
    # Ensure no periodic tasks with old datastructures are run:
    stop_task_scheduler()

    user.services.seeding.seed()
    dashboard.services.seeding.seed()
