import random, io, os, string
from functions import * #importing the functions from functions.py

path = "word_lists" #defines the path to the folder with word lists
included_filetypes = ["txt"] #what file should be includes in the word lists

word_lists = [fn for fn in os.listdir(path) if any(fn.endswith(ft) for ft in included_filetypes)] #create a list with all the word lists in the folder
word_lists_clean = clean_up_word_lists(word_lists) #cleans up the word list so that onlly the names are displayed

alpabet = set(string.ascii_uppercase) #define the alphabet used for game
lives = 6
guessed_letters = []
correct_letters = []
wrong_letters = []

#print(word_lists) #just for testing

if __name__ == "__main__":
    print("Welcome to Hangman! \n")

    #lets the user add custom words to the game
    custom = input("Do you want to add custom words? [y/n]: ")
    if custom == "y":
        custom_words = input("Enter the words you want to use with a comma: ")
        custom_word_list = custom_words.split(",")
        with open(os.path.join(path,"words_custom.txt"), "w") as f:
            for word in custom_word_list:
                f.write(word+"\n")


    #lets the user choose a word list from the options
    while True:
            word_list = choose_word_list(word_lists, word_lists_clean)
            if not word_list:
                print("Invalid Input")
            else:
                break

    #trys to open the chosen word list and the hangman pictures txt file            
    try:
        file_path = os.path.join(path, word_list)
        file = io.open(file_path, "r")
        hangman_pics = load_hangman_pictures("hangmanpictures.txt")
    except FileNotFoundError:
        print("File not found")


    num_of_lines = number_of_lines(file) #gets the number of lines in the chosen word list
    print("The word list that you chose contains " + str(num_of_lines) + " words")
    word = choose_random_word(file, num_of_lines) #picks a random word from the word list
    word = word.upper() #transfroms the word to uppercase
    #print(word) #just for testing
    blank = create_blank(word) #creates the blank version of the random word

    #main gameplay loop
    while lives > 0: #wheter the player still can guess
        print(hangman_pics[6 - lives]) #prints the hangman picture depending on the mistakes of the user

        #print the progress of the user
        print("The word you need to guess is: " + blank)
        print("The letters you have guessed so far are: " + " ".join(guessed_letters))
        print("The wrong letters you have guessed so far are: " + " ".join(wrong_letters))
        letter = input("Guess a letter: ").upper()

        #checks if the user input is invalid
        if len(letter) != 1 or letter not in alpabet:
            print("Invalid input. Please enter a single letter from A-Z.")
            continue

        #checks if the latter is in the word and updates the blank version word
        if letter in word:
            print("You found a correct letter!")
            guessed_letters.append(letter)
            correct_letters.append(letter)
            new_blank = ""
            for l in word:
                if l in correct_letters:
                    new_blank += l
                else:
                    new_blank += "_"
            blank = new_blank
        #if the letter is not in the word and wrong add it to wrong letters
        elif letter not in guessed_letters and letter not in wrong_letters: #also checks if it is already guessed
            print("The letter is not in the word.")
            guessed_letters.append(letter)
            wrong_letters.append(letter)
            lives -= 1

        #if the new blank word matches the chosen random word the player won
        if blank == word:
            print(f"You won! You found the word: {word}")
            break

    #checks whether the player lost
    if lives == 0:
        print(f"You lost! The word you should have guessed was: {word}")


    file.close()