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

        self.assertEqual(len(_roster.players), 3, "Add players to roster")
        self.assertIsInstance(_roster.players[0], Player, "Player list populated by player class members")

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
        _initial = copy.deepcopy(_roster.players)
        _roster.randomize_player_order()
        self.assertNotEqual(_initial, _roster.players, "Play list randomization")


class TestPlayerObject(unittest.TestCase):

    def setUp(self) -> None:
        self.player_Joe = Player("Joe")
        self.player_Sarah = Player("Sarah")

    def test_tally_match_results(self):
        _roster = PlayerRoster()
        _roster.add_player(self.player_Joe)
        _roster.add_player(self.player_Sarah)

        _roster.players[0].tally_result(_roster.players[0].resBUY, None, 1, 1)
        _roster.players[0].tally_result(_roster.players[0].resLOSS, "Sarah", 2, 4)
        _roster.players[0].tally_result(_roster.players[0].resWIN, "Meg", 3, 6)

        _expect = {
            "Result": _roster.players[0].resWIN,
            "Opponent": "Meg",
            "Round": 3,
            "Match": 6
        }

        self.assertEqual(_expect, _roster.players[0].player_record[3], "Player results tallied.")
        self.assertEqual(_roster.players[0].player_bracket, _roster.players[0].brktELIMINATION,
                         "Bracket placement after loss")

        _roster.players[0].tally_result(_roster.players[0].resLOSS, "Sarah", 2, 4)
        self.assertEqual(_roster.players[0].player_bracket,
                         _roster.players[0].brktOUT, "Bracket placement after elimination"
                         )
