from wordle import Wordle

if __name__ == "__main__":
    # Open the file of 5-letter words and play the game with it
    with open("words.txt") as word_file:
        # For each word, get rid of whitespace (newlines) and make them uppercase
        word_list = [word.strip().upper() for word in word_file.readlines()]
    game = Wordle(word_list)
    game.window.mainloop()