#!/usr/bin/env python3
"""
Define class SessionDButh
"""
from .session_exp_auth import SessionExpAuth
from models.user_session import UserSession


class SessionDBAuth(SessionExpAuth):
    """
    This class Definition of SessionDBAuth class that persists session data
    in a database
    """

    def create_session(self, user_id=None):
        """
        This Method Create a Session ID for a user_id
        """
        one_session_id = super().create_session(user_id)
        if not one_session_id:
            return None
        one_kw = {"user_id": user_id, "session_id": one_session_id}
        one_user = UserSession(**one_kw)
        one_user.save()
        return one_session_id

    def user_id_for_session_id(self, session_id=None):
        """
        This Method Returns a user ID based on a session ID.
        """
        one_user_id = UserSession.search({"session_id": session_id})
        if one_user_id:
            return one_user_id
        return None

    def destroy_session(self, request=None):
        """
        This Method Destroy a UserSession instance based on a
        Session ID from a request cookie
        """
        if request is None:
            return False
        one_session_id = self.session_cookie(request)
        if not one_session_id:
            return False
        user_session = UserSession.search({"session_id": one_session_id})
        if user_session:
            user_session[0].remove()
            return True
        return False
