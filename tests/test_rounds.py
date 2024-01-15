import unittest

from modules.exceptions import BracketPlayerCount
from modules.players import PlayerRoster, Player
from modules.rounds import RoundBrackets, Match


class TestMatchesAndBuys(unittest.TestCase):
    def setUp(self) -> None:
        self.player_Mary = Player("Mary")
        self.player_Sarah = Player("Sarah")
        self.player_Will = Player("Will")
        self.player_Margret = Player("Margret")
        self.player_Joe = Player("Joe")
        self.player_Jane = Player("Jane")
        self.player_Noa = Player("Noa")

    def test_matches_unit(self):
        Match.last_match_number = 0
        _match1 = Match()
        _match1.set_match_players(1, self.player_Noa, self.player_Jane)

        _match2 = Match()
        _match1.set_match_players(1, self.player_Joe, self.player_Will)

        self.assertEqual(2, _match1.last_match_number, "Increment match numbers")

    def test_roster_updates(self):
        _bracket = RoundBrackets(1)

        _roster = PlayerRoster()
        _roster.add_player(self.player_Mary)
        _roster.add_player(self.player_Sarah)
        _bracket.set_round_roster(_roster)

        self.assertEqual(_bracket.BracketRoster.Players[0].PlayerName, "Mary", "Bracket Roster Update")

    def test_buys_and_matches_functional(self):
        _bracket = RoundBrackets(1)

        _roster = PlayerRoster()
        _roster.add_player(self.player_Joe)
        _bracket.set_round_roster(_roster)
        _bracket.set_buys_and_matches()
        self.assertEqual(0, len(_bracket.Matches), "No matches if single player in bracket")

        _roster.add_player(self.player_Jane)
        _roster.add_player(self.player_Will)
        _bracket.set_round_roster(_roster)
        _bracket.set_buys_and_matches()

        self.assertEqual(2, len(_bracket.ActivePlayers), "Actives for 3 players")
        self.assertEqual(1, len(_bracket.Buys), "Buys for 3 players")
        self.assertEqual(1, len(_bracket.Matches), "Matches for 3 players")

        _roster.add_player(self.player_Margret)
        _bracket.set_buys_and_matches()
        self.assertEqual(4, len(_bracket.ActivePlayers), "Actives for 4 players")
        self.assertEqual(0, len(_bracket.Buys), "Buys for 4 players")
        self.assertEqual(2, len(_bracket.Matches), "Matches for 4 players")

        _roster.add_player(self.player_Noa)
        _bracket.set_buys_and_matches()
        self.assertEqual(2, len(_bracket.ActivePlayers), "Actives for 5 players")
        self.assertEqual(3, len(_bracket.Buys), "Buys for 5 players")
        self.assertEqual(1, len(_bracket.Matches), "Matches for 5 players")
