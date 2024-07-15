import random


class WordleGame():
    # Instance variables:
    # self.word: the target word
    # self.guesses: the guesses which the player has made
    # self.guessed_letters: a bool[26] array representing which letters have been guessed
    # self.wordlist: all possible answer words
    # self.legalwords: all legal guesses
    def __init__(self):
        self.word = None
        self.guesses = None
        self.good_letters = None
        self.used_letters = None

        self.wordlist = []
        f = open("wordle_words.txt")
        for line in f.readlines():
            self.wordlist.append(line.strip().upper())

        self.legalwords = []
        f = open("scrabble_v.txt")
        for line in f.readlines():
            self.legalwords.append(line.strip().upper())

        self.restartGame()

    def restartGame(self):
        self.word = random.choice(self.wordlist)
        self.guesses = []
        self.good_letters = [False]*26
        self.used_letters = [False]*26

    def charToInt(self, c):
        return ord(c) - ord("A")

    def intToChar(self, n):
        return chr(ord("A") + n)

    # given two words of the same length (or one word of length 5)
    # returns a list of that length containing 0, 1 or 2 corresponding to how correct word is:
    #   0 is an incorrect letter
    #   1 is correct in the wrong location
    #   2 is completely correct
    def getWordDistance(self, word, target=None):
        if target is None:
            target = self.word

        if len(word) != len(target):
            raise Exception("word and target do not have the same length: " + word + ", " + target)

        word = word.upper()
        target = target.upper()

        ans = [0 for i in range(len(word))]

        word_letters = [0]*26
        target_letters = [0]*26
        correct_loc_letters = [0]*26

        for i in range(len(word)):
            word_char = self.charToInt(word[i])
            target_char = self.charToInt(target[i])
            word_letters[word_char] += 1
            target_letters[target_char] += 1
            if word_char == target_char:
                correct_loc_letters[word_char] += 1
                ans[i] = 2

        correct_val_letters = [0]*26
        # now calculate which letters are in wrong spot, but are correct
        for j in range(26):
            correct_val_letters[j] = min(word_letters[j], target_letters[j])
            correct_val_letters[j] -= correct_loc_letters[j]

        # print(word_letters)
        # print(target_letters)
        # print(correct_loc_letters)
        # print(correct_val_letters)

        for i in range(len(word)):
            n = self.charToInt(word[i])
            if ans[i] == 0 and correct_val_letters[n] != 0:
                ans[i] = 1
                correct_val_letters[n] -= 1

        return ans

    # returns the word distance, or None if the word is not legal
    def guessWord(self, word):
        word = word.upper()
        if word not in self.legalwords:
            return None
        else:
            dist = self.getWordDistance(word)
            self.guesses.append(word)
            for i in range(len(word)):
                self.used_letters[self.charToInt(word[i])] = True
                if dist[i] != 0:
                    self.good_letters[self.charToInt(word[i])] = True
            return dist

    # returns pairs of guesses and their distance
    def getState(self):
        return [(g, self.getWordDistance(g)) for g in self.guesses]

    def getGoodLetters(self):
        alpha = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        return "".join([c for c in alpha if self.good_letters[self.charToInt(c)]])

    def getUsedLetters(self):
        alpha = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        return "".join([c for c in alpha if self.used_letters[self.charToInt(c)]])

    def gameWon(self):
        return self.word in self.guesses
