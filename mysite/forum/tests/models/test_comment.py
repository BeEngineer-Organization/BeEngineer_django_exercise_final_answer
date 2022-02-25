from django.test import TestCase
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile

from forum.models import Message, Topic, Comment
from accounts.models import CustomUser


class TestCommentModel(TestCase):
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
        cls.mes_content = "TestConent"
        cls.message = Message.objects.create(
            content=cls.mes_content,
            topic=cls.topic,
            user=cls.user,
        )

        # Comment
        cls.content = "TestConent"
        cls.comment = Comment.objects.create(
            content=cls.content,
            message=cls.message,
            user=cls.user,
        )

    def test_is_empty(self):
        records = Comment.objects.all()
        self.assertEqual(records.count(), 1)

    def test_created_num_by_content(self):
        records = Comment.objects.filter(content=self.content)
        self.assertEqual(records.count(), 1)
        self.assertIn(self.comment, records)

    def test_get_record(self):
        record = Comment.objects.get(id=self.comment.id)
        self.assertEqual(record, self.comment)

    def test_default_value(self):
        pass

    def test_update(self):
        self.comment.content = "TestContent2"
        self.comment.save()
        self.assertEqual(self.comment.content, "TestContent2")

    def test_delete(self):
        self.comment.delete()
        records = Comment.objects.filter(content=self.content)
        self.assertEqual(records.count(), 0)

    def test_relation_user(self):
        self.user.delete()
        records = Comment.objects.filter(content=self.content)
        self.assertEqual(records.count(), 0)
