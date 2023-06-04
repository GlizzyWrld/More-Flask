import os
from unittest import TestCase
from sqlalchemy import exc
from models import db, User, Message, Follows

os.environ['DATABASE_URL'] = "postgresql:///warbler-test"

# Now we can import app
from app import app

# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data
db.create_all()



class MessageModelTestCase(TestCase):
    """Test cases for the Message model."""

    def setUp(self):
        """Create test client, add sample data."""
        User.query.delete()
        Message.query.delete()
        Follows.query.delete()

        self.client = app.test_client()

    def test_message_model(self):
        """Does basic model work?"""
        user = User.create(
            username="testuser",
            email="test@test.com",
            password="HASHED_PASSWORD"
        )
        db.session.commit()

        message = Message(text="Test message", user_id=user.id)
        db.session.add(message)
        db.session.commit()

        self.assertEqual(len(user.messages), 1)
        self.assertEqual(user.messages[0].text, "Test message")