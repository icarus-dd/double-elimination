from modules.players import PlayerRoster, Player


class Match:

    last_match_number = 0

    def __init__(self):
        self.round_number: int = 0
        self.match_number: int = 0
        self.player1: Player | None = None
        self.player2: Player | None = None
        self.winner: Player | None = None
        self.loser: Player | None = None
        self.match_decided: bool = False

    def set_match_players(self, round_number: int, player1: Player, player2: Player):
        self.player1 = player1
        self.player2 = player2
        Match.last_match_number += 1
        self.match_number = Match.last_match_number
        self.round_number = round_number

    def set_match_results(self, winner: Player, loser: Player):
        self.winner = winner
        self.loser = loser
        winner.tally_result(Player.resWIN, loser, self.round_number, self.match_number)
        loser.tally_result(Player.resLOSS, loser, self.round_number, self.match_number)
        self.match_decided = True


class RoundBrackets:

    def __init__(self, round_number: int):
        self.bracket_roster: PlayerRoster = PlayerRoster()
        self.active_players: list[Player] = []
        self.buys: list[Player] = []
        self.matches: list[Match] = []
        self.active_round_number: int = round_number

    def set_round_roster(self, roster: PlayerRoster):
        self.bracket_roster = roster
        self.active_players = PlayerRoster()
        self.buys = PlayerRoster()
        self.matches = []

    def set_buys_and_matches(self):
        # Set the buys so that removing them makes the active player count
        # a power of 2. That way all buys end up in the first round up until
        # the final round.
        # if len(self.BracketRoster.Players) < 2:
        #     raise exceptions.BracketPlayerCount

        self.active_players = []
        self.buys = []
        self.matches = []

        # Determine number of active players
        __n = 2

        # Perfect round
        if not len(self.bracket_roster.players) % 2:
            __n = len(self.bracket_roster.players)
        else:
            while __n < len(self.bracket_roster.players):
                __n = __n * 2

        ___num_buys = __n - len(self.bracket_roster.players)
        ___num_active = len(self.bracket_roster.players) - ___num_buys

        self.active_players = self.bracket_roster.players[:___num_active:]
        self.buys = self.bracket_roster.players[___num_active::]

        __pool = []
        for __p in self.active_players:
            __pool.append(__p)

        while len(__pool):
            __p1 = __pool.pop(0)
            __p2 = __pool.pop(0)
            __m = Match()
            __m.set_match_players(self.active_round_number, __p1, __p2)
            self.matches.append(__m)

        return self.active_players, self.buys, self.matches


class Round:

    round_number = 1

    def __init__(self):
        self.winners_bracket = RoundBrackets(Round.round_number)
        self.elimination_bracket = RoundBrackets(Round.round_number)
        Round.round_number += 1

    def set_bracket_rosters(self, winners: PlayerRoster, elimination: PlayerRoster):
        self.winners_bracket = RoundBrackets(Round.round_number)
        self.winners_bracket.set_round_roster(winners)
        self.elimination_bracket = RoundBrackets(Round.round_number)
        self.elimination_bracket.set_round_roster(elimination)
