from unittest import TestCase, mock
from ..utils.misc import who_is


class TestMisc(TestCase):
    def setUp(self):
        self.mock_message = mock.Mock()
        mock_channel = mock.Mock()
        self.mock_member_1 = mock.Mock()
        self.mock_member_1.display_name = "John"
        self.mock_member_2 = mock.Mock()
        self.mock_member_2.display_name = "Sherlock"
        self.mock_message.mentions = []
        self.mock_message.channel = mock_channel
        mock_channel.members = [self.mock_member_1, self.mock_member_2]

    def test_no_person_found(self):
        self.assertEqual("", who_is("Adam", self.mock_message))

    def test_one_person_found_no_mention(self):
        self.assertEqual("John", who_is("john", self.mock_message))

    def test_one_person_found_with_mention(self):
        self.mock_message.mentions = [self.mock_member_2]
        self.assertEqual("Sherlock", who_is("sherlock", self.mock_message))

    def test_two_people_found_with_mention(self):
        self.mock_message.mentions = [self.mock_member_2, self.mock_member_1]
        self.assertEqual("", who_is("sherlock", self.mock_message))
