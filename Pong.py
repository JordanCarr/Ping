import pygame
import sys
import random

# Pygame setup
pygame.mixer.pre_init(44100, -16, 2, 512)  # resetting the sound buffer
pygame.init()
clock = pygame.time.Clock()

# Game window
screen_width = 1280
screen_height = 960
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Pong")

# Colours
light_grey = (200, 200, 200)
bg_colour = pygame.Color('grey12')
blue = (0, 0, 255)  # powerup color

# Ball split powerup    powerup variables
xcoordinate = random.randint(-250, 250)
ycoordinate = random.randint(-250, 250)
is_hit = False

# Initial States
# Dictionary is accessed like name["key"], these initial state variable allow for latter use of the initial states or
# overwriting them before resetting the game in order to change where the game pieces begin.
ball_initial_position = {"x": round(screen_width / 2) - 15, "y": round(screen_height / 2) - 15}
player_initial_position = {"x": screen_width - 20, "y": round(screen_height / 2) - 70}
opponent_initial_position = {"x": 10, "y": round(screen_height / 2) - 70}

# Game rectangles
ball = pygame.Rect(ball_initial_position["x"], ball_initial_position["y"], 30, 30)
# second ball required for ball split powerup
ball2 = pygame.Rect(round(screen_width / 2) - 15, round(screen_height / 2) - 15, 30, 30)
player = pygame.Rect(player_initial_position["x"], player_initial_position["y"], 10, 140)
opponent = pygame.Rect(opponent_initial_position["x"], opponent_initial_position["y"], 10, 140)
# generates a random position for the powerup to spawn
powerup = pygame.Rect(round(screen_width / 2) - xcoordinate, round(screen_height / 2) - ycoordinate, 50, 50)

# Game state variables
# To add new game modes first create a new Game State variable here. Then go to the Input functions section
in_game = False
one_player = False
two_player = False
one_frenzy = False
two_frenzy = False

# Game variables
ball_speed_x = 7 * random.choice((1, -1))
ball_speed_y = 7 * random.choice((1, -1))
ball2_speed_x = 7 * random.choice((1, -1))
ball2_speed_y = 7 * random.choice((1, -1))
player_one_speed = 0
player_two_speed = 0
ai_speed = 7

# Score text
player_score = 0
opponent_score = 0
basic_font = pygame.font.Font('freesansbold.ttf', 32)

# Sound effects
pong_sound = pygame.mixer.Sound("./media/pong.ogg")
score_sound = pygame.mixer.Sound("./media/score.ogg")


# Reset functions
def ball_reset():
    global ball_speed_x, ball_speed_y

    # move ball to the center
    ball.center = (round(screen_width / 2), round(screen_height / 2))

    # start the ball in a random direction
    ball_speed_y *= random.choice((1, -1))
    ball_speed_x *= random.choice((1, -1))


def ball2_reset():
    global ball2_speed_x, ball2_speed_y

    # move ball to the center
    ball2.center = (round(screen_width / 2), round(screen_height / 2))

    # start the ball in a random direction
    ball2_speed_y *= random.choice((1, -1))
    ball2_speed_x *= random.choice((1, -1))


def players_reset():
    player.x = player_initial_position["x"]
    player.y = player_initial_position["y"]
    opponent.x = opponent_initial_position["x"]
    opponent.y = opponent_initial_position["y"]


def score_reset():
    global player_score, opponent_score

    player_score = 0
    opponent_score = 0


def reset_game_state():
    global in_game, one_player, two_player

    in_game = False
    one_player = False
    two_player = False

    players_reset()
    ball_reset()
    score_reset()


# Ball function
def ball_animation():
    global ball_speed_x, ball_speed_y, player_score, opponent_score, is_hit

    ball.x += ball_speed_x
    ball.y += ball_speed_y

    # Ball collision (top or bottom)
    if ball.top <= 0 or ball.bottom >= screen_height:
        pygame.mixer.Sound.play(pong_sound)
        ball_speed_y *= -1

    # Player scores
    if ball.left <= 0:
        pygame.mixer.Sound.play(score_sound)
        player_score += 1
        ball_reset()

    # Opponent scores
    if ball.right >= screen_width:
        pygame.mixer.Sound.play(score_sound)
        opponent_score += 1
        ball_reset()

    # Ball collision (left or right)
    if ball.left <= 0 or ball.right >= screen_width:
        pygame.mixer.Sound.play(pong_sound)
        ball_reset()

    # Ball collision (player or opponent)
    if ball.colliderect(player) or ball.colliderect(opponent):
        ball_speed_x *= -1

    # ball collions (ball split powerup)
    if is_hit == False:  # stops balls from hitting invisible powerup
        if ball.colliderect(powerup):
            ball_speed_x *= -1
            ball_speed_y *= -1
            is_hit = True
            pygame.mixer.Sound.play(score_sound)  # plays sound when powerup is hit
    # End ball function


