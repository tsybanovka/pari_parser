import threading
import time, requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import pyautogui
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By



class Parser:      # Класс, использующий паттерн фабрика

    orders_list = [] # список предложений

    timedelta = 60     # время ожидания
    is_working = True  # работает ли парсер

    load_time = 3

    screen_width, screen_height = pyautogui.size()

    driver = None

    def start_checking_until_work(self): # работать пока is_working = True
        def work():

            while self.is_working: # цикл
                self.check_new_orders()
                t = 0
                while t != self.timedelta and self.is_working:    #
                    time.sleep(1)                                 #  эта часть отвечает за своевременное выключение
                    t += 1                                        #
                self.check_watching_orders()
            self.driver.close()
        threading.Thread(target=work).start() # создаем поток со стабильным парсингом

    def check_watching_orders(self):
        pass

    def check_new_orders(self): # функция для поиска новых предложений
        new_orders_list = self.get_new_orders_list()

        if new_orders_list != self.orders_list:
            new_orders = [order for order in new_orders_list if order not in self.orders_list]
            self.send_new_orders(new_orders)

    def get_new_orders_list(self): # кастомная функция для обновления списка новых предложений (возвращает)
        pass
    def send_new_orders(self, new_orders:list): # кастомная функция взаимодействия с новыми предложениями
        pass

    def fast_get_html(self, url:str, tab_name=""):  # функция быстрого получения html кода
        chrome_options = Options()
        chrome_options.add_argument('--window-size=1920x1080')  # Размер окна влияет на рендеринг страниц
        chrome_options.add_argument("--window-position=-9999,-9999")

        if not self.driver:
            driver = webdriver.Chrome(options=chrome_options)
            try:
                driver.get(url)

                was = driver.page_source
                time.sleep(self.load_time)
                while was != driver.page_source:
                    was = driver.page_source
                    time.sleep(self.load_time)
                self.driver = driver
                # Получаем исходный HTML-код страницы
                return driver.page_source
            except Exception as e:
                print(f"Ошибка при получении HTML: {e}")
                return None
        else:
            try:
                if self.driver.current_url == url:
                    self.driver.refresh()
                else:
                    if tab_name != "":
                        self.driver.switch_to.window(tab_name)
                    else:
                        self.driver.switch_to.window(self.driver.window_handles[0])
                    self.driver.get(url)

                if url != "https://pari.ru/results/volleyball":
                    WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "event-view--z1_OP")))
                else:
                    was = self.driver.page_source
                    time.sleep(self.load_time)
                    while was != self.driver.page_source:
                        was = self.driver.page_source
                        time.sleep(self.load_time)
                    self.driver = self.driver
                # Получаем исходный HTML-код страницы
                return self.driver.page_source
            except Exception as e:
                print(f"Ошибка при получении HTML: {e}")
                return None

