"""
File: FlippantTutor.py

The program teaches users how to play the dice game Flippant
via a simulated game with one to three computer-controlled
opponents. Their choices are chosen randomly, so players
shouldn't expect to learn strategies for competing with skilled
players, but this program should provide an excellent primer
for basic gameplay and scoring.

Flippant was developed Neil Austin and Shannon Benton.
Code written by Neil Austin, except where noted.
Dice graphics adapted from original art
    by Lonnie Tapscott from the Noun Project
"""

###
### The code in this version is a mess; NO REFUNDS!
###

import re
import tkinter as tk
from tkinter import ttk, messagebox
import random

class FlippantGame:

    def __init__(self,parent):

        self._top = parent
        self._top.geometry("+100+100")
        self._top.title("Flippant Tutorial")

        self.popUp = tk.Tk()
        self.popUp.geometry("+100+100")
        self.popUp.title("Default Title")

        # Initialize variables, load images
        self._InitVariables()
        self._InitImages()
        self._InitSwitches()

        # Initialize frames in advance
        self._InitAllFrames()
        self._InitTitle()
        self._InitNav()
        self._InitControls()
        self._InitCommentator()

        # Load just the frames needed at the start
        self._LoadTitle()
        self._LoadMainFrame()
        
        self.ScreenOne()

#  ██╗   ██╗ █████╗ ██████╗ ██╗ █████╗ ██████╗ ██╗     ███████╗███████╗
#  ██║   ██║██╔══██╗██╔══██╗██║██╔══██╗██╔══██╗██║     ██╔════╝██╔════╝
#  ██║   ██║███████║██████╔╝██║███████║██████╔╝██║     █████╗  ███████╗
#  ╚██╗ ██╔╝██╔══██║██╔══██╗██║██╔══██║██╔══██╗██║     ██╔══╝  ╚════██║
#   ╚████╔╝ ██║  ██║██║  ██║██║██║  ██║██████╔╝███████╗███████╗███████║
#    ╚═══╝  ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝╚═╝  ╚═╝╚═════╝ ╚══════╝╚══════╝╚══════╝

    def _InitVariables(self):

        # Some variables we'll need in multiple screens
        self._isTraditional = True
        self.styleVar = tk.BooleanVar(value=self._isTraditional)

        self._opponents = 1
        self.numOpponentsVar = tk.IntVar(value=self._opponents)

        # Lists to contain each player's selection of dice
        self.p1D = []
        self.p2D = []
        self.p3D = []
        self.p4D = []

        # Prepopulate those lists with the correct number of (impossible) dice
        #for i in range(7):
        #    self.p1D.append("d0")
        #    self.p2D.append("d0")
        #    self.p3D.append("d0")
        #    self.p4D.append("d0")

        # Each player's dice difference, before score calculation
        self.p1Diff = 0
        self.p2Diff = 0
        self.p3Diff = 0
        self.p4Diff = 0

        # Each player's score
        self.p1Score = 0
        self.p2Score = 0
        self.p3Score = 0
        self.p4Score = 0

        # Each player's name
        self.p1Name = tk.StringVar()
        self.p1Name.set("Player 1")

        self.stayAnon = tk.BooleanVar(value=False)

        self.Round = 1

        # Need this on screen 5 / Game Board
        self.isFlip = False
        
        self.diceDepressed = 0
        self.p1DiceInHand = []

        # These really should be a class, but maybe next version
        self.p2DiceAvailable = []
        self.p2DiceInHand = []
        self.p2DiceDiscards = []
        self.p2DiceButtons = []
        self.p2Name = tk.StringVar()
        self.p2Name.set("Player 2")
        self.p2Twins = False

        self.CPU1 = [self.p2DiceAvailable,
                     self.p2DiceInHand,
                     self.p2DiceDiscards,
                     self.p2DiceButtons,
                     self.p2Name,
                     self.p2Twins
                     ]
        
        self.p3DiceAvailable = []
        self.p3DiceInHand = []
        self.p3DiceDiscards = []
        self.p3DiceButtons = []
        self.p3Name = tk.StringVar()
        self.p3Name.set("Player 3")
        self.p3Twins = False

        self.CPU2 = [self.p3DiceAvailable,
                     self.p3DiceInHand,
                     self.p3DiceDiscards,
                     self.p3DiceButtons,
                     self.p3Name,
                     self.p3Twins
                     ]
        
        self.p4DiceAvailable = []
        self.p4DiceInHand = []
        self.p4DiceDiscards = []
        self.p4DiceButtons = []
        self.p4Name = tk.StringVar()
        self.p4Name.set("Player 4")
        self.p4Twins = False

        self.CPU3 = [self.p4DiceAvailable,
                     self.p4DiceInHand,
                     self.p4DiceDiscards,
                     self.p4DiceButtons,
                     self.p4Name,
                     self.p4Twins
                     ]
        
        self.inRecovery = False
        self.rolledTwins = False

        # Need this to close up shop at endgame.
        self.allButtons = []

#  ███████╗██╗    ██╗██╗████████╗ ██████╗██╗  ██╗███████╗███████╗
#  ██╔════╝██║    ██║██║╚══██╔══╝██╔════╝██║  ██║██╔════╝██╔════╝
#  ███████╗██║ █╗ ██║██║   ██║   ██║     ███████║█████╗  ███████╗
#  ╚════██║██║███╗██║██║   ██║   ██║     ██╔══██║██╔══╝  ╚════██║
#  ███████║╚███╔███╔╝██║   ██║   ╚██████╗██║  ██║███████╗███████║
#  ╚══════╝ ╚══╝╚══╝ ╚═╝   ╚═╝    ╚═════╝╚═╝  ╚═╝╚══════╝╚══════╝

    def _InitSwitches(self):
        # These switches allow images and labels to be loaded when the window
        # is first built and whenever they are changed by class methods
        self.listDice       = ("d4","d6","d8","d10","d100","d12","d20")
        self.dieSwitch      = {"d4":4,
                               "d6":6,
                               "d8":8,
                               "d10":10,
                               "d100":10,
                               "d12":12,
                               "d20":20}
        self.imgSwitch      = {"d4":self.imgD4,
                               "d6":self.imgD6,
                               "d8":self.imgD8,
                               "d10":self.imgD10,
                               "d100":self.imgD100,
                               "d12":self.imgD12,
                               "d20":self.imgD20}
        self.greyedOut      = {self.imgD4:self.imgD4g,
                               self.imgD6:self.imgD6g,
                               self.imgD8:self.imgD8g,
                               self.imgD10:self.imgD10g,
                               self.imgD100:self.imgD100g,
                               self.imgD12:self.imgD12g,
                               self.imgD20:self.imgD20g}
        self.restoredD      = {self.imgD4g:self.imgD4,
                               self.imgD6g:self.imgD6,
                               self.imgD8g:self.imgD8,
                               self.imgD10g:self.imgD10,
                               self.imgD100g:self.imgD100,
                               self.imgD12g:self.imgD12,
                               self.imgD20g:self.imgD20}

#  ██╗███╗   ███╗ █████╗  ██████╗ ███████╗███████╗
#  ██║████╗ ████║██╔══██╗██╔════╝ ██╔════╝██╔════╝
#  ██║██╔████╔██║███████║██║  ███╗█████╗  ███████╗
#  ██║██║╚██╔╝██║██╔══██║██║   ██║██╔══╝  ╚════██║
#  ██║██║ ╚═╝ ██║██║  ██║╚██████╔╝███████╗███████║
#  ╚═╝╚═╝     ╚═╝╚═╝  ╚═╝ ╚═════╝ ╚══════╝╚══════╝

    def _InitImages(self):
        
        # Load Images
        self.imgD0      = tk.PhotoImage(file="images\\d0.gif")
        self.imgD4      = tk.PhotoImage(file="images\\d4.gif")
        self.imgD6      = tk.PhotoImage(file="images\\d6.gif")
        self.imgD8      = tk.PhotoImage(file="images\\d8.gif")
        self.imgD10     = tk.PhotoImage(file="images\\d10.gif")
        self.imgD100    = tk.PhotoImage(file="images\\d100.gif")
        self.imgD12     = tk.PhotoImage(file="images\\d12.gif")
        self.imgD20     = tk.PhotoImage(file="images\\d20.gif")
        self.imgD4g     = tk.PhotoImage(file="images\\d4g.gif")
        self.imgD6g     = tk.PhotoImage(file="images\\d6g.gif")
        self.imgD8g     = tk.PhotoImage(file="images\\d8g.gif")
        self.imgD10g    = tk.PhotoImage(file="images\\d10g.gif")
        self.imgD100g   = tk.PhotoImage(file="images\\d100g.gif")
        self.imgD12g    = tk.PhotoImage(file="images\\d12g.gif")
        self.imgD20g    = tk.PhotoImage(file="images\\d20g.gif")

