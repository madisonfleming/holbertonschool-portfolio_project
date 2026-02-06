"""
This file is temporary - Kat's using it to sanity check the User model
From /my_little_bookworm, run:
        python3 -m models.user_tests
"""
from models.user import User


def testUsers():
    try:
        standardUser = User()
        print("standardUser created by default\n", {
            'id': standardUser.id,
            'role': standardUser.role
        })

        adminUser = User('admin')
        print("adminUser created with admin arg\n", {
            'id': adminUser.id,
            'role': adminUser.role
        })

        stdUserWithInvalidStrArg = User('adm1n')
        print("standardUser created if invalid str arg given\n", {
            'id': stdUserWithInvalidStrArg.id,
            'role': stdUserWithInvalidStrArg.role
        })

        stdUserWithIntArg = User(123)
        print('Oh no')
        print("standardUser created if int arg given\n", {
            'id': stdUserWithIntArg.id,
            'role': stdUserWithIntArg.role
        })
    except TypeError:
        print('Error was found')
    else:
        print('Nothing went wrong')


testUsers()
