import requests
import re
import os
import sys

def create(output_file, filter_preferences=False, filter_language=False):
    """Create a CSV file containing a list of games Ids and Names

    Parameters
    ----------
    output_file : String
        CSV file output path

    filter_preferences : bool, optional (default is False)
        Flag to filter Steam results based on the user's preferences

    filter_language : bool, optional (default is False)
        Flag to filter Steam results based on the user's language

    Returns
    -------
    Dict
        Dictionary containing information of all games based on the pagination
    """

    if os.path.isfile(output_file) or os.path.isdir(output_file):
        print("Output must be a non used path.")
        sys.exit(0)

    preferences, language = (1, 1)
    if filter_preferences is True:
        preferences = 0
    if filter_language is True:
        language = 0

    base_url = "https://store.steampowered.com/search?ignore_preferences={}&ndl={}&page={}"

    page = 1
    page_count = 0
    resp = requests.get(base_url.format(preferences, language, page))
    for line in resp.text.split(">"):
        if "SearchLinkClick" in line:
            resp_game = re.search(f'page=([0-9]+)', line)
            if int(resp_game.group(1)) > 3:
                        page_count = resp_game.group(1)

    print(page_count)

    steam_links = {}
    while page <= int(page_count):
        resp = requests.get(base_url.format(preferences, language, page))
        steam_links[page] = []
        for line in resp.text.split(">"):
            if "https://store.steampowered.com/app/" in line:
                resp_game = re.search(f'https:\/\/store.steampowered.com\/app\/([0-9]+)\/([a-zA-Z_0-9]+)', line)
                game_link = (resp_game.group(1), resp_game.group(2).lower())

                game_links = steam_links.get(page, [])
                game_links.append(game_link)
                steam_links[page] = game_links

                with open(output_file, 'a') as file:
                    file.write(f'{game_link[0]},{game_link[1]}\n')
        page += 1

    return steam_links
