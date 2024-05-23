#!/usr/bin/env python3
"""
Define SessionExpAuth class
"""
import os
from datetime import datetime, timedelta

from .session_auth import SessionAuth


class SessionExpAuth(SessionAuth):
    """
    This Method Definition of class SessionExpAuth that adds an
    expiration date to a Session ID.
    """

    def __init__(self):
        """
        This Method Initialize the class
        """
        try:
            duration = int(os.getenv("SESSION_DURATION"))
        except Exception:
            duration = 0
        self.session_duration = duration

    def create_session(self, user_id=None):
        """
        This Method Create a Session ID for a user_id.
        """
        one_session_id = super().create_session(user_id)
        if one_session_id is None:
            return None
        session_dictionary = {"user_id": user_id, "created_at": datetime.now()}
        self.user_id_by_session_id[one_session_id] = session_dictionary
        return one_session_id

    def user_id_for_session_id(self, session_id=None):
        """
        This Method Returns a user ID based on a session ID.
        """
        if session_id is None:
            return None
        one_user_details = self.user_id_by_session_id.get(session_id)
        if one_user_details is None:
            return None
        if "created_at" not in one_user_details.keys():
            return None
        if self.session_duration <= 0:
            return one_user_details.get("user_id")
        one_created_at = one_user_details.get("created_at")
        one_allowed_window = one_created_at + timedelta(seconds=self.session_duration)
        if one_allowed_window < datetime.now():
            return None
        return one_user_details.get("user_id")
