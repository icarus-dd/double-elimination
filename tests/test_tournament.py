import unittest

from modules.players import PlayerRoster, Player
from modules.tournament import Tournament


class TestTournamentInitialization(unittest.TestCase):

    def setUp(self) -> None:
        self.player_Joe = Player("Joe")
        self.player_Jane = Player("Jane")
        self.player_Will = Player("Will")
    def test_add_roster(self):
        # Mock data
        __roster = PlayerRoster()
        __roster.add_player(self.player_Joe)
        __roster.add_player(self.player_Jane)
        __roster.add_player(self.player_Will)

        tourn = Tournament()
        tourn.set_player_roster(__roster)
        self.assertEqual(__roster, tourn.full_roster, "Initialize full roster")
        self.assertEqual(__roster, tourn.winner_roster, "Initialize winner's bracket roster")

    def test_final_round(self):
        tourn = Tournament()

        __fr = PlayerRoster()
        __w = PlayerRoster()
        __e = PlayerRoster()
        __w.add_player(self.player_Joe)
        __e.add_player(self.player_Jane)
        tourn.winner_roster = __w
        tourn.elimination_roster = __e
        tourn.set_round()
        self.assertTrue(tourn.is_final_round, "Final round detection (1 of 3)")

        __w = PlayerRoster()
        __e = PlayerRoster()
        __w.add_player(self.player_Joe)
        __w.add_player(self.player_Jane)
        tourn.winner_roster = __w
        tourn.elimination_roster = __e
        tourn.set_round()
        self.assertTrue(tourn.is_final_round, "Final round detection (2 of 3)")

        __w = PlayerRoster()
        __e = PlayerRoster()
        __w.add_player(self.player_Joe)
        __w.add_player(self.player_Jane)
        __e.add_player(self.player_Will)
        tourn.winner_roster = __w
        tourn.elimination_roster = __e
        tourn.set_round()
        self.assertFalse(tourn.is_final_round, "Final round detection (3 of 3)")
