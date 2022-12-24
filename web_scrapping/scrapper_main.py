from bs4 import BeautifulSoup
from datetime import datetime
from pathlib import Path
import requests, subprocess, json

class webObjScrapper:

    def __init__(self,link):
        self.link = link
    
    def setup(self):
        self.generate_soup()
        self.format_matches()

    def generate_soup(self):
        raw_html = requests.get(self.link)
        self.soup = BeautifulSoup(raw_html.text, "html.parser")

    def format_matches(self):
        finished_match_data = []
        for html_tag in self.soup.select("h3.section-header__subtitle"):
            for parent_html_tag in html_tag.parents:
                if parent_html_tag.name == "of-match-cards-list":
                    teamA = [tag.string.strip() for tag in parent_html_tag.select(".simple-match-cards-list__match-card .simple-match-card-team__name")[::2]]
                    teamB = [tag.string.strip() for tag in parent_html_tag.select(".simple-match-cards-list__match-card .simple-match-card-team__name")[1::2]]
                    scoresA = [tag.string.strip() for tag in parent_html_tag.select(".simple-match-cards-list__match-card .simple-match-card-team__score")[::2]]
                    scoresB = [tag.string.strip() for tag in parent_html_tag.select(".simple-match-cards-list__match-card .simple-match-card-team__score")[1::2]]
                    match_time = [tag["datetime"] for tag in parent_html_tag.select(".simple-match-card__match-content time[datetime]:first-child")]
                    formatted_list = list(zip(zip(teamA,teamB),zip(scoresA,scoresB),match_time,[html_tag.string]*len(match_time)))
                    finished_match_data += formatted_list

        formatted_obj_list = ([{
                                "Home":{
                                    "name":nameA,
                                    "score":scoreA
                                },
                                "Away":{
                                    "name":nameB,
                                    "score":scoreB
                                },
                                "match_time":datetime.strptime(match_time,"%Y-%m-%dT%H:%M:%SZ").strftime("%Y-%m-%d %H:%M:%S UTC"),
                                "group_name": group_name
                                } for (nameA, nameB),(scoreA,scoreB),match_time,group_name in finished_match_data])
        self.result_formatted = formatted_obj_list

if "__main__" == __name__:

    # checks whether the HTML has already been generated 
    if not any([dir_file.name.lower() == "wcresults.html" for dir_file in Path(__file__).parent.iterdir()]):
        # if not, run selenium
        subprocess.run(["python",Path("web_scrapping","get_all_webpage.py")])

    with open(Path(Path(__file__).parent,"WCresults.html"),"r",encoding="utf-8") as f:
            scrapper2 = webObjScrapper("https://onefootball.com/en/competition/fifa-world-cup-12/fixtures")
            scrapper2.soup = BeautifulSoup(f.read(), "html.parser")
            scrapper2.format_matches()
            
            scrapper = webObjScrapper("https://onefootball.com/en/competition/fifa-world-cup-12/results")
            scrapper.setup()
            
            with open(Path(Path(__file__).parent,"WCresults.json"),"w") as f:
                test_list = scrapper.result_formatted + scrapper2.result_formatted
                res_list = [i for n, i in enumerate(test_list) if i not in test_list[n + 1:]]
                json.dump(res_list,fp=f)