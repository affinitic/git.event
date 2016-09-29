# -*- coding: utf-8 -*-
import re

KEYWORDS = {'resolve': ('fix', 'fixes', 'fixe', 'close', 'closes'),
            'refs': ('refs', 'ref', 'reference'),
            'production': ('prod', 'production', 'productions'),
            'test': ('test', 'tests', 'testing'),
            'leave': tuple(),
            'reassign': tuple(),
            'analyze': tuple(),
            'develop': tuple(),
            }


def parse_commit_message(message):
    """
    Return useful data in a commit message

    Ex: "This is a message refs #6060 affinitic"
    return [{"ticket": "6060",
             "trac": "affinitic"}]

    Ex2: "Refs 2020 arsia new commit message
          But also for refs #6060 affinitic"
    return [{"command": "refs",
             "ticket": "2020",
             "trac": "arsia"},
            {"command": "closes",
             "ticket": "6060",
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

    # ['closes', 'close', 'fix', ...]
    keywords = []
    [keywords.extend(val) for val in KEYWORDS.values()]

    # 'close|closes|fix...'
    keywords_re = '|'.join(keywords)

    # refs = ['Refs #6060 affinitic', 'fixes 2020 arsia']
    refs = re.findall("(?:%s)(?:\s[^\s]+){2}" % keywords_re,
                      message,
                      re.IGNORECASE)

    if not refs:
        return parseds

    for ref in refs:
        parsed = {}

        # datas = ['#5060', 'affinitic']
        split = ref.split()
        datas = split[-2:]

        ticket = '0'
        for data in datas:
            found = re.findall('\d+', data)
            if found:
                ticket = found[0]

        trac = ''
        for data in datas:
            found = re.findall('[a-zA-Z]+', data)
            if found:
                trac = found[0]

        command = _word_to_command(split[0])
        parsed["command"] = command
        parsed["ticket"] = ticket
        parsed["trac"] = trac.lower()
        parseds.append(parsed)

    return parseds


def _word_to_command(word):
    """
    Return corresponding command for a word
    """
    for command in KEYWORDS:
        for w in KEYWORDS[command]:
            if w == word:
                return command
