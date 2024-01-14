import copy
from modules.exceptions import BracketPlayerCount
from modules.players import PlayerRoster
from modules.rounds import Round


class Tournament:

    def __init__(self):
        self.full_roster = PlayerRoster()
        self.winner_roster = PlayerRoster()
        self.elimination_roster = PlayerRoster()
        self.is_final_round = False
        self.rounds = []

    def set_player_roster(self, roster: PlayerRoster) -> PlayerRoster:
        self.full_roster = roster
        self.full_roster.randomize_player_order()
        self.winner_roster = copy.deepcopy(self.full_roster)

        return self.full_roster

    def current_round_number(self):
        return len(self.rounds)

    def set_round(self):
        if (len(self.winner_roster) == 2 and len(self.elimination_roster) == 0) or \
                (len(self.winner_roster) == 1 and len(self.elimination_roster) == 1):
            self.is_final_round = True
            return
        else:
            self.is_final_round = False

        __r = Round()
        __r.winners_bracket.set_round_roster(self.winner_roster)
        __r.winners_bracket.set_buys_and_matches()
        __r.elimination_bracket.set_round_roster(self.elimination_roster)
        __r.elimination_bracket.set_buys_and_matches()

        
