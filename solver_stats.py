import solver
from matplotlib import pyplot as plt
import time


def check(guess, answer):
    guess_chars = []
    answer_chars = []
    guess_chars[:0] = guess
    answer_chars[:0] = answer
    result = []
    for i in range(5):
        if guess_chars[i] == answer_chars[i]:
            result += 'g'
        elif guess_chars[i] in answer_chars:
            result += 'y'
        else: result += 'w'
    return  "".join(result) 

num_guesses = []

def play_solver(answer): 
    global num_guesses
    tries = 0
    solver.alphabet = solver.count_letters(solver.words)
    solver.positions = solver.count_positions(solver.words)
    solver.close = 0
    solver.top_L(5)
    solver.top_W(True)
    solver.ranking(True)
    while True:
        guess = list(solver.rank.keys())[0]
        # print(guess)
        result = check(guess, answer)
        tries += 1
        if(result == "ggggg"):
            num_guesses.append(tries)
            break
        ls1 = solver.convert(guess)
        ls2 = solver.convert(result)
        guess_data = list(zip(ls1, ls2))
        solver.selecting(guess_data)

wordle_words = solver.list_words('/Users/vivianyiruoliu/Desktop/Summer2022/wordle_solver/wordle-nyt-answers-alphabetical.txt')
for word in wordle_words:
    play_solver(word)

avg = round(sum(num_guesses)/len(num_guesses), 2)
print("Average number of guesses: " + str(avg))
plt.hist(num_guesses, 10)
plt.title('Wordle Solver Histogram')
plt.xlabel('Number of Guesses')
plt.ylabel('Counts')
plt.show()
