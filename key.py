from directkeys import PressKey,ReleaseKey,SPACE,A,W,D,X
from tkinter import Tk, Label, StringVar, OptionMenu
from win32gui import GetWindowText, GetForegroundWindow
import time
import random

tk = Tk()

OptionList = [
"Random",
"A,W,D",
"A,D,W",
"W,A,D",
"W,D,A",
"D,W,A",
"D,A,W"
]

running = True
keys = [A,W,D,SPACE]
keys2 = keys.copy()
rand = A
currentPattern = OptionList[0]

def keySpammer():
    global currentPattern
    isMHWorldOpen = False
    windowsForm()
    counter = 0
    while(running):
        application = checkWindow()
        tkUpdate()
        while('MONSTER HUNTER' in application and running):
            counter += 1
            tkUpdate()
            application = checkWindow()
            if(currentPattern == "Random"):
                randomKeys()
            elif(currentPattern != "Random"):
                patternKeys()
            if(counter > 2):
                PressKey(X)
                time.sleep(0.01)
                ReleaseKey(X)
                counter = 0
                
def randomKeys():
    global keys,keys2,rand
    if(len(keys) > 0):
        rand = random.randrange(0,len(keys))
        PressKey(keys[rand])
        time.sleep(0.01)
        ReleaseKey(keys[rand])
        keys.remove(keys[rand])
    else:
        keys = keys2.copy()
        
def patternKeys():
    global keys,keys2
    if(len(keys) > 0):
        PressKey(keys[0])
        time.sleep(0.01)
        ReleaseKey(keys[0])
        keys.remove(keys[0])
    else:
        keys = keys2.copy()
        
def tkUpdate():
    global tk
    tk.update_idletasks()
    tk.update()
    
def windowsForm():
    global tk, OptionList
    tk.title('自動パチスロ')
    tk.geometry("400x200")
    label = Label(text="MONSTER HUNTERがアクティブになっている時だけキー押す\nアップデートで、hotkeyを設定できるようにするらしい\n終了するなら、アプリケーションを閉じてね", font=('Helvetica', 10), fg='Red')
    label.pack(side="bottom")
    labelTest = Label(text="パターンを選んで", font=('Helvetica', 12), fg='black')
    labelTest.pack(side="top")
    variable = StringVar(tk)
    variable.set(OptionList[0])
    opt = OptionMenu(tk, variable, *OptionList, command=getValue)
    opt.config(width=90, font=('Helvetica', 12))
    opt.pack(side="top")
    
def getValue(selection):
    global currentPattern, keys, keys2
    if(selection != "Random"):
        holder = Convert(selection)
        newKeys =[]
        for x in holder:
            newKeys.append(stringToKeys(x))
        keys = newKeys.copy()
        keys.append(SPACE)
        keys2 = keys.copy()
    elif(selection == "Random"):
        keys = [A,W,D,SPACE]
        keys2 = keys.copy()
    print(keys)
    print(selection)
    currentPattern = selection
    
def stringToKeys(argument): 
    switcher = { 
        'A': A, 
        'W': W, 
        'D': D, 
    } 
    return switcher.get(argument, "nothing")
def Convert(string): 
    li = list(string.split(",")) 
    return li

def on_closing():
    global tk,running
    running = False
    tk.destroy()
    
def checkWindow():
    path = GetWindowText(GetForegroundWindow())
    return path.split('\\')[-1]

tk.protocol("WM_DELETE_WINDOW", on_closing)
keySpammer()