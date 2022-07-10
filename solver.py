import string

""" PROCESSING WORDS IN TXT FILE """
def list_words(path):
    ls = []
    with open(path) as f:
        ls = f.readlines()
    return ls

words = list_words('/Users/vivianyiruoliu/Desktop/Summer2022/wordle_solver/totalwords.txt')

# for each letter count how many words in which it occurs
def count_letters(words):
    alphabet = dict.fromkeys(string.ascii_lowercase, 0)
    for word in words:
        for char in alphabet:
            if char in word:
                alphabet[char] += 1
    alphabet = dict(sorted(alphabet.items(), key=lambda item: item[1], reverse=True))
    return alphabet

alphabet = count_letters(words)

#for each position count most common letter to appear
def count_positions(words):
    positions = {}
    for i in range(5):
        positions[i]=dict.fromkeys(string.ascii_lowercase, 0)

    for word in words:
        for i in range(5):
            positions[i][word[i]] += 1

    for i in range(5):
        positions[i]=dict(sorted(positions[i].items(), key=lambda item: item[1], reverse=True))
    return positions

positions = count_positions(words)
    

""" WORD RECOMMENDATION FUNCTIONS """ 
#Declaring variables
top_letters = []
words_with_top = []
rank = {}
close = 0 #metric for how close we've gotten to guessing the word, based on how many green and yellow tiles guessed
    
def top_L(num):
    """
    find top num most frequently occurring letters
    """
    global top_letters
    top_letters.clear()
    for letter in alphabet:
        if num == 0: break
        top_letters += letter
        num -= 1

def top_W(no_repeats):
    """
    find words with most common letters, if no_repeats = True then require no repeating letters
    """
    global words_with_top
    words_with_top.clear()
    for word in words:
        count = 0
        for char in word:
            if no_repeats:
                if char in top_letters and word.count(char)==1:
                    count += 1
            else:
                if char in top_letters:
                    count += 1
            if count==5 and word not in words_with_top:
                words_with_top.append(word)

def ranking(condition):
    """
    rank the most common words by how commonly their letters are in each position
    if condition = true, ranks words with more vowels highers
    """
    global rank
    rank.clear()
    vowels = ['a', 'e', 'i', 'o', 'u', 'y']
    for word in words_with_top:
        value = 0
        for i in range(5):
            value += positions[i][word[i]]
            if condition and word[i] in vowels: value +=1500
            rank[word] = value
    
    rank = dict(sorted(rank.items(), key=lambda item: item[1], reverse=True))

def selecting(lst):
    """
    restrict letter choice and position base on user input to generate next recommended word
    """
    global close
    for i in range(5):
        if lst[i][1] == 'w':
            for n in range(5):
                positions[n][lst[i][0]] = -50000
        elif lst[i][1] == 'y':
            close += 1
            for j in range(5):
                if j != i:
                    positions[j][lst[i][0]] += 20000
            positions[i][lst[i][0]] = -100000
        elif lst[i][1] == 'g':
            close += 3
            positions[i][lst[i][0]] += 100000

    if close<13: 
        top_L(18)
        top_W(True)
        ranking(True)
    else: 
        top_L(26)
        top_W(False)
        ranking(False)


""" PROMPT USER, PLAY WORDLE """
def convert(string):
    list=[]
    list[:0]=string
    return list

def play(): 
    global words
    tries = 0
    top_L(5)
    top_W(True)
    ranking(True)
    while True:
        test_word = input ("Recommended word: " + list(rank.keys())[0] + "Guess: " )

        while True:
            if not test_word.isalpha() or len(test_word) != 5:
                test_word = input("Please give a five letter word: ")
            else: break

        test_word = test_word.lower()

        test_result = input ("How did you do? g-green, y-yellow w-white, e.g. wwgyw: ")

        
        while True:
            not_valid = False
            gyw = 'gyw'
            for char in test_result: 
                if char not in gyw:
                    not_valid = True
                    break
            if (not type(test_result) is str) or len(test_result) != 5 or not_valid:
                test_result = input("Please give valid results: ")
            else: break
        
        test_result = test_result.lower()
        tries += 1
        if test_result=="ggggg": 
            print("Congratulations! You got it in " + str(tries) + " tries!")
            break

        # words.remove(test_word)
        ls1 = convert(test_word)
        ls2 = convert(test_result)
        guess_data = list(zip(ls1, ls2))
        selecting(guess_data)