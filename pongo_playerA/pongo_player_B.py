# Pongo by @blogmywiki / Giles Booth
# player B code

import radio
from microbit import *
from music import play, POWER_UP, JUMP_DOWN, NYAN, FUNERAL

a_bat = 2              # starting position of player A bat
b_bat = 2              # starting position of player B bat
bat_map = {0: 4, 1: 3, 2: 2, 3: 1, 4: 0}
ball_x = 2             # starting position of ball
ball_y = 2
a_points = 0
b_points = 0
winning_score = 5
game_over = False
radio.on()     # like the roadrunner

def parse_message():
    global a_bat, incoming, bat_map, ball_x, ball_y, a_points, b_points
    msg_type = incoming[:1]    # find out what kind of message we have received
    msg = incoming[1:]         # strip initial letter from message
    if msg_type == 'p':
        display.set_pixel(a_bat, 0, 0)
        their_bat = int(msg)     # mirror their bat position
        a_bat = bat_map[their_bat]
    if msg_type == 'x':
        display.set_pixel(ball_x, ball_y, 0)
        ball_x = bat_map[int(msg)]
    if msg_type == 'y':
        display.set_pixel(ball_x, ball_y, 0)
        ball_y = bat_map[int(msg)]
    if msg_type == 'a':
        a_points = int(msg)
        play(JUMP_DOWN, wait=False)
    if msg_type == 'b':
        b_points = int(msg)
        play(POWER_UP, wait=False)

while not game_over:
    display.set_pixel(b_bat, 4, 6)
    display.set_pixel(a_bat, 0, 6)
    display.set_pixel(ball_x, ball_y, 9)  # draw ball
    if button_a.was_pressed():
        display.set_pixel(b_bat, 4, 0)
        b_bat = b_bat - 1
        if b_bat < 0:
            b_bat = 0
        radio.send(str(b_bat))
    if button_b.was_pressed():
        display.set_pixel(b_bat, 4, 0)
        b_bat = b_bat + 1
        if b_bat > 4:
            b_bat = 4
        radio.send(str(b_bat))
    incoming = radio.receive()
    if incoming:
        parse_message()
    if a_points == winning_score or b_points == winning_score:
        game_over = True

if a_points < b_points:
    play(NYAN, wait=False)
    display.scroll('B wins!')
else:
    play(FUNERAL, wait=False)
    display.scroll('A wins!')
