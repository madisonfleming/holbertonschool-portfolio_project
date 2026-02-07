"""
This file is temporary - Kat's using it to sanity check the User model
From /my_little_bookworm, run:
        python3 -m models.user_tests
"""
from models.user import User


def testUsers():
    try:
        standardUser = User('Mary Standard', 'mary@example.com')
        print("standardUser created by default\n", {
            'id': standardUser.id,
            'name': standardUser.name,
            'role': standardUser.role
        })

        adminUser = User('Martha Admin', 'martha@example.com', 'admin')
        print("adminUser created with admin arg\n", {
            'id': adminUser.id,
            'name': adminUser.name,
            'role': adminUser.role
        })

        stdUserWithInvalidStrArg = User(
            'Arthur Standard', 'arthur@example.com', 'adm1n')
        print("standardUser created if invalid str arg given\n", {
            'id': stdUserWithInvalidStrArg.id,
            'name': stdUserWithInvalidStrArg.name,
            'role': stdUserWithInvalidStrArg.role
        })

        stdUserWithIntArg = User('Integer Mike', 'intmike@example.com', 123)
        print('Oh no')
        print("standardUser created if int arg given\n", {
            'id': stdUserWithIntArg.id,
            'role': stdUserWithIntArg.role
        })
    except TypeError:
        print('Error was found')
    else:
        print('Nothing went wrong')


# testUsers()

user = User('Mary', 'mary@example.co')
print('before:', user.name, 'was updated at ', user.updated_at)

user.update_profile({'name': 'Martha', 'occupation': 'Plumber'})
print('after:', user.name, 'was updated at ', user.updated_at)

# Check email validation - should throw error
# user = User('Mary', 'mary@@example.co')
