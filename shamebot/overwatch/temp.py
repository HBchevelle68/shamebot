#std && 3rd party
from bs4 import BeautifulSoup as BS
import requests

#internal
from overwatch import consts as owc
from overwatch import errors
#https://playoverwatch.com/en-us/career/pc/HBchevelle68-11717

class Overwatch:

    bnet_name = None
    hero = None
    hero_val = 0

    def __init__(self, acct_full=None, hero=None):
        try:
            if acct_full is None:
                raise errors.EmptyAccountString
            else:
                self.bnet_name = str(acct_full)

            if hero is None:
                self.hero = "ALL HEROES"
            elif hero not in owc.char_options:
                raise errors.InvalidHeroName
            else:
                self.hero = str(hero)
                self.hero_val = owc.char_options[hero]

        except errors.InvalidHeroName:
            print("Hero name invlaid -- Use proper case (ex: Ana, Roadhog, etc)")
            print()
        except errors.EmptyAccountString:
            print("Account string cannot be empty")
            print()
