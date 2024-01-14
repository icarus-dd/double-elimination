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

    # Brackets (This probably should be tracket elsewhere. tournement() ? )
    brktWINNER = 2
    brktELIMINATION = 1
    brktOUT = 0

    def __init__(self, player_name):
        self.PlayerName = player_name
        self.PlayerBracket = None
        self.PlayerRecord = [None]

    def __eq__(self, other):
        return self.PlayerName == other.PlayerName and \
            self.PlayerRecord == other.PlayerRecord and \
            self.PlayerBracket == other.PlayerBracket

    def __ne__(self, other):
        return self.PlayerName == other.PlayerName and \
            self.PlayerRecord == other.PlayerRecord and \
            self.PlayerBracket == other.PlayerBracket

    def tally_result(self, result, opponent, round_number, match_number):
        _result = dict(Result=result, Opponent=opponent, Round=round_number, Match=match_number)

        self.PlayerRecord.append(_result)

        if result == self.resBUY or result == self.resWIN:
            return
        else:
            match self.PlayerBracket:
                case self.brktWINNER:
                    self.PlayerBracket = self.brktELIMINATION
                case self.brktELIMINATION:
                    self.PlayerBracket = self.brktOUT
                case _:
                    raise modules.exceptions.BracketAssignmentError


class PlayerRoster:

    def __init__(self):
        self.Players = []
        self.NumPlayers = 0

    def __eq__(self, other):
        self_names = []
        other_names = []

        for _sp in self.Players:
            self_names.append(_sp.PlayerName)

        for _op in other.Players:
            other_names.append(_op.PlayerName)

        return sorted(self_names) == sorted(other_names)

    def __len__(self):
        return len(self.Players)

    def add_player(self, player: Player):
        for _p in self.Players:
            if _p.PlayerName == player.PlayerName:
                raise modules.exceptions.DuplicatePlayerError

        p = player
        p.PlayerBracket = Player.brktWINNER
        self.Players.append(p)
        self.NumPlayers += 1

    def randomize_player_order(self):
        # We want to be sure the random list is always distinct, so specifically
        # catch the edge case where shuffle() leaves the list unmodified
        _original = copy.deepcopy(self.Players)
        while _original == self.Players:
            random.shuffle(self.Players)
