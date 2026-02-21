from flask_smorest import Blueprint

user_bp = Blueprint(
    "Contacts",
    "contact",
    url_prefix="/contacts",
    description="Contacts CRUD for Lexmax Challenge",
)

from . import routes
