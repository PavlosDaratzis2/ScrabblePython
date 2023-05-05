import json
import random
from itertools import permutations

lets = {'Α': [12, 1], 'Β': [1, 8], 'Γ': [2, 4], 'Δ': [2, 4], 'Ε': [8, 1], 'Ζ': [1, 10], 'Η': [7, 1],
        'Θ': [1, 10], 'Ι': [8, 1], 'Κ': [4, 2], 'Λ': [3, 3], 'Μ': [3, 3], 'Ν': [6, 1], 'Ξ': [1, 10],
        'Ο': [9, 1], 'Π': [4, 2], 'Ρ': [5, 2], 'Σ': [7, 1], 'Τ': [8, 1], 'Υ': [4, 1], 'Φ': [1, 8],
        'Χ': [1, 8], 'Ψ': [1, 10], 'Ω': [3, 4]
        }
greek7 = {}


class Player:
    def __init__(self, name):
        self.name = name
        self.score = 0
        self.playerLetters = []

    @staticmethod
    def word_in_dict(word):
        global greek7
        if word in greek7:
            return True
        return False

    def check_word(self, word):
        temp_list = self.playerLetters.copy()
        wrong_letters = []
        flag1 = True
        flag2 = False
        for i in word:
            if i in temp_list:
                temp_list.remove(i)
            else:
                wrong_letters += i
                flag1 = False

        flag2 = self.word_in_dict(word)

        if not flag1:
            print(wrong_letters, " are not in your tiles")
            return flag1
        elif not flag2:
            print(word, " doesnt exists")
            return flag2

    @staticmethod
    def word_val(word):
        temp_score = 0
        for i in word:
            temp_score += lets[i][1]
        return temp_score

    def update_letters(self, word):
        for i in word:
            self.playerLetters.remove(i)
        print("Remaining letters are: ", self.playerLetters)

    def print_letters(self):
        for l in self.playerLetters:
            if l in lets:
                a = lets[l][1]
                print("|", l, ",", a, "|", end=' ')
        print()


class Human(Player):
    def __init__(self, name):
        super().__init__(name)

    def play(self):
        print("Now Playing:", self.name, " Score: ", self.score)
        print("Your letters: ")
        self.print_letters()
        word = input("Player enter your word or p to Pass: ").upper()
        if word == "P":
            print("You passed")
            return "p"
        while self.check_word(word) == False:
            word = input("Enter a new word or p to Pass: ").upper()
            if word == "P":
                print("You passed your turn. All your letters will be returned")
                return "p"
        turn_score = self.word_val(word)
        self.score += turn_score
        self.update_letters(word)
        print("You got ", turn_score, " points.")


class Computer(Player):
    def __init__(self, algorithm):
        super().__init__("Computer")
        self.algorithm = algorithm

    def min_letters(self):
        for i in range(2, 8):
            perm = permutations(self.playerLetters, i)
            for j in list(perm):
                word = ""
                for k in j:
                    word += k
                if self.word_in_dict(word) == True:
                    print(word)
                    return word
        return False

    def max_letters(self):
        for i in reversed(range(2, 8)):
            perm = permutations(self.playerLetters, i)
            for j in list(perm):
                word = ""
                for k in j:
                    word += k
                if self.word_in_dict(word) == True:
                    print(word)
                    return word
        return False

    def smart(self):
        max_points = 0
        best_word = ""
        for i in range(2, 8):
            perm = permutations(self.playerLetters, i)
            for j in list(perm):
                word = ""
                for k in j:
                    word += k
                if self.word_in_dict(word) == True:
                    if max_points < self.word_val(word):
                        max_points = self.word_val(word)
                        best_word = word
        if max_points == 0:
            return False
        else:
            return best_word

    def play(self):
        print("Computer's turn.")
        print("Computer letters are: ")
        self.print_letters()

        if self.algorithm == "Min_letters":
            print("Playing with: ", self.algorithm)
            word = self.min_letters()
        elif self.algorithm == "Max_letters":
            print("Playing with: ", self.algorithm)
            word = self.max_letters()
        else:
            print("Playing with: ", self.algorithm)
            word = self.smart()

        if word == False:
            print("Computer could not find a word")
            return False

        print("Computer entered word: ", word)

        self.update_letters(word)
        turn_score = self.word_val(word)
        self.score += turn_score
        print("Computer got ", turn_score, " points.")


