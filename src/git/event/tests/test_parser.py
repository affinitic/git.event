from git.event.parser import parse_commit_message
import unittest


class TestParser(unittest.TestCase):

    def test_single_ticket(self):
        parsed = parse_commit_message("Message refs #1 affinitic")
        self.assertEquals(
            parsed,
            [{'ticket': '1', 'command': 'refs', 'trac': 'affinitic'}]
        )
        parsed = parse_commit_message("Message refs 1 affinitic")
        self.assertEquals(
            parsed,
            [{'ticket': '1', 'command': 'refs', 'trac': 'affinitic'}]
        )
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
        parsed = parse_commit_message("Message refs #1 affinitic and refs #2 affinitic")
        self.assertEquals(
            parsed,
            [{'ticket': '1', 'command': 'refs', 'trac': 'affinitic'},
             {'ticket': '2', 'command': 'refs', 'trac': 'affinitic'}]
        )

    def test_double_tracs(self):
        parsed = parse_commit_message("Message refs #1 affinitic and refs #2 arsia")
        self.assertEquals(
            parsed,
            [{'ticket': '1', 'command': 'refs', 'trac': 'affinitic'},
             {'ticket': '2', 'command': 'refs', 'trac': 'arsia'}]
        )
