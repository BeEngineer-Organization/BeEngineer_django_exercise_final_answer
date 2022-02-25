from django.test import TestCase
from django.core.exceptions import ValidationError

from forum.models import Tag, Topic, Message
from accounts.models import CustomUser


class TestTagModel(TestCase):
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

    def test_is_empty(self):
        records = Tag.objects.all()
        self.assertEqual(records.count(), 1)

    def test_created_num(self):
        records = Tag.objects.filter(name=self.tag_name)
        self.assertEqual(records.count(), 1)
        self.assertIn(self.tag, records)

    def test_get_record(self):
        record = Tag.objects.get(id=self.tag.id)
        self.assertEqual(record, self.tag)

    def test_default_value(self):
        self.assertEqual(self.tag.message.count(), 0)

    def test_update(self):
        self.tag.name = "TestTag2"
        self.tag.save()
        self.assertEqual(self.tag.name, "TestTag2")

    def test_delete(self):
        self.tag.delete()
        records = Tag.objects.filter(name=self.tag_name)
        self.assertEqual(records.count(), 0)

    def test_relation(self):
        self.tag.message.add(self.message)
        self.assertEqual(self.tag.message.count(), 1)
        self.assertIn(self.message, self.tag.message.all())

        self.tag.message.remove(self.message)
        self.assertEqual(self.tag.message.count(), 0)
