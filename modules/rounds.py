from modules.players import PlayerRoster, Player


class Match:

    last_match_number = 0

    def __init__(self):
        self.RoundNumber = 0
        self.MatchNumber = 0
        self.player1 = self.player2 = None
        self.Winner = None
        self.Loser = None
        self.MatchDecided = False

    def set_match_players(self, round_number: int, player1: Player, player2: Player):
        self.player1 = player1
        self.player2 = player2
        Match.last_match_number += 1
        self.MatchNumber = Match.last_match_number
        self.RoundNumber = round_number

    def set_match_results(self, winner: Player, loser: Player):
        self.Winner = winner
        self.Loser = loser
        winner.tally_result(Player.resWIN, loser, self.RoundNumber, self.MatchNumber)
        loser.tally_result(Player.resLOSS, loser, self.RoundNumber, self.MatchNumber)
        self.MatchDecided = True

class RoundBrackets:

    def __init__(self, RoundNumber: int):
        self.BracketRoster: PlayerRoster = PlayerRoster()
        self.ActivePlayers: list[Player] = []
        self.Buys: list[Player] = []
        self.Matches: list[Match] = []
        self.ActiveRoundNumber: int = RoundNumber

    def set_round_roster(self, roster: PlayerRoster):
        self.BracketRoster = roster
        self.ActivePlayers = PlayerRoster()
        self.Buys = PlayerRoster()
        self.Matches = []

    def set_buys_and_matches(self):
        # Set the buys so that removing them makes the active player count
        # a power of 2. That way all buys end up in the first round up until
        # the final round.
        # if len(self.BracketRoster.Players) < 2:
        #     raise exceptions.BracketPlayerCount

        self.ActivePlayers = []
        self.Buys = []
        self.Matches = []

        # Determine number of active players
        __n = 2

        # Perfect round
        if not len(self.BracketRoster.Players) % 2:
            __n = len(self.BracketRoster.Players)
        else:
            while __n < len(self.BracketRoster.Players):
                __n = __n * 2

        ___num_buys = __n - len(self.BracketRoster.Players)
        ___num_active = len(self.BracketRoster.Players) - ___num_buys

        self.ActivePlayers = self.BracketRoster.Players[:___num_active:]
        self.Buys = self.BracketRoster.Players[___num_active::]

        __pool = []
        for __p in self.ActivePlayers:
            __pool.append(__p)

        while len(__pool):
            __p1 = __pool.pop(0)
            __p2 = __pool.pop(0)
            __m = Match()
            __m.set_match_players(self.ActiveRoundNumber, __p1, __p2)
            self.Matches.append(__m)

        return self.ActivePlayers, self.Buys, self.Matches


class Round:

    last_round_number = 0

    def __init__(self):
        self.winners_bracket = RoundBrackets(Round.last_round_number)
        self.elimination_bracket = RoundBrackets(Round.last_round_number)
        Round.last_round_number += 1

    def set_bracket_rosters(self, winners: PlayerRoster, elimination: PlayerRoster):
        self.winners_bracket = RoundBrackets()
        self.winners_bracket.set_round_roster(winners)
        self.elimination_bracket = RoundBrackets()
        self.elimination_bracket.set_round_roster(elimination)
