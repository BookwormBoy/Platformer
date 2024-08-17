
# Platformer

My submission for the Zense recruitment drive for the GameDev section. I've played Mario since I was a child and I've always loved platformer style games and that is the type of game I wanted to create for this project!

## Project Goals

My goal was to create a fun and challenging platformer inspired by Mario, and some of the levels people have made themselves in MarioMaker. I wanted it to be fast-paced and exciting. 

I have already made two games in the past, also using pygame, so this time I wanted to push myself further and implement things I wasn't capable of earlier. This includes things like the throwable-shell in the game and the horizontal and vertical moving platforms. I also wanted to create a multi-level game which I hadn't done before.
## Methodology

I used pygame to develop this platformer. I do not like 3D games games so I did not need to learn Unity and I was comfortable with pygame so I decided to go ahead with it.

I used Tiled to design the levels. Tiled generates a csv file which I can then use to place elements on the screen. 

Most of the art and music is from itch.io.

I used OOP to make my life simpler, a lot of obstacles with redundant functions were grouped into one class that they inherited from and then they possessed unique features of their own. 
## Challenges Faced

One of the challenges was figuring out that pygame uses ints to position rects. I kept getting inaccurate and glitchy movement for my sprites until I realized this. When positions got negative, it rounded them up and gave wrong positions. To fix this, I stored positions in a 2D vector and and then manually converted to int for figuring out the rect position.

The next challenge was elements was the camera. The camera for my previous game was quite basic. It kept the player in a box and moved the background if the player went outside the box. But I realized this meant much of what was coming up wasn't visible to the player. I went back and played New Super Mario Bros. and figured how they modelled the camera. Depending on which way the player is facing, the camera moves so that most of the level is in front of the player. I made my camera in a similar way.

Managing the art was quite a headache too. Some tilesets were 16bit others were 32 bit and some others in rather random resolutions. Cropping, resizing, splitting images to make them look good together took quite a long time.


## How to Play

Clone the github repository. Navigate to the repo and open it in the terminal. Type in: python3 main.py to run the game. You must have pygame installed.

Controls:

Left and Rigtht Arrow to move

D to jump

S to run

L_SHIFT to hold/regrab a shell. Let go of L_SHIFT to throw a shell. If you let go while pressing UP_ARROW you will throw the shell upwards.

SPACE to attack. The player will attack thrice once you press space. To cancel attaking in the middle press the arrow opposite to the direction you are facing.

While landing on shells and bullets, if you are holding the jump button you will jump higher.

While next to a wall if you press the arrow in the direction of the wall, you will slide. While sliding, press jump to perform a wall jump.

In the overworld press UP_ARROW to start a level.

## Future Scope

Add even more obstacles and levels

Initially I wanted to add a swinging/grappling hook mechanism but it proved too difficult in the time I had. I would love to implement this in the future.

More bosses. Perhaps one for each level.

Better combat system with more powerful attacks if you get certain combos/streaks.

Demo Link: https://youtu.be/EoG76wMe1T0
