
import socket
from tkinter import *
from  threading import Thread
from PIL import ImageTk, Image

screen_width = None
screen_height = None

SERVER = None
PORT = None
IP_ADDRESS = None
playerName = None

canvas1 = None
canvas2 = None

playerName = None
nameEntry = None
nameWindow = None

leftBoxes = []
rightBoxes = []
finishingBox = None

playerType = None
playerTurn = None
player1Name = 'joining'
player2Name = 'joining'
player1Label = None
player2Label = None

player1Score = 0
player2Score = 0
player2ScoreLabel = None
player2ScoreLabel = None

dice = None

rollButton = None
resetButton = None

winingMessage = None

winingFunctionCall = 0


def saveName():
    global SERVER
    global playerName
    global nameWindow
    global nameEntry
    
    playerName=nameEntry.get()
    nameEntry.delete(0,END)
    nameWindow.destroy()
    SERVER.send(playerName.encode())



def askPlayerName():
    global playerName
    global nameEntry
    global nameWindow
    global canvas1
    global screen_width
    global screen_height

    nameWindow=Tk()
    nameWindow.title("ludo ladder")
    nameWindow.attributes('-fullscreen',True)
    screen_width=nameWindow.winfo_screenwidth()
    screen_height=nameWindow.winfo_screenheight()
    
    bg=ImageTk.PhotoImage(file="./assets/background.png")

    canvas1=Canvas(nameWindow,width=500,height=500)
    canvas1.pack(fill="both", expand=True)

    canvas1.create_image(0,0,image=bg,anchor="nw")
    canvas1.create_text(screen_width/2, screen_height/5, text="Enter name", font=("Chalkboard SE", 100), fill="white")

    nameEntry=Entry(nameWindow, width=15, justify="center", bd=5, bg="white", font=("Chalkboard SE", 50))
    nameEntry.place(x=screen_width/2-220, y=screen_height/4+100)
    button=Button(nameWindow,text="Save", width=15, height=2, bd=3, bg="blue", font=("Chalkboard SE", 30), command=saveName)
    button.place(x=screen_width/2-130, y=screen_height/2-30)

    nameWindow.resizable(True,True)


    nameWindow.mainloop()

def movePlayer1(steps):
    global leftBoxes
    boxPosition=checkColorPosition(leftBoxes[1:],"purple")
    if(boxPosition):
        diceValue=steps
        coloredBoxIndex=boxPosition
        totalSteps=10
        remainingSteps=totalSteps-coloredBoxIndex

        if(steps==remainingSteps):
            for box in leftBoxes[1:]:
                box.configure(bg="white")
            global finishingBox
            finishingBox.configure(bg="blue")
            global SERVER
            global playerName
            greetMessage=f'Purple Wins the Game'
            SERVER.send(greetMessage.encode())

        elif(steps<remainingSteps):
            for box in leftBoard[1:]:
                box.configure(bg="white")
                nextStep=(coloredBoxIndex+1).diceValue
                leftBoxes[nextStep].configure(bg="purple")
        else:
            print("Move False")
    else:
        leftBoxes[steps].configure(bg="purple")


def movePlayer2(steps):
    global rightBoxes
    temptBoxes=rightBoxes[-2::-1]
    boxPosition=checkColorPosition(temptBoxes[1:],"blue")
    if(boxPosition):
        diceValue=steps
        coloredBoxIndex=boxPosition
        totalSteps=10
        remainingSteps=totalSteps-coloredBoxIndex

        if(diceValue==remainingSteps):
            for box in rightBoxes[-2::-1]:
                box.configure(bg="white")
            global finishingBox
            finishingBox.configure(bg="blue")
            global SERVER
            global playerName
            greetMessage=f'Blue Wins the Game'
            SERVER.send(greetMessage.encode())

        elif(diceValue<remainingSteps):
            for box in rightBoard[-2::-1]:
                box.configure(bg="white")
                nextStep=(coloredBoxIndex+1)+diceValue
                rightBoxes[::-1][nextStep].configure(bg="blue")
        else:
            print("Move False")
    else:
        rightBoxes[len(rightBoxes)-(steps+1)].configure(bg="blue")


def rollDice():
    global SERVER
    #create a number variable in which the list of all the ASCII characters of the string will be stored
    #Use backslash because unicode must have a backslash
    diceChoices=['\u2680','\u2681','\u2682','\u2683','\u2684','\u2685']

    #configure the label
    value = random.choice(diceChoices)

    global playerType
    global rollButton
    global playerTurn

    rollButton.destroy()
    playerTurn = False

    if(playerType == 'player1'):
        SERVER.send(f'{value}player2Turn'.encode())

    if(playerType == 'player2'):
        SERVER.send(f'{value}player1Turn'.encode())





