from django.test import TestCase
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile

from forum.models import Message, Topic
from accounts.models import CustomUser


class TestMessageModel(TestCase):
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

    def test_is_empty(self):
        records = Message.objects.all()
        self.assertEqual(records.count(), 1)

    def test_created_num_by_content(self):
        records = Message.objects.filter(content=self.content)
        self.assertEqual(records.count(), 1)
        self.assertIn(self.message, records)

    def test_get_record(self):
        record = Message.objects.get(id=self.message.id)
        self.assertEqual(record, self.message)

    def test_default_value(self):
        self.assertEqual(self.message.image, None)

    def test_update(self):
        self.message.content = "TestContent2"
        self.message.save()
        self.assertEqual(self.message.content, "TestContent2")

    def test_delete(self):
        self.message.delete()
        records = Message.objects.filter(content=self.content)
        self.assertEqual(records.count(), 0)

    def test_relation_user(self):
        self.user.delete()
        records = Message.objects.filter(content=self.content)
        self.assertEqual(records.count(), 0)

    def test_save_image(self):
        self.gif = (
            b"\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x00\x00\x00\x21\xf9\x04"
            b"\x01\x0a\x00\x01\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02"
            b"\x02\x4c\x01\x00\x3b"
        )
        self.image = SimpleUploadedFile("test.gif", self.gif, content_type="image/gif")
        self.message = Message.objects.create(
            content=self.content,
            image=self.image,
            topic=self.topic,
            user=self.user,
        )
        self.assertNotEqual(self.message.image, None)
