from flask import jsonify
from flask_login import current_user
import pydash_app.dashboard
import pydash_logger
import pydash_app.dashboard.services


logger = pydash_logger.Logger(__name__)


def visitor_heatmap(dashboard_id):
    pass