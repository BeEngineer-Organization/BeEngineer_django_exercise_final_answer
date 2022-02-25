from django.test import TestCase
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile

from forum.forms import MessageForm

from forum.models import Tag, Topic, Message
from accounts.models import CustomUser


class TestMessageForm(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Topic
        cls.name = "TestTopic"
        cls.topic = Topic.objects.create(name=cls.name)

        # User
        cls.username = "TestName"
        cls.email = "test@test.com"
        cls.user = CustomUser.objects.create(username=cls.username, email=cls.email)

        # Message
        cls.content = "TestConent"
        cls.message = Message.objects.create(
            content=cls.content,
            topic=cls.topic,
            user=cls.user,
        )

        # Tag
        cls.tag_name = "TestTag"
        cls.tag = Tag.objects.create(
            name=cls.tag_name,
        )

        # Tag
        cls.tag_name2 = "TestTag2"
        cls.tag2 = Tag.objects.create(
            name=cls.tag_name2,
        )

        # Image
        cls.gif = (
            b"\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x00\x00\x00\x21\xf9\x04"
            b"\x01\x0a\x00\x01\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02"
            b"\x02\x4c\x01\x00\x3b"
        )
        cls.image = SimpleUploadedFile("test.gif", cls.gif, content_type="image/gif")

    def test_fields(self):
        form = MessageForm()
        self.assertEqual(len(form.fields), 3)

    def test_valid_with_image(self):
        valid_data = {
            "tag": [1],
            "content": "TestContent",
            "image": self.image,
        }
        valid_form = MessageForm(valid_data)
        self.assertTrue(valid_form.is_valid())

    def test_valid_without_image(self):
        valid_data = {
            "tag": [1],
            "content": "TestContent",
        }
        valid_form = MessageForm(valid_data)
        self.assertTrue(valid_form.is_valid())

    def test_valid_with_tags(self):
        valid_data = {
            "tag": [1, 2],
            "content": "TestContent",
        }
        valid_form = MessageForm(valid_data)
        self.assertTrue(valid_form.is_valid())

    def test_valid_without_tag(self):
        valid_data = {
            "content": "TestContent",
        }
        valid_form = MessageForm(valid_data)
        self.assertTrue(valid_form.is_valid())

    def test_invalid_not_exist_tag(self):
        invalid_data = {
            "tag": [3],
            "content": "TestContent",
        }
        invalid_form = MessageForm(invalid_data)
        self.assertFalse(invalid_form.is_valid())
        self.assertIn(
            "is not one of the available choices", invalid_form.errors["tag"][0]
        )

    def test_invalid_too_long_content(self):
        invalid_data = {
            "content": "a" * 201,
        }
        invalid_form = MessageForm(invalid_data)
        self.assertFalse(invalid_form.is_valid())
        self.assertIn("at most 200 characters", invalid_form.errors["content"][0])

    def test_invalid_without_content(self):
        invalid_data = {}
        invalid_form = MessageForm(invalid_data)
        self.assertFalse(invalid_form.is_valid())
        self.assertIn("This field is required.", invalid_form.errors["content"][0])
