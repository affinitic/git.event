# -*- coding: utf-8 -*-
from zope.interface import Interface, Attribute


class IGitEvent(Interface):
    request = Attribute('The request object')


class IPullRequestEvent(IGitEvent):
    """
    An event type that is a Pull request
    """


class IPushEvent(IGitEvent):
    """
    An event type that is a Push
    """


class IGitRequest(Interface):

    event = Attribute('The name of the event')


class IPullRequest(IGitRequest):

    base_repo_url = Attribute('')

    base_repo_name = Attribute('')

    head_repo_url = Attribute('')

    head_repo_name = Attribute('')


class ICommit(Interface):

    id = Attribute('id')

    branch = Attribute('branch')

    author = Attribute('author')

    message = Attribute('message')

    timestamp = Attribute('timestamp')


class IPushRequest(IGitRequest):

    base_repo_url = Attribute('')

    base_repo_name = Attribute('')

    commits = Attribute('List of commit')