class Game:
    def __init__(self, game_mode):
        self.initialize_accepted_words()

        pname = input('Enter Players Name: ')
        self.player_human = Human(pname)
        self.player_computer = Computer(game_mode)
        self.game_sak = SakClass()
        self.round = 0
        self.Setup()

    def __repr__(self):
        return 'Game Instance'

    @staticmethod
    def word_size(s):
        return len(s)

    @staticmethod
    def word_val2(word):
        temp_score = 0
        for i in word:
            temp_score += lets[i][1]
        return temp_score

    def initialize_accepted_words(self):
        global greek7
        print("Initializing file")

        with open('greek7.txt', 'r', encoding='utf') as f7:
            a = f7.readlines()
            for index, i in enumerate(a):
                a[index] = i.strip('\n')
                greek7[a[index]] = self.word_val2(a[index])

    def Setup(self):
        print("Setting Up")
        self.run()

    def run(self):
        print("Game Started")
        game = "1"
        while game != "q" and game != ";":
            self.round += 1
            print("--------------------")
            print("      Round ", self.round)
            print("--------------------")
            # human
            letters_to_Draw = 7 - len(self.player_human.playerLetters)
            if self.game_sak.letters_available - letters_to_Draw < 0:
                print("No Letters available")
                self.end()
                return
            self.player_human.playerLetters += self.game_sak.randomLetters(letters_to_Draw)
            a = self.player_human.play()
            if a == "p":
                # returning letters
                self.game_sak.return_letters(self.player_human.playerLetters)
                self.player_human.playerLetters.clear()
            print("-------------------------")
            letters_to_Draw = 7 - len(self.player_computer.playerLetters)
            if self.game_sak.letters_available - letters_to_Draw < 0:
                print("No Letters available")
                self.end()
                return
            self.player_computer.playerLetters += self.game_sak.randomLetters(letters_to_Draw)
            flag = self.player_computer.play()
            if flag == False:
                print("Computer Passed")
                self.game_sak.return_letters(self.player_computer.playerLetters)
                self.player_computer.playerLetters.clear()
            print()
            print("--------------------------")
            print("End of round. Score is: ", self.player_human.name, ": ", self.player_human.score, " Computer: ",
                  self.player_computer.score)
            print("Tiles remaining: ", self.game_sak.letters_available)
            print("--------------------------")
            print()
            game = input("Play next round? [Any key] to continue [q | ;] Quit ")
        self.end()

    def end(self):
        data = {
            "name": self.player_human.name,
            "score_h": self.player_human.score,
            "score_c": self.player_computer.score,
            "rounds": self.round
        }

        with open('score_file.json', 'r+') as file:
            file_data = json.load(file)
            file_data["games"].append(data)
            file.seek(0)
            json.dump(file_data, file, indent=4)
        print("Game over")
        self.final_score()

    def final_score(self):
        ph = self.player_human.score
        pc = self.player_computer.score
        pn = self.player_human.name

        print("---------------------------------------------")
        print("With ", self.round, " rounds played, the Final score is ", pn, " ", ph, "-- Computer: ", pc)
        print("---------------------------------------------")

        if ph > pc:
            print(pn, " is the winner!!")
        elif ph < pc:
            print("Computer is the winner!!")
        else:
            print("Its a tie")
        print()


class SakClass:
    def __init__(self):
        self.letters_available = 102
        self.game_sak = lets.copy()

    def randomLetters(self, amount_of_letters):
        new_letters = []
        w = []
        for i in range(0, amount_of_letters):
            for l in self.game_sak:
                w.append(self.game_sak[l][0])
            if self.letters_available - amount_of_letters >= 0:
                draw = random.choices(list(self.game_sak.keys()), weights=w)
                a = self.game_sak[draw[0]]
                if a[0] - 1 > 0:
                    a[0] -= 1
                    self.letters_available -= 1
                else:
                    del self.game_sak[draw[0]]
                    self.letters_available -= 1
                new_letters += draw
            w = []
        return new_letters

    def return_letters(self, letters_returned):
        for l in letters_returned:
            flag = False
            for i in self.game_sak:
                if l == i:
                    a = self.game_sak[i]
                    a[0] += 1
                    self.letters_available += 1
                    flag = True
                    break
            if flag == False:
                self.game_sak[l] = lets[l].copy()
                self.game_sak[l][0] = 1
                self.letters_available += 1
