import classes as m
import json
from os.path import exists

game_mode = "Max_letters"


def guidelines():
    """
    >Κλάσεις: Player, Human, Computer, Game, SakClass

    >Η Human και η Computer κληρονομούν την κλάση Player

    >Οι μέθοδοι Human και Computer μέσω του constructor τους καλούν την init
    της μητρικής τους κλάσης Player

    >Στο αρχείο classes.py, έγινε χρήση @staticmethod Decorator στις μεθόδους word_val,
    word_in_dict, word_size και word_val2

    >Οι λέξεις της γλώσσας στην αρχή του παιχνιδιού φορτώνονται σε ενα λεξικό
    το οποίο χρησιμοποιείται για όποια αναζήτηση γίνεται στη συνέχεια

    >Για τον ηλ. Υπολογιστή υλοποιήθηκαν οι: min_letters, max_letters, smart.
    Ως default είναι ορισμένη η max_letters.
    """
    return


def menu():
    print("[1] Score")
    print("[2] Settings")
    print("[3] Game")
    print("[q] Quit")


def settings():
    print("Settings")
    print("[1] Min_letters")
    print("[2] Max_letters")
    print("[3] Smart")


def initialize_score_file():
    if exists('score_file.json'):
        data = {"games": []}
        with open("score_file.json", "r+") as file:
            one_char = file.read(1)
            if len(one_char) > 0:
                return
            else:
                json.dump(data, file)
    else:
        data = {"games": []}
        with open("score_file.json", "a") as file:
            json.dump(data, file)


def option1():
    try:
        with open("score_file.json", "r") as read_file:
            data = json.load(read_file)
            cnt = 0
            for i in data["games"]:
                cnt += 1
                rounds = i["rounds"]
                name = i["name"]
                score_h = i["score_h"]
                score_c = i["score_c"]
                print("--------------------------------------------")
                print("Game", cnt)
                print("Played by: ", name)
                print("Final score in ", rounds, "rounds:")
                print(name, ": ", score_h, " vs computer: ", score_c)
                print("--------------------------------------------")
            if cnt == 0:
                print("There isn't any history of games!")
    except:
        print("There isn't any history of games!")


def option2():
    settings()
    global game_mode
    print("Current mode is: ", game_mode)
    a = input()
    while a != "1" and a != "2" and a != "3":
        print("Select a valid game mode")
        a = input()
    if a == "1":
        game_mode = "Min_letters"
    elif a == "2":
        game_mode = "Max_letters"
    elif a == "3":
        game_mode = "Smart"
    print("Mode set to: ", game_mode)


def option3():
    new_game = m.Game(game_mode)


print("""
========================================
              Welcome to
.---..---..---..---..---..---..---..---.
| S || C || R || A || B || B || L || E |
'---''---''---''---''---''---''---''---'
========================================
"""
      )

menu()
initialize_score_file()
option = input("Enter your option: ")
while option != "q":
    if option == "1":
        option1()
    if option == "2":
        option2()
    if option == "3":
        option3()
    menu()
    option = input("Enter your option: ")

print("""
========================================
           Thanks For Playing
.---..---..---..---..---..---..---..---.
| _ || _ || B || Y || E || ! || _ || _ |
'---''---''---''---''---''---''---''---'
========================================
"""
      )