def leftBoard():
    global gameWindow
    global leftBoxes
    global screen_height

    xPos = 30
    for box in range(0,11):
        if(box == 0):
            boxLabel = Label(gameWindow, font=("Helvetica",30), width=2, height=1, relief='ridge', borderwidth=0, bg="red")
            boxLabel.place(x=xPos, y=screen_height/2 - 88)
            leftBoxes.append(boxLabel)
            xPos +=50
        else:
            boxLabel = Label(gameWindow, font=("Helvetica",55), width=2, height=1, relief='ridge', borderwidth=0, bg="white")
            boxLabel.place(x=xPos, y=screen_height/2- 100)
            leftBoxes.append(boxLabel)
            xPos +=75


def rightBoard():
    global gameWindow
    global rightBoxes
    global screen_height

    xPos = 988
    for box in range(0,11):
        if(box == 10):
            boxLabel = Label(gameWindow, font=("Helvetica",30), width=2, height=1, relief='ridge', borderwidth=0, bg="yellow")
            boxLabel.place(x=xPos, y=screen_height/2-88)
            rightBoxes.append(boxLabel)
            xPos +=50
        else:
            boxLabel = Label(gameWindow, font=("Helvetica",55), width=2, height=1, relief='ridge', borderwidth=0, bg="white")
            boxLabel.place(x=xPos, y=screen_height/2 - 100)
            rightBoxes.append(boxLabel)
            xPos +=75


def finishingBox():
    global gameWindow
    global finishingBox
    global screen_width
    global screen_height

    finishingBox = Label(gameWindow, text="Home", font=("Chalkboard SE", 32), width=8, height=4, borderwidth=0, bg="green", fg="white")
    finishingBox.place(x=screen_width/2 - 68, y=screen_height/2 -160)



def gameWindow():
    global gameWindow
    global canvas2
    global screen_width
    global screen_height
    global dice
    global winingMessage
    global resetButton


    gameWindow = Tk()
    gameWindow.title("Ludo Ladder")
    gameWindow.attributes('-fullscreen',True)

    screen_width = gameWindow.winfo_screenwidth()
    screen_height = gameWindow.winfo_screenheight()

    bg = ImageTk.PhotoImage(file = "./assets/background.png")

    canvas2 = Canvas( gameWindow, width = 500,height = 500)
    canvas2.pack(fill = "both", expand = True)

    # Display image
    canvas2.create_image( 0, 0, image = bg, anchor = "nw")

    # Add Text
    canvas2.create_text( screen_width/2, screen_height/5, text = "Ludo Ladder", font=("Chalkboard SE",100), fill="white")

  

    # Declaring Wining Message
    winingMessage = canvas2.create_text(screen_width/2 + 10, screen_height/2 + 250, text = "", font=("Chalkboard SE",100), fill='#fff176')

    # Creating Reset Button
    resetButton =  Button(gameWindow,text="Reset Game", fg='black', font=("Chalkboard SE", 15), bg="grey",command=restGame, width=20, height=5)


    leftBoard()
    rightBoard()
    finishingBox()

    global rollButton

    rollButton = Button(gameWindow,text="Roll Dice", fg='black', font=("Chalkboard SE", 15), bg="grey",command=rollDice, width=20, height=5)

    global playerTurn
    global playerType
    global playerName
   
    global player1Name
    global player2Name
    global player1Label
    global player2Label
    global player1Score
    global player2Score
    global player1ScoreLabel
    global player2ScoreLabel



    if(playerType == 'player1' and playerTurn):
        rollButton.place(x=screen_width / 2 - 80, y=screen_height/2  + 250)
    else:
        rollButton.pack_forget()

    dice = canvas2.create_text(screen_width/2 + 10, screen_height/2 + 100, text = "\u2680", font=("Chalkboard SE",250), fill="white")

    player1Label = canvas2.create_text(400,  screen_height/2 + 100, text = player1Name, font=("Chalkboard SE",80), fill='#fff176' )
    player2Label = canvas2.create_text(screen_width - 300, screen_height/2 + 100, text = player2Name, font=("Chalkboard SE",80), fill='#fff176' )

    player1ScoreLabel = canvas2.create_text(400,  screen_height/2 - 160, text = player1Score, font=("Chalkboard SE",80), fill='#fff176' )
    player2ScoreLabel = canvas2.create_text(screen_width - 300, screen_height/2 - 160, text = player2Score, font=("Chalkboard SE",80), fill='#fff176' )


    gameWindow.resizable(True, True)
    gameWindow.mainloop()


def setup():
    global SERVER
    global PORT
    global IP_ADDRESS

    PORT  = 5000
    IP_ADDRESS = '127.0.0.1'

    SERVER = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    SERVER.connect((IP_ADDRESS, PORT))

    askPlayerName()




setup()
