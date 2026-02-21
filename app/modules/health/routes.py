from flask.views import MethodView
from sqlalchemy import text
from app.shared.db import db
from .schemas import HealthSchema
from . import health_bp


@health_bp.route("/")
class HealthResource(MethodView):
    @health_bp.doc(
        summary="Health check",
        description="Checks API liveness and database connectivity.",
        responses={
            200: {
                "description": "Service is healthy",
                "schema": HealthSchema,
            },
            500: {
                "description": "Service is unhealthy",
                "schema": HealthSchema,
            },
        },
    )
    def get(self):
        session = db.get_session()

        try:
            session.execute(text("SELECT 1"))
            session.close()

            return {
                "status": "ok",
                "database": "connected",
            }, 200

        except Exception:
            session.close()

            return {
                "status": "error",
                "database": "disconnected",
            }, 500
