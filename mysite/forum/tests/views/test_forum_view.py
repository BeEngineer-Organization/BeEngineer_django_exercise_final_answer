from django.test import TestCase

from django.core.files.uploadedfile import SimpleUploadedFile

from forum.models import Tag, Topic, Message, Comment
from accounts.models import CustomUser


class TestWithAuthMixin:
    @classmethod
    def setUpTestData(cls):
        cls._username = "TestName"
        cls._email = "test@test.com"
        cls._password = "thisistest"
        cls.user = CustomUser.objects.create_user(
            username=cls._username, email=cls._email, password=cls._password
        )

    def login(self):
        return self.client.login(username=self._username, password=self._password)


class TestForumView(TestWithAuthMixin, TestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()

        # Topic
        cls.topic_name = "TestTopic"
        cls.topic = Topic.objects.create(name=cls.topic_name)

        # Tag
        cls.tag_name = "TestTag"
        cls.tag = Tag.objects.create(
            name=cls.tag_name,
        )

        cls.tag_name2 = "TestTag2"
        cls.tag2 = Tag.objects.create(
            name=cls.tag_name2,
        )

        # Message
        cls.content = "TestConent"
        cls.message = Message.objects.create(
            content=cls.content,
            topic=cls.topic,
            user=cls.user,
        )

        # Image
        cls.gif = (
            b"\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x00\x00\x00\x21\xf9\x04"
            b"\x01\x0a\x00\x01\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02"
            b"\x02\x4c\x01\x00\x3b"
        )
        cls.image = SimpleUploadedFile("test.gif", cls.gif, content_type="image/gif")

        cls.forum_url = f"/ja/forum/{cls.topic_name}/"

    def test_get(self):
        res = self.client.get(self.forum_url)
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, "forum/forum.html")

    def test_valid_message_post_with_image(self):
        self.login()
        valid_form = {
            "message": "value",  # ボタンを押した想定
            "content": self.content,
            "tag": [1],
            "image": self.image,
        }
        res = self.client.post(self.forum_url, valid_form)
        self.assertRedirects(
            res,
            self.forum_url,
            status_code=302,
            target_status_code=200,
            fetch_redirect_response=True,
        )
        records = Message.objects.filter(content=self.content)
        self.assertEqual(records.count(), 2)

    def test_valid_message_post_without_image(self):
        self.login()
        valid_form = {
            "message": "value",  # ボタンを押した想定
            "content": self.content,
            "tag": [1],
        }
        res = self.client.post(self.forum_url, valid_form)
        self.assertRedirects(
            res,
            self.forum_url,
            status_code=302,
            target_status_code=200,
            fetch_redirect_response=True,
        )
        records = Message.objects.filter(content=self.content)
        self.assertEqual(records.count(), 2)

    def test_valid_message_post_without_tag(self):
        self.login()
        valid_form = {
            "message": "value",  # ボタンを押した想定
            "content": self.content,
        }
        res = self.client.post(self.forum_url, valid_form)
        self.assertRedirects(
            res,
            self.forum_url,
            status_code=302,
            target_status_code=200,
            fetch_redirect_response=True,
        )
        records = Message.objects.filter(content=self.content)
        self.assertEqual(records.count(), 2)

    def test_valid_message_post_with_tags(self):
        self.login()
        valid_form = {
            "message": "value",  # ボタンを押した想定
            "content": self.content,
            "tag": [1, 2],
            "image": self.image,
        }
        res = self.client.post(self.forum_url, valid_form)
        self.assertRedirects(
            res,
            self.forum_url,
            status_code=302,
            target_status_code=200,
            fetch_redirect_response=True,
        )
        records = Message.objects.filter(content=self.content)
        self.assertEqual(records.count(), 2)

    def test_invalid_message_post_not_authenticated(self):
        invalid_form = {
            "message": "value",  # ボタンを押した想定
            "content": "TestContent",
            "tag": [1],
            "image": self.image,
        }
        res = self.client.post(self.forum_url, invalid_form)
        self.assertEqual(res.status_code, 302)  # ここはリダイレクト
        records = Message.objects.filter(content=self.content)
        self.assertEqual(records.count(), 1)

    def test_invalid_message_post_not_exist_tag(self):
        self.login()
        invalid_form = {
            "message": "value",  # ボタンを押した想定
            "content": "TestContent",
            "tag": [3],
            "image": self.image,
        }
        res = self.client.post(self.forum_url, invalid_form)
        self.assertEqual(res.status_code, 302)
        records = Message.objects.filter(content=self.content)
        self.assertEqual(records.count(), 1)

    def test_invalid_message_post_too_long_content(self):
        self.login()
        invalid_form = {
            "message": "value",  # ボタンを押した想定
            "content": "a" * 201,
        }
        res = self.client.post(self.forum_url, invalid_form)
        self.assertEqual(res.status_code, 302)
        records = Message.objects.filter(content=self.content)
        self.assertEqual(records.count(), 1)

    def test_invalid_message_post_without_content(self):
        self.login()
        invalid_form = {
            "message": "value",  # ボタンを押した想定
        }
        res = self.client.post(self.forum_url, invalid_form)
        self.assertEqual(res.status_code, 302)
        records = Message.objects.filter(content=self.content)
        self.assertEqual(records.count(), 1)

    def test_valid_comment_post(self):
        self.login()
        valid_form = {
            "comment": "1",  # ボタンを押した想定
            "content": self.content,
        }
        res = self.client.post(self.forum_url, valid_form)
        self.assertRedirects(
            res,
            self.forum_url,
            status_code=302,
            target_status_code=200,
            fetch_redirect_response=True,
        )
        records = Comment.objects.filter(content=self.content)
        self.assertEqual(records.count(), 1)

    def test_invalid_comment_post_not_authenticated(self):
        invalid_form = {
            "comment": "1",  # ボタンを押した想定
            "content": self.content,
        }
        res = self.client.post(self.forum_url, invalid_form)
        self.assertEqual(res.status_code, 302)
        records = Comment.objects.filter(content=self.content)
        self.assertEqual(records.count(), 0)

    def test_invalid_comment_post_not_exist_message(self):
        self.login()
        invalid_form = {
            "comment": "2",  # ボタンを押した想定
            "content": self.content,
        }
        res = self.client.post(self.forum_url, invalid_form)
        self.assertEqual(res.status_code, 404)
        records = Comment.objects.filter(content=self.content)
        self.assertEqual(records.count(), 0)

    def test_invalid_comment_post_without_content(self):
        self.login()
        invalid_form = {
            "comment": "2",  # ボタンを押した想定
        }
        res = self.client.post(self.forum_url, invalid_form)
        self.assertEqual(res.status_code, 302)
        records = Comment.objects.filter(content=self.content)
        self.assertEqual(records.count(), 0)

    def test_valid_message_search_post(self):
        self.login()
        valid_url = f"{self.forum_url}?keyword=test_keyword"
        res = self.client.get(valid_url)
        self.assertEqual(res.status_code, 200)
