#std && 3rd party
from bs4 import BeautifulSoup as BS
import requests
import re

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
                raise errors.EmptyAccountStringError
            else:
                self.bnet_name = str(acct_full)

            if hero is None:
                self.hero = "ALL HEROES"
            elif hero not in owc.char_options:
                raise errors.InvalidHeroNameError
            else:
                self.hero = str(hero)
                self.hero_val = owc.char_options[hero]

        except errors.InvalidHeroNameError:
            raise errors.InvalidHeroNameError("Hero name invlaid -- Use proper case (ex: Ana, Roadhog, etc)")

        except errors.EmptyAccountStringError:
            raise errors.EmptyAccountStringError("Empty Account String\n")

        acc_url = owc.BASE_URL + self.bnet_name
        req = requests.get(acc_url)

        # Invert the consts dict so we can map ID to hero name
        id2hero = owc.char_options
        hero2id = {v: k for (k, v) in id2hero.items()}

        # Create the soup and parse
        soup = BS(req.content, "html.parser")

        # We have stats for both comp and quickplay
        self.stats = dict()
        for gt in ["quickplay", "competitive"]:
            self.stats[gt] = dict()

            # All the stats in the bar chart are contained in the full stats, so we ignore it
            _, gt_stats = soup.find("div", id="quickplay").find_all("section", "u-max-width-container career-section")

            # Each of the following tags contains the data we want for individual or all heroes
            data_tags = gt_stats.find_all(attrs={"class": re.compile("js-stats")})
            for tag in data_tags:
                hero_id = str(tag.attrs["data-category-id"])
                hero_name = hero2id[hero_id]
                hero_stats = self._parse_stat_tag(tag)
                self.stats[gt][hero_name] = hero_stats


    @staticmethod
    def _parse_stat_tag(tag):
        """@TODO  Document. Parsing is also somewhat fragile at the moment
        """
        stats = dict()
        for child in tag.children:
            category_name = str(child.find(attrs={"class": "stat-title"}).string)
            stats[category_name] = dict()
            
            for row in child.find_all(attrs={"class": "DataTable-tableRow"}):
                row_title = str(row.contents[0].string)
                if "time" in row_title.lower() and not "inspire uptime" in row_title.lower():
                    # Time is listed in HR:MIN:SEC format OR MIN:SEC format,
                    # this should handle both cases
                    # For now we will convert all durations to hours
                    time_consts = [1/(60**2), 1/60, 1] # Conversion factors from S:M:H -> H
                    tokens = str(row.contents[1].string).strip().split(":")
                    row_val = sum([float(t)*c for (t, c) in zip(tokens[::-1], time_consts)])
                else:
                    r_str = str(row.contents[1].string)
                    if "%" in r_str:
                        r_str = r_str.strip().strip("%")
                    row_val = float(r_str)
                stats[category_name][row_title] = row_val
        return stats

