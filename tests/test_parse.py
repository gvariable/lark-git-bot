import unittest
import json
from parse import PushPayload


class TestParse(unittest.TestCase):
    def test_push(self):
        with open("tests/data/push.json") as f:
            payload = json.load(f)
            meta = PushPayload(payload)
            print(meta)


if __name__ == "__main__":
    unittest.main()
