from parsing.getting.pari import PariVolleyball
import threading, time

class Parsing():

    timedelta = 60
    step = 10

    parse = ["pariVolleyball"]

    def __init__(self):
        self.pariVolleyball = PariVolleyball()

    def start_parse(self):
        for p in self.parse:
            setattr(eval(f"self.{p}"), "timedelta", self.timedelta)
            setattr(eval(f"self.{p}"), "step", self.step)
            eval(f"self.{p}.start_checking_until_work()")

    def get_parsing_result(self):
        for p in self.parse:
            yield eval(f"self.{p}.get_new_res()")

    def get_own_parsing_result(self, what:str):
        if what in self.parse:
            return eval(f"self.{what}.get_new_res()")
        else:
            return None

    def stop_parse(self):
        ln = len(self.parse)
        for i, p in enumerate(self.parse):
            eval(f"self.{p}").is_working = False
            print(f"{i}/{ln}")

    def set_values(self):
        for p in self.parse:
            setattr(eval(f"self.{p}"), "timedelta", self.timedelta)
            setattr(eval(f"self.{p}"), "step", self.step)
            setattr(eval(f"self.{p}"), "load_time", self.load_time)
            setattr(eval(f"self.{p}"), "load_time_step", self.load_time_step)
            setattr(eval(f"self.{p}"), "load_time_min", self.load_time_min)
            setattr(eval(f"self.{p}"), "load_time_max", self.load_time_max)