from django.test import TestCase
from django.core.exceptions import ValidationError

from forum.models import Topic


class TestTopicModel(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.name = "TestTopic"
        cls.topic = Topic.objects.create(name=cls.name)

    def test_is_empty(self):
        records = Topic.objects.all()
        self.assertEqual(records.count(), 1)

    def test_created_num(self):
        records = Topic.objects.filter(name=self.name)
        self.assertEqual(records.count(), 1)
        self.assertIn(self.topic, records)

    def test_get_record(self):
        record = Topic.objects.get(id=self.topic.id)
        self.assertEqual(record, self.topic)

    def test_default_value(self):
        pass

    def test_update(self):
        self.topic.name = "TestTopic2"
        self.topic.save()
        self.assertEqual(self.topic.name, "TestTopic2")

    def test_delete(self):
        self.topic.delete()
        records = Topic.objects.filter(name=self.name)
        self.assertEqual(records.count(), 0)

    def test_relation(self):
        pass
