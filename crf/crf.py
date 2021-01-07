import re


class CRF:
    Feature = {}
    Weight = []
    STATE = ["B", "E", "M", "S"]
    STATE2ID = {"B": 0, "E": 1, "M": 2, "S": 3}

    def CRFInit(self, Model):
        Inp = open(Model, "r", encoding="utf-8")
        for Line in Inp:
            Line = Line.strip()
            match1 = re.search("(\d+)\s([^:]+):(.*)", Line)
            match2 = re.search("(-?\d+\.\d+)", Line)
            if match2:
                self.Weight.append(float(match2.group(0)))
            elif match1:
                if not self.Feature.get(match1.group(2)):
                    self.Feature[match1.group(2)] = {}
                self.Feature[match1.group(2)][match1.group(3)] = int(match1.group(1))
        Inp.close()

    def GetStateProb(self, HZArray, No, State):
        Prob = 0.0
        if self.Feature["U01"].get(HZArray[No - 1]):
            Prob += self.Weight[self.Feature["U01"][HZArray[No - 1]] + self.STATE2ID[State]]
        if self.Feature["U02"].get(HZArray[No]):
            Prob += self.Weight[self.Feature["U02"][HZArray[No]] + self.STATE2ID[State]]
        if self.Feature["U08"].get(HZArray[No - 1] + "/" + HZArray[No]):
            Prob += self.Weight[self.Feature["U08"][HZArray[No - 1] + "/" + HZArray[No]] + self.STATE2ID[State]]
        if No < len(HZArray) - 1:
            if self.Feature["U03"].get(HZArray[No + 1]):
                Prob += self.Weight[self.Feature["U03"][HZArray[No + 1]] + self.STATE2ID[State]]
            if self.Feature["U09"].get(HZArray[No] + "/" + HZArray[No + 1]):
                Prob += self.Weight[self.Feature["U09"][HZArray[No] + "/" + HZArray[No + 1]] + self.STATE2ID[State]]
        return Prob

    def GetTransitionProb(self, State1, State2):
        ID = 4 * self.STATE2ID[State1] + self.STATE2ID[State2]
        return self.Weight[ID]

    def Format(self, RetArray):
        Ret=""
        for Unit in RetArray:
            if Unit[0] == "S":
                Ret+=" "
                Ret+=Unit[3]
                Ret+=" "
            elif Unit[0] == "B":	
                Ret+=" "
                Ret+=Unit[3]
            else:
                Ret+=Unit[3]
        Ret=re.sub("^\s","",Ret)
        Ret=re.sub("\s$","",Ret)
        return 	Ret
        

    def Viterbi(self, Sentence):
        HZArray = []
        Lattice = []
        RetArray = []
        self.Sent2Array(Sentence, HZArray)
        self.BuildLattice(HZArray, Lattice)
        self.SearchLattice(Lattice, HZArray)
        self.GetRet(Lattice, RetArray)
        Ret = self.Format(RetArray)
        return Ret

    def Sent2Array(self, Sentence, HZArray):
        HZArray.append("_B-1")
        for i in range(len(Sentence)):
            HZArray.append(Sentence[i])
        HZArray.append("_B+1")

    def BuildLattice(self, HZArray, Lattice):
        for HZ in HZArray:
            HZs = []
            Column = []
            for S in self.STATE:
                Unit = []
                Unit.append(S)
                Unit.append(-100.0)
                Unit.append(0)
                Unit.append(HZ)
                Column.append(Unit)
            Lattice.append(Column)

    def SearchLattice(self, Lattice, HZArray):
        for i in range(1, len(Lattice)):
            for j in range(len(Lattice[i])):
                Prob = 0.0
                Max = -1000
                for k in range(len(Lattice[i - 1])):
                    TransitionProb = self.GetTransitionProb(Lattice[i - 1][k][0], Lattice[i][j][0])
                    StateProb = self.GetStateProb(HZArray, i, Lattice[i][j][0])
                    Prob = StateProb + TransitionProb + Lattice[i - 1][k][1]
                    if Prob > Max:
                        Lattice[i][j][2] = k
                        Max = Prob
                Lattice[i][j][1] = Max

    def GetRet(self, Lattice, RetArray):
        Unit = []
        ColumnNo = len(Lattice) - 1
        Unit = Lattice[ColumnNo][len(Lattice[ColumnNo]) - 1]
        while ColumnNo > 0:
            if Unit[3] != "_B+1":
                RetArray.insert(0, Unit)
            Unit = Lattice[ColumnNo - 1][Unit[2]]
            ColumnNo -= 1


def Main():
    obCRF = CRF()
    print("Init....", end="")
    obCRF.CRFInit("model_Bi.txt")
    print("Done!")
    while 1:
        Sentence=input("Pls:")
        if Sentence == "q":
            break
        Ret=obCRF.Viterbi(Sentence)
        print(Ret)


Main()