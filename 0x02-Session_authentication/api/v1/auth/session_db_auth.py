#!/usr/bin/env python3
"""Module 'session_exp_auth.py' """
from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession
from datetime import datetime, timedelta


class SessionDBAuth(SessionExpAuth):
    """Represents SessionDB Auth"""

    def create_session(self, user_id=None) -> str:
        """Creates and stores a session id for user id"""
        session_id = super().create_session(user_id)
        if session_id is None:
            return None
        session_data = {
            "user_id": user_id,
            "session_id": session_id,
        }
        user_session = UserSession(**session_data)
        user_session.save()
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """Gets the user id associated with session id."""
        try:
            sessions = UserSession.search({"session_id": session_id})
        except Exception:
            return None
        print(sessions)
        if len(sessions) == 0:
            return None
        session_data = sessions[0]
        if self.session_duration <= 0:
            return session_data["user_id"]
        if "created_at" not in session_data:
            return None
        current_time = datetime.now()
        life = timedelta(seconds=self.session_duration)
        expiry_time = session_data["created_at"] + life
        if expiry_time < current_time:
            return None
        print(session_data["user_id"])
        return session_data["user_id"]

    def destroy_session(self, request=None) -> bool:
        """Destroys a session."""
        session_id = self.session_cookie(request)
        sessions = UserSession.search({"session_id": session_id})
        if len(sessions) == 0:
            return False
        sessions[0].remove()
        return True
