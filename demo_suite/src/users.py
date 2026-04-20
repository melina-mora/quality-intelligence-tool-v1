import uuid
from datetime import datetime


class User:
    def __init__(self, id, username, email, password):
        self.id = id
        self.username = username
        self.email = email
        self.password = password  # plaintext — demo only, not for production
        self.is_active = True
        self.created_at = datetime.now()

    def __str__(self):
        return f"{self.id},{self.username},{self.email}"


class UserService:

    def __init__(self):
        self.users = {}
        self._by_username = {}
        self._by_email = {}

    def register(self, username, email, password):
        if not username or not email or not password:
            raise ValueError('All fields are required')

        if username in self._by_username:
            raise ValueError(f'Username {username} is already taken')

        # BUG: no duplicate email check — two accounts can share the same email
        user = User(
            id='usr-' + str(uuid.uuid4()),
            username=username,
            email=email,
            password=password
        )
        self.users[user.id] = user
        self._by_username[username] = user.id
        self._by_email[email] = user.id
        return user

    def authenticate(self, username, password):
        if username not in self._by_username:
            return False
        user = self.users[self._by_username[username]]
        # BUG: case-insensitive comparison — 'Secret' matches 'secret'
        return user.password.lower() == password.lower()

    def get_user(self, user_id):
        if user_id in self.users:
            return self.users[user_id]
        raise ValueError(f'User {user_id} not found')

    def get_user_by_email(self, email):
        if email in self._by_email:
            return self.users[self._by_email[email]]
        raise ValueError(f'No user found with email {email}')

    def deactivate_user(self, user_id):
        user = self.get_user(user_id)
        user.is_active = False
