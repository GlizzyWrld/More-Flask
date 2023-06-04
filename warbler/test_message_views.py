"""Message View tests."""

# run these tests like:
#
#    FLASK_ENV=production python -m unittest test_message_views.py

import os
from unittest import TestCase
from sqlalchemy import exc
from models import db, User, Message, Follows
from app import app, CURR_USER_KEY

# Set the test database URL
os.environ['DATABASE_URL'] = "postgresql:///warbler-test"

# Create the tables
db.create_all()


class MessageViewsTestCase(TestCase):
    """Test cases for message views."""

    def setUp(self):
        """Create test client, add sample data."""
        User.query.delete()
        Message.query.delete()
        Follows.query.delete()

        self.client = app.test_client()

        self.user = User.create(
            username="testuser",
            email="test@test.com",
            password="HASHED_PASSWORD"
        )
        db.session.commit()

        self.message = Message(
            text="Test message",
            user_id=self.user.id
        )
        db.session.add(self.message)
        db.session.commit()

    def tearDown(self):
        """Clean up any fouled transaction."""
        db.session.rollback()

    def test_logged_out_user_cannot_add_message(self):
        """When logged out, are you prohibited from adding messages?"""
        with self.client as client:
            response = client.post(
                "/messages/new",
                data={"text": "New message"},
                follow_redirects=True
            )
            self.assertEqual(response.status_code, 200)
            self.assertIn(b"Access unauthorized.", response.data)

    def test_logged_in_user_can_add_message(self):
        """When logged in, can you add a message as yourself?"""
        with self.client as client:
            with client.session_transaction() as session:
                session["user_id"] = self.user.id

            response = client.post(
                "/messages/new",
                data={"text": "New message"},
                follow_redirects=True
            )
            self.assertEqual(response.status_code, 200)
            self.assertIn(b"New message", response.data)

    def test_logged_out_user_cannot_delete_message(self):
        """When logged out, are you prohibited from deleting messages?"""
        with self.client as client:
            response = client.post(
                f"/messages/{self.message.id}/delete",
                follow_redirects=True
            )
            self.assertEqual(response.status_code, 200)
            self.assertIn(b"Access unauthorized.", response.data)

    def test_logged_in_user_can_delete_message(self):
        """When logged in, can you delete a message as yourself?"""
        with self.client as client:
            with client.session_transaction() as session:
                session["user_id"] = self.user.id

            response = client.post(
                f"/messages/{self.message.id}/delete",
                follow_redirects=True
            )
            self.assertEqual(response.status_code, 200)
            self.assertNotIn(b"Test message", response.data)

    def test_logged_in_user_cannot_add_message_as_another_user(self):
        """When logged in, are you prohibited from adding a message as another user?"""
        with self.client as client:
            with client.session_transaction() as session:
                session["user_id"] = self.user.id

            response = client.post(
                f"/messages/new",
                data={"text": "New message", "user_id": self.user.id + 1},
                follow_redirects=True
            )
            self.assertEqual(response.status_code, 200)
            self.assertIn(b"Access unauthorized.", response.data)

    def test_logged_in_user_cannot_delete_message_as_another_user(self):
        """When logged in, are you prohibited from deleting a message as another user?"""
        other_user = User.create(
            username="otheruser",
            email="other@test.com",
            password="HASHED_PASSWORD"
        )
        db.session.commit()

        other_user_message = Message(
            text="Other user's message",
            user_id=other_user.id
        )
        db.session.add(other_user_message)
        db.session.commit()

        with self.client as client:
            with client.session_transaction() as session:
                session["user_id"] = self.user.id

            response = client.post(
                f"/messages/{other_user_message.id}/delete",
                follow_redirects=True
            )
            self.assertEqual(response.status_code, 200)
            self.assertIn(b"Access unauthorized.", response.data)

