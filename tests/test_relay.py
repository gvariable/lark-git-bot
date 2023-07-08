import unittest
import requests
import json
from dotenv import load_dotenv


class TestRelay(unittest.IsolatedAsyncioTestCase):
    def setUp(self) -> None:
        if not load_dotenv(".env.test"):
            # TODO(gpl): error handling
            pass
        self.host = "localhost"
        self.port = 8080

    def send(self, headers, payload):
        return requests.post(
            f"http://{self.host}:{self.port}/relay",
            headers=headers,
            json=payload,
        )

    def test_push(self):
        with open("tests/data/push.json", "r") as f:
            headers = {"X-GitHub-Event": "push"}
            payload = json.load(f)
            resp = self.send(headers, payload)
            self.assertEqual(resp.status_code, 200)

    def test_pr(self):
        with open("tests/data/pr.json", "r") as f:
            headers = {"X-GitHub-Event": "pull_request"}
            payload = json.load(f)
            resp = self.send(headers, payload)
            self.assertEqual(resp.status_code, 200)

    def test_issue(self):
        with open("tests/data/issues.json", "r") as f:
            headers = {"X-GitHub-Event": "issues"}
            payload = json.load(f)
            resp = self.send(headers, payload)
            self.assertEqual(resp.status_code, 200)


if __name__ == "__main__":
    unittest.main()
