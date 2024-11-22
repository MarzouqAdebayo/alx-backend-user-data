#!/usr/bin/env python3
"""
Main file
"""
from auth import Auth

email = "bob@bob.com"
password = "MyPwdOfBob"
auth = Auth()
auth.register_user(email, password)
session_id = auth.create_session(email)
user = auth.get_user_from_session_id(session_id + "hy")
if user:
    print(user.email)
else:
    print(user)

#
#
# print(auth.valid_login(email, password))
#
# print(auth.valid_login(email, "WrongPwd"))
#
# print(auth.valid_login("unknown@email", password))
