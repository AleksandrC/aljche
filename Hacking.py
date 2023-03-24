from uagame import Window
from time import sleep
from random import randint, choice
    
    
def create_window():
    window = Window('Hacking', 600, 500)
    window.set_font_name('couriernew')
    window.set_font_size(18)
    window.set_font_color('green')
    window.set_bg_color('black')    
    return window

# create window



def display_line(window, string, location):
    pause_time = 0.3
    string_height = window.get_font_height()    
    window.draw_string(string, location[0], location[1])
    window.update()
    sleep(pause_time)
    location[1] = location[1] + string_height  

def display_header(window, location, attempts): 
    
    header = ['DEBUG MODE', str(attempts)+' ATTEMPT(S) LEFT', '']
    
    for header_line in header:
        # display header line
        display_line(window, header_line, location)  

def embed_password(password, size):
    fill = '!@#$%^*()-+=~[]{}'  
    embedding=''
    password_size = len(password)
    split_index = randint(0, size - password_size)
    for index in range (0, split_index):
        embedding += choice (fill)
    embedding = embedding + password
    for index in range (split_index+ password_size, size):
        embedding += choice (fill)
    return embedding

def display_password_list(window, location):
    # Display the game passwords, update the location for the next
    # text and return the correct password
    # - window is the Window to display in
    # - location is a list containing the int x and y coords of
    # where the first password should be displayed and it should
    # be updated for the next output
    size = 20
    password_list = ['PROVIDE', 'SETTING', 'CANTINA', 'CUTTING', 'HUNTERS', 'SURVIVE',  'HEARING', 'HUNTING', 'REALIZE', 'NOTHING', 'OVERLAP', 'FINDING', 'PUTTING']
    for password in password_list:
        pass_line = embed_password(password, size)
        display_line(window, pass_line, location)
    
    display_line(window, '', location)
    
    # choose password
    return password_list[7]    
    
#   choose password

def prompt_user(window, prompt, location):
    guess = window.input_string(prompt, location[0], location[1])
    location[1] = location[1] + window.get_font_height() 
    return guess

def check_warning(window, attempts_left):
    if attempts_left == 1:
        # display warning
        warning_string = '*** LOCKOUT WARNING ***'
        warning_x = window.get_width() - window.get_string_width(warning_string)
        warning_y = window.get_height() - window.get_font_height()
        #window.draw_string(warning_string, warning_x, warning_y)
        warning_loc = [warning_x,warning_y]
        display_line(window, warning_string, warning_loc)
    

def display_hint(window, password, guess, location):
    
    display_line(window, guess + ' INCORRECT', location)
    i=0
    rank=0
    for letter in guess:
        if letter == password[i]:
            rank+=1
        i+=1
    display_line(window, str(rank) + '/7 IN MATCHING POSITIONS', location)

def get_guesses(window, password, location, attempts_left):
    hint_x_pos= window.get_width() // 2
    hint_location = [hint_x_pos,0]    
    
    # prompt for guess
    # get guesses
    prompt = 'ENTER PASSWORD >'
    #   prompt for guess
    guess = prompt_user(window, prompt, location)
    
    attempts_left = attempts_left - 1  
    string_height = window.get_font_height()
    
    while guess != password and attempts_left > 0:
        # get next guess
        #   display attempts left
        display_line(window, str(attempts_left), [0,string_height])
        
        
        display_hint(window, password, guess, hint_location)
        #   check warning    
        check_warning(window, attempts_left)
                    
        #   prompt for guess
        guess = prompt_user(window, prompt, location)
        
        attempts_left = attempts_left - 1  
    

    return guess


    
    
    #   display outcome 
    #     compute y coordinate
    
def display_outcome(window, outcome):
    
    #   display outcome 
    #     compute y coordinate
    outcome_height = (len(outcome) + 1)*window.get_font_height()
    y_space = window.get_height() - outcome_height
    line_y = y_space // 2
    
    for outcome_line in outcome:
        # display centered outcome line
        #    compute x coordinate
        x_space = window.get_width() - window.get_string_width(outcome_line)
        line_x = x_space // 2
        
        window.draw_string(outcome_line, line_x, line_y)
        window.update()
        sleep(0.3)
        line_y = line_y + window.get_font_height()
    #prompt_user(window, prompt, [line_x,line_y])
    return [line_x,line_y]



def end_game(window, guess, password):
    window.clear()
    if guess == password:
        # create success
        outcome = [guess, '', 'EXITING DEBUG MODE', '', 'LOGIN SUCCESSFUL - WELCOME BACK', '']
        prompt = 'PRESS ENTER TO CONTINUE'
    else:
        # create failure
        outcome = [guess, '', 'LOGIN FAILURE - TERMINAL LOCKED', '','PLEASE CONTACT AN ADMINISTRATOR', '']
        prompt = 'PRESS ENTER TO EXIT'      
    
    
    locat = display_outcome(window, outcome)
    
    x_space = window.get_width() - window.get_string_width(prompt)
    locat[0] = x_space // 2
    
    prompt_user(window, prompt, locat)
   
#   close window
    #window.close()
        
def main():
    window = create_window()
    location = [0,0]  
    attempts_left = 4  
    
    display_header(window, location, attempts_left)
    password = display_password_list(window, location)
    guess = get_guesses(window, password, location, attempts_left)
    end_game(window, guess, password)
    
    #close window
    window.close()    
        
main()