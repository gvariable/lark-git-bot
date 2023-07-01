from typing import *
from typing import Dict
import json


class Meta(object):
    def __init__(self, payload: Dict) -> None:
        self._sender = payload["sender"]
        self._avatar = self._sender["avatar_url"]
        self._user = self._sender["login"]
        self._repo = payload["repository"]
        self._link = None
        self._title = None
        self._body = None

    @property
    def repo(self) -> str:
        return self._repo["full_name"]

    @property
    def avatar(self) -> str:
        return self._avatar

    @property
    def user(self) -> str:
        return self._user

    @property
    def link(self) -> str:
        return self._link

    @property
    def title(self) -> str:
        if not self._title:
            return ""
        return self._title

    @property
    def body(self):
        if not self._body:
            return ""
        return self._body


class InteractiveMessage(Meta):
    def __init__(self, primary, payload: Dict) -> None:
        super().__init__(payload)
        self._primary = primary
        self._number = payload[primary]["number"]
        self._action = payload["action"]
        self._title = payload[primary]["title"]
        self._body = payload[primary]["body"]
        self._link = payload[primary]["html_url"]

    @property
    def title(self):
        primary = " ".join(self._primary.split("_")).capitalize()
        return f"[{self.repo}] {primary} {self._action}: #{self._number} {self._title}"


class Push(Meta):
    def __init__(self, payload: Dict) -> None:
        super().__init__(payload)
        self._title = payload["head_commit"]["message"].split("\n")[0]
        self._link = payload["head_commit"]["url"]
        self._body = payload["head_commit"]["message"].split("\n")[1:]

    @property
    def title(self):
        return f"[{self.repo}] Push: {self._title}"


if __name__ == "__main__":

    def test(fn, primary):
        with open(fn) as f:
            im = InteractiveMessage(primary, json.load(f))
            print(im.title)
            print(im.body)
            print(im.link)
            print()

    test("pr.json", "pull_request")
    test("issue.json", "issue")

    with open("push.json") as f:
        p = Push(json.load(f))
        print(p.title)
        print(p.body)
        print(p.link)
        print()
