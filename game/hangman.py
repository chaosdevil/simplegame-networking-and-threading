from random import randrange, sample
from game.draw import phases


class Hangman:

    def __init__(self):
        self.answer = "".join(map(str, sample([0,1,2,3,4,5,6,7,8,9], 5)))
        self.empty_answer = "_" * len(self.answer)
        self.tries = 5
        self.phase = 0
        self.available_numbers = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
        self.won = False

    def check(self, guess: str):
        if self.tries != 0:
            if self.check_available_numbers(guess):
                if guess in self.answer:
                    # fill number in empty answer
                    self.fill(guess)

                    # check if won the game
                    self.is_won()

                    # remove guess as guess is not available anymore
                    self.available_numbers.remove(guess)

                    # print hangman
                    correct_guess = f"Correct! There is {guess} in the answer"
                    av_nums = f"Available numbers left : {self.available_numbers}"
                    return self.print_hangman(), av_nums, correct_guess
                else:
                    self.tries -= 1
                    self.phase += 1

                    self.available_numbers.remove(guess)

                    # reduce number of tries
                    # print hangman
                    incorrect_guess = "Incorrect! There is no such number"
                    av_nums = f"Available numbers left : {self.available_numbers}"
                    return self.print_hangman(), av_nums, incorrect_guess
            else:
                not_available_num = f"{guess} was already used!"
                av_nums = f"Available numbers left : {self.available_numbers}"
                return self.print_hangman(), av_nums, not_available_num

    def fill(self, guess):
        for i in range(len(self.answer)):
            if guess == self.answer[i]:
                self.empty_answer = self.empty_answer[:i] + \
                    guess + self.empty_answer[i+1:]

    # check if empty_answer is
    def is_won(self):
        for ch in self.empty_answer:
            if ch == "_":
                self.won = False
                return
        self.won = True

    def print_hangman(self):
        return phases[self.phase]

    def check_available_numbers(self, guess):
        if guess in self.available_numbers:
            return True
        return False


# driver code
if __name__ == "__main__":
    hangman = Hangman()

    while not hangman.won and hangman.tries != 0:
        n = input("Enter number : ")
        if len(n) == 1:
            if n.isalpha():
                print("Enter only numbers")
            else:
                hang, available_numbers = hangman.check(n)
                print(hang)
                print(hangman.empty_answer)
                print(available_numbers)
        else:
            print("1 digit number accepted!")

        if hangman.won:
            print(f"You won! The answer is {hangman.answer}")
            break


    


