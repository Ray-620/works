def ReadModel(File,RefUNK)
{
	temp=""
	In=open(File,"r")
	for Line in In:
		Line=Line.strip("#")
		Line=Line.strip()
		List=Line.split(" ")
		if not (List[1]):	#读出汉字
			if not RefUNK.get(List[0]):
				RefUNK[List[0]]={}
				temp=List[0]
				
		if (List[1]):	#读男女概率
			if not (temp):
				RefUNK["default"]=List[1]
			if not RefUNK[temp].get([List[0]]):	  #List[0]-> 男或女   List[1]-> 对应概率
				RefUNK[temp][List[0]]=List[1]				
	In.close()
}

def GetProb(hz,sex,RefUNK)
{
	if not RefUNK.get(hz):		#未找到已有汉字返回默认值
		return RefUNK["default"]
		
	if RefUNK.get(hz):
		if RefUNK[hz].get(sex):		   #汉字-性别 有数据可查时，返回数据
			return RefUNK[hz][sex]
	
	return RefUNK["default"]	  #其他情况返回默认值
}



def Bayes(name,RefUNK)
{
	male=0
	female=0
	Probmale=0
	Probfemale=0
	name1=name.decode("gbk")

	for i in range(len(name1)):
		HZ=name[i].encode("gbk")
		male=GetProb(HZ,"男",RefUNK)
		female=GetProb(HZ,"女"，RefUNK)
		Probmale+=male
		Probfemale+=female
	
	res="female"
	if(Probmale>Probfemale):
		res="male"
	
	return res
}

def Main
{
	RefUNK={}
	ReadModel("Model.txt",RefUNK);

	while 1:
	Name=""
	res=""
	Name=input("Pls Input:")
	if Name == "q":
		break
		
	Ret=Bayes(Name,RefUNK)
	print(RefUNK)
	#print(res)
	#print(Ret)
}

Main();