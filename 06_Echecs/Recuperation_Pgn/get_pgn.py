# Copyright © 2025 Charles Theetten
# Tous droits réservés.
# Ce programme est distribué sous licence CC BY-NC-ND 4.0.

################################################################################

# pylint: disable=C0301

################################################################################

""" get_pgn """

################################################################################

import  argparse
import  re
import  numpy       as np
import  pandas      as pd
import  requests

################################################################################

ENDPOINT_STATS  = "https://api.chess.com/pub/player/{}/stats"
ENDPOINT_GAMES  = "https://api.chess.com/pub/player/{}/games/archives"

HEADERS         = { "User-Agent" : "User_Agent_1.0" }

################################################################################

def get_player_stats(player):
    """ get_player_stats """
    data = requests.get(ENDPOINT_STATS.format(player), headers = HEADERS, timeout = 10)

    return data.json()

################################################################################

def build_df_stats(player):
    """ build_df_stats function"""
    records         = {}
    data            = []
    stats           = get_player_stats(player)

    blitz           = stats["chess_blitz"]
    nb_games        = blitz["record"]["win"] + blitz["record"]["loss"] + blitz["record"]["draw"]
    records["win"]  = np.round(blitz["record"]["win"] / nb_games, 2)
    records["loss"] = np.round(blitz["record"]["loss"] / nb_games, 2)
    records["draw"] = np.round(blitz["record"]["draw"] / nb_games, 2)

    data.append(records)

    return pd.DataFrame(data)

################################################################################

def get_player_games_archives(player):
    """ get_player_archives """
    data = requests.get(ENDPOINT_GAMES.format(player), headers = HEADERS, timeout = 10)

    return data.json()

################################################################################

def extract_field(pgn, field):
    """ extract_field function """
    start   = pgn.find(field)
    end     = pgn.find("]", start)

    fields  = re.findall(r'"(.*)"', pgn[start:end])

    return fields[0] if len(fields) > 0 else np.nan

################################################################################

def extract_moves(pgn, field):
    """ extract_moves function """
    start   = pgn.find(field)
    end     = pgn.find("\n", start)

    moves   = pgn[start:end]
    moves   = re.sub(r"{.*?}", "", moves)
    moves   = re.sub(r" [\d]{1,3}\.{3} ", "", moves)

    return moves

################################################################################

def build_df_games(player):
    """ build_df_games function"""
    data        = []
    archives    = get_player_games_archives(player)

    for link in archives["archives"]:
        games = requests.get(link, headers = HEADERS, timeout = 10).json()
        for game in games["games"]:
            pgn                 = game["pgn"]
            infos               = {}
            infos["Date"]       = extract_field(pgn, "Date")
            infos["White"]      = extract_field(pgn, "White")
            infos["Black"]      = extract_field(pgn, "Black")
            infos["Result"]     = extract_field(pgn, "Result")
            infos["WhiteElo"]   = extract_field(pgn, "WhiteElo")
            infos["BlackElo"]   = extract_field(pgn, "BlackElo")
            infos["ECO"]        = extract_field(pgn, "ECO")
            infos["Moves"]      = extract_moves(pgn, "1. ")

            data.append(infos)

    return pd.DataFrame(data)

################################################################################

def check_games(value):
    """ check_games function """
    games = int(value)

    if games not in [0, 1]:
        raise argparse.ArgumentTypeError(f"GAMES must be 0 or 1, got {games}.")

    return games

def check_args():
    """ check_args function """
    parser = argparse.ArgumentParser()

    parser.add_argument("USERNAME", help = "PLAYER'S USERNAME", type = str)
    parser.add_argument("GAMES", help = "PLAYER'S GAMES", type = check_games)
    parser.parse_args()

    return parser.parse_args()

################################################################################

def main():
    """ main function """
    args        = check_args()

    player      = args.USERNAME
    games       = args.GAMES

    df_stats    = build_df_stats(player)

    print(df_stats.head())
    print("-" * 80)

    if games == 1:
        df_games = build_df_games(player)

        print(df_games.head())
        print("-" * 80)

        df_games.to_csv(f"{player}_games.csv")

################################################################################

if __name__ == "__main__":
    main()

################################################################################
