#!/usr/bin/env python3
"""
Main file
"""
from auth import Auth

email = "bob@bob.com"
password = "MyPwdOfBob"
auth = Auth()
user = auth.register_user(email, password)
# session_id = auth.create_session(email)
# auth.destroy_session(user.id)
user = auth.get_user_from_session_id(None)
if user:
    print(user.email)
else:
    print(user)

print(auth.get_reset_password_token(email))
#
#
# print(auth.valid_login(email, password))
#
# print(auth.valid_login(email, "WrongPwd"))
#
# print(auth.valid_login("unknown@email", password))
