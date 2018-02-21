
from textureFlattening.helpers import dotWait
from textureFlattening.textureFlattening import textureFlattening
from morphing.try_morph import autoMorphing


print("Welcome to Magic Cam World, hope you have a great journey here")
dotWait()
print("Enter Young Cam, please type in 1")
print("Enter I-Wanna-Marry-U Cam, please type in 2\n===========================================\n")

numCam = input("I want to enter\n")
while numCam != '1' and numCam != '2':
    numCam = input("Please input 1 or 2, I want to enter\n")

if numCam == '1':
    mode = input("if you want see a demo, please press 1,\n Else please press 2 and "
                 "look at the webcam of your laptop\n")
    while mode != '1' and mode != '2':
        mode = input("Please input 1 or 2, I want to enter mode #")
    textureFlattening(mode)
elif numCam == '2':
    autoMorphing()