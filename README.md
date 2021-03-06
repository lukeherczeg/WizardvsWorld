<img src = "https://cdn.discordapp.com/attachments/347967840655245316/807707133423648778/unknown.png">


#### Inspired by the Fire Emblem series, Wizard vs. World is a 2D tactical roguelike role-playing game built using the PyGame 1.9.6 engine. 

_______________________________________________________________________________________________________________________________________

## See the "WizardVsWorldHowToDownload" file for detailed instructions on how to play!

_______________________________________________________________________________________________________________________________________

## Install directly from PIP
1. You must be using Python 3.7.x (Meaning: 3.7.0 <= your_python_version < 3.8.0)
2. Install the game: `python3.7 -m pip install WizardVsWorld`
    - NOTE: `python3.7` represents whatever Python 3.7 is aliased to on your machine it could also be `py`, `python`, etc.
3. Run the game: `WizardVsWorld`

## If you require a virtual environment 
1. Create a virtual environment for Python3.7: `virtualenv -p="/usr/bin/python3.7" <env_name>`
2. Use the virtual environment: `source <env_name>/bin/activate`
3. Install the WizardVsWorld Package from PIP: `pip install WizardVsWorld`
4. Run the game: `WizardVsWorld`

## Running from Source 
1. Download the source
2. `python3.7 -m pip3 install pygame`
3. `python3.7 -m game.py`

## Requirements
* PyGame 1.9.6

## Installation
Package Name: WizardVsWorld

Executable Command: WizardVsWorld

Initialization Command: WizardVsWorld(?)

Required Python Version: >= Python 3.7.0 && < Python 3.8.0

## Miscellaneous

### Contributors
* Luke Herczeg
* Jacob Hyde
* Gus Segovia
* Logan Smith
* Juan Suhr

### Configuring WSL and PyCharm for PyGame (For Development)
PyGame 1.9.7 (the latest stable version) has some issues working with Python 3.8, so to run the project we need to make sure we set up PyCharm to use 'WSL: Python 3.7' as its interpreter, and use PyCharm to install PyGame 1.9.6, which is compatible with Python 3.7.
These instructions assume that you are using Ubuntu 20.04 (You probably are if you installed a new Ubuntu version for this class)

1. Check if you have Python 3.7 installed on your WSL by running `python3.7 --version`, if it is installed skip to step 3
2. Run the following commands (after list) to add the `deadsnakes` repo (for older versions of python) and install Python 3.7
3. Open the project in Python and go to File > Settings and search "Interpreter" in the search box at the top and navigate to "Python Interpreter"
4. Click on the Gear icon next to the "Python Interpreter" line, then click "Add"
5. Click on the WSL option on the left side
6. Ensure the correct Linux distribution is selected if you have multiple (mine was just called Ubuntu)
7. Set the "Python Interpreter Path" to `/usr/bin/python3.7`, click OK twice to close the menus
8. Click on the Environment Dropdown to the left of the play button at the top of the editor, click "Edit Configurations"
9. Click on the "+" button in the upper left of the pop-up, click on "Python"
10. Name the Configuration whatever you want
11. Set the script path to the absolute path of "game.py"
12. Set the interpreter to "3.7 @ Ubuntu"
13. Click OK and ensure that your new Configuration is selected

```
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt-get update
sudo apt-get install python3.7
```
