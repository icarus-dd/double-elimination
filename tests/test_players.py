import copy
import unittest

from modules.exceptions import DuplicatePlayerError
from modules.players import PlayerRoster, Player


class TestPlayerRoster(unittest.TestCase):

    def setUp(self) -> None:
        self.player_Joe = Player("Joe")
        self.player_Jane = Player("Jane")
        self.player_Will = Player("Will")

    def test_add_player(self):
        _roster = PlayerRoster()
        _roster.add_player(self.player_Joe)
        _roster.add_player(self.player_Jane)
        _roster.add_player(self.player_Will)

        self.assertEqual(len(_roster.Players), 3, "Add players to roster")
        self.assertIsInstance(_roster.Players[0], Player, "Player list populated by player class members")

    def test_duplicate_player_error(self):
        _roster = PlayerRoster()
        _roster.add_player(self.player_Joe)
        with self.assertRaises(DuplicatePlayerError):
            _roster.add_player(self.player_Joe)

    def test_randomize_player_order(self):
        _roster = PlayerRoster()
        _roster.add_player(self.player_Joe)
        _roster.add_player(self.player_Jane)
        _roster.add_player(self.player_Will)

        # we want to ensure that the new player list is ALWAYS unique from the initial one,
        # even in cases where it randomly goes back to the original order
        _initial = copy.deepcopy(_roster.Players)
        _roster.randomize_player_order()
        self.assertNotEqual(_initial, _roster.Players, "Play list randomization")


class TestPlayerObject(unittest.TestCase):

    def setUp(self) -> None:
        self.player_Joe = Player("Joe")
        self.player_Sarah = Player("Sarah")

    def test_tally_match_results(self):
        _roster = PlayerRoster()
        _roster.add_player(self.player_Joe)
        _roster.add_player(self.player_Sarah)

        _roster.Players[0].tally_result(_roster.Players[0].resBUY, None, 1, 1)
        _roster.Players[0].tally_result(_roster.Players[0].resLOSS, "Sarah", 2, 4)
        _roster.Players[0].tally_result(_roster.Players[0].resWIN, "Meg", 3, 6)

        _expect = {
            "Result": _roster.Players[0].resWIN,
            "Opponent": "Meg",
            "Round": 3,
            "Match": 6
        }

        self.assertEqual(_expect, _roster.Players[0].PlayerRecord[3], "Player results tallied.")
        self.assertEqual(_roster.Players[0].PlayerBracket, _roster.Players[0].brktELIMINATION,
                         "Bracket placement after loss")

        _roster.Players[0].tally_result(_roster.Players[0].resLOSS, "Sarah", 2, 4)
        self.assertEqual(_roster.Players[0].PlayerBracket,
                         _roster.Players[0].brktOUT, "Bracket placement after elimination"
                         )
