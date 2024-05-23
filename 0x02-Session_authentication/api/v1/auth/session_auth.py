#!/usr/bin/env python3
"""
Definition of class SessionAuth.
"""
import base64
from uuid import uuid4
from typing import TypeVar

from .auth import Auth
from models.user import User


class SessionAuth(Auth):
    """Implement Session Authorization protocol methods."""

    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """
        This Method Creates a Session ID for a user with id user_id.
        """
        if user_id is None or not isinstance(user_id, str):
            return None
        id = uuid4()
        self.user_id_by_session_id[str(id)] = user_id
        return str(id)

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """
        This Method Returns a user ID based on a session ID.

        """
        if session_id is None or not isinstance(session_id, str):
            return None
        return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None):
        """
        This Method Return a user instance based on a cookie value.

        """
        one_session_cookie = self.session_cookie(request)
        one_user_id = self.user_id_for_session_id(one_session_cookie)
        one_user = User.get(one_user_id)
        return one_user

    def destroy_session(self, request=None):
        """
        This Method Deletes a user session.
        """
        if request is None:
            return False
        one_session_cookie = self.session_cookie(request)
        if one_session_cookie is None:
            return False
        user_id = self.user_id_for_session_id(one_session_cookie)
        if user_id is None:
            return False
        del self.user_id_by_session_id[one_session_cookie]
        return True
