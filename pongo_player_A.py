# Pongo by @blogmywiki / Giles Booth
# player A code - main game controller

import radio
import random
from microbit import *
from music import play, POWER_UP, JUMP_DOWN, NYAN, FUNERAL

a_bat = 2              # starting position of player A bat
b_bat = 2              # starting position of player B bat
bat_map = {0: 4, 1: 3, 2: 2, 3: 1, 4: 0}
ball_x = 2             # starting position of ball
ball_y = 2
directions = [1, -1]   # pick a random direction for ball at start
x_direction = random.choice(directions)
y_direction = random.choice(directions)
delay = 1000           # used as a crude timer
counter = 0            # used as a crude timer
a_points = 0
b_points = 0
winning_score = 5
game_over = False

def move_ball():
    global ball_x, ball_y, x_direction, y_direction, counter, a_bat, b_bat, a_points, b_points, delay
    display.set_pixel(ball_x, ball_y, 0)
    ball_x = ball_x + x_direction
    ball_y = ball_y + y_direction
    if ball_x < 0:							# bounce if hit left wall
        ball_x = 0
        x_direction = 1
    if ball_x > 4:							# bounce if hit right wall
        ball_x = 4
        x_direction = -1
    if ball_y == 0:
        if ball_x == b_bat:					# bounce if player B hit ball
            ball_y = 0
            y_direction = 1
            delay -= 50						# speed up after bat hits
        else:
            play(POWER_UP, wait=False)      # A gets point if B missed ball
            a_points += 1
            ball_y = 0
            y_direction = 1
            radio.send('a'+str(a_points))			# transmit points

    if ball_y == 4:							# bounce if player A hits ball
        if ball_x == a_bat:
            ball_y = 4
            y_direction = -1
            delay -= 50						# speed up after bat hits
        else:
            play(JUMP_DOWN, wait=False)     # player B gets point if A misses
            b_points += 1
            ball_y = 4
            y_direction = -1
            radio.send('b'+str(b_points))
    counter = 0
    radio.send('x'+str(ball_x))				# transmit ball position
    radio.send('y'+str(ball_y))

radio.on()    # like the roadrunner

while not game_over:
    counter += 1
    display.set_pixel(a_bat, 4, 6)        # draw bats
    display.set_pixel(b_bat, 0, 6)
    display.set_pixel(ball_x, ball_y, 9)  # draw ball
    if button_a.was_pressed():
        display.set_pixel(a_bat, 4, 0)
        a_bat = a_bat - 1
        if a_bat < 0:
            a_bat = 0
        radio.send('p'+str(a_bat))
    if button_b.was_pressed():
        display.set_pixel(a_bat, 4, 0)
        a_bat = a_bat + 1
        if a_bat > 4:
            a_bat = 4
        radio.send('p'+str(a_bat))
    incoming = radio.receive()
    if incoming:
        display.set_pixel(b_bat, 0, 0)
        b_bat = bat_map[int(incoming)]
    if counter == delay:
        move_ball()
    if a_points == winning_score or b_points == winning_score:
        game_over = True

if a_points > b_points:
    play(NYAN, wait=False)
    display.scroll('A wins!')
else:
    play(FUNERAL, wait=False)
    display.scroll('B wins!')

display.scroll('Press reset to play again')
