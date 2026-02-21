from flask.views import MethodView
from app.shared.db import db
from . import user_bp
from .controllers.user_controller import UserController
from app.modules.user.schemas import (
    UserSchema,
    UserQuerySchema,
    UserListResponseSchema,
)
from app.shared.schemas import ErrorSchema


@user_bp.route("/")
class UsersCollection(MethodView):
    # CREATE USER
    @user_bp.doc(
        summary="Create a new user",
        description="Creates a user with name, lastname and email.",
        responses={
            201: {
                "description": "User created successfully",
                "content": {"application/json": {"schema": UserSchema}},
            },
            400: {
                "description": "Invalid input data",
                "content": {"application/json": {"schema": ErrorSchema}},
            },
            409: {
                "description": "Email already exists",
                "content": {"application/json": {"schema": ErrorSchema}},
            },
            500: {
                "description": "Internal server error",
                "content": {"application/json": {"schema": ErrorSchema}},
            },
            "default": {},
        },
    )
    @user_bp.arguments(UserSchema, location="json")
    def post(self, data):
        with db.get_session() as session:
            controller = UserController(session)
            user = controller.create_user(data)

        return UserSchema().dump(user), 201

    # LIST USERS
    @user_bp.doc(
        summary="List users",
        description="Returns a list of users with optional pagination and email filtering.",
        responses={
            200: {
                "description": "Users retrieved successfully",
                "content": {"application/json": {"schema": UserListResponseSchema}},
            },
            400: {
                "description": "Invalid pagination parameters",
                "content": {"application/json": {"schema": ErrorSchema}},
            },
            500: {
                "description": "Internal server error",
                "content": {"application/json": {"schema": ErrorSchema}},
            },
            "default": {},
        },
    )
    @user_bp.arguments(UserQuerySchema, location="query")
    def get(self, args):
        page = args.get("page")
        limit = args.get("limit")
        email = args.get("email")

        with db.get_session() as session:
            controller = UserController(session)
            result = controller.list_users(
                page=page,
                limit=limit,
                email=email,
            )

        return UserListResponseSchema().dump(result), 200


@user_bp.route("/<int:user_id>")
class UserResource(MethodView):
    # GET USER
    @user_bp.doc(
        summary="Get user by ID",
        description="Returns a single user by its ID.",
        responses={
            200: {
                "description": "User retrieved successfully",
                "content": {"application/json": {"schema": UserListResponseSchema}},
            },
            404: {
                "description": "User not found",
                "content": {"application/json": {"schema": ErrorSchema}},
            },
            500: {
                "description": "Internal server error",
                "content": {"application/json": {"schema": ErrorSchema}},
            },
            "default": {},
        },
    )
    def get(self, user_id):
        with db.get_session() as session:
            controller = UserController(session)
            user = controller.get_user(user_id)

        return UserSchema().dump(user), 200

    # UPDATE USER
    @user_bp.doc(
        summary="Update a user",
        description="Updates mandatory fields (name, lastname, email) of an existing user.",
        responses={
            200: {
                "description": "User updated successfully",
                "content": {"application/json": {"schema": UserSchema}},
            },
            400: {
                "description": "Invalid input data",
                "content": {"application/json": {"schema": ErrorSchema}},
            },
            404: {
                "description": "User not found",
                "content": {"application/json": {"schema": ErrorSchema}},
            },
            409: {
                "description": "Email already exists",
                "content": {"application/json": {"schema": ErrorSchema}},
            },
            500: {
                "description": "Internal server error",
                "content": {"application/json": {"schema": ErrorSchema}},
            },
            "default": {},
        },
    )
    @user_bp.arguments(UserSchema, location="json")
    def put(self, data, user_id):
        with db.get_session() as session:
            controller = UserController(session)
            user = controller.update_user(user_id, data)

        return UserSchema().dump(user), 200

    # DELETE USER
    @user_bp.doc(
        summary="Delete a user",
        description="Deletes a user by ID.",
        responses={
            204: {"description": "User deleted successfully"},
            404: {
                "description": "User not found",
                "content": {"application/json": {"schema": ErrorSchema}},
            },
            500: {
                "description": "Internal server error",
                "content": {"application/json": {"schema": ErrorSchema}},
            },
            "default": {},
        },
    )
    def delete(self, user_id):
        with db.get_session() as session:
            controller = UserController(session)
            controller.delete_user(user_id)

        return "", 204