#  ███████╗██████╗  █████╗ ███╗   ███╗███████╗███████╗
#  ██╔════╝██╔══██╗██╔══██╗████╗ ████║██╔════╝██╔════╝
#  █████╗  ██████╔╝███████║██╔████╔██║█████╗  ███████╗
#  ██╔══╝  ██╔══██╗██╔══██║██║╚██╔╝██║██╔══╝  ╚════██║
#  ██║     ██║  ██║██║  ██║██║ ╚═╝ ██║███████╗███████║
#  ╚═╝     ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝     ╚═╝╚══════╝╚══════╝

    def _InitAllFrames(self):

        # frames definitions and geometry
        self._frmMain  = tk.Frame(self._top)
        self._frmTitle = tk.Frame(self._frmMain)
        self._frmNav   = tk.Frame(self._frmMain)
        self._frmPlay  = tk.Frame(self._frmMain)
        self._frmMenu1 = tk.Frame(self._frmMain)
        self._frmMenu2 = tk.Frame(self._frmMain)
        self._frmMenu3 = tk.Frame(self._frmMain)
        self._frmMenu4 = tk.Frame(self._frmMain)
        self._frmBoard = tk.Frame(self._frmMain)

        self._frmNav.grid(
            row=2,
            column=0,
            pady=5,
            sticky="SE")

    def _LoadMainFrame(self):
        
        self._frmMain.grid(
            row=1,
            column=0,
            padx=5,
            pady=5,
            sticky="W"
            )

    def _LoadCommentator(self):

        self.Commentator.grid(row=4,column=0)
        self.Scrollbar.grid(row=4,column=1)
        self.Scrollbar.config(command=self.Commentator.yview)
        self.Commentator.config(yscrollcommand=self.Scrollbar.set)

    def _InitCommentator(self):

        # Commentator is the scrollable text box at the bottom of the screen
        # where information about each new event is posted.
        self.Commentator = tk.Text(
            self._frmMain,
            height=6,
            width=74,
            font="Verdana 12"
            )

        self.Scrollbar = tk.Scrollbar(self._frmMain)

#   ██████╗ ██████╗ ███╗   ██╗████████╗██████╗  ██████╗ ██╗     ███████╗
#  ██╔════╝██╔═══██╗████╗  ██║╚══██╔══╝██╔══██╗██╔═══██╗██║     ██╔════╝
#  ██║     ██║   ██║██╔██╗ ██║   ██║   ██████╔╝██║   ██║██║     ███████╗
#  ██║     ██║   ██║██║╚██╗██║   ██║   ██╔══██╗██║   ██║██║     ╚════██║
#  ╚██████╗╚██████╔╝██║ ╚████║   ██║   ██║  ██║╚██████╔╝███████╗███████║
#   ╚═════╝ ╚═════╝ ╚═╝  ╚═══╝   ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚══════╝╚══════╝
#                                                                       

    def _LoadControls(self):

        self.btnNext.grid_forget()
        
        self.btnRecover.grid(
            row=0,
            column=0,
            sticky="SE"
            )
        self.btnRoll.grid(
            row=0,
            column=1,
            sticky="SE"
            )
        self.btnClear.grid(
            row=0,
            column=2,
            sticky="SE"
            )

    def _InitControls(self):
        
        # Actual game controls in _frmPlay
        self.btnRecover = tk.Button(
            self._frmNav,
            text="Recover",
            #command=Recover,
            width=7,
            font="Verdana 12 bold",
            bg="green",
            fg="white",
            state="disabled"
            )

        self.btnRoll = tk.Button(
            self._frmNav,
            text="Roll",
            #command=pass,
            width=4,
            font="Verdana 12 bold",
            bg="green",
            fg="white",
            state="disabled"
            )

        self.btnClear = tk.Button(
            self._frmNav,
            text="Clear",
            width=5,
            font="Verdana 12 bold",
            bg="green",
            fg="white",
            state="disabled"
            )

#  ███╗   ██╗ █████╗ ██╗   ██╗██╗ ██████╗  █████╗ ████████╗███████╗
#  ████╗  ██║██╔══██╗██║   ██║██║██╔════╝ ██╔══██╗╚══██╔══╝██╔════╝
#  ██╔██╗ ██║███████║██║   ██║██║██║  ███╗███████║   ██║   █████╗  
#  ██║╚██╗██║██╔══██║╚██╗ ██╔╝██║██║   ██║██╔══██║   ██║   ██╔══╝  
#  ██║ ╚████║██║  ██║ ╚████╔╝ ██║╚██████╔╝██║  ██║   ██║   ███████╗
#  ╚═╝  ╚═══╝╚═╝  ╚═╝  ╚═══╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝   ╚═╝   ╚══════╝
#                                                                  

    def _LoadNav(self,state="normal"):

        self.btnNext.grid(
            row=1,
            column=0,
            sticky="SE"
            )

        if state == "disabled":
            self.btnNext["state"] = "disabled"

        self.popUp.focus()

    def _InitNav(self):

        # Where the NEXT button lives
        self.btnNext = tk.Button(
            self._frmNav,
            text="Next",
            #command=self.Next,
            width=8,
            font="Verdana 12 bold",
            bg="green",
            fg="white"
            )

#  ████████╗██╗████████╗██╗     ███████╗
#  ╚══██╔══╝██║╚══██╔══╝██║     ██╔════╝
#     ██║   ██║   ██║   ██║     █████╗  
#     ██║   ██║   ██║   ██║     ██╔══╝  
#     ██║   ██║   ██║   ███████╗███████╗
#     ╚═╝   ╚═╝   ╚═╝   ╚══════╝╚══════╝
#                                       

    def _LoadTitle(self):
        self._frmTitle.grid(
            row=0,
            column=0,
            padx=5,
            pady=10,
            columnspan=7,
            sticky="NEWS"
            )

        self.lblTitleL1.grid(
            row=0,
            column=0,
            columnspan=1,
            sticky="NEWS"
            )
        self.lblTitleL2.grid(
            row=0,
            column=1,
            columnspan=1,
            sticky="NEWS"
            )
        
    def _InitTitle(self):

        # TKinter doesn't want to space politely, so here's a hack
        self.lblTitleL1 = tk.Label(
            self._frmTitle,
            text="",
            #width=15,
            )
        self.lblTitleL2 = tk.Label(
            self._frmTitle,
            text="",
            #width=15,
            )

        # The actual Title portion of this Frame
        self.lblTitleFLIP = tk.Label(
            self._frmTitle,
            text="FLIP",
            anchor="e",
            width=5,
            bg="green",
            fg="white",
            font="Verdana 16 bold"
            ).grid(
                row=0,
                column=2,
                columnspan=1,
                sticky="NES"
                )
        
        self.lblTitlePANT = tk.Label(
            self._frmTitle,
            text="PANT",
            anchor="w",
            width=5,
            bg="white",
            fg="green",
            font="Verdana 16 bold"
            ).grid(
                row=0,
                column=3,
                columnspan=1,
                sticky="NES"
                )
        
        self.lblTitleTutor = tk.Label(
            self._frmTitle,
            text="Game Tutorial",
            width=12,
            font="Verdana 14",
            anchor="w"
            ).grid(
                row=0,
                column=4,
                columnspan=1,
                sticky="NEWS"
                )
        
        self.lblTitleR1 = tk.Label(
            self._frmTitle,
            text="",
            #width=15,
            ).grid(
                row=0,
                column=5,
                columnspan=1,
                sticky="NEWS"
                )
        
        self.lblTitleR2 = tk.Label(
            self._frmTitle,
            text=""
            ).grid(
                row=0,
                column=6,
                columnspan=1,
                sticky="NEWS"
                )

    def Cheat(self):
        tk.messagebox.showwarning("Hey!","Cheating not yet implemented")

    def Next(self, event=None):
        self._scrSwitch[self._nextScreen]()
        self._nextScreen+=1

#  ██████╗  ██████╗ ██████╗ ██╗   ██╗██████╗ ███████╗
#  ██╔══██╗██╔═══██╗██╔══██╗██║   ██║██╔══██╗██╔════╝
#  ██████╔╝██║   ██║██████╔╝██║   ██║██████╔╝███████╗
#  ██╔═══╝ ██║   ██║██╔═══╝ ██║   ██║██╔═══╝ ╚════██║
#  ██║     ╚██████╔╝██║     ╚██████╔╝██║     ███████║
#  ╚═╝      ╚═════╝ ╚═╝      ╚═════╝ ╚═╝     ╚══════╝
#                                                    

    def Messages(self, title="PopUp Window", txt="Message Failed", h=10, hide=True):
        self.popUp.geometry("+100+100")
        self.popUp.title(title)
        f = tk.Frame(self.popUp)
        f.grid(column=0,row=0)
        t = tk.Text(self.popUp,
                    padx=20,
                    width=60,
                    height=h,
                    wrap="word",
                    font="Verdana 12")
        t.grid(column=0,row=0)
        t.insert('1.0',"\n"+txt)

        def HidePopUp(e='<None>'):
            self.popUp.withdraw()
            t.destroy()
            f.destroy()
            self._top.deiconify()
            self.btnNext.focus()

        def ShowPopUp(hide=False):
            if hide == True:
                self._top.withdraw()
            self.popUp.deiconify()
            self.popUp.focus()

        btnClose = tk.Button(
            self.popUp,
            text="Close",
            command=HidePopUp,
            width=8,
            font="Verdana 12 bold",
            bg="green",
            fg="white")

        self.popUp.bind('<Return>',HidePopUp)
        
        btnClose.grid(row=1,column=0)
        ShowPopUp(hide)

# Big Text from: http://patorjk.com/software/taag/#p=display&f=ANSI%20Shadow

# ██╗       ██╗███╗   ██╗████████╗██████╗  ██████╗ 
#███║██╗    ██║████╗  ██║╚══██╔══╝██╔══██╗██╔═══██╗
#╚██║╚═╝    ██║██╔██╗ ██║   ██║   ██████╔╝██║   ██║
# ██║██╗    ██║██║╚██╗██║   ██║   ██╔══██╗██║   ██║
# ██║╚═╝    ██║██║ ╚████║   ██║   ██║  ██║╚██████╔╝
# ╚═╝       ╚═╝╚═╝  ╚═══╝   ╚═╝   ╚═╝  ╚═╝ ╚═════╝ 
        
    # This seems redundant, but I guess if I need to reload the name screen,
    # I can go straight back to it, instead of throwing the popup window again
    def ScreenOne(self):
        
        aboutText = \
