import threading
import time


def save(p, is_working:threading.Event, timedelta, step):

    with open("res.txt", "a") as file:
        file.write("[\n")

    while not is_working.isSet():
        with open("res.txt", "a") as file:
            data = p.get_own_parsing_result("pariVolleyball")
            for dt in data:
                file.write(str(dt) + ", \n")

        i = 0
        while not is_working.isSet() and i < timedelta.value:
            time.sleep(step.value)
            i += step.value

    with open("res.txt", "a") as file:
        file.write("]")