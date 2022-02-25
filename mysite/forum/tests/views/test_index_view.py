from django.test import TestCase


class TestIndexView(TestCase):
    def test_get(self):
        res = self.client.get("/ja/forum/")
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, "forum/index.html")