def ball2_animation():
    global ball2_speed_x, ball2_speed_y, player_score, opponent_score

    ball2.x += ball2_speed_x
    ball2.y += ball2_speed_y

    # Ball collision (top or bottom)
    if ball2.top <= 0 or ball2.bottom >= screen_height:
        pygame.mixer.Sound.play(pong_sound)
        ball2_speed_y *= -1

    # Player scores
    if ball2.left <= 0:
        pygame.mixer.Sound.play(score_sound)
        player_score += 1
        ball2_reset()

    # Opponent scores
    if ball2.right >= screen_width:
        pygame.mixer.Sound.play(score_sound)
        opponent_score += 1
        ball2_reset()

    # Ball collision (left or right)
    if ball2.left <= 0 or ball2.right >= screen_width:
        pygame.mixer.Sound.play(pong_sound)
        ball2_reset()

    # Ball collision (player or opponent)
    if ball2.colliderect(player) or ball2.colliderect(opponent):
        ball2_speed_x *= -1

    # Ball collision with other ball
    if ball2.colliderect(ball):
        ball2_speed_x *= -1
        ball2_speed_y *= -1
        pygame.mixer.Sound.play(pong_sound)


# Player and opponent functions
def player_one_animation():
    player.y += player_one_speed

    if player.top <= 0:
        player.top = 0
    if player.bottom >= screen_height:
        player.bottom = screen_height


def player_two_animation():
    opponent.y += player_two_speed

    if opponent.top <= 0:
        opponent.top = 0
    if opponent.bottom >= screen_height:
        opponent.bottom = screen_height


def ai_animation():
    if opponent.top < ball.y:
        opponent.y += ai_speed
    if opponent.bottom > ball.y:
        opponent.y -= ai_speed

    if opponent.top <= 0:
        opponent.top = 0
    if opponent.bottom >= screen_height:
        opponent.bottom = screen_height
# End player and opponent functions


# Drawing to screen functions
def draw_background(bg):
    screen.fill(bg)


def draw_menu():
    draw_background(bg_colour)
    screen.blit(basic_font.render("PONG", False, light_grey), (600, 200))
    screen.blit(basic_font.render("1 Player", False, light_grey), (300, 400))
    screen.blit(basic_font.render("[1]", False, light_grey), (350, 450))
    screen.blit(basic_font.render("2 Player", False, light_grey), (800, 400))
    screen.blit(basic_font.render("[2]", False, light_grey), (850, 450))
    screen.blit(basic_font.render("1 Player Frenzy Mode", False, light_grey), (190, 650))
    screen.blit(basic_font.render("[3]", False, light_grey), (350, 700))
    screen.blit(basic_font.render("2 Player Frenzy Mode", False, light_grey), (700, 650))
    screen.blit(basic_font.render("[4]", False, light_grey), (850, 700))
    screen.blit(basic_font.render("[ESC] to Return to Menu", False, light_grey), (450, 800))


def draw_standard_opponent():
    pygame.draw.rect(screen, light_grey, opponent)


def draw_standard_player():
    pygame.draw.rect(screen, light_grey, player)


def draw_standard_ball():
    pygame.draw.ellipse(screen, light_grey, ball)


def draw_center_line():
    pygame.draw.aaline(screen, light_grey, (screen_width / 2, 0), (screen_width / 2, screen_height))


def draw_standard_score_text():
    player_text = basic_font.render(f'{player_score}', False, light_grey)
    screen.blit(player_text, (660, 470))

    opponent_text = basic_font.render(f'{opponent_score}', False, light_grey)
    screen.blit(opponent_text, (600, 470))


def draw_standard_play_area():
    draw_background(bg_colour)
    draw_standard_player()
    draw_standard_opponent()
    draw_standard_ball()
    draw_center_line()


# End drawing to screen functions

# Powerup Functions
def draw_powerup():
    pygame.draw.ellipse(screen, blue, powerup)


# Splits ball in two when powerup is hit
def split_ball():
    pygame.draw.ellipse(screen, light_grey, ball2)
    ball2_animation()


# Input functions
# When creating a new game mode and after creating the game state variable add it to the global list here. Once that is
# done choose a key that will select the game mode from the menu. Create an if statement for that key and within it set
# the in_game variable to True and the new mode's variable to True. From here go to the process_inputs functions.
def process_menu_inputs(pressed):
    global in_game, one_player, two_player, one_frenzy, two_frenzy

    # For the main menu it doesn't matter if the mode select key is pressed or released so only check for which key
    if pressed.key == pygame.K_1:
        in_game = True
        one_player = True
    elif pressed.key == pygame.K_2:
        in_game = True
        two_player = True
    elif pressed.key == pygame.K_3:
        in_game = True
        one_frenzy = True
    elif pressed.key == pygame.K_4:
        in_game = True
        two_frenzy = True


def process_one_player_inputs(pressed):
    global player_one_speed

    # For player one it matters whether the key is down or released so check that first and then which key it is
    if pressed.type == pygame.KEYDOWN:
        if pressed.key == pygame.K_UP:
            player_one_speed -= 6
        elif pressed.key == pygame.K_DOWN:
            player_one_speed += 6
    else:
        if pressed.key == pygame.K_UP:
            player_one_speed += 6
        elif pressed.key == pygame.K_DOWN:
            player_one_speed -= 6


