# python -m pip install pygame-menu pygame #for installing the modules

import random, io, os, string, pygame, pygame_menu
from functions import * #importing the functions from functions.py
from pygame_menu import themes

path = "word_lists" #defines the path to the folder with word lists
included_filetypes = ["txt"] #what file should be includes in the word lists

word_lists = [fn for fn in os.listdir(path) if any(fn.endswith(ft) for ft in included_filetypes)] #create a list with all the word lists in the folder (solution by Ben Hoyt from Stackoverflow)
word_lists_clean = clean_up_word_lists(word_lists) #cleans up th words, so that only the names of the txt files are displayed

pygame.init() 
pygame.display.set_caption("Hangman") #changes the window name to Hangman
screen = pygame.display.set_mode((1280, 720)) #declaration of the size of the window
clock = pygame.time.Clock()
running = True

backgrond = pygame.Surface((1280, 720))
backgrond.fill((0, 0, 0)) #creates background as big as the screen in black

theme = pygame_menu.themes.THEME_DARK.copy() #adjusting the pygame_menu themes
theme.title_font = pygame_menu.font.FONT_8BIT
theme.title_font_size = 50
theme.widget_font = pygame_menu.font.FONT_8BIT
theme.widget_font_size = 30

FONT = pygame.font.SysFont("comicsans",32) #initialization of the font (type and size)

alpabet = set(string.ascii_uppercase) #define the alphabet used for game
lives = 6 
guessed_letters = []
correct_letters = []
wrong_letters = []
hangmanPics = []

#buttons
radius = 30
gap = 20
buttons = []
startx = 100
starty = 100
for i in range(26):
    if i<24:
        x = startx + gap * 2 + ((radius * 2 + gap) * (i % 4))
        y = starty + ((i // 4) * (gap + radius * 2))
    else:
        x = startx + gap * 2 + ((radius * 2 + gap) * ((i+1) % 4))
        y = starty + (((i+1) // 4) * (gap + radius * 2))
    buttons.append([x, y, chr(65 + i), True])   #creates the button layout taken from adislksn from github 

def choose_word_list_menu():
    mainmenu._open(list_menu)

def choose_and_start(filename):
    list_menu._close()
    start_game(filename)

def add_word_menu():
    list_menu._open(add_menu)
    
def get_words(): #gets the text input from the user and adds it to the txt file
    custom_words = custom_input.get_value() 
    custom_word_list = custom_words.split(",")
    with open(os.path.join(path,"words_custom.txt"), "w") as f:
        for word in custom_word_list:
            f.write(word+"\n")
    add_menu.close()
    add_menu._open(list_menu)   
      
mainmenu = pygame_menu.Menu("Hangman", 1280, 720, theme=theme) #creation of the mainmenu
mainmenu.add.button("Choose Word List", choose_word_list_menu) #create the button of the selection menu
mainmenu.add.button("Quit", pygame_menu.events.EXIT) #creates the exit button with the function that it exits the programm

list_menu = pygame_menu.Menu("Choose a Word List", 1280, 720, theme=theme) #creates the submenu - where the user should choose the word list
for i in range(len(word_lists)):
    list_menu.add.button(word_lists_clean[i], lambda f=word_lists[i]: choose_and_start(f)) #displays the name of the different txt files (solution with the lambda found on StackOverflow)
custom_btn = list_menu.add.button("Add custom words", add_word_menu)    
back_btn = list_menu.add.button("Back", pygame_menu.events.BACK) #creates a back button
back_btn.set_background_color((0, 0, 0)) #gives this button a black background
back_btn._font_color = (255, 255, 255) #the color of the text included is white in this case

add_menu = pygame_menu.Menu("Add words", 1280, 720, theme=theme)
custom_input = add_menu.add.text_input("Enter the words with a comma: ", font_name=FONT) #asks for user input
add_menu.add.button("Save", get_words)
back_btn_add = add_menu.add.button("Back", pygame_menu.events.BACK) #creates a back button
back_btn_add.set_background_color((0, 0, 0)) #gives this button a black background
back_btn_add._font_color = (255, 255, 255) #the color of the text included is white in this case

def check_letter(letter, word, blank): #checks if the letter is included in the word or not and updates blank
    letter = letter.upper()
    global lives
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
    elif letter not in guessed_letters and letter not in wrong_letters: #also checks if it is already guessed
            print("The letter is not in the word.")
            guessed_letters.append(letter)
            wrong_letters.append(letter)
            lives -= 1

    return blank        


def start_game(filename): #main function start starts the game

    for i in range(7):
        hangmanPics.append(pygame.image.load(os.path.join("images", f"hangman{i}.png"))) #load the different hangmanpictures from the folder

    try:
        file_path = os.path.join(path, filename) #tries to open/read the chosen word list
        file = io.open(file_path, "r")
    except FileNotFoundError:
        print("File not found")
        return None

    num_of_lines = number_of_lines(file) #gets the number of lines in the chosen word list
    word = choose_random_word(file, num_of_lines) #picks a random word from word list

    word = word.upper() #transfroms the word to uppercase
    blank = create_blank(word) #creates the blank version of the random word

    

    def draw(): #drawing of the visual elements on the main screen 
        screen.fill((255,255,255)) #white background
        if lives > 0:
            screen.blit(hangmanPics[6 - lives], (800, 100)) #updates the picture of hangman dependend on the lives
        
        text = FONT.render("Hangman", 1, (0,0,0)) #initializes the font the text
        screen.blit(text, (550, 20)) # displays the text

        offset = 0
        for l in word: #creates the blank squares where the user needs to guess
            black_rec = pygame.draw.rect(screen, "black", (500+offset, 550, 50, 10))
            offset += 70

        for button in buttons: #draws the buttons
            x, y, txt, status = button
            if status is True: #checks if the button should still be displayed
                pygame.draw.circle(screen, "black", (x, y), radius, 3)
                text = FONT.render(txt, 1, (0,0,0))
                screen.blit(text, (x - text.get_width()/2, y - text.get_height()/2))

        for i, l in enumerate(blank): #displays when blank updated the correct letters on top of the squares
            text = FONT.render(l, 1, (0,0,0))
            screen.blit(text, (515 + 70 * i, 512))
            

    while True: #main game loop
        for event in pygame.event.get(): #checks if you quit the programm -> so the programm exists
            if event.type == pygame.QUIT:
                pygame.quit()
                return None
            if event.type == pygame.MOUSEBUTTONDOWN: #checks whether the user presses down the button
                mouse_x, mouse_y = pygame.mouse.get_pos() #gets the position of the mouse
                for button in buttons:
                    x, y, letter, status = button
                    if status: #if button is still active
                        if (x - radius) <= mouse_x <= (x + radius) and (y - radius) <= mouse_y <= (y + radius): #and the mouse is on the button
                            button[3] = 0   #disable the button
                            blank = check_letter(letter, word, blank) #check the selected button
            if lives == 0: #losing condition
                screen.fill((255,0,0))
                text = FONT.render(f"You lost! The word was {word}", 1, (0,0,0))
                screen.blit(text, (450, 300))
                pygame.display.flip()
                pygame.time.delay(3000)
                pygame.quit()
            elif blank == word: #winning condition
                screen.fill((0,255,0))
                text = FONT.render(f"You won! The word was {word}", 1, (0,0,0))
                screen.blit(text, (550, 350))
                pygame.display.flip()
                pygame.time.delay(3000)
                pygame.quit()

        screen.blit(backgrond, (0, 0))
        draw() #updates the screen
        pygame.display.flip()
        clock.tick(60)

mainmenu.mainloop(screen)