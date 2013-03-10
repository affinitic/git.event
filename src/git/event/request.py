# -*- coding: utf-8 -*-
import json
from pyramid.decorator import reify
from pyramid.request import Request


class GitRequest(Request):
    event = None

    @reify
    def json_body(self):
        return json.loads(self.body, encoding=self.charset)


class GitPullRequest(GitRequest):
    event = 'pull_request'


class GitPushRequest(GitRequest):
    event = 'push'
