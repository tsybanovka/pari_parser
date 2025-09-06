from parsing import Parsing
from threading import Event, Thread
from excel.everyminutesave import save
import multiprocessing as mp

event = Event()

timedelta_save_hash = 60  #3600
timedelta_save = mp.Value('d', timedelta_save_hash) # в секундах

timedelta_parsing = 60  #1200

step_save_hash = 60
step_save = mp.Value('d', step_save_hash)

step_parsing = 5
load_time = 1
load_time_step = 0.1
load_time_min = 1
load_time_max = 5

chapters = ["timedelta_save", "timedelta_parsing", "step_save", "step_parsing", "load_time", "load_time_step", "load_time_min", "load_time_max"]

def print_intsruction(filepath:str):
    with open("instructions/"+filepath, "r", encoding="utf-8") as file:
        print("".join(file.readlines()))

p = Parsing()
p.timedelta = timedelta_parsing
p.step = step_parsing
p.load_time = load_time
p.load_time_step = load_time_step
p.load_time_min = load_time_min
p.load_time_max = load_time_max
p.start_parse()

Thread(target=save, args=[p, event, timedelta_save, step_save]).start()


print_intsruction("instruciton.txt")

action = input("Введите действие: ").replace(" ", "")

while action != "0":

    if action == "1":

        print_intsruction("1/start")

        choice = input("Введите ответ: ").replace(" ", "")

        while choice != "0":
            value = input("Введите значение: ").replace(" ", "")
            if value.isdigit():
                value = int(value)
                if choice == "1":
                    timedelta_save_hash = value
                elif choice == "2":
                    timedelta_parsing = value
                elif choice == "3":
                    step_save_hash = value
                elif choice == "4":
                    step_parsing = value
                elif choice == "5":
                    load_time = value
                elif choice == "6":
                    load_time_step = value
                elif choice == "7":
                    load_time_min = value
                elif choice == "8":
                    load_time_max = value
                elif choice == "9":
                    p.timedelta = timedelta_parsing
                    p.step = step_parsing
                    p.load_time = load_time
                    p.load_time_step = load_time_step
                    p.load_time_min = load_time_min
                    p.load_time_max = load_time_max

                    p.set_values()

                    timedelta_save.value = timedelta_save_hash
                    step_save.value = step_save_hash

                elif choice == "10" or choice == "0":
                    timedelta_parsing = p.timedelta
                    step_parsing = p.step
                    load_time = p.load_time
                    load_time_step = p.load_time_step
                    load_time_min = p.load_time_min
                    load_time_max = p.load_time_max

                    timedelta_save_hash = timedelta_save.value
                    step_save_hash = step_save.value
                else:
                    print("Неизвестное действие, выберите из списка предложенного выше")

                print_intsruction("1/end_of_operation")
            else:
                print("Введите число")
    elif action == "2":
        print_intsruction("2/start")

        choice = input("Введите интересующий вас раздел: ").replace(" ", "")

        while choice != "0":

            if choice.isdigit():
                choice = int(choice)
                if len(chapters) >= choice >= 1:
                    print(chapters[choice-1])
                    print_intsruction("2/"+chapters[choice-1])
                else:
                    print("Неизвестное действие, выберите из списка предложенного выше")
            else:
                print("Введите число")

            choice = input("Введите интересующий вас раздел: ").replace(" ", "")
    else:
        print("Неизвестная команда, выберите из списка предложенного выше")

    print_intsruction("instruciton.txt")
    action = input("Введите действие: ").strip()

print("Осталось чуть чуть...", f"Примерно {max((p.timedelta, p.step, 1))//60} мин. {max((p.timedelta, p.step, 1))%60} с")
event.set()
p.stop_parse()