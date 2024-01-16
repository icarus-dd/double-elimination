import argparse
import modules.exceptions
from modules.rounds import RoundBrackets
from modules.players import PlayerRoster, Player
from modules.tournament import Tournament


def populate_roster(_ui):
    __r = PlayerRoster()

    _ui.emit('')
    _ui.emit('Begin adding players to the roster. Enter a blank name when done.')

    while True:
        __prompt = ' + Player %d\'s name: ' % (len(__r) + 1)

        __newplayer = _ui.query(' + Player %d\'s name: ' % (len(__r) + 1))

        if len(__newplayer):
            try:
                __r.add_player(Player(__newplayer))
            except modules.exceptions.DuplicatePlayerError:
                _ui.emit('Player \'%s\' has already been added to the roster' % __newplayer)
        else:
            if len(__r) > 2:
                if _ui.query('Done adding players?', False, 'YN') == 'Y':
                    break

    _ui.emit('')
    _ui.emit('Tournament Roster:')
    for __i in range(0, len(__r.players)):
        _ui.emit('%3d. %s' % (__i, __r.players[__i].player_name))
    return __r


def run_round_bracket(bracket: RoundBrackets):
    for __match in bracket.matches:
        ui.emit(' -> Match %s:  1: %s vs. 2: %s' %
                (str(__match.match_number).rjust(3), __match.player1.player_name, __match.player2.player_name)
                )
        __winner = None
        __loser = None
        __w = ui.query('    Who won?', False, '12')
        if __w == '1':
            __match.set_match_results(__match.player1, __match.player2)
            __winner = __match.player1
            __loser = __match.player2
        else:
            __match.set_match_results(__match.player2, __match.player1)
            __winner = __match.player2
            __loser = __match.player1

        for __p in __match.player1, __match.player2:
            __status = ''
            if __p.player_bracket == Player.brktWINNER:
                __status = 'advances in the Winner\'s Bracket'
            elif __p.player_bracket == Player.brktELIMINATION:
                __status = 'advances in the Elimination Bracket'
            else:
                __status = 'is eliminated from the tournament. (Better luck next time!)'

            ui.emit('      %s %s' % (__p.player_name, __status))


def run_current_round(tournament: Tournament(), _ui):
    tournament.set_round()

    _ui.emit('')
    _ui.emit('+-------------------------------------------------+')
    _ui.emit('| Beginning Winner\'s bracket, round %s, %s matches |' % (
        str(tournament.current_round_number()).rjust(3),
        str(len(tournament.current_round.winners_bracket.matches)).rjust(2)
    ))
    _ui.emit('+-------------------------------------------------+')
    run_round_bracket(tournament.current_round.winners_bracket)

    _ui.emit('')

    _ui.emit('+----------------------------------------------------+')
    _ui.emit('| Beginning Elimination bracket, round %s, %s matches |' % (
        str(tournament.current_round_number()).rjust(3),
        str(len(tournament.current_round.winners_bracket.matches)).rjust(2)
    ))
    _ui.emit('+----------------------------------------------------+')
    run_round_bracket(tournament.current_round.elimination_bracket)


def main(_ui):
    tournament = Tournament()
    tournament.set_player_roster(populate_roster(_ui))

    while not tournament.is_final_round:
        run_current_round(tournament, _ui)


if __name__ == '__main__':
    argParser = argparse.ArgumentParser()
    argParser.add_argument('--console', action=argparse.BooleanOptionalAction, help='Run in console mode')

    args = argParser.parse_args()
    if args.console:
        from modules.console_ui import UI
    else:
        from modules.ui import UI

    ui = UI()
    main(ui)
