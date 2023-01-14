import requests
import re

def main():
    base_url = "https://store.steampowered.com/search?ignore_preferences=1&ndl=1&page={}"

    steam_links = {}
    page = 1

    while page <= 5464:
        resp = requests.get(base_url.format(page))
        steam_links[page] = []
        for line in resp.text.split(">"):
            if "https://store.steampowered.com/app/" in line:
                resp_game = re.search(f'https:\/\/store.steampowered.com\/app\/([0-9]+)\/([a-zA-Z_0-9]+)', line)
                game_link = (resp_game.group(1), resp_game.group(2).lower())

                game_links = steam_links.get(page, [])
                game_links.append(game_link)
                steam_links[page] = game_links

                with open('games.csv', 'a') as file:
                    file.write(f'{game_link[0]},{game_link[1]}\n')
        page += 1

    print(steam_links)

if __name__ == "__main__":
    main()