"Flippant is a dice game for two or more players, designed to be played with \
standard table-top gaming (TTG) dice. This program will teach you how the \
rules of Flippant work for each player, and how your choices affect the \
outcome of the game.\n\
\n\
But before we begin, would you like to introduce yourself?"

        self.Messages("Introduction",aboutText,8)
        self._scrIntro()

    def _scrIntro(self):
       
        # Begin Layout
        self._frmMenu1.grid(row=1,column=0)
        self._LoadNav()

        ## ROW 0
        # Moved to its own frame.

        ## ROW 1

        self.lblWhatIsYourName = tk.Label(
            self._frmMenu1,
            font="Verdana 12",
            text="Enter your name: "
            )
        self.lblWhatIsYourName.grid(
            row=1,
            column=0,
            sticky="NEWS"
            )
        
        self.ntrWhatYourNameIs = tk.Entry(
            self._frmMenu1,
            width=10,
            textvariable = self.p1Name,
            )
        self.ntrWhatYourNameIs.grid(
            row=1,
            column=1,
            sticky="NEWS"
            )

        ## ROW 2

        self.chkAnonymous = ttk.Checkbutton(
            self._frmMenu1,
            text='I want to remain anonymous',
            variable=self.stayAnon,
            onvalue=True,
            offvalue=False
            )
        self.chkAnonymous.grid(
                row=2,
                column=0,
                columnspan=3,
                sticky="NES"
                )

        def SetNextStateCHK(e):
            
            # If not checked BEFORE this click
            if self.stayAnon.get() == False:
                self.ntrWhatYourNameIs['state'] = "disabled"
                self.btnNext['state'] = "normal"
                self.btnNext.bind('<Button-1>', self.ScreenTwo)
                self.btnNext.bind('<Return>', self.ScreenTwo)
            else:
                self.ntrWhatYourNameIs['state'] = "normal"
                if len(self.p1Name.get()) > 0:
                    self.btnNext['state'] = "normal"
                    self.btnNext.bind('<Button-1>', self.ScreenTwo)
                    self.btnNext.bind('<Return>', self.ScreenTwo)
                else:
                    self.btnNext['state'] = "disabled"
                    self.btnNext.unbind('<Button-1>')
                    self.btnNext.unbind('<Return>')
            
        def SetNextStateNTR(e):
            if self.stayAnon.get() == False:
                if len(self.p1Name.get()) == 0:
                    self.btnNext['state'] = "disabled"
                    self.btnNext.unbind('<Button-1>')
                    self.btnNext.unbind('<Return>')
                else:
                    self.btnNext['state'] = "normal"
                    self.btnNext.bind('<Button-1>', self.ScreenTwo)
                    self.btnNext.bind('<Return>', self.ScreenTwo)
            else:
                if len(self.p1Name.get()) > 0:
                    self.btnNext['state'] = "disabled"
                    self.btnNext.unbind('<Button-1>')
                    self.btnNext.unbind('<Return>')
                else:
                    self.btnNext['state'] = "normal"
                    self.btnNext.bind('<Button-1>', self.ScreenTwo)
                    self.btnNext.bind('<Return>', self.ScreenTwo)
        
        # I'm not sure if this is a solid solution, but horseshoes/hand grenades
        self.ntrWhatYourNameIs.bind('<KeyRelease>', SetNextStateNTR)        
        self.chkAnonymous.bind('<Button-1>', SetNextStateCHK)
        self.btnNext.bind('<Button-1>', self.ScreenTwo)
        self.btnNext.bind('<Return>', self.ScreenTwo)


#██████╗        ███████╗████████╗██╗   ██╗██╗     ███████╗
#╚════██╗██╗    ██╔════╝╚══██╔══╝╚██╗ ██╔╝██║     ██╔════╝
# █████╔╝╚═╝    ███████╗   ██║    ╚████╔╝ ██║     █████╗  
#██╔═══╝ ██╗    ╚════██║   ██║     ╚██╔╝  ██║     ██╔══╝  
#███████╗╚═╝    ███████║   ██║      ██║   ███████╗███████╗
#╚══════╝       ╚══════╝   ╚═╝      ╚═╝   ╚══════╝╚══════╝
                                                         
    def ScreenTwo(self,e):

        aboutText = ""

        if self.stayAnon.get() == True:
            self.p1Name.set("Player 1")
            aTH = 11

        else:
            aboutText += "Welcome " + self.p1Name.get() + ",\n\n"
            aTH = 13
        
        self.ntrWhatYourNameIs.unbind('<KeyRelease>')
        self.chkAnonymous.unbind('<Button-1>')
        self.btnNext.unbind('<Button-1>')
        self.btnNext.unbind('<Return>')

        aboutText += \
"There are two variations of Flippant that you'll need to decide between in a \
moment. Traditional Flippant is played with a hand of six standard dice, namely \
one each of d4, d6, d8, d10, d12, and d20, and one duplicate die of the player's \
choice. In the variant form of the game, each player may choose any combination \
of those dice, so, for example, a hand of seven d20 dice would be acceptable. \n\
\n\
On the next screen, you will choose which variation you wish to play."
        
        self.Messages("Flippant Variations",aboutText,aTH)
        self._scrGameMode()
        
    def _scrGameMode(self):

        # Begin Layout
        self._frmMenu1.destroy()
        self._frmMenu2.grid(row=1,column=0)
                
        ## ROW 2
        # I kinda wanted to center this, but it's not worth the time right now.
        self.rdoTraditional = tk.Radiobutton(
            self._frmMenu2,
            text="Traditional",
            indicatoron=1,
            variable=self.styleVar,
            value=True,
            font="Verdana 12"
            ).grid(
                row=0,
                column=0,
                sticky="NSW"
                )
        self.rdoFreeCombo = tk.Radiobutton(
            self._frmMenu2,
            text="Freehand",
            indicatoron=1,
            variable=self.styleVar,
            value=False,
            font="Verdana 12"
            ).grid(
                row=1,
                column=0,
                sticky="NSW"
                )

        self.btnNext.bind('<Button-1>', self.ScreenThree)
        self.btnNext.bind('<Return>', self.ScreenThree)

#██████╗        ██████╗ ██╗ ██████╗██╗  ██╗    ██████╗ ██╗ ██████╗███████╗
#╚════██╗██╗    ██╔══██╗██║██╔════╝██║ ██╔╝    ██╔══██╗██║██╔════╝██╔════╝
# █████╔╝╚═╝    ██████╔╝██║██║     █████╔╝     ██║  ██║██║██║     █████╗  
# ╚═══██╗██╗    ██╔═══╝ ██║██║     ██╔═██╗     ██║  ██║██║██║     ██╔══╝  
#██████╔╝╚═╝    ██║     ██║╚██████╗██║  ██╗    ██████╔╝██║╚██████╗███████╗
#╚═════╝        ╚═╝     ╚═╝ ╚═════╝╚═╝  ╚═╝    ╚═════╝ ╚═╝ ╚═════╝╚══════╝

    def ScreenThree(self,e):

        if self.styleVar.get() == True:
            aboutText = \
"Since each player has most of the same dice in their hand, Traditional \
Flippant puts a greater emphasis on chance and intuition. An observant player \
will know which dice are still in play after each round, and choose their own \
next roll accordingly.\n\
\n\
Right now, you just need to choose one die to complete your hand."
            aTH = 8
        else:
            aboutText = \
