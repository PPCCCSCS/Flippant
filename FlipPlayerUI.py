"""
File: FlipPlayerUI.py
00: Build the game window for one Flippant/Fate player
00.1: Flip dice images to greyed-out versions when disabled
01: Write server/networking code for multiple players/bots
"""

from tkinter import *
from tkinter import ttk
import random
from socket import *
from codecs import decode

class PlayerWindow:

    def __init__(self,
                 d1 =   "d4",
                 d2 =   "d6",
                 d3 =   "d8",
                 d4 =   "d10",
                 d5 =   "d100",
                 d6 =   "d12",
                 d7 =   "d20",
                 name = "Hans Olo",
                 mode = "count"):

        # tkinter-required variables defined here
        self._top = Tk()
        self._top.title("Flippant Dice Game")
        #self._top.geometry("600x600") # <-- Figure out optimal dimensions for this later
        #self._top.minsize(600,600)
        #self._top.maxsize(600,600)

        self._mainFrame = Frame(self._top)
        self._mainFrame.grid(row=1,column=0)

        # Load Images
        self.imgD4      = PhotoImage(file="images\\d4.gif")
        self.imgD6      = PhotoImage(file="images\\d6.gif")
        self.imgD8      = PhotoImage(file="images\\d8.gif")
        self.imgD10     = PhotoImage(file="images\\d10.gif")
        self.imgD100    = PhotoImage(file="images\\d100.gif")
        self.imgD12     = PhotoImage(file="images\\d12.gif")
        self.imgD20     = PhotoImage(file="images\\d20.gif")
        self.imgD4g     = PhotoImage(file="images\\d4g.gif")
        self.imgD6g     = PhotoImage(file="images\\d6g.gif")
        self.imgD8g     = PhotoImage(file="images\\d8g.gif")
        self.imgD10g    = PhotoImage(file="images\\d10g.gif")
        self.imgD100g   = PhotoImage(file="images\\d100g.gif")
        self.imgD12g    = PhotoImage(file="images\\d12g.gif")
        self.imgD20g    = PhotoImage(file="images\\d20g.gif")

        # These switches allow images and labels to be loaded when the window is first built
        # and whenever they are changed by class methods
        self.dieSwitch = {"d4":4,"d6":6,"d8":8,"d10":10,"d100":10,"d12":12,"d20":20}
        self.imgSwitch = {"d4":self.imgD4,"d6":self.imgD6,"d8":self.imgD8,"d10":self.imgD10,"d100":self.imgD100,"d12":self.imgD12,"d20":self.imgD20}
        self.grySwitch = {"d4":self.imgD4g,"d6":self.imgD6g,"d8":self.imgD8g,"d10":self.imgD10g,"d100":self.imgD100g,"d12":self.imgD12g,"d20":self.imgD20g}

        # Game-specific variables start here
        self.name           = name
        self.mode           = mode
        self.round          = 1 # Games always start with Round 1
        self.score          = 0 # Everybody starts somewhere
        self.inRecover      = False # Toggle to change self.select() behavior for die recovery

        # Layout the main screen now

        ## Row 0

        self.lblPlayer = Label(self._mainFrame, text="Player: "+self.name+" ", justify="left",font="Verdana 16 bold")
        self.lblPlayer.grid(row=0,column=0,columnspan=7,sticky="NSEW")

        ## ROW 1
        
        self.lblRound = Label(self._mainFrame, text="Round:", justify="right",width=7,font="Verdana 16 bold")
        self.lblRound.grid(row=1,column=0,sticky="NSE")
        self.ntrRound = Label(self._mainFrame,text="  "+str(self.round),justify="left",font="Verdana 16")
        self.ntrRound.grid(row=1,column=1,sticky="NSW")
        
        self.lblMode = Label(self._mainFrame, text="Mode:", justify="right",width=7,font="Verdana 16 bold")
        self.lblMode.grid(row=1,column=2,sticky="NSE")
        self.ntrMode = Label(self._mainFrame,text="  "+self.mode,justify="left",font="Verdana 16")
        self.ntrMode.grid(row=1,column=3,sticky="NSW")

        self.lblScore = Label(self._mainFrame, text="Score:", justify="right", width=7,font="Verdana 16 bold")
        self.lblScore.grid(row=1,column=4,sticky="NSE")
        self.ntrScore = Label(self._mainFrame,text="  "+str(self.score),justify="left",font="Verdana 16")
        self.ntrScore.grid(row=1,column=5,sticky="NSW")

        ## ROW 2
                
        self.infobox        = Label(self._mainFrame,text = "Choose two dice, then click Roll to begin",justify="left",font="Verdana 12 italic")
        self.infobox.grid(row=2,column=0,columnspan=7,sticky="NEWS")

        ## ROW 3

        self.lblImgDie1 = Label(self._mainFrame, image=self.imgSwitch[d1],borderwidth=3,relief="raised")
        self.lblImgDie1.grid(row=3,column=0)
        self.lblImgDie2 = Label(self._mainFrame, image=self.imgSwitch[d2],borderwidth=3,relief="raised")
        self.lblImgDie2.grid(row=3,column=1)
        self.lblImgDie3 = Label(self._mainFrame, image=self.imgSwitch[d3],borderwidth=3,relief="raised")
        self.lblImgDie3.grid(row=3,column=2)
        self.lblImgDie4 = Label(self._mainFrame, image=self.imgSwitch[d4],borderwidth=3,relief="raised")
        self.lblImgDie4.grid(row=3,column=3)
        self.lblImgDie5 = Label(self._mainFrame, image=self.imgSwitch[d5],borderwidth=3,relief="raised")
        self.lblImgDie5.grid(row=3,column=4)
        self.lblImgDie6 = Label(self._mainFrame, image=self.imgSwitch[d6],borderwidth=3,relief="raised")
        self.lblImgDie6.grid(row=3,column=5)
        self.lblImgDie7 = Label(self._mainFrame, image=self.imgSwitch[d7],borderwidth=3,relief="raised")
        self.lblImgDie7.grid(row=3,column=6)

        ## ROW 4

        self.valDie1 = IntVar()
        self.chkDie1 = Checkbutton(self._mainFrame, text=d1, variable=self.valDie1, command=lambda: self.select(1), justify="center",width=7,font="Verdana 12")
        self.chkDie1.grid(row=4,column=0,columnspan=1,sticky="NEWS")

        self.valDie2 = IntVar()
        self.chkDie2 = Checkbutton(self._mainFrame, text=d2, variable=self.valDie2, command=lambda: self.select(2), justify="center",width=7,font="Verdana 12")
        self.chkDie2.grid(row=4,column=1,columnspan=1,sticky="NEWS")

        self.valDie3 = IntVar()
        self.chkDie3 = Checkbutton(self._mainFrame, text=d3, variable=self.valDie3, command=lambda: self.select(3), justify="center",width=7,font="Verdana 12")
        self.chkDie3.grid(row=4,column=2,columnspan=1,sticky="NEWS")

        self.valDie4 = IntVar()
        self.chkDie4 = Checkbutton(self._mainFrame, text=d4, variable=self.valDie4, command=lambda: self.select(4), justify="center",width=7,font="Verdana 12")
        self.chkDie4.grid(row=4,column=3,columnspan=1,sticky="NEWS")

        self.valDie5 = IntVar()
        self.chkDie5 = Checkbutton(self._mainFrame, text=d5, variable=self.valDie5, command=lambda: self.select(5), justify="center",width=7,font="Verdana 12")
        self.chkDie5.grid(row=4,column=4,columnspan=1,sticky="NEWS")

        self.valDie6 = IntVar()
        self.chkDie6 = Checkbutton(self._mainFrame, text=d6, variable=self.valDie6, command=lambda: self.select(6), justify="center",width=7,font="Verdana 12")
        self.chkDie6.grid(row=4,column=5,columnspan=1,sticky="NEWS")

        self.valDie7 = IntVar()
        self.chkDie7 = Checkbutton(self._mainFrame, text=d7, variable=self.valDie7, command=lambda: self.select(7), justify="center",width=7,font="Verdana 12")
        self.chkDie7.grid(row=4,column=6,columnspan=1,sticky="NEWS")

        ## ROW 5

        self.btnRecover = Button(self._mainFrame, text="Recover", command=self.recover, justify="center", state="disabled", font="Verdana 14")
        self.btnRecover.grid(row=5,column=4,columnspan=1)

        self.btnRoll = Button(self._mainFrame, text="Roll", command=self.roll, justify="center", state="disabled",font="Verdana 14")
        self.btnRoll.grid(row=5,column=5,columnspan=1)

        self.btnClear = Button(self._mainFrame, text="Clear", command=self.clear, justify="center", state="disabled",font="Verdana 14")
        self.btnClear.grid(row=5,column=6,columnspan=1)

        # These switches are used by class methods to address individual widgets that have now been defined
        self.btnSwitch = {1:self.chkDie1,2:self.chkDie2,3:self.chkDie3,4:self.chkDie4,5:self.chkDie5,6:self.chkDie6,7:self.chkDie7}
        self.valSwitch = {1:self.valDie1,2:self.valDie2,3:self.valDie3,4:self.valDie4,5:self.valDie5,6:self.valDie6,7:self.valDie7}
        self.rowSwitch = {self.chkDie1:self.lblImgDie1,self.chkDie2:self.lblImgDie2,self.chkDie3:self.lblImgDie3,self.chkDie4:self.lblImgDie4,self.chkDie5:self.lblImgDie5,self.chkDie6:self.lblImgDie6,self.chkDie7:self.lblImgDie7}
        self.dictDice = {self.chkDie1:self.valDie1,self.chkDie2:self.valDie2,self.chkDie3:self.valDie3,self.chkDie4:self.valDie4,self.chkDie5:self.valDie5,self.chkDie6:self.valDie6,self.chkDie7:self.valDie7}

    def invert(self):
        
        for die in (self.chkDie1,self.chkDie2,self.chkDie3,self.chkDie4,self.chkDie5,self.chkDie6,self.chkDie7):
            if die["state"] == "disabled":
                #print(die["state"])
                die["state"] = "normal"
                self.rowSwitch[die]["image"] = self.imgSwitch[die["text"]]
                self.rowSwitch[die]["relief"] = "raised"
            else:
                #print(die["state"])
                die["state"] = "disabled"
                self.rowSwitch[die]["image"] = self.grySwitch[die["text"]]
                self.rowSwitch[die]["relief"] = "sunken"

    def refresh(self):
        for die in (self.chkDie1,self.chkDie2,self.chkDie3,self.chkDie4,self.chkDie5,self.chkDie6,self.chkDie7):
            if self.dictDice[die].get() == 1:
                self.rowSwitch[die]["relief"] = "sunken"
            elif die["state"] == "normal":
                self.rowSwitch[die]["relief"] = "raised"

    def recover(self):
        
        self.btnClear["state"] = "disabled"
        self.btnRoll["state"] = "disabled"
        self.btnRecover["state"] = "disabled"
        #self.invert()
        self.roll()
        self.inRecover = False

    def select(self,button):

        if self.inRecover:
            self.refresh()
            # If only one die is selected to be recovered
            if (self.valDie1.get()+self.valDie2.get()+self.valDie3.get()+self.valDie4.get()+self.valDie5.get()+self.valDie6.get()+self.valDie7.get()) == 1:
                for die in (self.chkDie1,self.chkDie2,self.chkDie3,self.chkDie4,self.chkDie5,self.chkDie6,self.chkDie7):
                    # For any of the dice that were checked
                    if self.dictDice[die].get() == 1:
                        self.dieSelection = die["text"]
                self.infobox["text"] = "A "+self.dieSelection+" will be returned to your hand"
                self.btnRecover["state"] = "normal"
            else:
                self.infobox["text"] = "Select one die from the discard pile to return to your hand"
                self.btnRecover["state"] = "disabled"
            
        else:
            self.refresh()
            if self.round < 4:
                if (self.valDie1.get()+self.valDie2.get()+self.valDie3.get()+self.valDie4.get()+self.valDie5.get()+self.valDie6.get()+self.valDie7.get()) == 2:
                    self.infobox["text"] = "Click the \'Roll\' button to continue"
                    self.btnRoll["state"] = "normal"
                else:
                    self.infobox["text"] = "Please choose two dice to roll"
                    self.btnRoll["state"] = "disabled"
            elif self.round == 4:
                if (self.valDie1.get()+self.valDie2.get()+self.valDie3.get()+self.valDie4.get()+self.valDie5.get()+self.valDie6.get()+self.valDie7.get()) == 1:
                    self.btnRoll["state"] = "normal"
                else:
                    self.btnRoll["state"] = "disabled"
            else:
                self.btnRoll["state"]   = "normal"
                self.btnClear["state"]  = "disabled"
                
            if self.round <= 4:
                if (self.valDie1.get()+self.valDie2.get()+self.valDie3.get()+self.valDie4.get()+self.valDie5.get()+self.valDie6.get()+self.valDie7.get()) > 0:
                    self.btnClear["state"] = "normal"
                else:
                    self.btnClear["state"] = "disabled"
                    
    def diceMatched(self):
        self.inRecover = True
        self.invert()
    
    def roll(self):
        self.btnRecover["state"] = "disabled"
        self.btnRoll["state"] = "disabled"
        self.btnClear["state"] = "disabled"

        if self.inRecover:
            # If only one die is selected to be recovered
            if (self.valDie1.get()+self.valDie2.get()+self.valDie3.get()+self.valDie4.get()+self.valDie5.get()+self.valDie6.get()+self.valDie7.get()) == 1:
                for die in (self.chkDie1,self.chkDie2,self.chkDie3,self.chkDie4,self.chkDie5,self.chkDie6,self.chkDie7):
                    # For any of the dice that were checked
                    if self.dictDice[die].get() == 1:
                        die["state"] = "disabled"                        
                        self.rowSwitch[die]["image"] = self.grySwitch[die["text"]]
                        die.deselect()
            self.invert()
        else:
            dieOne = 0
            dieTwo = 0
            dieLess = 0
            dieMore = 0
            self.TieBreaker = 0

            if self.round < 4:  # Regular rounds, roll exactly two dice per round
                # Look through all of the player's dice
                for die in (self.chkDie1,self.chkDie2,self.chkDie3,self.chkDie4,self.chkDie5,self.chkDie6,self.chkDie7):
                    # For any of the dice that were checked
                    if self.dictDice[die].get() == 1:
                        # Set the first checked die to 'dieOne'
                        if dieOne == 0:
                            dieOne = self.dieSwitch[die["text"]]
                        # Set the second checked die to 'dieTwo'
                        else:
                            dieTwo = self.dieSwitch[die["text"]]
                        # Grey out and unselect those two dice
                        die["state"] = "disabled"
                        self.rowSwitch[die]["image"] = self.grySwitch[die["text"]]
                        die.deselect()
                
                dieMore = max(dieOne,dieTwo)
                dieLess = min(dieOne,dieTwo)

                print("Round "+str(self.round)+": Rolling d"+str(dieMore)+" and d"+str(dieLess)+"; ",end="")

                self.tally(dieMore,dieLess)
                
            else:
                self.btnRoll["state"] = "normal"
                self.btnClear["state"] = "disabled"
                if self.TieBreaker == 0:
                    for die in (self.chkDie1,self.chkDie2,self.chkDie3,self.chkDie4,self.chkDie5,self.chkDie6,self.chkDie7):
                        die["state"] = "disabled"
                        if self.dictDice[die].get() == 1:
                            self.TieBreaker = self.dieSwitch[die["text"]]
                        else:
                            self.rowSwitch[die]["image"] = self.grySwitch[die["text"]] 

                print("Tie-Breaker "+str(self.round-3)+": Rolling d"+str(self.TieBreaker)+"; ",end="")
                self.tally(self.TieBreaker)

            self.round += 1
            self.ntrRound["text"] = str(self.round)
            self.ntrScore["text"] = str(self.score)

    def clear(self):        # Clear any checkboxes indicating dice selections
        self.btnRecover["state"] = "disabled"
        self.btnClear["state"] = "disabled"
        self.btnRoll["state"] = "disabled"
                
        for die in (self.chkDie1,self.chkDie2,self.chkDie3,self.chkDie4,self.chkDie5,self.chkDie6,self.chkDie7):
            if die["state"] == "normal":
                self.rowSwitch[die]["relief"] = "raised"
                die.deselect()
            
    def tally(self,More,Less=0):
        rM = random.randint(1,More)

        if Less>0:
            rL = random.randint(1,Less)
            print(str(rM)+","+str(rL))
            if More != Less:
                if rL > rM:
                    if self.mode == "flip":
                        self.mode = "count"
                    else:
                        self.mode = "flip"
                    self.ntrMode["text"] = "  "+self.mode
                elif rL == rM:
                    self.diceMatched()
                self.score+=abs(rM-rL)
            else:
                self.score+=abs(rM-rL)
                if rL == rM:
                    self.diceMatched()
        else:
            print(str(rM))
            self.score+=rM
        self.ntrScore["text"] = "  "+str(self.score)

def main():
    p1 = PlayerWindow()

if __name__=="__main__":
    main()
