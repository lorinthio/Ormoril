from Tkinter import Label, END, Text, INSERT

def enterChat(textObj, text):
    textObj.insert(INSERT, text + "\n")
    
def enterChatVar(textObj, var):
    enterChat(textObj, var.get())
    var.set("")