"Freehand Flippant brings an added element of randomness to each game. Unless \
house rules require each player to choose their hand openly, there is no way to \
know in advance what dice you should choose to counter your opponent's hand. \
If they've chosen to play seven d20s, you already know that they'll never flip \
play, and are expecting to win with big numbers. You could choose a similar \
hand, and let fate decide, or build your hand with d4s and d6s in an attempt \
to flip the scoring?\n\
\n\
Your opponents today will be randomly generated, without any real strategy, so \
feel free to try out any combination of dice you can think of."
            aTH = 14
        
        self.btnNext.unbind('<Button-1>')
        self.btnNext.unbind('<Return>')

        self.Messages("Selecting Dice",aboutText,aTH)
        self._scrPickDice()

    def _scrPickDice(self):

        # Begin Layout
        self._frmMenu2.destroy()
        self._frmMenu3.grid(row=1,column=0)

        self.btnNext['state'] = "disabled"
        self.btnNext.unbind('<Button-1>')
        self.btnNext.unbind('<Return>')

        tempList = []
        self.urDice = []
        
        self.urDice.append(tk.Button(self._frmMenu3,
                                     text="??",
                                     compound="top",
                                     image=self.imgD0,
                                     command=lambda: RemoveADie(0)))
        self.urDice.append(tk.Button(self._frmMenu3,
                                     text="??",
                                     compound="top",
                                     image=self.imgD0,
                                     command=lambda: RemoveADie(1)))
        self.urDice.append(tk.Button(self._frmMenu3,
                                     text="??",
                                     compound="top",
                                     image=self.imgD0,
                                     command=lambda: RemoveADie(2)))
        self.urDice.append(tk.Button(self._frmMenu3,
                                     text="??",
                                     compound="top",
                                     image=self.imgD0,
                                     command=lambda: RemoveADie(3)))
        self.urDice.append(tk.Button(self._frmMenu3,
                                     text="??",
                                     compound="top",
                                     image=self.imgD0,
                                     command=lambda: RemoveADie(4)))
        self.urDice.append(tk.Button(self._frmMenu3,
                                     text="??",
                                     compound="top",
                                     image=self.imgD0,
                                     command=lambda: RemoveADie(5)))
        self.urDice.append(tk.Button(self._frmMenu3,
                                     text="??",
                                     compound="top",
                                     image=self.imgD0,
                                     command=lambda: RemoveADie(6)))

        def UpdateUrDice():

            for i in range(7):
                if self.urDice[i]['text'] != '??':
                    self.urDice[i].grid(row=5,column=i)
                else:
                    self.urDice[i].grid_forget()

        def AddADie(choice):

            if len(tempList) < 7:
                tempList.append(choice)
                self.urDice[len(tempList)-1]['text'] = choice
                self.urDice[len(tempList)-1]['image'] = self.imgSwitch[choice]
                updated = True
            else:
                updated = False

            if len(tempList) == 7:
                self.btnNext['state'] = "normal"
                self.btnNext.bind('<Button-1>', self.ScreenFour)
                self.btnNext.bind('<Return>', self.ScreenFour)

            UpdateUrDice()

        def RemoveADie(choice):

            self.btnNext['state'] = "disabled"

            tempList.remove(self.urDice[choice]['text'])

            i = choice
            while i < 6:
                self.urDice[i]['text'] = self.urDice[i+1]['text']
                self.urDice[i]['image'] = self.urDice[i+1]['image']
                i += 1
            self.urDice[6]['text'] = '??'

            # If you've removed a die, don't go to the next screen!
            self.btnNext.unbind('<Button-1>')
            self.btnNext.unbind('<Return>')

            UpdateUrDice()

                
        self._lblAvailableDice = tk.Label(
            self._frmMenu3,
            text="Available Dice: (Click to Add)",
            font="Verdana 12 bold")
        self._lblAvailableDice.grid(
            row=0,
            column=0,
            columnspan=3)
   
        # ROW 1

        # d4
        self.btnChooseD4 = tk.Button(
            self._frmMenu3,
            text="d4",
            image=self.imgD4,
            compound="top",
            command=lambda: AddADie("d4") 
            )
        self.btnChooseD4.grid(row=2,column=0)
        
        # d6
        self.btnChooseD6 = tk.Button(
            self._frmMenu3,
            text="d6",
            image=self.imgD6,
            compound="top",
            command=lambda: AddADie("d6")
            )
        self.btnChooseD6.grid(row=2,column=1)

        # d8
        self.btnChooseD8 = tk.Button(
            self._frmMenu3,
            text="d8",
            image=self.imgD8,
            compound="top",
            command=lambda: AddADie("d8")
            )
        self.btnChooseD8.grid(row=2,column=2)

        # d10
        self.btnChooseD10 = tk.Button(
            self._frmMenu3,
            text="d10",
            image=self.imgD10,
            compound="top",
            command=lambda: AddADie("d10")
            )
        self.btnChooseD10.grid(row=2,column=3)

        # d100
        self.btnChooseD100 = tk.Button(
            self._frmMenu3,
            text="d100",
            image=self.imgD100,
            compound="top",
            command=lambda: AddADie("d100")
            )
        self.btnChooseD100.grid(row=2,column=4)

        # d12
        self.btnChooseD12 = tk.Button(
            self._frmMenu3,
            text="d12",
            image=self.imgD12,
            compound="top",
            command=lambda: AddADie("d12"),
            )
        self.btnChooseD12.grid(row=2,column=5)

        # d20
        self.btnChooseD20 = tk.Button(
            self._frmMenu3,
            text="d20",
            image=self.imgD20,
            compound="top",
            command=lambda: AddADie("d20")
            )
        self.btnChooseD20.grid(row=2,column=6)

        # ROW 2

        self._lblYourDice = tk.Label(
            self._frmMenu3,
            text="Your Dice: (Click to Remove)",
            font="Verdana 12 bold"
            )
        self._lblYourDice.grid(
            row=4,
            column=0,
            columnspan=3
            )
        
        if self.styleVar.get() == True:
            self.btnChooseD4.invoke()
            self.urDice[0]['state'] = "disabled"
            self.btnChooseD6.invoke()
            self.urDice[1]['state'] = "disabled"
            self.btnChooseD8.invoke()
            self.urDice[2]['state'] = "disabled"
            self.btnChooseD10.invoke()
            self.urDice[3]['state'] = "disabled"
            self.btnChooseD12.invoke()
            self.urDice[4]['state'] = "disabled"
            self.btnChooseD20.invoke()
            self.urDice[5]['state'] = "disabled"

#██╗  ██╗       ██╗   ██╗███████╗██████╗ ███████╗██╗   ██╗███████╗
#██║  ██║██╗    ██║   ██║██╔════╝██╔══██╗██╔════╝██║   ██║██╔════╝
#███████║╚═╝    ██║   ██║█████╗  ██████╔╝███████╗██║   ██║███████╗
#╚════██║██╗    ╚██╗ ██╔╝██╔══╝  ██╔══██╗╚════██║██║   ██║╚════██║
#     ██║╚═╝     ╚████╔╝ ███████╗██║  ██║███████║╚██████╔╝███████║
#     ╚═╝         ╚═══╝  ╚══════╝╚═╝  ╚═╝╚══════╝ ╚═════╝ ╚══════╝

    def ScreenFour(self,e):

        aboutText = \
"Flippant can be played with as few as two players, and as many players as you \
can find dice and table space for. Just to keep things simple while you are \
learning to play, we'll limit the number of opponents you can choose to two, \
three, or four. Your strategies may change subtly as more players are added to \
the game, but for now, just focus on learning how scoring changes with each roll."
        aTH = 8
        
        self.btnNext.unbind('<Button-1>')
        self.btnNext.unbind('<Return>')

        self.Messages("Selecting Dice",aboutText,aTH)
        self._scrNumberOpps()

    def _scrNumberOpps(self):

        # Begin Layout

        for i in range(7):
            self.p1D.append(self.urDice[i]['text'])
        
        self._frmMenu3.destroy()
        self._frmMenu4.grid(row=1,column=0)

        tk.Label(self._frmMenu4,
                 text="How many opponents?",
                 font="Verdana 12 bold").grid(
                     row=0,
                     column=0,
                     columnspan=4,
                     sticky="NSW")

        self.rdoOneOpponent = tk.Radiobutton(
            self._frmMenu4,
            text="One",
            indicatoron=1,
            variable=self.numOpponentsVar,
            value=1,
            font="Verdana 12"
            ).grid(
                row=1,
                column=0,
                sticky="NSW"
                )
        self.rdoTwoOpponents = tk.Radiobutton(
            self._frmMenu4,
            text="Two",
            indicatoron=1,
            variable=self.numOpponentsVar,
            value=2,
            font="Verdana 12"
            ).grid(
                row=1,
                column=1,
                sticky="NSW"
                )
        self.rdoThreeOpponents = tk.Radiobutton(
            self._frmMenu4,
            text="Three",
            indicatoron=1,
            variable=self.numOpponentsVar,
            value=3,
            font="Verdana 12"
            ).grid(
                row=1,
                column=2,
                sticky="NSW"
                )

        self.btnNext.bind('<Button-1>', self.ScreenFive)
        self.btnNext.bind('<Return>', self.ScreenFive)

#███████╗       ██████╗ ██╗      █████╗ ██╗   ██╗██╗
#██╔════╝██╗    ██╔══██╗██║     ██╔══██╗╚██╗ ██╔╝██║
#███████╗╚═╝    ██████╔╝██║     ███████║ ╚████╔╝ ██║
#╚════██║██╗    ██╔═══╝ ██║     ██╔══██║  ╚██╔╝  ╚═╝
#███████║╚═╝    ██║     ███████╗██║  ██║   ██║   ██╗
#╚══════╝       ╚═╝     ╚══════╝╚═╝  ╚═╝   ╚═╝   ╚═╝

    def ScreenFive(self,e):

        aboutText = \
