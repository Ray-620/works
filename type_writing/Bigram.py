import math

In=open("train.001","r")
Unigram={}
Bigram={}
Total=0
for Line in In:
	Line=Line.strip()
	for i in range(len(Line)):
		if not Unigram.get(Line[i]):
			Unigram[Line[i]]=0
		Unigram[Line[i]]+=1	
		
		if i == 0:
			continue
		if not Bigram.get(Line[i-1]+Line[i]):
			Bigram[Line[i-1]+Line[i]]=0
		Bigram[Line[i-1]+Line[i]]+=1
	Total+=1	
In.close()

Out=open("prob.txt","w")
Prob=0.0
for k in Unigram.keys():
	Prob=math.log(Unigram[k]/Total)
	print(k,Prob,file=Out)

for k in Bigram.keys():
	if Unigram.get(k[0]):
		Prob=math.log(Bigram[k]/Unigram[k[0]])
		print(k,Prob,file=Out)
	
Out.close()
	