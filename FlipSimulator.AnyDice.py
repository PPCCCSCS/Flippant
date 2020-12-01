import random

class Player(object):

    def __init__(self, pid):
        self.pid      = pid
        self.alldice  = [4,6,8,10,12,20]
        self.dicebag  = []
        for i in range(7):
            self.dicebag.append(random.choice(self.alldice))
        self.discard  = []
        self.score    = 0
        self.history  = ""
        self.picks    = ""
        self.lastRoll = ()

    def roll(self,tiebreaker=False):
        if tiebreaker == True:
            if len(self.dicebag) > 1:
                temp = random.choice(self.dicebag)
                self.dicebag.remove(temp)
                for die in self.dicebag:
                    self.dicebag.remove(die)
                    self.discard.append(die)
                self.dicebag.append(temp)
            a = random.randint(1,self.dicebag[0])
            self.lastRoll = (self.dicebag[0],a)
            self.history+=str(self.dicebag[0])+":"+str(a)+" "
            #self.picks+="T:d"+str(self.dicebag[0])+" "
            return (self.dicebag[0],a)
        elif len(self.dicebag) > 1:
            # Pick one random die from the bag
            first = random.choice(self.dicebag)
            self.dicebag.remove(first)
            self.discard.append(first)
            # Pick another random die from the bag
            second = random.choice(self.dicebag)
            self.dicebag.remove(second)
            self.discard.append(second)
            # die0 is the die with more sides
            die0 = max(first,second)
            die1 = min(first,second)
            # roll both dice
            a = random.randint(1,die0)
            b = random.randint(1,die1)
            # record the results in larger_die&smaller_die order
            self.lastRoll = ((die0,a),(die1,b))
            self.history+="d"+str(die0)+":"+str(a)+"&"+"d"+str(die1)+":"+str(b)+" "
            self.picks+="(d"+str(die0)+",d"+str(die1)+") "
            # return rolls as a tuple as (larger_die,smaller_die)
            return ((die0,a),(die1,b))
        else:
            return None

    def recover(self,die=None):
        if die in self.discard:
            self.discard.remove(die)
            self.dicebag.append(die)
            self.history+="REC: d"+str(die)+" "
            #self.picks+="R:d"+str(die)+"] "
            return die
        if len(self.discard) > 0:
            # Move one random die from discard to dicebag
            recovered = random.choice(self.discard)
            self.discard.remove(recovered)
            self.dicebag.append(recovered)
            self.history+="REC: d"+str(recovered)+" "
            #self.picks+="R:d"+str(recovered)+" "
            return recovered
        else:
            return None

    def getScore(self):
        return self.score

    def setScore(self,points):
        self.score += points

    def getHistory(self):
        return self.history

    def getPicks(self):
        return self.picks

    def getLastRoll(self):
        return self.lastRoll

    def getDicebag(self):
        return self.dicebag

    def getDiscard(self):
        return self.discard

class FlipGame(object):

    def __init__(self,players=2):
        self.isFlipped = False
        self.pList = []
        self.leaders = []
        for i in range(0,players):
            self.pList.append(Player(i+1))
        self.winningPicks = ""

    def playRound(self):
        # All players roll before Count/Flip can be determined
        for player in self.pList:
            d0,d1 = player.roll()
            # If two different die are rolled and the smaller scores higher than the larger, flip state
            if d0[0] != d1[0] and d0[1] < d1[1]:
                self.isFlipped = not self.isFlipped
        # Twin scoring depends on state, so we need a second loop each round for scoring
        for player in self.pList:
            d0,d1 = player.getLastRoll()
            diff = abs(d0[1]-d1[1])
            # if there's zero difference, player gets a die back from discards
            if d0[1] == d1[1]:
                    player.recover()
            # if the player rolled two of the same dice
            if d0[0] == d1[0]:
                if self.isFlipped == True:
                    player.setScore( diff//2 )
                else:
                    player.setScore( diff*2 )
            # if the player rolled two different dice, just add the difference
            else:
                player.setScore( diff )

        allScores = []
        leaders   = []
        self.leaders = []
        bestScore = -1
        for player in self.pList:
            allScores.append(player.getScore())
        if self.isFlipped:
            bestScore = min(allScores)
        else:
            bestScore = max(allScores)
        for player in self.pList:
            if player.getScore() == bestScore:
                leaders.append(player.pid)
                self.leaders.append(player)
                

    def playTieBreaker(self):
        #print("TIEBREAKER!")
        allScores = []
        leaders = []
        bestScore = -1
        for player in self.leaders:
            roll = player.roll(True)
            player.setScore(roll[1])
            allScores.append(player.getScore())
            #print("P"+str(player.pid)+":"+str(player.getScore()))
            #print(player.getLastRoll())
        if self.isFlipped:
            bestScore = min(allScores)
        else:
            bestScore = max(allScores)
        for player in self.leaders:
            if player.getScore() == bestScore:
                leaders.append(player.pid)
            else:
                self.leaders.remove(player)

    def getState(self):
        if self.isFlipped:
            print("State is Flip")
        else:
            print("State is Count")

    def getScoreboard(self):
        for player in self.pList:
             print("P"+str(player.pid)+":"+str(player.getScore()))
             print(player.getLastRoll())

    def getLeaders(self):
        allScores = []
        leaders   = []
        self.leaders = []
        bestScore = -1
        for player in self.pList:
            allScores.append(player.getScore())
        if self.isFlipped:
            bestScore = min(allScores)
        else:
            bestScore = max(allScores)
        for player in self.pList:
            if player.getScore() == bestScore:
                leaders.append(player.pid)
                self.leaders.append(player)
        
        if len(self.leaders) > 1:
            print("leaders:", leaders)
        else:
            print("WINNER is P"+str(leaders[0]))

    def playGame(self):
        self.playRound()
        self.playRound()
        self.playRound()

        while len(self.leaders) > 1:
            self.playTieBreaker()

        return self.leaders[0].getPicks()
            
def main():

    f = open("KiloFlipAny2-10.txt","a")

    dictWins = dict()
    for i in range(1000000):

        j = random.randint(2,10)

        result = FlipGame(j).playGame()
        if result in dictWins:
            dictWins[result]+=1
        else:
            dictWins[result]=1

    for k in sorted(dictWins.items(), key=lambda x:x[1], reverse=True):
        f.write(str(k)+"\n")

    f.close

    print("DONE!")

if __name__ == "__main__":
    main()

