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

    Ex: "This is a message refs affinitic #6060"
    return [{"command": "refs",
             "ticket": "6060",
             "trac": "affinitic"}]

    Ex2: "Refs arsia 2020 new commit message
          But also for refs affinitic #6060"
    return [{"command": "refs",
             "ticket": "2020",
             "trac": "arsia"},
            {"command": "closes",
             "ticket": "6060",
             "trac": "affinitic"}]

    Allowed formats:
        "Message refs affinitic 6060"
        "Message refs affinitic #6060 #7070 #8080"
        "Message Refs affinitic 6060"
        "Message refs affinitic 6060"
        "refs affinitic 6060 Message"
        "Message refs affinitic 6060 and refs arsia #2020"
    """
    # ['closes', 'close', 'fix', ...]
    keywords = []
    [keywords.extend(val) for val in KEYWORDS.values()]
    # we need to sort to match longuest command possible
    keywords.sort(lambda x, y: cmp(len(y), len(x)))
    # 'closes|close|fix...'
    keywords_re = '|'.join(keywords)

    # [('refs', 'affinitic', '#1'), ('refs', 'affinitic', '#2')]
    refs = re.findall('(%s)[ ]*([a-z]+)[ ]*([# \d]*)' % keywords_re,
                      message,
                      re.IGNORECASE)

    parseds = []
    for ref in refs:
        if len(ref) != 3:
            # XXX envoi de mail si 1 < ref < 3 ?
            continue

        command = _word_to_command(ref[0])
        trac = ref[1].lower()
        tickets = ref[2]

        ticket = '0'
        tickets_split = re.findall('\d+', tickets)
        for ticket in tickets_split:
            parsed = {}
            parsed["command"] = command
            parsed["ticket"] = ticket
            parsed["trac"] = trac
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
