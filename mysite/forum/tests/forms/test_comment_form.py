from django.test import TestCase
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile

from forum.forms import CommentForm

from forum.models import Topic, Message, Comment
from accounts.models import CustomUser


class TestCommentForm(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass

    def test_fields(self):
        form = CommentForm()
        self.assertEqual(len(form.fields), 1)

    def test_valid(self):
        valid_data = {
            "content": "TestContent",
        }
        valid_form = CommentForm(valid_data)
        self.assertTrue(valid_form.is_valid())

    def test_invalid_too_long_content(self):
        invalid_data = {
            "content": "a" * 201,
        }
        invalid_form = CommentForm(invalid_data)
        self.assertFalse(invalid_form.is_valid())
        self.assertIn("at most 200 characters", invalid_form.errors["content"][0])

    def test_invalid_without_content(self):
        invalid_data = {}
        invalid_form = CommentForm(invalid_data)
        self.assertFalse(invalid_form.is_valid())
        self.assertIn("This field is required.", invalid_form.errors["content"][0])
