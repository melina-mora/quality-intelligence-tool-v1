import pytest
from src.users import UserService


class TestUserRegistration:

    def test_register_user_success(self, user_service):
        """New user can register with valid credentials."""
        user = user_service.register('alice', 'alice@example.com', 'secret123')
        assert user.username == 'alice'
        assert user.is_active is True

    def test_register_duplicate_username_raises(self, user_service):
        """Registering with an existing username should raise ValueError."""
        user_service.register('bob', 'bob@example.com', 'pass1')
        with pytest.raises(ValueError):
            user_service.register('bob', 'bob2@example.com', 'pass2')

    def test_register_duplicate_email_raises(self, user_service):
        """Two accounts should not share the same email address."""
        user_service.register('carol', 'carol@example.com', 'pass1')
        with pytest.raises(ValueError):
            user_service.register('carol2', 'carol@example.com', 'pass2')

    def test_register_missing_fields_raises(self, user_service):
        """Registration with any empty field should raise ValueError."""
        with pytest.raises(ValueError):
            user_service.register('', 'test@example.com', 'password')

    def test_registered_user_is_retrievable(self, user_service):
        """A registered user should be accessible by their ID."""
        user = user_service.register('dave', 'dave@example.com', 'pass')
        fetched = user_service.get_user(user.id)
        assert fetched.username == 'dave'


class TestAuthentication:

    def test_authenticate_correct_credentials(self, user_service):
        """Correct username and password should return True."""
        user_service.register('eve', 'eve@example.com', 'MyPassword')
        assert user_service.authenticate('eve', 'MyPassword') is True

    def test_authenticate_wrong_password(self, user_service):
        """Wrong password should return False."""
        user_service.register('frank', 'frank@example.com', 'correct')
        assert user_service.authenticate('frank', 'wrong') is False

    def test_authenticate_is_case_sensitive(self, user_service):
        """Authentication should be case-sensitive — 'Secret' != 'secret'."""
        user_service.register('grace', 'grace@example.com', 'Secret')
        assert user_service.authenticate('grace', 'secret') is False

    def test_authenticate_nonexistent_user(self, user_service):
        """Authenticating a username that does not exist should return False."""
        assert user_service.authenticate('nobody', 'pass') is False

    def test_deactivate_user(self, user_service):
        """Deactivated user should have is_active set to False."""
        user = user_service.register('henry', 'henry@example.com', 'pass')
        user_service.deactivate_user(user.id)
        assert user_service.get_user(user.id).is_active is False
