This script allows you to give as input a .ydk file and build a deck in Yu-Gi-Oh Master Duels automatically since Konami decided not to implement such a basic feature.

Due to several limitations in searching for cards (try and look for One for One and you'll understand) the script makes mistakes, I don't know if I will ever fix this, but it works well enough for now.


# HOW TO USE

In the current iteration the script is meant for users with a basic knowledge of python, it is in very early beta.

### Requirements

- install the requirements.txt using pip, highly suggest creating a virtual environment first
- open Master Duels in 1920x1080, haven't tested in other ratios

### How To

- cd into the folder
- (if you created the virtual environment enable it)
- open the deck editor in the game
- run the script with the command
```
python masterduels_deckbuilder.py -ydk name_ofyour_file.ydk
```
- wait for the process to finish

## HOW TO STOP IT

I haven't really programmed a stop button, but pressing ESC until it opens the prompt to exit deck builder, then by either closing the terminal or pressing CTRL+C. Works good enough since the script looks for specific images that the prompt blocks, don't @ me I made this in one morning.

![example](https://user-images.githubusercontent.com/48190278/187905966-4d67f516-c437-4141-abda-113cb4b2f622.gif)
