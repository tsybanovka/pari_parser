import threading
import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from parsing.getting.fabric_parser import Parser
from parsing.processing.Pari import processeVolleyball
from bs4 import BeautifulSoup

class PariVolleyball(Parser):

    timedelta = 15
    step = 10

    load_time_step = 0.1
    load_time_border_max = 5
    load_time_border_min = 1

    url = "https://pari.ru"

    new_res = []

    tabs = ""

    watching_list = []

    que = []
    results = {}

    def get_new_orders_list(self):

        while True and self.is_working:

            html = self.fast_get_html(self.url + "/results/volleyball")

            bs = BeautifulSoup(html, "html.parser")
            ans = []
            error = []

            try:
                for s in bs.find("div", class_="results-list--hIcWo").find("div", class_="virtual-list--FMDYy _vertical--GsTT6").find_all("div", class_="results-event--Me6XJ"):
                    try:
                        a = s.find("a", class_="clear-outline--Cqh52 results-event-team--FDSQS")
                        ans.append([" - ".join(a.text.split("\n\n")[1:]), self.url+a["href"]])
                    except Exception as e:
                        error.append([str(e), s])
            except:
                self.load_time += self.load_time_step
                continue

            break

        if not self.is_working:
            ans = []

        return ans

    def refresh_for_new_orders(self):
        html = self.driver.page_source

        bs = BeautifulSoup(html, "html.parser")
        ans = []
        error = []

        for s in bs.find("div", class_="sport-area--HekVy").find_all("div", class_="sport-base-event-wrap--WmtIb"):
            try:
                a = s.find("div", class_="sport-base-event__main--FHhdx").find("a", class_="table-component-text--Tjj3g sport-event__name--YAs00 _clickable--xICGO _event-view--nrsM2 _compact--MZ0VP")
                ans.append([a.text, self.url+a["href"]])
            except Exception as e:
                error.append([str(e), s])

        return ans


    def send_new_orders(self, lst):

        for name, url in lst:
            if self.is_working:
                html = self.fast_get_html(url)
                html = BeautifulSoup(html, "html.parser")

                score = html.find("div", class_="event-view-header--GcIpo").find("div", class_="event-view-score__summary--D029y _l--InvI4").text

                name = html.find("div", class_="event-view-header--GcIpo").find_all("div", class_="event-view-team__name--aJ2oU")
                name = list(map(lambda x: x.text, name))

                data = html.find("div", class_="result-statistic--kmHFj").find_all("div", class_="results-scoreBlock--aHrej")
                for i, dt in enumerate(data):
                    data[i] = dt.find_all("div")[0].text + ":" + dt.find_all("div")[1].text

                for i in range(len(data), 5):
                    data.append("")

                self.new_res.append([name, score, data])

    def get_new_res(self):
        new_res = self.new_res.copy()
        self.new_res = []
        return new_res