def process_two_player_inputs(pressed):
    global player_two_speed

    # For the standard two player mode the first player's behaviour is unchanged so just call that function
    process_one_player_inputs(pressed)

    # To handle the second player check the key press type for down or release and then which key
    if pressed.type == pygame.KEYDOWN:
        if pressed.key == pygame.K_w:
            player_two_speed -= 6
        elif pressed.key == pygame.K_s:
            player_two_speed += 6
    else:
        if pressed.key == pygame.K_w:
            player_two_speed += 6
        elif pressed.key == pygame.K_s:
            player_two_speed -= 6


# When creating a new game mode and after adding the mode select to the menu; create an input processing function for
# the mode. Add this function to the in_game part of the 'for pressed ...' loop below on the condition of the mode's
# game state variable being True. From here go to the Game loop section.
def process_inputs():
    global in_game, one_player, two_player, one_frenzy, two_frenzy, is_hit
    events = pygame.event.get()

    # This if statement filters through all the event for any that match a quit event. It checks to see if there is
    # anything in that filter result and if there is it quits and exits the game.
    if any(filter(quit_events, events)):
        pygame.quit()
        sys.exit()

    # This for loop filters only events that match a keypress and then passes those keys to their respective input
    # processing function. Inside the input processing function you will only have events that are key presses so
    # there is no need to check the type again unless you need to perform a different action on a down press or release
    for pressed in filter(keypress_events, events):
        if in_game:
            if pressed.key == pygame.K_ESCAPE:
                is_hit = False
                reset_game_state()
            elif one_player or one_frenzy:
                process_one_player_inputs(pressed)
            elif two_player or two_frenzy:
                process_two_player_inputs(pressed)
        else:
            process_menu_inputs(pressed)
# End input functions


# Filter input functions
# Takes a pygame event as an input and returns whether the type pygame.QUIT is True or False
def quit_events(event):
    return event.type == pygame.QUIT


# Takes a pygame event as an input and returns True if it is either a keydown or keyup event, otherwise it returns False
def keypress_events(event):
    return event.type == pygame.KEYDOWN or event.type == pygame.KEYUP
# End filter input functions


# Render screen function
def render_screen():
    pygame.display.flip()
    clock.tick(60)  # redraws the screen every 16.6...ms
# End render screen function


# Game loops
# When creating a new game mode and after adding the input processing function of that game mode create a new while loop
# below for when in_game and you mode's game state variable are True. Within this loop you start with the
# process_inputs function and end with the render_screen() function. Between these two functions add whichever
# animation, game logic, visual, text, or other functions required to run the game mode. From here go to the Invalid
# game state detection and error code below.
if __name__ == "__main__":
    while True:
        # Menu loop
        while not in_game:
            # Inputs
            process_inputs()
            # Visuals
            draw_menu()
            # Final screen render
            render_screen()

        # One player loop
        while in_game and one_player:
            # Inputs
            process_inputs()
            # Animations
            ball_animation()
            player_one_animation()
            ai_animation()
            # Visuals
            draw_standard_play_area()
            # Text
            draw_standard_score_text()
            # Final screen render
            render_screen()

        # Two player loop
        while in_game and two_player:
            # Inputs
            process_inputs()
            # Animations
            ball_animation()
            player_one_animation()
            player_two_animation()
            # Visuals
            draw_standard_play_area()
            # Text
            draw_standard_score_text()
            # Final screen render
            render_screen()

        # One player frenzy mode loop
        while in_game and one_frenzy:
            # Inputs
            process_inputs()
            # Animations
            ball_animation()
            player_one_animation()
            ai_animation()
            # Visuals
            draw_standard_play_area()
            # Text
            draw_standard_score_text()
            # checks if powerup is hit
            if is_hit == False:
                draw_powerup()
            else:
                split_ball()
            # Final screen render
            render_screen()

        # Two player frenzy mode loop
        while in_game and two_frenzy:
            # Inputs
            process_inputs()
            # Animations
            ball_animation()
            player_one_animation()
            player_two_animation()
            # Visuals
            draw_standard_play_area()
            # Text
            draw_standard_score_text()
            # checks if powerup is hit
            if is_hit == False:
                draw_powerup()
            else:
                split_ball()
            # Final screen render
            render_screen()

        # Invalid game state detection and error message
        # when creating a new game mode and after adding the new game loop add the mode's name and state to this code
        # both in the if statement and in the string. This allows the game to exit if an error occurs and describe what
        # that state was for easier debugging.
        if in_game and (not one_player or not two_player or not one_frenzy):
            print(f'Pong entered an invalid state where it was in game while '
                  f'1 player mode was {one_player} and '
                  f'2 player mode was {two_player}'
                  f'2 player frenzy mode was {one_frenzy}')
            pygame.quit()
            sys.exit(1)
