from Tkinter import Label, END, Text, INSERT, DISABLED, NORMAL

def enterChat(textObj, text):
    textObj.insert(INSERT, text + "\n")
    
def enterChatVar(textObj, var):
    textObj.config(state=NORMAL)
    enterChat(textObj, var.get())
    var.set("")
    textObj.config(state=DISABLED)