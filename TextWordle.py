from WordleGame import WordleGame
from EvilWordleGame import EvilWordleGame


wg = EvilWordleGame()
flag = True
guess_count = 0

while flag:
    print("Guess a word:")
    a = input()
    dist = wg.guessWord(a)
    if dist is None:
        print("that is not a valid word")
    elif all([el == 2 for el in dist]):
        print("That's correct!")
        print("used {} guesses".format(guess_count+1))
        flag = False
    else:
        print("".join([str(n) for n in dist]))
        guess_count += 1

    # print(len(wg.word))
    # print(wg.getUsedLetters())
