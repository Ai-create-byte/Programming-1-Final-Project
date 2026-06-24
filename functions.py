import os,io,random,string


#loads the hangman pictures from the txt file into a list
def load_hangman_pictures(file_name) -> list:
    with io.open(file_name, "r") as file:
        content = file.read()
    return content.split("'''\n")

#gives the number of lines in the chosen word list
def number_of_lines(file_name) -> int:
    return len(file_name.readlines())
    
#cleaning up the word list names for better display
def clean_up_word_lists(word_lists) -> list:
    cleaned_list = []
    for i in range(len(word_lists)):
        part1, part2 = word_lists[i].split("_", 1)
        result = part2.split(".txt", 1)[0]
        cleaned_list.append(result)
    return cleaned_list

#lets the user choose a word list frrom word_lists folder
def choose_word_list(word_lists, word_lists_clean) -> int:
    try:
        num_word_lists = int(input(f"Choose a word list {word_lists_clean}: "))
    except ValueError:
        return None
    if num_word_lists > 0 and num_word_lists <= len(word_lists):
        return word_lists[num_word_lists - 1]
    else:
        return None    

#picks a random word from the chosen word list
def choose_random_word(file_name, num_lines) -> str:
    random_line = random.randint(0, num_lines - 1)
    #print(random_line) #just for testing
    file_name.seek(0) # file pointer back to the first line
    for i in range(random_line + 1):
        word = file_name.readline().strip()
    return word

#creates the blank word without any letters
def create_blank(word) -> str:
    blank = ""
    for letter in word:
        blank += "_"
    return blank


    