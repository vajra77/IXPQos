from flask import Blueprint
from ixpqos.app.logger import Logger

api = Blueprint('api', __name__)

Logger.info("starting app blueprint")

from . import auth, collector
