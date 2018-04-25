"""
The `pydash_app` package contains all business domain logic of the PyDash application: Everything that is not part of rendering a set of webpages.
"""
import pydash_app.user
import pydash_app.dashboard

from pydash_app.impl.periodic_tasks import default_task_scheduler
import pydash_app.fetching.dashboard_fetch as dashboard_fetch


def start_task_scheduler():
    default_task_scheduler.start()


def stop_task_scheduler():
    default_task_scheduler.stop()


def schedule_periodic_tasks():
    import datetime  # <- remove this line when custom interval no longer necessary for testing.
    dashboard_fetch.schedule_all_periodic_dashboards_tasks(
        interval=datetime.timedelta(seconds=1)
    )


def seed_datastructures():
    # Ensure no periodic tasks with old datastructures are run:
    stop_task_scheduler()

    user.user_repository.seed_users()
    dashboard.dashboard_repository.seed_dashboards()
