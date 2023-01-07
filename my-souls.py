import requests
import re

def main():
    steam_base_url = "https://store.steampowered.com/app/"
    my_souls = [
        ("570940", "DARK_SOULS_REMASTERED"), 
        ("335300", "DARK_SOULS_II_Scholar_of_the_First_Sin"), 
        ("442010", "DARK_SOULS_III__Season_Pass")
    ]
    my_souls_data = {}

    for my_soul in my_souls:
        discount=False
        resp = requests.get(steam_base_url + my_soul[0] + "/" + my_soul[1])

        # Price data
        price_currency = re.search(f'"priceCurrency" content="([a-zA-Z0-9,]+)"', resp.text)
        price = re.search(f'"price" content="([a-zA-Z0-9,]+)"', resp.text)

        # Discount data
        discount_countdown = re.search(f'discount_countdown">([a-zA-Z !áé0-9]+)', resp.text)
        discount_pct = re.search(f'discount_pct">([a-zA-Z \-%!áé0-9]+)', resp.text)
        discount_final_price = re.search(f'discount_final_price">([a-zA-Z \-%$,!áé0-9]+)', resp.text)
        discount_original_price = re.search(f'discount_original_price">([a-zA-Z \-%$,!áé0-9]+)', resp.text)

        if not discount_countdown is None or not discount_pct is None or not discount_final_price is None or not discount_original_price is None:
            discount=True

        my_souls_data[my_soul[1]] = {
            'price': discount_original_price.group(1) if discount else price.group(1) + " " + price_currency.group(1),
            'discount': {
                'discountPrice': discount_final_price.group(1) + " " + price_currency.group(1),
                'discountPercentage': discount_pct.group(1),
                'discountCountdown': discount_countdown.group(1)
            } if discount else "No current discount"
        }
    
    print(my_souls_data)

if __name__ == "__main__":
    main()