import random
import time


class Codenames:
    def __init__(self):
        self.in_progress = True
        self.red_turn = True
        self.board = []
        self.colours = {}
        self.generate_board()
        self.generate_colours()
        self.red_clues = []
        self.blue_clues = []
        self.red_points = 0
        self.blue_points = 0

    def generate_board(self):
        with open('words.txt', 'r') as wordfile:
            lines = wordfile.readlines()
            used_indices = []
            for i in range(0, 25):
                random_index = get_random_index(used_indices, len(lines))
                self.board.append(lines[random_index].strip("\n"))

    def generate_colours(self):
        for i in range(0, 25):
            used_indices = []
            for i in range(0, 9):
                random_index = get_random_index(used_indices, 25)
                self.colours[random_index] = "RED"
            for j in range(0, 8):
                random_index = get_random_index(used_indices, 25)
                self.colours[random_index] = "BLUE"
            for k in range(0, 7):
                random_index = get_random_index(used_indices, 25)
                self.colours[random_index] = "NEUTRAL"
            random_index = get_random_index(used_indices, 25)
            self.colours[random_index] = "ASSASSIN"

    def print_board(self):
        board_2d = [[], [], [], [], []]
        row = 0
        for i in range(0, 5):
            for j in range(0, 5):
                board_2d[i].append(self.board[j+row])
                while len(board_2d[i][j]) != 15:
                    board_2d[i][j] += " "
            row += 5
            print(board_2d[i])

    def print_colours(self):
        colours_2d = [[], [], [], [], []]
        row = 0
        for i in range(0, 5):
            for j in range(0, 5):
                colours_2d[i].append(self.colours[j + row])
                while len(colours_2d[i][j]) != 15:
                    colours_2d[i][j] += " "
            row += 5
            print(colours_2d[i])

    def guess(self, guess):
        colour = self.colours[self.board.index(guess.capitalize())]
        self.board[self.board.index(guess.capitalize())] = colour
        if colour == "ASSASSIN":
            assassinate(self.red_turn)
            self.end_game()
        if colour == "RED":
            if self.red_turn:
                self.red_points += 1
                if self.red_points == 9:
                    print("Red team wins!!!")
                    self.end_game()
                return True, colour
            else:
                return False, colour
        elif colour == "BLUE":
            if not self.red_turn:
                self.blue_points += 1
                if self.blue_points == 9:
                    print("Blue team wins!!!")
                    self.end_game()
                return True, colour
            else:
                return False, colour
        else:
            return False, colour

    def end_game(self):
        print("Game over!")
        self.in_progress = False

    def show_clues(self):
        if self.red_turn:
            print(self.red_clues)
        else:
            print(self.blue_clues)


def get_random_index(used, range):
    while True:
        random_index = random.randint(0, range-1)
        if random_index not in used:
            used.append(random_index)
            return random_index


def assassinate(red_team):
    if red_team:
        print("You hit the assassin! Blue team wins!")
    else:
        print("You hit the assassin! Red team wins!")


game = Codenames()

print("Welcome to Codenames!")
print()

reader_red = input("Enter the reader's name for the Red team: ")
reader_blue = input("Enter the reader's name for the Blue team: ")

print()

while game.in_progress:
    gameover = False

    print("%s (%s), it's your turn! Here is the board: " % (reader_red if game.red_turn else reader_blue, "Red" if game.red_turn else "Blue"))
    game.print_board()
    print()
    print("Here are the colours:")
    game.print_colours()

    clue, number = input("Please enter a clue and the number of words it corresponds to (e.g. Dog 2): ").split()
    if game.red_turn:
        game.red_clues.append((clue, number))
    else:
        game.blue_clues.append((clue, number))

    for i in range(0, 100):
        print(".")

    print("%s (%s)'s team! Here are the clues so far:" % (reader_red if game.red_turn else reader_blue, "Red" if game.red_turn else "Blue"))
    game.show_clues()
    print()
    print("Here is the board:")
    game.print_board()
    for i in range(0, int(number)+1):
        guess = input("Please guess word " + str(i+1) + ": ")
        while guess.capitalize() not in game.board:
            guess = input("That word isn't on the board! Guess again: ")
        correct, actual_colour = game.guess(guess)
        if correct:
            if not game.in_progress:
                gameover = True
                break
            if (i+1) != int(number)+1:
                guess_again = input("Correct! Would you like to guess again? Enter y for yes: ")
                if guess_again.lower() == "y":
                    print("Ok! Here is the board:")
                    game.print_board()
                else:
                    break
            else:
                break
        else:
            if not game.in_progress:
                gameover = True
                break
            print("Wrong! That one was " + actual_colour)
            break

    if gameover:
        break

    # Toggle player's turn
    game.red_turn = not game.red_turn

    print("Your turn is over! Switching to reader mode in 5 seconds.")
    time.sleep(5)
    for i in range(0, 100):
        print(".")
