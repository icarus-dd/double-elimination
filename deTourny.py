import argparse
import modules.exceptions
from modules.players import PlayerRoster, Player
from modules.tournament import Tournament


def populate_roster(ui):
    __r = PlayerRoster()

    ui.emit("")
    ui.emit("Begin adding players to the roster. Enter a blank name when done.")

    while True:
        __prompt = " + Player %d's name: " % (len(__r) + 1)

        __newplayer = ui.query(" + Player %d's name: " % (len(__r) + 1))

        if len(__newplayer):
            try:
                __r.add_player(Player(__newplayer))
            except modules.exceptions.DuplicatePlayerError:
                ui.emit("Player '%s' has already been added to the roster" % __newplayer)
        else:
            if len(__r) > 2:
                if ui.query("Done adding players?", False, "YN") == 'Y':
                    break

    ui.emit("")
    ui.emit("Tournament Roster:")
    for __i in range(0, len(__r.Players)):
        ui.emit("%3d. %s" % (__i, __r.Players[__i].PlayerName))
    return __r


def run_current_round(tournament: Tournament(), ui):
    ui.emit("")
    ui.emit("+----------------------+")
    ui.emit("| Beginning round %s |" % (str(len(tournament.rounds))).ljust(4))
    ui.emit("+----------------------+")

    ui.emit("")


def main(ui):
    tournament = Tournament()
    tournament.set_player_roster(populate_roster(ui))
    tournament.set_round()

    while not tournament.is_final_round:
        run_current_round(tournament, ui)


if __name__ == "__main__":
    argParser = argparse.ArgumentParser()
    argParser.add_argument("--console", action=argparse.BooleanOptionalAction, help="Run in console mode")

    args = argParser.parse_args()
    if args.console:
        from modules.console_ui import UI
    else:
        from modules.ui import UI

    ui = UI()
    main(ui)
