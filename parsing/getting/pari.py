import threading
import time

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

    def start_checking_until_work(self):
        threading.Thread(target=self.make_que).start()
        super().start_checking_until_work()

    def get_new_orders_list(self):

        while True and self.is_working:

            html = self.fast_get_html(self.url + "/sports/volleyball")

            bs = BeautifulSoup(html, "html.parser")
            ans = []
            error = []

            try:
                for s in bs.find("div", class_="sport-area--HekVy").find_all("div", class_="sport-base-event-wrap--WmtIb"):
                    try:
                        a = s.find("div", class_="sport-base-event__main--FHhdx").find("a", class_="table-component-text--Tjj3g sport-event__name--YAs00 _clickable--xICGO _event-view--nrsM2 _compact--MZ0VP")
                        ans.append([a.text, self.url+a["href"]])
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


    def send_new_orders(self, list):

        was_null_names = False

        for name, url in list:
            if name == "":
                was_null_names = True
                if self.load_time < self.load_time_border_max:
                    self.load_time += self.load_time_step
                continue
            self.orders_list.append([name, url])
            threading.Thread(target=self.watch_the_offer, args=[name, url]).start()

        if not was_null_names and self.load_time_border_min > self.load_time:
            self.load_time -= self.load_time_step
        else:
            new_orders_list = self.get_new_orders_list()

            if new_orders_list != self.orders_list:
                new_orders = [order for order in new_orders_list if order not in self.orders_list]
                self.send_new_orders(new_orders)

        #processeVolleyball(self, list)

    def _check_the_offer(self, name:str, html:str):

        def get_data(html:str):
            html = BeautifulSoup(html, "html.parser").find("div", class_="header__fill--X3wSZ").find("div",
                                                                                                     class_="event-view__header__scoreboard-container--MlRoW")
            html = html.find_all("div")[1].find("div", class_="scoreboard__table--Tx2YX")
            score = None
            data = None
            if html:
                score = html.find("div", class_="column--fgNW_ _active--jPFnC _bold--Aw_dH")

                status = html.find("div", class_="text-label--jz1xn")

                if status:
                    if score and status.text.lower() == "итог":
                        dt = html.find_all("div", class_="column--fgNW_ _separator--jZ9hO")
                        data = []
                        for d in dt:
                            data.append([d.find("div", class_="column__t1--WCEcc").text, d.find("div", class_="column__t2--rn4_E").text])


            return data, score

        data, score = get_data(html)

        if self.is_working and data:
            self.new_res.append([name, data, score])
            return True
        return False

    def watch_the_offer(self, name, url):

        if not self.driver:
            with open("error.txt", "w") as file:
                file.write("The driver is not activated")
            raise "The driver is not activated"

        self.results[url] = None
        self.que.append([url, [url], "create new tab"])
        while self.results[url] == None:
            time.sleep(1)
        tab_name = self.results[url]

        print(name, url)

        self.results[tab_name] = None
        self.que.append([tab_name, [], "get html"])
        while self.results[tab_name] == None:
            time.sleep(1)

        while not self._check_the_offer(name, self.results[tab_name]) and self.is_working:
            time.sleep(self.step)
            self.results[tab_name] = None
            self.que.append([tab_name, [], "get html"])
            while self.results[tab_name] == None:
                time.sleep(1)

        self.que.append(tab_name, [], "close")



    def get_new_res(self):
        new_res = self.new_res.copy()
        self.new_res = []
        return new_res


    def make_que(self): # get html, refresh, create new tab, close
        while self.is_working or self.que != []:
            if self.que != []:
                tab_name, arguments, action = self.que.pop()
                if action == "get html":
                    self.driver.switch_to.window(tab_name)
                    self.results[tab_name] = self.driver.page_source
                elif action == "refresh":
                    self.driver.switch_to.window(tab_name)
                    self.driver.refresh()
                    self.results[tab_name] = True
                elif action == "create new tab":
                    self.driver.execute_script("window.open('about:blank', '_blank');")
                    self.fast_get_html(url=arguments[0], tab_name=self.driver.window_handles[-1])
                    self.results[tab_name] = self.driver.window_handles[-1]
                elif action == "close":
                    self.driver.switch_to.window(tab_name)
                    print("The url:", self.driver.current_url, "closed")
                    self.driver.close()

            else:
                time.sleep(0.01)