import os
from unittest import TestCase
from sqlalchemy import exc
from models import db, User, Message, Follows

# BEFORE we import our app, let's set an environmental variable
# to use a different database for tests (we need to do this
# before we import our app, since that will have already
# connected to the database
os.environ['DATABASE_URL'] = "postgresql:///warbler-test"

# Now we can import app
from app import app

# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data
db.create_all()


class UserModelTestCase(TestCase):
    """Test cases for the User model."""

    def setUp(self):
        """Create test client, add sample data."""
        User.query.delete()
        Message.query.delete()
        Follows.query.delete()

        self.client = app.test_client()

    def test_user_repr(self):
        """Does the repr method work as expected?"""
        u = User(
            email="test@test.com",
            username="testuser",
            password="HASHED_PASSWORD"
        )

        self.assertEqual(repr(u), "<User #None: testuser, test@test.com>")

    def test_user_is_following(self):
        """Does is_following successfully detect when user1 is following user2?"""
        user1 = User(
            email="test1@test.com",
            username="testuser1",
            password="HASHED_PASSWORD1"
        )
        user2 = User(
            email="test2@test.com",
            username="testuser2",
            password="HASHED_PASSWORD2"
        )
        db.session.add_all([user1, user2])
        db.session.commit()

        user1.following.append(user2)
        db.session.commit()

        self.assertTrue(user1.is_following(user2))

    def test_user_is_not_following(self):
        """Does is_following successfully detect when user1 is not following user2?"""
        user1 = User(
            email="test1@test.com",
            username="testuser1",
            password="HASHED_PASSWORD1"
        )
        user2 = User(
            email="test2@test.com",
            username="testuser2",
            password="HASHED_PASSWORD2"
        )
        db.session.add_all([user1, user2])
        db.session.commit()

        self.assertFalse(user1.is_following(user2))

    def test_user_is_followed_by(self):
        """Does is_followed_by successfully detect when user1 is followed by user2?"""
        user1 = User(
            email="test1@test.com",
            username="testuser1",
            password="HASHED_PASSWORD1"
        )
        user2 = User(
            email="test2@test.com",
            username="testuser2",
            password="HASHED_PASSWORD2"
        )
        db.session.add_all([user1, user2])
        db.session.commit()

        user2.following.append(user1)
        db.session.commit()

        self.assertTrue(user1.is_followed_by(user2))

    def test_user_is_not_followed_by(self):
        """Does is_followed_by successfully detect when user1 is not followed by user2?"""
        user1 = User(
            email="test1@test.com",
            username="testuser1",
            password="HASHED_PASSWORD1"
        )
        user2 = User(
            email="test2@test.com",
            username="testuser2",
            password="HASHED_PASSWORD2"
        )
        db.session.add_all([user1, user2])
        db.session.commit()

        self.assertFalse(user1.is_followed_by(user2))

    def test_user_create_success(self):
        """Does User.create successfully create a new user given valid credentials?"""
        user = User.create(
            username="testuser",
            email="test@test.com",
            password="HASHED_PASSWORD"
        )
        db.session.commit()

        self.assertIsNotNone(user)
        self.assertEqual(user.username, "testuser")
        self.assertEqual(user.email, "test@test.com")

    def test_user_create_failure(self):
        """Does User.create fail to create a new user if any of the validations fail?"""
        user1 = User.create(
            username="testuser",
            email="test@test.com",
            password="HASHED_PASSWORD"
        )
        db.session.commit()

        user2 = User.create(
            username="testuser",
            email="test2@test.com",
            password="HASHED_PASSWORD"
        )

        self.assertIsNone(user2)
        self.assertRaises(exc.IntegrityError)

    def test_user_authenticate_success(self):
        """Does User.authenticate successfully return a user when given a valid username and password?"""
        user = User.create(
            username="testuser",
            email="test@test.com",
            password="HASHED_PASSWORD"
        )
        db.session.commit()

        authenticated_user = User.authenticate("testuser", "HASHED_PASSWORD")

        self.assertIsNotNone(authenticated_user)
        self.assertEqual(authenticated_user.username, "testuser")

    def test_user_authenticate_invalid_username(self):
        """Does User.authenticate fail to return a user when the username is invalid?"""
        user = User.create(
            username="testuser",
            email="test@test.com",
            password="HASHED_PASSWORD"
        )
        db.session.commit()

        authenticated_user = User.authenticate("invalidusername", "HASHED_PASSWORD")

        self.assertFalse(authenticated_user)

    def test_user_authenticate_invalid_password(self):
        """Does User.authenticate fail to return a user when the password is invalid?"""
        user = User.create(
            username="testuser",
            email="test@test.com",
            password="HASHED_PASSWORD"
        )
        db.session.commit()

        authenticated_user = User.authenticate("testuser", "INVALID_PASSWORD")

        self.assertFalse(authenticated_user)





