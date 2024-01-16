"""
Define the player object, and player roster collection of players
that are used by the other modules.
"""
import copy
import modules.exceptions
import random


class Player:
    # Results of match
    resWIN = 2
    resLOSS = 1
    resBUY = 0

    # Brackets (This probably should be tracked elsewhere. tournament() ? )
    brktWINNER = 2
    brktELIMINATION = 1
    brktOUT = 0

    def __init__(self, player_name: str):
        self.player_name: str = player_name
        self.player_bracket: int | None = None
        self.player_record: list[dict] = []

    def __eq__(self, other):
        return self.player_name == other.player_name and \
            self.player_record == other.player_record and \
            self.player_bracket == other.player_bracket

    def __ne__(self, other):
        return self.player_name == other.player_name and \
            self.player_record == other.player_record and \
            self.player_bracket == other.player_bracket

    def __str__(self):
        return self.player_name

    def tally_result(self, result, opponent, round_number, match_number):
        __result = dict(Result=result, Opponent=opponent, Round=round_number, Match=match_number)

        self.player_record.append(__result)

        if result == self.resBUY or result == self.resWIN:
            return
        else:
            match self.player_bracket:
                case self.brktWINNER:
                    self.player_bracket = self.brktELIMINATION
                case self.brktELIMINATION:
                    self.player_bracket = self.brktOUT
                case _:
                    raise modules.exceptions.BracketAssignmentError


class PlayerRoster:

    def __init__(self):
        self.players = []
        self.num_players = 0

    def __eq__(self, other):
        self_names = []
        other_names = []

        for _sp in self.players:
            self_names.append(_sp.player_name)

        for _op in other.players:
            other_names.append(_op.player_name)

        return sorted(self_names) == sorted(other_names)

    def __len__(self):
        return len(self.players)

    def add_player(self, player: Player):
        for _p in self.players:
            if _p.player_name == player.player_name:
                raise modules.exceptions.DuplicatePlayerError

        p = player
        p.player_bracket = Player.brktWINNER
        self.players.append(p)
        self.num_players += 1

    def randomize_player_order(self):
        # We want to be sure the random list is always distinct, so specifically
        # catch the edge case where shuffle() leaves the list unmodified
        _original = copy.deepcopy(self.players)
        while _original == self.players:
            random.shuffle(self.players)
