from Tkinter import Toplevel

def setupGrid(frame, width, height):
    frame.grid()  
    for x in range(width):
        frame.columnconfigure(x, weight=1) 
    for y in range(height):
        frame.rowconfigure(y, weight=1)  
        
def centerWindow(window, width, height):
    window.minsize(width, height)
    window.maxsize(width, height)

    ws = window.winfo_screenwidth()
    hs = window.winfo_screenheight()
    x = (ws/2) - (width/2)
    y = (hs/2) - (height/2)        

    window.geometry("{}x{}+{}+{}".format(width, height, x, y))  
    
def makeNotification(title):
    top = Toplevel()
    top.title(title)
    
    w = 300
    h = 60
    
    centerWindow(top, w, h)
    
    return top 