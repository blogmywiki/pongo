# pongo
Wireless Pong for 2 BBC micro:bits

![alt text](http://www.suppertime.co.uk/blogmywiki/wp-content/uploads/2016/12/DSCF85883.jpg)

## Introduction
I love the wireless capabilities of Python on the BBC microbit and [I’ve been using it with some success in my Year 8 classes.](http://www.suppertime.co.uk/blogmywiki/2016/11/microbit-radio/)

I thought I’d have a go at writing a wireless Pong game in Python – it took me a lot longer than I expected for various reasons. I really wanted to have the same code running on both microbits, but I soon abandoned that as too complex. Much easier to have one microbit – Player A – controlling the game and deciding who gets a point and when. Player B is the ‘slave’ only sending its left and right paddle moves back to Player A and mirroring (literally) Player A’s screen.

I was keen to have each screen the same – rather than extending a long screen like a wired version I’ve seen. This is because I want each player to be able to be quite far apart, so seeing the other player’s screen isn’t necessary.

## How to play

Flash Player A code on to one Microbit using the Mu editor, and Player B on to a separate microbit. You can optionally connect a headphone or buzzer to pins 0 and 1 on each microbit for some audio feedback joy.

Power up Player B first – it will wait for messages from Player A. Then power up Player A. The game starts straight away with the ball – the bright dot in the middle of the screen – moving in a random direction. Move your paddle left and right using A and B buttons. If you fail to hit the ball when it reaches your end the other player gets a point (points tallies are not shown on the screen) and the first player to 5 points wins. To play again you both need to press the reset button on the back of the microbits.

## How it works

Player B is the easy one to explain. It runs a loop constantly polling for messages and keypresses. If you press button A to move left, or B to move right, it sends a message with your bat’s new position. It also listens for different kinds of messages from player A’s microbit. They all start with different code letters:
*p + a number is the position of player A’s bat.
*x and y messages give the current location of the ball, which is then inverted using a dictionary look-up table called `bat_map`.
*a and b messages give the respective scores or player A and B.

If a player reaches the winning score (5) it breaks out of the loop and plays a happy song (Nyan cat) if player B has won and a sad song (funeral march) is player A has won.

Player A is the master controller. It picks a random direction for the ball to start moving and bounces the ball if it hits any of the sides. If it hits the top or bottom and a player’s bat isn’t in the way, the other player gets a point. It has a crude timer using variables counter and delay – every time it reaches 1000 it moves the ball (I couldn’t work out how to get proper timers to work in micro:bit Python – if indeed this is possible). If a player hits the ball with their bat it speeds up a bit.

It sends messages (as described above) to Player B with the ball position, score and player A bat position. The game ends in the same way as player B’s code described above, except you get the happy tune if player A wins and the sad one if player B wins.

## How to mod

You can make the game faster by making the value of delay smaller. You can also make it last longer by increasing the value of `winning_score` in both sets of code.

A nice extension would be to add more sound (when you hit the ball for example) and to add levels with the game getting faster each time someone wins a game.

Let me know how you get on with it and if you have any other ideas for improvements – the physics of the ball bouncing is one area that I could do with help on!
