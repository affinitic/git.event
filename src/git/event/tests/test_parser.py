from git.event.parser import parse_commit_message
import unittest


class TestParser(unittest.TestCase):

    def test_empty(self):
        parsed = parse_commit_message("Message foo affinitic #1")
        self.assertEquals(
            parsed,
            []
        )

    def test_ambiguous_actions(self):
        parsed = parse_commit_message("Message ref affinitic #1")
        self.assertEquals(
            parsed,
            [{'ticket': '1', 'command': 'refs', 'trac': 'affinitic'}]
        )
        parsed = parse_commit_message("Message refs affinitic #1")
        self.assertEquals(
            parsed,
            [{'ticket': '1', 'command': 'refs', 'trac': 'affinitic'}]
        )
        parsed = parse_commit_message("Message close affinitic #1")
        self.assertEquals(
            parsed,
            [{'ticket': '1', 'command': 'resolve', 'trac': 'affinitic'}]
        )
        parsed = parse_commit_message("Message closes affinitic #1")
        self.assertEquals(
            parsed,
            [{'ticket': '1', 'command': 'resolve', 'trac': 'affinitic'}]
        )

    def test_single_ticket(self):
        parsed = parse_commit_message("Message refs affinitic #1")
        self.assertEquals(
            parsed,
            [{'ticket': '1', 'command': 'refs', 'trac': 'affinitic'}]
        )
        parsed = parse_commit_message("Message refs affinitic 1")
        self.assertEquals(
            parsed,
            [{'ticket': '1', 'command': 'refs', 'trac': 'affinitic'}]
        )

    def test_double_tickets(self):
        parsed = parse_commit_message("Message refs affinitic #1 and refs affinitic #2")
        self.assertEquals(
            parsed,
            [{'ticket': '1', 'command': 'refs', 'trac': 'affinitic'},
             {'ticket': '2', 'command': 'refs', 'trac': 'affinitic'}]
        )

    def test_double_tracs(self):
        parsed = parse_commit_message("Message refs affinitic #1 and refs arsia #2")
        self.assertEquals(
            parsed,
            [{'ticket': '1', 'command': 'refs', 'trac': 'affinitic'},
             {'ticket': '2', 'command': 'refs', 'trac': 'arsia'}]
        )

    def test_condensed_tickets(self):
        parsed = parse_commit_message("Message refs affinitic #1 #2 #3")
        self.assertEquals(
            parsed,
            [{'ticket': '1', 'command': 'refs', 'trac': 'affinitic'},
             {'ticket': '2', 'command': 'refs', 'trac': 'affinitic'},
             {'ticket': '3', 'command': 'refs', 'trac': 'affinitic'}]
        )
        parsed = parse_commit_message("Message refs affinitic #1 #2 #3 and refs arsia #5")
        self.assertEquals(
            parsed,
            [{'ticket': '1', 'command': 'refs', 'trac': 'affinitic'},
             {'ticket': '2', 'command': 'refs', 'trac': 'affinitic'},
             {'ticket': '3', 'command': 'refs', 'trac': 'affinitic'},
             {'ticket': '5', 'command': 'refs', 'trac': 'arsia'}]
        )
