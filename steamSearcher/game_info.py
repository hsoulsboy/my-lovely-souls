import requests
import re
import sys
import os
import csv
from bs4 import BeautifulSoup

def get_discount(csv_file, game_name):
    """Get discount data of a game

    Parameters
    ----------
    csv_file : File
        CSV file containing Steam games Id and Name

    game_name : String
        Name of the game to be searched

    Returns
    -------
    Dict
        Dictionary containing discount information based on the games that were found
    """

    # Check CSV File
    if not os.path.isfile(csv_file) or csv_file[-4:].lower() != ".csv":
        print("A CSV file must be provided")
        sys.exit(0)

    steam_base_url = "https://store.steampowered.com/app/"
    game_data = {}
    game_name = game_name.replace(' ', '_').lower()

    with open(csv_file, 'r') as file:
        csvFile = csv.reader(file)
        
        for game in csvFile:
            if not game_name in game[1]:
                continue

            discount=False
            resp = requests.get(steam_base_url + game[0] + "/" + game[1])

            # Price data
            price_currency = re.search(f'"priceCurrency" content="([a-zA-Z0-9,]+)"', resp.text)
            price = re.search(f'"price" content="([a-zA-Z0-9,]+)"', resp.text)

            if price_currency is None or price is None:
                print("No game was found by the name of: '{}'")
                sys.exit(0)

            # Discount data
            discount_countdown = re.search(f'discount_countdown">([a-zA-Z !áé0-9]+)', resp.text)
            discount_pct = re.search(f'discount_pct">([a-zA-Z \-%!áé0-9]+)', resp.text)
            discount_final_price = re.search(f'discount_final_price">([a-zA-Z \-%$,!áé0-9]+)', resp.text)
            discount_original_price = re.search(f'discount_original_price">([a-zA-Z \-%$,!áé0-9]+)', resp.text)

            if not discount_countdown is None and not discount_pct is None and not discount_original_price is None:
                discount=True
            
            game_data[game[1]] = {
                'price': discount_original_price.group(1) + " " + price_currency.group(1) if discount else price.group(1) + " " + price_currency.group(1),
                'discount': {
                    'discountPrice': discount_final_price.group(1) + " " + price_currency.group(1),
                    'discountPercentage': discount_pct.group(1),
                    'discountCountdown': discount_countdown.group(1)
                } if discount else "No current discount"
            }
    
    return game_data

def get_system_requirements(csv_file, game_name):
    """Get system requirements data of a game

    Parameters
    ----------
    csv_file : File
        CSV file containing Steam games Id and Name

    game_name : String
        Name of the game to be searched

    Returns
    -------
    Dict
        Dictionary containing system requirements information based on the games that were found
    """

    # Check CSV File
    if not os.path.isfile(csv_file) or csv_file[-4:].lower() != ".csv":
        print("A CSV file must be provided")
        sys.exit(0)

    steam_base_url = "https://store.steampowered.com/app/"
    game_data = {}
    game_name = game_name.replace(' ', '_').lower()

    with open(csv_file, 'r') as file:
        csvFile = csv.reader(file)
        
        for game in csvFile:
            if not game_name in game[1]:
                continue

            resp = requests.get(steam_base_url + game[0] + "/" + game[1])

            # Create Soup Html Parser
            soup = BeautifulSoup(resp.text, 'html.parser')

            # Get System Requirements data
            game_area_sys_req = soup.findAll('div', attrs={"class": "game_area_sys_req"})

            system_requirements = {}
            system_requirements['Minimum'] = {}
            for line in str(game_area_sys_req[0]).split('<br/>'):
                if "<li>" in line:
                    sys_req = re.search(r'<li>(<strong>)?([a-zA-Z 0-9íçõ-]+)(:)?(<\/strong>)?([ ãa-zA-Z0-9ç,\(\).\/[í-]+)?', line)
                    
                    if sys_req.group(2) not in system_requirements['Minimum'].keys():
                        req = system_requirements.get('Minimum', {})
                        req[sys_req.group(2)] = "No requirement" if sys_req.group(5) is None else sys_req.group(5).strip()
                        system_requirements['Minimum'] = req
                    else:
                        req = system_requirements.get('Recommended', {})
                        req[sys_req.group(2)] = "No requirement" if sys_req.group(5) is None else sys_req.group(5).strip()
                        system_requirements['Recommended'] = req

            game_data[game[1]] = system_requirements
    
    return game_data