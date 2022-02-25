from django.test import TestCase
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile

from forum.forms import MessageSearchForm

from forum.models import Topic, Message, Comment
from accounts.models import CustomUser


class TestMessageSearchForm(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass

    def test_fields(self):
        form = MessageSearchForm()
        self.assertEqual(len(form.fields), 1)

    def test_valid(self):
        valid_data = {
            "keyword": "TestKeyword",
        }
        valid_form = MessageSearchForm(valid_data)
        self.assertTrue(valid_form.is_valid())

    def test_invalid_without_content(self):
        invalid_data = {}
        invalid_form = MessageSearchForm(invalid_data)
        self.assertFalse(invalid_form.is_valid())
        self.assertIn("This field is required.", invalid_form.errors["keyword"][0])
