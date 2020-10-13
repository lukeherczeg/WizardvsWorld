# WizardvsWorld
A 2D, tactical role-playing game where you play as a single wizard fighting an army of endless soldiers.

## Configuring WSL and PyCharm for PyGame
PyGame 1.9.7 (the latest stable version) has some issues working with Python 3.8, so to run the project we need to make sure we set up PyCharm to use 'WSL: Python 3.7' as its iterpreter, and use PyCharm to install PyGame 1.9.6, which is compatible with Python 3.7.
These instructions assume that you are using Ubuntu 20.04 (You probably are if you installed a new Ubuntu version for this class)

1. Check if you have Python 3.7 installed on your WSL by running `python3.7 --version`, if it is installed skip to step 3
2. Run the following commands to add the `deadsnakes` repo (for older versions of python) and install Python 3.7:
```
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt-get update
sudo apt-get install python3.7
```
3. Open the project in Python and go to File > Settings and search "Interpreter" in the search box at the top and navigate to "Python Interpreter"
4. Click on the Gear icon next to the "Python Interpreter" line, then click "Add"
5. Click on the WSL option on the left side
7. Ensure the correct Linux distribution is selected if you have multiple (mine was just called Ubuntu)
7. Set the "Python Interpreter Path" to `/usr/bin/python3.7`, click OK twice to close the menus
8. Click on the Environment Dropdown to the left of the play button at the top of the editor, click "Edit Configurations"
9. Click on the "+" button in the upper left of the pop-up, click on "Python"
10. Name the Configuration whatever you want
11. Set the script path to the absolute path of "game.py"
12. Set the interpreter to "3.7 @ Ubuntu"
13. Click OK and ensure that your new Configuration is selected
