# Roger You
# 15112 F

from cmu_graphics import *
import random

class WordHuntBoard:
    def __init__(self, size=4):
        self.size = size  # Board size (e.g., 4x4)
        self.board = [['' for _ in range(size)] for _ in range(size)]
        self.dictionary = ["cat", "dog", "apple", "code", "hunt", "game", "word", "python", "tree", "game", "run", "fun"]  # Sample words
        self.wordsPlaced = set()

    def generateBoard(self):
        # Ensure at least 20 words are placed
        attempts = 0
        while len(self.wordsPlaced) < 20 and attempts < 50:
            word = random.choice(self.dictionary)
            if self.placeWord(word):
                self.wordsPlaced.add(word)
            attempts += 1

