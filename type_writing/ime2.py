def PY2HZInit(PYFile,P2HZ):
	In=open(PYFile,"r")
	His=[]
	for Line in In:
		Line=Line.strip()
		List=Line.split(" ")
		for i in range(1,len(List)):
			if not P2HZ.get(List[0]):
				P2HZ[List[0]]=[]
			P2HZ[List[0]].append(List[i])
			
	
	P2HZ["E"]=[]			
	P2HZ["B"]=[]
	P2HZ["E"].append("E")			
	P2HZ["B"].append("B")			
	In.close()

	
def NgramInit(ProbFile,NgramProb):
	In=open(ProbFile,"r")
	His=[]
	for Line in In:
		Line=Line.strip()
		List=Line.split(" ")
		NgramProb[List[0]]=float(List[1])
	In.close()


def IME(PY,P2HZ,NgramProb):
	Lattice=[]
	if BuildLattice(PY,Lattice,P2HZ) == 0:
		return
	SearchLattice(Lattice,NgramProb)
	Ret=BackLattice(Lattice)
	return Ret
	
	
	

def Main(PYFile,ProbFile):
	P2HZ={}
	NgramProb={}
	
	
	PY2HZInit(PYFile,P2HZ)
	NgramInit(ProbFile,NgramProb)
	PinYin=list(P2HZ.keys())   #获得拼音列表
	#print(PinYin) 
	
	while 1:
		PY=""
		res=""
		PY=input("Pls Input:")
		if PY == "q":
			break
			
		while (PY):
			i=6
			while(i>=1):
				now=PY[:i]
				for j in range(len(PinYin)):
					if now==PinYin[j]:
						PY=PY[i:]
						if (res):
							res=res+" "
						res=res+now
						break
				i=i-1		
					   
		Ret=IME(res,P2HZ,NgramProb)
		#print(PinYin[7])
		#print(res)
		print(Ret)



def GetCandidate(PY,P2HZ,HZs):
	if P2HZ.get(PY):
		for HZ in P2HZ[PY]:
			HZs.append(HZ)

def GetProb(HZs,NgramProb):
	Ret=-100.0
	if	NgramProb.get(HZs):
		Ret=NgramProb[HZs]
	return Ret
		
def	BuildLattice(InpPY,Lattice,P2HZ):
	List=InpPY.split(" ")
	List.insert(0,"B")
	List.append("E")
	
	for PY in List:
		HZs=[]
		GetCandidate(PY,P2HZ,HZs)
		if len(HZs) == 0:
			return 0
		Column=[]
		for HZ in HZs:
			Unit=[]
			Unit.append(HZ)
			Unit.append(-100.0)
			Unit.append(0)
			Column.append(Unit)
		Lattice.append(Column)
	return 1	
		
def	SearchLattice(Lattice,NgramProb):
	for i in range(1,len(Lattice)):
		for j in range(len(Lattice[i])):
			Prob=0.0
			Max=-1000
			
			for k in range(len(Lattice[i-1])):
				if i-1 > 0:
					HZ=Lattice[i-1][k][0]+Lattice[i][j][0]
				else:	
					HZ=Lattice[i][j][0]
				
				Prob=GetProb(HZ,NgramProb)+Lattice[i-1][k][1]
				if Prob >Max:
					Lattice[i][j][2]=k
					Max=Prob
			Lattice[i][j][1]=Max

				
def	BackLattice(Lattice):
	Unit=[]
	ColumnNo=len(Lattice)-1
	Unit=Lattice[ColumnNo][len(Lattice[ColumnNo])-1]
	RetArray=[]
	while ColumnNo >0 :
		if Unit[0] != "E":
			RetArray.insert(0,Unit[0])		
		Unit=Lattice[ColumnNo-1][Unit[2]]
		ColumnNo-=1
		
	Ret="".join(RetArray)
	return Ret

Main("invert.txt","prob.txt")