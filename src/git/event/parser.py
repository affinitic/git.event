# -*- coding: utf-8 -*-
import re


def parse_commit_message(message):
    """
    Return useful data in a commit message

    Ex: "This is a message refs #6060 affinitic"
    return {"ticket": "6060",
            "trac": "affinitic"}
    Allowed formats:
        "Message refs 6060 affinitic"
        "Message refs #6060 affinitic"
        "Message Refs 6060 affinitic"
        "Message refs affinitic 6060"
        "refs 6060 affinitic Message"
    """
    parsed = {}

    # refs = ['Refs #5060 affinitic']
    refs = re.findall("refs(?:\s[^\s]+){2}",
                      message,
                      re.IGNORECASE)
    if not refs:
        return parsed

    # datas = ['#5060', 'affinitic']
    datas = refs[-1].split()[-2:]

    ticket = 0
    for data in datas:
        found = re.findall('\d+', data)
        if found:
            ticket = found[0]

    trac = ''
    for data in datas:
        found = re.findall('[a-zA-Z]+', data)
        if found:
            trac = found[0]

    parsed["ticket"] = ticket
    parsed["trac"] = trac.lower()

    return parsed