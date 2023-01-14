# Steam Searcher

Tool designed to search information about games registered on Steam without using an API Key.

## Getting Started

First, clone the repo and access the created directory:
```bash
$ git clone https://github.com/hsoulsboy/steamSearcher
$ cd steamSearcher/
```

Then, install the package using pip
```bash
$ python3 -m pip install .
```

In order to test it, open a Python terminal and import the package:
```bash
$ python3
>>> from steamSearcher import game_db, game_info
```

Create the game database according to your preferences:
```bash
>>> game_db.create('games.csv', filter_preferences=True, filter_language=True)
```

After creating the database, search for any game:
```bash
>>> game_info.get_discount('games.csv', 'plague tale')
{'a_plague_tale_requiem': {'price': '169,90 BRL', 'discount': 'No current discount'}, 'a_plague_tale_innocence': {'price': '129,90 BRL', 'discount': 'No current discount'}}
```
