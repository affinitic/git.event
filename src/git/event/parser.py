# -*- coding: utf-8 -*-
import re


def parse_commit_message(message):
    """
    Return useful data in a commit message

    Ex: "This is a message refs #6060 affinitic"
    return [{"ticket": "6060",
             "trac": "affinitic"}]

    Ex2: "Refs 2020 arsia new commit message
          But also for refs #6060 affinitic"
    return [{"ticket": "2020",
             "trac": "arsia"},
            {"ticket": "6060",
             "trac": "affinitic"}]

    Allowed formats:
        "Message refs 6060 affinitic"
        "Message refs #6060 affinitic"
        "Message Refs 6060 affinitic"
        "Message refs affinitic 6060"
        "refs 6060 affinitic Message"
        "Message refs 6060 affinitic and refs #2020 arsia"
    """
    parseds = []

    # refs = ['Refs #5060 affinitic']
    refs = re.findall("refs(?:\s[^\s]+){2}",
                      message,
                      re.IGNORECASE)
    if not refs:
        return parseds

    for ref in refs:
        parsed = {}

        # datas = ['#5060', 'affinitic']
        datas = ref.split()[-2:]

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
        parseds.append(parsed)

    return parseds