import pydash_app.impl.periodic_tasks as pt
import datetime
from functools import partial

pt.start_default_scheduler()  # Perhaps move this to pydash.__init__.py to ensure the task scheduler is always running and make sure that we don't start it again when importing this module.

def add_endpoint_to_fetch_from()