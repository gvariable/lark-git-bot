from typing import *
from typing import Dict
import json

__all__ = ["InteractivePayload", "PushPayload"]


class Meta(object):
    def __init__(self, payload: Dict) -> None:
        self._sender = payload["sender"]
        self._avatar = self._sender["avatar_url"]
        self._user = self._sender["login"]
        self._user_link = self._sender["html_url"]
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
    def user_link(self) -> str:
        return self._user_link

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

    def __repr__(self) -> str:
        meta = {
            "title": self.title,
            "body": self.body,
            "user": self.user,
            "link": self.link,
            "user_link": self.user_link,
        }
        return json.dumps(meta, indent=4, ensure_ascii=False)


class InteractivePayload(Meta):
    def __init__(self, primary, payload: Dict) -> None:
        super().__init__(payload)
        if primary == "issues":
            primary = "issue"
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


class PushPayload(Meta):
    def __init__(self, payload: Dict) -> None:
        super().__init__(payload)
        self._title = f"{len(payload['commits'])} new commit"
        self._branch = payload["ref"].split("/")[-1]
        self._default_branch = payload["repository"]["default_branch"]
        self._link = payload["head_commit"]["url"]
        self._body = ""

        for commit in payload["commits"]:
            id = commit["id"][:7]
            url = commit["url"]
            message = commit["message"]
            self._body += f"[{id}]({url}): {message}\n"

    @property
    def title(self):
        return f"[{self.repo}:{self._branch}] {self._title}"
