import threading
import time, os
from excel.make_excel import *


def save(p, is_working:threading.Event, timedelta, step, filename):

    while not is_working.isSet():
        data = p.get_own_parsing_result("pariVolleyball")
        fl = filename.value.decode("utf-8")
        if os.path.isfile(fl):
            append_data(fl, data)
        else:
            write_data(fl, data)

        i = 0
        while not is_working.isSet() and i < timedelta.value:
            time.sleep(step.value)
            i += step.value
