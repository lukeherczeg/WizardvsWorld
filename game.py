from tkinter import *
import os
import wsl

wsl.set_display_to_host()
print("Distro:\t", wsl.get_wsl_distro())
print("Host:\t", wsl.get_wsl_host())
print("Display:", os.environ['DISPLAY'])

root = Tk()

w = Label(root, text = "Lets count a stack of n+10!")
w.pack()
print("What number do you want to start from? ", end = '')
start = int(input())
for i in range(start-1, start+9):
    w = Label(root, text = i+1, height = 2, width = 15, font = "helvetica", background = "white")
    w.pack()

w = Label(root, text = "Done!")
w.pack()

root.mainloop()
