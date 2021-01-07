import struct
import time
import os

def RetHZOffset(HZ):
	HZOffset=32*((HZ[0]-0xa0-1)*94+(HZ[1]-0xa0-1))
	return HZOffset



def ShowHZS(HZS,No):
	for i in range(No,16):
		for j in range(len(HZS[i])):
			print(HZS[i][j],end="")
		print("")

	for i in range(No):
		for j in range(len(HZS[i])):
			print(HZS[i][j],end="")
		print("")



def GetHZ(HZ,Handle,HZs):
	Offset=RetHZOffset(HZ)
	Handle.seek(Offset,0)
	Dot=Handle.read(32)
	DotInfo=struct.unpack("32B",Dot)

	for i in range(16):
		Line=[]
		for j in range(8):
			if  ( (0x80>>j) & DotInfo[2*i] ) != 0:
				Line.append("*")
			else:
				Line.append(" ")

		for j in range(8):
			if ( (0x80>>j) & DotInfo[2*i+1] ) != 0:
				Line.append("*")
			else:
				Line.append(" ")
		HZs.append(Line)
		

def GetHZs(HZS,Handle,HZSInfo):
	for i in range(len(HZS)):
		GB=HZS[i].encode("gbk")
		HZInfo=[]
		GetHZ(GB,Handle,HZInfo)
		for j in range(0,len(HZInfo)):
			HZSInfo[j].append("  ")
			for k in range(0,len(HZInfo[j])):
				HZSInfo[j].append(HZInfo[j][k])

				
def Main(HZS):
	HZArray=[]
	I=open("hzk.dat","rb")
	HZArray=[[] for i in range(16)]
	GetHZs(HZS,I,HZArray)
	I.close()
	
	while 1:
		for i in range(len(HZArray[0])):
			time.sleep(1)
			os.system("cls")
			ShowHZS(HZArray,i)

Main("我成功了")

