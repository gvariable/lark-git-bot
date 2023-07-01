from bot import send_card
import unittest


class TestBot(unittest.IsolatedAsyncioTestCase):
    def setUp(self) -> None:
        self.meta = {
            "title": "Title placeholder",
            "body": "Body placeholder",
            "user": "gvariable",
            "link": "https://github.com",
            "user_link": "https://github.com/gvariable",
        }

    async def test_send_card(self):
        retval = await send_card(self.meta)
        self.assertEqual(retval, None)


if __name__ == "__main__":
    unittest.main()