"Okay, " + self.p1Name.get() + ", it's time to play some Flippant!\n\
\n\
For the first three rounds, pick two dice, then click the 'roll' button. If you \
roll two of the same number, you'll get to reclaim one of your discarded dice, \
and if two or more players have the same winning score at the end of the third \
round, they'll get to pick one of their remaining dice to roll until there is a \
definite winner.\n\
\n\
Once you've finished your first game, you'll be able to change all of the \
options we've just gone through (in a single popup, no worries!) and try again \
with different choices."
        
        aTH = 14
        
        self.btnNext.unbind('<Button-1>')
        self.btnNext.unbind('<Return>')

        self.Messages("Time to Play!",aboutText,aTH)
        self._scrGameBoard()

    def _scrGameBoard(self):
        # Begin Layout
        self._frmMenu4.destroy()
        self._frmBoard.grid(row=1,column=0)

        self._LoadControls()

        self.opponents = []
        if self.numOpponentsVar.get() >= 1:
            self.opponents.append(self.CPU1)
            if self.numOpponentsVar.get() >= 2:
                self.opponents.append(self.CPU2)
                if self.numOpponentsVar.get() >= 3:
                    self.opponents.append(self.CPU3)

        self.allButtons.extend([self.btnRecover,self.btnNext,self.btnClear])

        if self.styleVar.get():
            for i in self.opponents:
                i[0].append("d4")
                i[0].append("d6")
                i[0].append("d8")
                i[0].append("d10")
                i[0].append("d12")
                i[0].append("d20")
                i[0].append(random.choice(self.listDice))
        else:
            for i in self.opponents:
                for j in range(7):
                    i[0].append(random.choice(self.listDice))

        self.lblPlayerName = tk.Label(
            self._frmBoard,
            text="Player\nName",
            font="Verdana 12 bold"
            )

        self.lblRound = tk.Label(
            self._frmBoard,
            text="Round: ",
            font="Verdana 12 bold"
            )
        self.lblRoundNum = tk.Label(
            self._frmBoard,
            text=str(self.Round),
            font="Verdana 12",
            bg="white"
            )

        self.lblStyle = tk.Label(
            self._frmBoard,
            text="Style: ",
            font="Verdana 12 bold"
            )
        self.lblStyleName = tk.Label(
            self._frmBoard,
            text=("Traditional" if self.styleVar.get() == True else "Freehand"),
            font="Verdana 12",
            bg="white"
            )

        self.lblMode = tk.Label(
            self._frmBoard,
            text="Count/Flip: ",
            font="Verdana 12 bold"
            )
        self.lblModeName = tk.Label(
            self._frmBoard,
            text=("Flip" if self.isFlip == True else "Count"),
            font="Verdana 12",
            bg=("black" if self.isFlip == True else "white"),
            fg=("lime" if self.isFlip == True else "black")
            )
        self.lblDieOne = tk.Label(
            self._frmBoard,
            text="Larger\nDIE",
            font="Verdana 12 bold"
            )
        self.lblDieTwo = tk.Label(
            self._frmBoard,
            text="Smaller\nDIE",
            font="Verdana 12 bold"
            )
        self.lblRoundScore = tk.Label(
            self._frmBoard,
            text="Round\nScore",
            font="Verdana 12 bold"
            )
        self.lblTotalScore = tk.Label(
            self._frmBoard,
            text="Total\nScore",
            font="Verdana 12 bold"
            )

        self.lblPlayerName.grid(column=0,row=0)
        self.lblRound.grid(column=1,row=0)
        self.lblRoundNum.grid(column=2,row=0)

        self.lblStyle.grid(column=3,row=0)
        self.lblStyleName.grid(column=4,row=0)

        self.lblMode.grid(column=5,row=0)
        self.lblModeName.grid(column=6,row=0)

        self.lblDieOne.grid(column=8,row=0)
        self.lblDieTwo.grid(column=9,row=0)
        self.lblRoundScore.grid(column=10,row=0)
        self.lblTotalScore.grid(column=11,row=0)

        #  ___   _      __    _     ____  ___       ___   _      ____ 
        # | |_) | |    / /\  \ \_/ | |_  | |_)     / / \ | |\ | | |_  
        # |_|   |_|__ /_/--\  |_|  |_|__ |_| \     \_\_/ |_| \| |_|__ 
        #

        self.lblP1Name = tk.Label(
            self._frmBoard,
            text=self.p1Name.get(),
            font="Verdana 16 bold",
            )
        
        # Dice for Player 1
        self.btnP1Die1 = tk.Button(
            self._frmBoard,
            text=self.p1D[0],
            image=self.imgSwitch[self.p1D[0]],
            compound="top",
            relief="raised",
            bd=3,
            command=lambda: Toggle(0) 
            )
        self.btnP1Die2 = tk.Button(
            self._frmBoard,
            text=self.p1D[1],
            image=self.imgSwitch[self.p1D[1]],
            compound="top",
            relief="raised",
            bd=3,
            command=lambda: Toggle(1) 
            )
        self.btnP1Die3 = tk.Button(
            self._frmBoard,
            text=self.p1D[2],
            image=self.imgSwitch[self.p1D[2]],
            compound="top",
            relief="raised",
            bd=3,
            command=lambda: Toggle(2) 
            )
        self.btnP1Die4 = tk.Button(
            self._frmBoard,
            text=self.p1D[3],
            image=self.imgSwitch[self.p1D[3]],
            compound="top",
            relief="raised",
            bd=3,
            command=lambda: Toggle(3) 
            )
        self.btnP1Die5 = tk.Button(
            self._frmBoard,
            text=self.p1D[4],
            image=self.imgSwitch[self.p1D[4]],
            compound="top",
            relief="raised",
            bd=3,
            command=lambda: Toggle(4) 
            )
        self.btnP1Die6 = tk.Button(
            self._frmBoard,
            text=self.p1D[5],
            image=self.imgSwitch[self.p1D[5]],
            compound="top",
            relief="raised",
            bd=3,
            command=lambda: Toggle(5) 
            )
        self.btnP1Die7 = tk.Button(
            self._frmBoard,
            text=self.p1D[6],
            image=self.imgSwitch[self.p1D[6]],
            compound="top",
            relief="raised",
            bd=3,
            command=lambda: Toggle(6) 
            )

        self.lblP1D1Rolled = tk.Label(
            self._frmBoard,
            text="0",
            width=4,
            height=4,
            font="Verdana 16 bold",
            )
        self.lblP1D2Rolled = tk.Label(
            self._frmBoard,
            text="0",
            width=4,
            height=4,
            font="Verdana 16 bold",
            )
        self.lblP1scrRound = tk.Label(
            self._frmBoard,
            text="0",
            width=4,
            height=4,
            font="Verdana 16 bold",
            )
        self.lblP1scrTotal = tk.Label(
            self._frmBoard,
            text="0",
            width=4,
            height=4,
            font="Verdana 16 bold",
            )

        self.lblP1Name.grid(column=0,row=1)
        self.btnP1Die1.grid(column=1,row=1)
        self.btnP1Die2.grid(column=2,row=1)
        self.btnP1Die3.grid(column=3,row=1)
        self.btnP1Die4.grid(column=4,row=1)
        self.btnP1Die5.grid(column=5,row=1)
        self.btnP1Die6.grid(column=6,row=1)
        self.btnP1Die7.grid(column=7,row=1)
        self.allButtons.extend([self.btnP1Die1,
                                self.btnP1Die2,
                                self.btnP1Die3,
                                self.btnP1Die4,
                                self.btnP1Die5,
                                self.btnP1Die6,
                                self.btnP1Die7]
                               )
        self.lblP1D1Rolled.grid(column=8,row=1)
        self.lblP1D2Rolled.grid(column=9,row=1)
        self.lblP1scrRound.grid(column=10,row=1)
        self.lblP1scrTotal.grid(column=11,row=1)

        # Only used by Player 1. CPU players recover in-line.
        def Recover():
            dice = [self.btnP1Die1,
                    self.btnP1Die2,
                    self.btnP1Die3,
                    self.btnP1Die4,
                    self.btnP1Die5,
                    self.btnP1Die6,
                    self.btnP1Die7
                    ]

            # This for loop flips disabled and normal buttons
            # so the player can choose from previously chosen
            # dice, but not dice that haven't been used yet.
            for die in dice:
                if die['state'] == "disabled":
                    die['state'] = "normal"
                    die['relief'] = "raised"
                else:
                    if die['relief'] == "raised":
                        die['state'] = "disabled"
                        die['relief'] = "flat"
                    else:
                        die['relief'] = "raised"

            # Recovery is one-and-done per round, so reset it now.
            self.btnRecover['state'] = "disabled"
            self.inRecovery = False
            self.diceDepressed = 0
            self.p1DiceInHand.clear()

        # Attach the command to the button after it has been defined.
        self.btnRecover['command'] = Recover
        
        def Roll():
            self.lblP1D1Rolled['text'] = ""
            self.lblP1D2Rolled['text'] = ""
            dice = [self.btnP1Die1,
                    self.btnP1Die2,
                    self.btnP1Die3,
                    self.btnP1Die4,
                    self.btnP1Die5,
                    self.btnP1Die6,
                    self.btnP1Die7
                    ]

            # Dice selected in the previous round were indicated by using
            # "ridge" for relief. Those should be reset to flat now
            if self.Round < 5:
                for die in dice:
                    if die['relief'] == "ridge":
                        die['relief'] = "flat"

            # Opponents all need to choose dice to roll at this point.
            for opps in self.opponents:
                opps[3][8]['text'] = ""
                opps[3][9]['text'] = ""
                if self.Round < 5:
                    # Reset button ridges indicating choices from last round
                    for b in range(1,8):
                        if opps[3][b]['relief'] == "ridge":
                            opps[3][b]['relief'] = "flat"
                    tDie = random.choice(opps[0])       # randomly choose 1 die from available
                    opps[0].remove(tDie)                # remove that die from available
                    opps[1].append(tDie)                # add that die to hand
                    opps[2].append(tDie)                # add that die to discards
                    # Before Round 4, a second die must be rolled for each opponent
                    if self.Round < 4:
                        tDie = random.choice(opps[0])   # randomly choose another die from available
                        opps[0].remove(tDie)            # remove that die from available
                        opps[1].append(tDie)            # add that die to hand
                        opps[2].append(tDie)            # add that die to discards

                        # Set Twins flag for opponent if two of the same die are chosen
                        if self.dieSwitch[opps[1][0]] == self.dieSwitch[opps[1][1]]:
                            opps[5] = True
                        else:
                            opps[5] = False

                        # Get the number of sides of the smaller die
                        rDieSides = min(self.dieSwitch[opps[1][0]],
                                        self.dieSwitch[opps[1][1]])
                        # 'roll' that smaller die
                        rDieRoll = random.randint(1,rDieSides)
                        # Write the result of that roll to the screen
                        opps[3][9]['text'] = rDieRoll

                        # Find a matching die in the opponent's hand
                        # and disable it (not guaranteed to be the
                        # same die randomly chosen, but who will know?
                        for b in range(1,8):
                            if opps[3][b]['text'] == opps[1][1] and\
                            opps[3][b]['state'] == "normal":
                                opps[3][b]['state'] = "disabled"
                                opps[3][b]['relief'] = "ridge"
                                break

                        # Get the number of sides of the larger die
                        lDieSides = max(self.dieSwitch[opps[1][0]],
                                        self.dieSwitch[opps[1][1]])
                        # if both dice are the same, set the Twins flag
                        if lDieSides == rDieSides:
                            opps[5] = True
                        else:
                            opps[5] = False
                    # In round 4, each player picks their tiebreaker die
                    elif self.Round == 4:
                        lDieSides = self.dieSwitch[opps[1][0]]

                        # FOR OPPONENTS
                        # Find the unused die matching the click
                        # disable it, but highlight it with a ridge
                        for b in range(1,8):
                            if opps[3][b]['text'] == opps[1][0] and\
                            opps[3][b]['state'] == "normal":
                                opps[3][b]['state'] = "disabled"
                                opps[3][b]['relief'] = "ridge"
                                break
                        # Set all remaining opponent dice to disabled
                        for b in range(1,8):
                            opps[3][b]['state'] = "disabled"

                    # in Rounds 1-4 only
                    lDieRoll = random.randint(1,lDieSides)
                    opps[3][8]['text'] = lDieRoll

                    # If CPU rolls the same number on each die, return
                    # a randomly chosen die to their available dice list.
                    if self.Round < 4:
                        if lDieRoll == rDieRoll:

                            # List maintenance; important!
                            temp = random.choice(opps[2])
                            opps[2].remove(temp)
                            opps[0].append(temp)

                            # Update the button state for the selected die.
                            for b in range(1,8):
                                if opps[3][b]['text'] == temp and \
                                   opps[3][b]['state'] == "disabled":
                                    opps[3][b]['state'] = "normal"
                                    
                    # Rounds 1-4 only (dice don't change after Round 4)    
                    for b in range(1,8):
                        if opps[3][b]['text'] == opps[1][0] and\
                        opps[3][b]['state'] == "normal":
                            opps[3][b]['state'] = "disabled"
                            
                            opps[3][b]['relief'] = "ridge"
                            break
                    #
                    # Highlight score display based on roll results.
                    # ONLY changes highlights for CPU players. Player 1
                    # must be updated separately below.
                    #
                    if self.Round < 4:
                        # Highlight YELLOW if duplicate numbers rolled
                        # (CPU RECOVERS A DIE)
                        if lDieRoll == rDieRoll:
                            opps[3][8]['fg'] = "black"
                            opps[3][8]['bg'] = "yellow"
                            opps[3][9]['fg'] = "black"
                            opps[3][9]['bg'] = "yellow"
                        # Highlight GREY if same dice were rolled
                        # (NO FLIP, SCORE MULTIPLIERS APPLIED)
                        elif lDieSides == rDieSides:
                            opps[3][8]['fg'] = "SystemButtonFace"
                            opps[3][8]['bg'] = "grey"
                            opps[3][9]['fg'] = "SystemButtonFace"
                            opps[3][9]['bg'] = "grey"
                        # Highlight BLACK if larger die rolled lower
                        # (FLIP CONDITION!)
                        elif lDieRoll < rDieRoll:
                            self.isFlip = not self.isFlip
                            opps[3][8]['fg'] = "lime"
                            opps[3][8]['bg'] = "black"
                            opps[3][9]['fg'] = "lime"
                            opps[3][9]['bg'] = "black"
                        # Normal display. BLACK on GREY
                        else:
                            opps[3][8]['fg'] = "black"
                            opps[3][8]['bg'] = "SystemButtonFace"
                            opps[3][9]['fg'] = "black"
                            opps[3][9]['bg'] = "SystemButtonFace"
                        opps[1].clear()
                    # Show only one die roll after first three rounds.
                    # Set once in Round 4 then never change.
                    elif self.Round == 4:
                        opps[3][8]['fg'] = "black"
                        opps[3][8]['bg'] = "SystemButtonFace"
                        opps[3][9]['fg'] = "SystemButtonFace"
                        opps[3][9]['bg'] = "SystemButtonFace"
                # For rounds 5+
                else:
                    lDieSides = self.dieSwitch[opps[1][0]]
                    lDieRoll = random.randint(1,lDieSides)
                    opps[3][8]['text'] = lDieRoll

            if self.Round <= 4:
                # FOR PLAYER
                # Disable all dice, set the chosen die to ridge
                # and all other dice to flat
                for die in dice:
                    if self.Round == 4:
                        die['state'] = "disabled"
                        
                    if die['relief'] == "sunken":
                        die['state'] = "disabled"
                        die['relief'] = "ridge"
                    elif self.Round == 4:
                        die['relief'] = "flat"

            # ALL ROUNDS NOW       
            # Flatten and disable used dice buttons
            for die in dice:
                if die['relief'] == "sunken":
                    die['relief'] = "flat"
                    die['state'] = "disabled"

            # All players roll, do some math, update scoreboard

            if len(self.p1DiceInHand) == 2:
                lDieSides = max((self.dieSwitch[self.p1DiceInHand[0]],
                                 self.dieSwitch[self.p1DiceInHand[1]]))
                lDieRoll  = random.randint(1,lDieSides)
                self.lblP1D1Rolled['text'] = lDieRoll

                rDieSides = min((self.dieSwitch[self.p1DiceInHand[0]],
                                 self.dieSwitch[self.p1DiceInHand[1]]))
                rDieRoll  = random.randint(1,rDieSides)
                self.lblP1D2Rolled['text'] = rDieRoll

                # Set Twins flag for Player 1
                if lDieSides == rDieSides:
                    self.rolledTwins = True
                else:
                    self.rolledTwins = False

                # YELLOW highlight for duplicate roll by Player 1
                if lDieRoll == rDieRoll:
                    self.lblP1D1Rolled['bg'] = "yellow"
                    self.lblP1D1Rolled['fg'] = "black"
                    self.lblP1D2Rolled['bg'] = "yellow"
                    self.lblP1D2Rolled['fg'] = "black"
                # Player 1 rolled twins, gets grey highlights
                elif self.rolledTwins == True:
                    self.lblP1D1Rolled['fg'] = "white"
                    self.lblP1D1Rolled['bg'] = "grey"
                    self.lblP1D2Rolled['fg'] = "white"
                    self.lblP1D2Rolled['bg'] = "grey"
                # FLIP/Inverted display colors on scoreboard for Player 1
                elif lDieRoll < rDieRoll and not self.rolledTwins:
                    self.lblP1D1Rolled['bg'] = "black"
                    self.lblP1D1Rolled['fg'] = "lime"
                    self.lblP1D2Rolled['bg'] = "black"
                    self.lblP1D2Rolled['fg'] = "lime"
                # Normal display colors on scoreboard for Player 1
                else:
                    self.lblP1D1Rolled['bg'] = "SystemButtonFace"
                    self.lblP1D1Rolled['fg'] = "black"
                    self.lblP1D2Rolled['bg'] = "SystemButtonFace"
                    self.lblP1D2Rolled['fg'] = "black"
                    
                # Player 1's raw roll difference. **SIGNED**
                self.p1Diff = lDieRoll - rDieRoll

                # Flip the Flip flag if Player 1 rolls less on larger die
                if self.p1Diff < 0 and not self.rolledTwins:
                    self.isFlip = not self.isFlip

                # When Player 1 rolls the same value on two dice,
                # Player 1 can recover one die from discards or last roll
                if self.p1Diff == 0:
                    self.inRecovery = True
                    self.p1DiceInHand.clear()
                    # Flip normal/disabled for all dice in hand so Player 1
                    # can choose one previously played die to recover
                    for die in [self.btnP1Die1,
                    self.btnP1Die2,
                    self.btnP1Die3,
                    self.btnP1Die4,
                    self.btnP1Die5,
                    self.btnP1Die6,
                    self.btnP1Die7
                    ]:
                        if die['state'] == "disabled":
                            die['state'] = "normal"
                            die['relief'] = "raised"
                        else:
                            die['state'] = "disabled"
                            die['relief'] = "flat"
                else:
                    # Reset the Recovery mode flag if different numbers were rolled.
                    self.inRecovery = False
                    
            # If roll was clicked after Round 3, only display one die
            else:
                # Normal display for one die after Round 4
                if self.Round == 4:
                    self.lblP1D1Rolled['bg'] = "SystemButtonFace"
                    self.lblP1D1Rolled['fg'] = "black"
                    self.lblP1D2Rolled['bg'] = "SystemButtonFace"
                    self.lblP1D2Rolled['fg'] = "SystemButtonFace"

                oDieSides = self.dieSwitch[self.p1DiceInHand[0]]
                oDieRoll  = random.randint(1,oDieSides)
                self.lblP1D1Rolled['text'] = oDieRoll
                self.lblP1D2Rolled['text'] = ""
                self.p1Diff = oDieRoll
                
            # Reset button states and temp variables
            if self.Round < 4:
                self.diceDepressed = 0
                self.p1DiceInHand = []
                self.btnRoll['state'] = "disabled"
            self.btnClear['state'] = "disabled"

            # Update the player's score after player and cpus have rolled
            if self.Round < 4:
                if self.rolledTwins == True:
                    if self.isFlip == False:
                        self.lblP1scrRound['text'] = abs(self.p1Diff) * 2
                    else:
                        self.lblP1scrRound['text'] = abs(self.p1Diff) // 2
                else:
                    self.lblP1scrRound['text'] = abs(self.p1Diff)
            else:
                self.lblP1scrRound['text'] = self.p1Diff
            self.lblP1scrTotal['text'] = int(self.lblP1scrTotal['text']) + \
                                         int(self.lblP1scrRound['text'])

            self.lblP1scrRound['fg'] = "black"
            self.lblP1scrRound['bg'] = "SystemButtonFace"
            self.lblP1scrTotal['fg'] = "black"
            self.lblP1scrTotal['bg'] = "SystemButtonFace"

            # Update each CPU's score after everyone has rolled
            for opps in self.opponents:
                if self.Round < 4:
                    if opps[5] == True:
                        if self.isFlip == False:
                            opps[3][10]['text'] = abs(opps[3][8]['text'] - \
                                                      opps[3][9]['text']) * 2
                        else:
                            opps[3][10]['text'] = abs(opps[3][8]['text'] - \
                                                      opps[3][9]['text']) // 2
                    else:
                        opps[3][10]['text'] = abs(opps[3][8]['text'] -
                                                  \
                                                  opps[3][9]['text'])
                else:
                    opps[3][10]['text'] = opps[3][8]['text']
                opps[3][11]['text'] = int(opps[3][11]['text']) + \
                                      int(opps[3][10]['text'])
                
                # Reset Display Colors before setting Winner Colors
                opps[3][10]['fg'] = "black"
                opps[3][10]['bg'] = "SystemButtonFace"
                opps[3][11]['fg'] = "black"
                opps[3][11]['bg'] = "SystemButtonFace"

            # Change Count/Flip indicator box
            self.Round += 1                
            self.lblRoundNum['text'] = str(self.Round)
            self.lblModeName['text'] = ("Flip" if self.isFlip == True else "Count")
            self.lblModeName['fg'] = ("lime" if self.isFlip == True else "black")
            self.lblModeName['bg'] = ("black" if self.isFlip == True else "white")

            # All scores should be calculated by this point
            # Count/Flip should be calculated by this point
            # Look through all player scores, highlight round winner
            ## If round is 3 or higher, check for a winner

            buttonList = [self.lblP1scrRound]
            totalList = [self.lblP1scrTotal]
            for opps in self.opponents:
                buttonList.append(opps[3][10])
                totalList.append(opps[3][11])
            ShowBestScores(buttonList)
            gameWon = ShowBestScores(totalList)

            # If somebody won, pop up a message (congratulatory, if it was
            # Player 1, and disable all of the buttons (for now) so it's clear
            # that the game is over. Consider adding a 'play again' button later
            if self.Round > 3 and gameWon:
                theWinner = "Nobody"
                if self.lblP1scrTotal['bg'] == "green":
                    theWinner = "Congratulations " + self.p1Name.get() + ", you"
                elif self.lblP2scrTotal['bg'] == "green":
                    theWinner = self.CPU1[4].get()
                elif self.lblP3scrTotal['bg'] == "green":
                    theWinner = self.CPU2[4].get()
                elif self.lblP4scrTotal['bg'] == "green":
                    theWinner = self.CPU3[4].get()

                if self.isFlip == True:
                    explainer = "In Flip mode, the player with the single lowest score after Round 3 wins.\n\n"
                else:
                    explainer = "In Count mode, the player with the single highest score after Round 3 wins.\n\n"
                    
                for btn in self.allButtons:
                    btn['state'] = "disabled"
                self.Messages("GAME OVER", explainer + theWinner + " won!",6,False)                

        self.btnRoll['command'] = Roll

        def Clear():
            self.p1DiceInHand = []
            self.diceDepressed = 0
            self.btnRecover['state'] = "disabled"
            self.btnRoll['state'] = "disabled"
            self.btnClear['state'] = "disabled"

            dice = [self.btnP1Die1,
                    self.btnP1Die2,
                    self.btnP1Die3,
                    self.btnP1Die4,
                    self.btnP1Die5,
                    self.btnP1Die6,
                    self.btnP1Die7
                    ]
            for die in dice:
                if die['state'] == "normal":
                    die['relief'] = "raised"
                    
        self.btnClear['command'] = Clear

        def Toggle(die):
            dice = [self.btnP1Die1,
                    self.btnP1Die2,
                    self.btnP1Die3,
                    self.btnP1Die4,
                    self.btnP1Die5,
                    self.btnP1Die6,
                    self.btnP1Die7
                    ]

            # One die when recovering dice
            # Two dice rounds 1-3
            # One die in round 4
            # Same die in subsequent rounds
            if self.inRecovery:
                limit = 1
            elif self.Round < 4:
                limit = 2
            elif self.Round == 4:
                limit = 1
            else:
                limit = 0

            if dice[die]['relief'] == "raised":
                if self.diceDepressed < limit:
                    self.diceDepressed += 1
                    dice[die]['relief'] = "sunken"
                    self.p1DiceInHand.append(dice[die]['text'])
            elif dice[die]['relief'] == "sunken":
                self.diceDepressed -= 1
                dice[die]['relief'] = "raised"
                self.p1DiceInHand.remove(dice[die]['text'])
    
            if len(self.p1DiceInHand) == limit:
                if self.inRecovery:
                    self.btnRecover['state'] = "normal"
                    self.btnRoll['state'] = "disabled"
                else:
                    self.btnRoll['state'] = "normal"
                    self.btnRecover['state'] = "disabled"
            else:
                self.btnRoll['state'] = "disabled"
                self.btnRecover['state'] = "disabled"
                
            if len(self.p1DiceInHand) > 0:
                self.btnClear['state'] = "normal"
            else:
                self.btnClear['state'] = "disabled"

        def cmp_text(i):
            return int(i['text'])

        def ShowBestScores(lblList):
            if self.isFlip:
                rWin = min(lblList, key=cmp_text)
            else:
                rWin = max(lblList, key=cmp_text)

            if [cmp_text(x) for x in lblList].count(int(rWin['text'])) == 1:
                rWin['bg'] = "green"
                rWin['fg'] = "white"
                return True
            else:
                for b in lblList:
                    if b['text'] == rWin['text']:
                        b['bg'] = "white"
                        b['fg'] = "green"
                return False
            
        #   ___   _      __    _     ____  ___      _____  _       ___  
        #  | |_) | |    / /\  \ \_/ | |_  | |_)      | |  \ \    // / \ 
        #  |_|   |_|__ /_/--\  |_|  |_|__ |_| \      |_|   \_\/\/ \_\_/ 
        #

        self.lblP2Name = tk.Label(
            self._frmBoard,
            text=self.p2Name.get(),
            font="Verdana 16 bold",
        )

        # Dice for Player 2
        self.btnP2Die1 = tk.Button(
            self._frmBoard,
            text=self.CPU1[0][0],
            image=self.imgSwitch[self.CPU1[0][0]],
            compound="top",
            relief="flat",
            bd=3,
            #command=lambda: PickADie(self.p2D[0]) 
            )
        self.btnP2Die2 = tk.Button(
            self._frmBoard,
            text=self.CPU1[0][1],
            image=self.imgSwitch[self.CPU1[0][1]],
            compound="top",
            relief="flat",
            bd=3,
            #command=lambda: PickADie(self.p2D[1]) 
            )
        self.btnP2Die3 = tk.Button(
            self._frmBoard,
            text=self.CPU1[0][2],
            image=self.imgSwitch[self.CPU1[0][2]],
            compound="top",
            relief="flat",
            bd=3,
            #command=lambda: PickADie(self.p2D[2]) 
            )
        self.btnP2Die4 = tk.Button(
            self._frmBoard,
            text=self.CPU1[0][3],
            image=self.imgSwitch[self.CPU1[0][3]],
            compound="top",
            relief="flat",
            bd=3,
            #command=lambda: PickADie(self.p2D[3]) 
            )
        self.btnP2Die5 = tk.Button(
            self._frmBoard,
            text=self.CPU1[0][4],
            image=self.imgSwitch[self.CPU1[0][4]],
            compound="top",
            relief="flat",
            bd=3,
            #command=lambda: PickADie(self.p2D[4]) 
            )
        self.btnP2Die6 = tk.Button(
            self._frmBoard,
            text=self.CPU1[0][5],
            image=self.imgSwitch[self.CPU1[0][5]],
            compound="top",
            relief="flat",
            bd=3,
            #command=lambda: PickADie(self.p2D[5]) 
            )
        self.btnP2Die7 = tk.Button(
            self._frmBoard,
            text=self.CPU1[0][6],
            image=self.imgSwitch[self.CPU1[0][6]],
            compound="top",
            relief="flat",
            bd=3,
            #command=lambda: PickADie(self.p2D[6]) 
            )

        self.lblP2D1Rolled = tk.Label(
            self._frmBoard,
            text="0",
            width=4,
            height=4,
            font="Verdana 16 bold",
            )
        self.lblP2D2Rolled = tk.Label(
            self._frmBoard,
            text="0",
            width=4,
            height=4,
            font="Verdana 16 bold",
            )
        self.lblP2scrRound = tk.Label(
            self._frmBoard,
            text="0",
            width=4,
            height=4,
            font="Verdana 16 bold",
            )
        self.lblP2scrTotal = tk.Label(
            self._frmBoard,
            text="0",
            width=4,
            height=4,
            font="Verdana 16 bold",
            )
        
        self.CPU1[3].extend([self.lblP2Name,
                             self.btnP2Die1,
                             self.btnP2Die2,
                             self.btnP2Die3,
                             self.btnP2Die4,
                             self.btnP2Die5,
                             self.btnP2Die6,
                             self.btnP2Die7,
                             self.lblP2D1Rolled,
                             self.lblP2D2Rolled,
                             self.lblP2scrRound,
                             self.lblP2scrTotal
                             ])

        self.lblP2Name.grid(column=0,row=2)
        self.btnP2Die1.grid(column=1,row=2)
        self.btnP2Die2.grid(column=2,row=2)
        self.btnP2Die3.grid(column=3,row=2)
        self.btnP2Die4.grid(column=4,row=2)
        self.btnP2Die5.grid(column=5,row=2)
        self.btnP2Die6.grid(column=6,row=2)
        self.btnP2Die7.grid(column=7,row=2)
        self.allButtons.extend([self.btnP2Die1,
                                self.btnP2Die2,
                                self.btnP2Die3,
                                self.btnP2Die4,
                                self.btnP2Die5,
                                self.btnP2Die6,
                                self.btnP2Die7]
                               )
        self.lblP2D1Rolled.grid(column=8,row=2)
        self.lblP2D2Rolled.grid(column=9,row=2)
        self.lblP2scrRound.grid(column=10,row=2)
        self.lblP2scrTotal.grid(column=11,row=2)

        #   ___   _      __    _     ____  ___      _____  _     ___   ____  ____ 
        #  | |_) | |    / /\  \ \_/ | |_  | |_)      | |  | |_| | |_) | |_  | |_  
        #  |_|   |_|__ /_/--\  |_|  |_|__ |_| \      |_|  |_| | |_| \ |_|__ |_|__ 
        #                                                                         

        if self.numOpponentsVar.get() > 1:
            self.lblP3Name = tk.Label(
                self._frmBoard,
                text=self.p3Name.get(),
                font="Verdana 16 bold",
                )

            # Dice for Player 1
            self.btnP3Die1 = tk.Button(
                self._frmBoard,
                text=self.CPU2[0][0],
                image=self.imgSwitch[self.CPU2[0][0]],
                compound="top",
                relief="flat",
                bd=3,
                #command=lambda: PickADie(self.p3D[0]) 
                )
            self.btnP3Die2 = tk.Button(
                self._frmBoard,
                text=self.CPU2[0][1],
                image=self.imgSwitch[self.CPU2[0][1]],
                compound="top",
                relief="flat",
                bd=3,
                #command=lambda: PickADie(self.p3D[1]) 
                )
            self.btnP3Die3 = tk.Button(
                self._frmBoard,
                text=self.CPU2[0][2],
                image=self.imgSwitch[self.CPU2[0][2]],
                compound="top",
                relief="flat",
                bd=3,
                #command=lambda: PickADie(self.p3D[2]) 
                )
            self.btnP3Die4 = tk.Button(
                self._frmBoard,
                text=self.CPU2[0][3],
                image=self.imgSwitch[self.CPU2[0][3]],
                compound="top",
                relief="flat",
                bd=3,
                #command=lambda: PickADie(self.p3D[3]) 
                )
            self.btnP3Die5 = tk.Button(
                self._frmBoard,
                text=self.CPU2[0][4],
                image=self.imgSwitch[self.CPU2[0][4]],
                compound="top",
                relief="flat",
                bd=3,
                #command=lambda: PickADie(self.p3D[4]) 
                )
            self.btnP3Die6 = tk.Button(
                self._frmBoard,
                text=self.CPU2[0][5],
                image=self.imgSwitch[self.CPU2[0][5]],
                compound="top",
                relief="flat",
                bd=3,
                #command=lambda: PickADie(self.p3D[5]) 
                )
            self.btnP3Die7 = tk.Button(
                self._frmBoard,
                text=self.CPU2[0][6],
                image=self.imgSwitch[self.CPU2[0][6]],
                compound="top",
                relief="flat",
                bd=3,
                #command=lambda: PickADie(self.p3D[6]) 
                )

            self.lblP3D1Rolled = tk.Label(
                self._frmBoard,
                text="0",
                width=4,
                height=4,
                font="Verdana 16 bold",
                )
            self.lblP3D2Rolled = tk.Label(
                self._frmBoard,
                text="0",
                width=4,
                height=4,
                font="Verdana 16 bold",
                )
            self.lblP3scrRound = tk.Label(
                self._frmBoard,
                text="0",
                width=4,
                height=4,
                font="Verdana 16 bold",
                )
            self.lblP3scrTotal = tk.Label(
                self._frmBoard,
                text="0",
                width=4,
                height=4,
                font="Verdana 16 bold",
                )

            self.CPU2[3].extend([self.lblP3Name,
                                 self.btnP3Die1,
                                 self.btnP3Die2,
                                 self.btnP3Die3,
                                 self.btnP3Die4,
                                 self.btnP3Die5,
                                 self.btnP3Die6,
                                 self.btnP3Die7,
                                 self.lblP3D1Rolled,
                                 self.lblP3D2Rolled,
                                 self.lblP3scrRound,
                                 self.lblP3scrTotal
                                 ])

            self.lblP3Name.grid(column=0,row=3)
            self.btnP3Die1.grid(column=1,row=3)
            self.btnP3Die2.grid(column=2,row=3)
            self.btnP3Die3.grid(column=3,row=3)
            self.btnP3Die4.grid(column=4,row=3)
            self.btnP3Die5.grid(column=5,row=3)
            self.btnP3Die6.grid(column=6,row=3)
            self.btnP3Die7.grid(column=7,row=3)
            self.allButtons.extend([self.btnP3Die1,
                                    self.btnP3Die2,
                                    self.btnP3Die3,
                                    self.btnP3Die4,
                                    self.btnP3Die5,
                                    self.btnP3Die6,
                                    self.btnP3Die7]
                                   )
            self.lblP3D1Rolled.grid(column=8,row=3)
            self.lblP3D2Rolled.grid(column=9,row=3)
            self.lblP3scrRound.grid(column=10,row=3)
            self.lblP3scrTotal.grid(column=11,row=3)

        #   ___   _      __    _     ____  ___       ____  ___   _     ___  
        #  | |_) | |    / /\  \ \_/ | |_  | |_)     | |_  / / \ | | | | |_) 
        #  |_|   |_|__ /_/--\  |_|  |_|__ |_| \     |_|   \_\_/ \_\_/ |_| \ 
        #                                                                   

        if self.numOpponentsVar.get() > 2:
            self.lblP4Name = tk.Label(
                self._frmBoard,
                text=self.p4Name.get(),
                font="Verdana 16 bold",
                )

            # Dice for Player 1
            self.btnP4Die1 = tk.Button(
                self._frmBoard,
                text=self.CPU3[0][0],
                image=self.imgSwitch[self.CPU3[0][0]],
                compound="top",
                relief="flat",
                bd=3,
                #command=lambda: PickADie(self.p4D[0]) 
                )
            self.btnP4Die2 = tk.Button(
                self._frmBoard,
                text=self.CPU3[0][1],
                image=self.imgSwitch[self.CPU3[0][1]],
                compound="top",
                relief="flat",
                bd=3,
                #command=lambda: PickADie(self.p4D[1]) 
                )
            self.btnP4Die3 = tk.Button(
                self._frmBoard,
                text=self.CPU3[0][2],
                image=self.imgSwitch[self.CPU3[0][2]],
                compound="top",
                relief="flat",
                bd=3,
                #command=lambda: PickADie(self.p4D[2]) 
                )
            self.btnP4Die4 = tk.Button(
                self._frmBoard,
                text=self.CPU3[0][3],
                image=self.imgSwitch[self.CPU3[0][3]],
                compound="top",
                relief="flat",
                bd=3,
                #command=lambda: PickADie(self.p4D[3]) 
                )
            self.btnP4Die5 = tk.Button(
                self._frmBoard,
                text=self.CPU3[0][4],
                image=self.imgSwitch[self.CPU3[0][4]],
                compound="top",
                relief="flat",
                bd=3,
                #command=lambda: PickADie(self.p4D[4]) 
                )
            self.btnP4Die6 = tk.Button(
                self._frmBoard,
                text=self.CPU3[0][5],
                image=self.imgSwitch[self.CPU3[0][5]],
                compound="top",
                relief="flat",
                bd=3,
                #command=lambda: PickADie(self.p4D[5]) 
                )
            self.btnP4Die7 = tk.Button(
                self._frmBoard,
                text=self.CPU3[0][6],
                image=self.imgSwitch[self.CPU3[0][6]],
                compound="top",
                relief="flat",
                bd=3,
                #command=lambda: PickADie(self.p4D[6]) 
                )

            self.lblP4D1Rolled = tk.Label(
                self._frmBoard,
                text="0",
                width=4,
                height=4,
                font="Verdana 16 bold",
                )
            self.lblP4D2Rolled = tk.Label(
                self._frmBoard,
                text="0",
                width=4,
                height=4,
                font="Verdana 16 bold",
                )
            self.lblP4scrRound = tk.Label(
                self._frmBoard,
                text="0",
                width=4,
                height=4,
                font="Verdana 16 bold",
                )
            self.lblP4scrTotal = tk.Label(
                self._frmBoard,
                text="0",
                width=4,
                height=4,
                font="Verdana 16 bold",
                )

            self.CPU3[3].extend([self.lblP4Name,
                                 self.btnP4Die1,
                                 self.btnP4Die2,
                                 self.btnP4Die3,
                                 self.btnP4Die4,
                                 self.btnP4Die5,
                                 self.btnP4Die6,
                                 self.btnP4Die7,
                                 self.lblP4D1Rolled,
                                 self.lblP4D2Rolled,
                                 self.lblP4scrRound,
                                 self.lblP4scrTotal
                                 ])

            self.lblP4Name.grid(column=0,row=4)
            self.btnP4Die1.grid(column=1,row=4)
            self.btnP4Die2.grid(column=2,row=4)
            self.btnP4Die3.grid(column=3,row=4)
            self.btnP4Die4.grid(column=4,row=4)
            self.btnP4Die5.grid(column=5,row=4)
            self.btnP4Die6.grid(column=6,row=4)
            self.btnP4Die7.grid(column=7,row=4)
            self.allButtons.extend([self.btnP4Die1,
                                    self.btnP4Die2,
                                    self.btnP4Die3,
                                    self.btnP4Die4,
                                    self.btnP4Die5,
                                    self.btnP4Die6,
                                    self.btnP4Die7]
                                   )
            self.lblP4D1Rolled.grid(column=8,row=4)
            self.lblP4D2Rolled.grid(column=9,row=4)
            self.lblP4scrRound.grid(column=10,row=4)
            self.lblP4scrTotal.grid(column=11,row=4)
       
def main():
    root = tk.Tk()
    game = FlippantGame(root)
    root.mainloop()

if __name__=="__main__":
    main()
