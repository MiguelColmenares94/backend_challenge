from flask_smorest import Blueprint

health_bp = Blueprint(
    "health",
    __name__,
    url_prefix="/health",
    description="System health monitoring endpoints",
)

from . import routes
