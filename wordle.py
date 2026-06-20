import random
import tkinter as tk
from tkinter import messagebox
import webbrowser


class Wordle:
    def __init__(self, word_list):
        # Style attributes
        self.font = "Helvectica"
        self.bg_color = "white"
        # Setup window
        self.window = tk.Tk()
        self.window.title("PyWordle")
        self.window.config(bg="white")
        # Center window
        self.center_window()
        # Game Components
        self.guess_entry = None
        self.guess_results = []
        self.letters = [["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P"],
                        ["A", "S", "D", "F", "G", "H", "J", "K", "L"],
                        ["Z", "X", "C", "V", "B", "N", "M"]]
        self.key_rows = []
        self.word_list = word_list
        self.guess_count = 0
        self.guessed_words = []
        self.target_word = self.pick_word()
        # Setup frames for game window
        self.setup_frames()
        # Play Again Button
        play_again = tk.Button(self.window, text="Play Again", justify="center", font=(self.font, 20),
                               highlightbackground=self.bg_color, bg=self.bg_color, width=10, command=self.play_again)
        play_again.grid(row=5, column=0)

    def center_window(self):
        """
        Centers the root window using the screen size and window size
        """
        # Screen dimensions
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        # Window dimensions
        window_width = 400
        window_height = 680
        # (x,y) starts at top left of window (0, 0)
        # x increases moving right, decreases moving left
        # y increases moving down, decreases moving up
        x = screen_width / 2 - window_width / 2  # position top left corner's x at this x
        y = screen_height / 2 - window_height  # position top left corner's y at a smaller y (otherwise window too low)
        self.window.geometry(
            "%dx%d+%d+%d" % (window_width, window_height, x, y))  # Adds x and y offsets to window dims
        self.window.resizable(width=False, height=False)  # Prevent window from being resizable

    def setup_frames(self) -> None:
        """
        Sets up the frames for the game window
        """
        self.setup_title_frame()
        self.setup_guess_entry()
        self.setup_guess_results()
        self.setup_letter_frame()

    def setup_title_frame(self) -> None:
        """
        Sets up the title for the game window
        """
        title_frame = tk.Frame(self.window)
        title_frame.grid(row=0, column=0)
        title = tk.Label(title_frame, text="PYWORDLE", font=(self.font, 40, "bold"),
                         justify="center", bg=self.bg_color)
        title.grid(row=0, column=0)
        # Create a separator between title and guess entry
        separator = tk.Frame(self.window, relief="solid", width=400, height=2,
                             highlightbackground="black", highlightthickness=5)
        separator.grid(row=1, column=0)

    def setup_guess_entry(self) -> None:
        """
        Sets up the guess entry frame for the game window
        """
        guess_entry_frame = tk.Frame(self.window)
        guess_entry_frame.grid(row=2, column=0, pady=10)
        self.guess_entry = tk.Entry(guess_entry_frame, width=8, font=(self.font, 30), justify="center")
        self.guess_entry.grid(row=0, column=0)
        self.guess_entry.bind("<Return>", self.check_guess)  # When pressing the Enter key, run the check_guess function
        self.guess_entry.focus_set()  # Automatically have the cursor in the guess entry field

    def setup_guess_results(self) -> None:
        """
        Sets up the guess results frame for the game window
        """
        results_frame = tk.Frame(self.window)
        results_frame.grid(row=3, column=0)
        for i in range(0, 6):
            result_row = tk.Frame(results_frame, bg=self.bg_color, padx=30, pady=2)
            result_row.grid(row=i, column=0)
            row_list = []
            for j in range(0, 5):
                result_square = tk.Label(result_row, bg=self.bg_color, width=6, height=3, relief="solid")
                result_square.grid(row=0, column=j, padx=2)
                row_list.append(result_square)
            self.guess_results.append(row_list)

    def setup_letter_frame(self) -> None:
        """
        Sets up the letter frame for the game window
        """
        key_frame = tk.Frame(self.window, bg=self.bg_color)
        key_frame.grid(row=4, column=0)
        for i in range(0, len(self.letters)):
            key_row = tk.Frame(key_frame)
            key_row.grid(row=i, column=0)
            for j in range(0, len(self.letters[i])):
                key_label = tk.Label(key_row, font=(self.font, 25), text=self.letters[i][j],
                                     bg=self.bg_color)
                key_label.grid(row=0, column=j)
            self.key_rows.append(key_row)

    def pick_word(self) -> str:
        """
        Pick a random 5-letter word from a curated list
        :return: a random 5-letter word as a string
        """
        # Picking a random word from the list of words
        return random.choice(self.word_list)

    def check_game_over(self, guess_word) -> None:
        """
        Check if the game is over and report the results to the user
        :param guess_word: the user's guess word
        """
        # Game is over once the user makes 6 guesses or gets the word
        if self.guess_count == 6 or guess_word == self.target_word:
            if self.guess_count == 6 and guess_word != self.target_word:
                messagebox.showinfo(message=f"YOU LOSE...\nThe word was {self.target_word}")
                self.guess_entry.insert(0, self.target_word)
            else:
                messagebox.showinfo(message=f"YOU WIN!\nThe word was {self.target_word}\nGuesses: {self.guess_count}/6")
                self.guess_entry.insert(0, self.target_word)
                self.guess_entry.config(fg="green")
            self.guess_entry.config(state="readonly")
            self.get_word_def() # Pull up the word definition

    def check_guess(self, event) -> None:
        """
        Get and check the user's guess for what the target word is
        :param event: the event that will result in the guess being recorded
        """
        guess_word = self.guess_entry.get().upper() # Get the guess word from text entry
        # If the user's guess is 5 letters long, in the word list, not already guessed, and has made less than 6 guesses
        if len(guess_word) == 5 and guess_word in self.word_list and guess_word not in self.guessed_words and self.guess_count < 6:
            # Accept the user's guess and show them the results
            self.guessed_words.append(guess_word)
            self.guess_entry.delete(0, tk.END)
            self.get_guess_results(guess_word)
            self.guess_count += 1
        # Otherwise notify the user if there are any errors with any of the three conditions above
        elif len(guess_word) != 5:
            messagebox.showerror(message="Guess MUST be 5 letters long!")
        elif guess_word not in self.word_list:
            messagebox.showerror(message="Guess is NOT a valid word.")
        else:
            messagebox.showerror(message="You've already guessed this word.")
        self.window.focus_set() # Set focus back to window (messagebox popups move focus out of window)
        self.guess_entry.focus_set() # Move focus to the guess entry
        self.check_game_over(guess_word) # Check if the game is over (user guessed the word or 6 guesses used up)

    def play_again(self) -> None:
        """
        Resets the Wordle game so the user can play again
        """
        # Reset game stats
        self.guessed_words = []
        self.guess_count = 0
        self.guess_entry.config(state="normal", fg="black") # User can make guesses again, reset font color to black
        self.guess_entry.delete(0, tk.END) # Clear the guess entry
        self.target_word = self.pick_word() # Pick another random word
        # Reset the key display (red letters back to black)
        for key_row in self.key_rows:
            for key_label in key_row.winfo_children():
                key_label.config(fg="black")
        # Reset guess result squares
        for i in range(0, 6):
            for j in range(0, 5):
                self.guess_results[i][j].config(text="", bg="white")

    def make_green(self, guess_chars, target_chars, guess) -> None:
        """
        Makes green squares and marks the corresponding square letters green if they aren't already
        :param guess_chars: list of chars in the guess word
        :param target_chars: list of chars in the target word
        :param guess: the guess word itself
        """
        # Making green squares
        for j in range(0, 5):
            # If the guess char is the same as the target char in the current position
            if guess_chars[j] == target_chars[j]:
                # Make the square at the position green
                self.guess_results[self.guess_count][j].config(text=guess_chars[j], bg="green")
                # Making the corresponding key green
                for key_row in self.key_rows:
                    for key_label in key_row.winfo_children():
                        # Check if the key matches the letter
                        if key_label.cget("text") == guess[j]:
                            key_label.config(fg="green")
                guess_chars[j], target_chars[j] = "", ""  # Make the letter from both words blank

    def make_yellow(self, guess_chars, target_chars, guess) -> None:
        """
        Makes green squares and marks the corresponding square letters yellow if they are white
        :param guess_chars: list of chars in the guess word
        :param target_chars: list of chars in the target word
        :param guess: the guess word itself
        """
        for k in range(0, 5):
            if guess_chars[k] in target_chars and guess_chars[k] != "":
                # Make the square at the position yellow
                self.guess_results[self.guess_count][k].config(text=guess_chars[k], bg="yellow")
                # Making the corresponding key yellow
                for key_row in self.key_rows:
                    for key_label in key_row.winfo_children():
                        # Check if the key matches the letter and is not green
                        if key_label.cget("text") == guess[k] and key_label.cget("fg") != "green":
                            key_label.config(fg="#FBC901")
                target_chars[target_chars.index(guess_chars[k])] = "" # Make the letter in target word blank first
                guess_chars[k] = "" # Then make this character blank

    def make_white(self, guess_chars, guess) -> None:
        """
        Makes white squares in the current guess result row
        :param guess_chars: list of chars in the guess word
        :param guess: the guess word itself
        """
        for l in range(0, 5):
            if guess_chars[l] != "" and guess_chars[l] not in self.target_word:
                # Removing the letters from the guess word that are not in the target word at all
                for key_row in self.key_rows:
                    for key_label in key_row.winfo_children():
                        # Check if the key matches the letter
                        if key_label.cget("text") == guess[l]:
                            key_label.config(fg="white") # White background, so the letter appears invisible

    def get_guess_results(self, guess) -> None:
        """
        Get the results of comparing the user's guess with the target
        :param guess: the user's word guess
        """
        # To more easily compare guess with target (char by char)
        target_chars = [char for char in self.target_word]
        guess_chars = [char for char in guess]
        # Display the letters of the guess word onto the current result row
        for i in range(0, 5):
            self.guess_results[self.guess_count][i].config(text=guess[i])
        # Making green squares and marking letters in target in right place
        self.make_green(guess_chars, target_chars, guess)
        # Making yellow squares and marking letters in target but wrong place
        self.make_yellow(guess_chars, target_chars, guess)
        # Making white squares and marking letters not in target
        self.make_white(guess_chars, guess)

    def get_word_def(self) -> None:
        """
        Gets the definition of the target word, if the user desires it
        """
        see_word = messagebox.askyesno(message=f"Wanna see the definition for {self.target_word}?")
        if see_word:
            webbrowser.open(f"https://www.google.com/search?client=safari&rls=en&q={self.target_word}+word+definition&ie=UTF-8&oe=UTF-8")