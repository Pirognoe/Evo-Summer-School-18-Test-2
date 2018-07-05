import sys
import random
import math

x = int(sys.argv[2]) #Number of servers for simulator
y = sys.argv[3] #Mode of simulator: random or mirror
k = 2 # if we compairing only 2 arbitrary servers
C = math.factorial(x)/(math.factorial(k)*math.factorial(x-k)) #Number of unique server pairs

#Declare all our variables
Server_Name = {}
for i in range(1,int(x)+1):
	Server_Name["S_" + str(i)] = []
	
shards = [i for j in range(2) for i in range(1,101)] #Declare our shards
counter = 0

def mirror(): #Define our mirror case with a separate function
	for i in range(len(Server_Name)):
		for j in range(20*i,20+20*i):
			Server_Name["S_"+str(i+1)].append(shards[j])
	return Server_Name

def randomize(): #Define our random case with a separate function
	shards2 = []
	for i in range(len(Server_Name)-1): #Fill our first 9 Servers - piece of cake
		while len(Server_Name["S_"+str(i+1)]) < 20 :
			n = random.choice(shards)
			if n not in Server_Name["S_"+str(i+1)]:
				Server_Name["S_"+str(i+1)].append(n)
				shards.remove(n) #Very important trick to make sure we are not duplicating shards
	for item in shards:
		if item not in Server_Name["S_10"]:
			Server_Name["S_10"].append(item)
		else:
			shards2.append(item)
	#If there are 2 identical shards left for the 10th Server - just substitute them from S_1 - silly and simple
	for copy in shards2:
		flag = 0
		for unique_item in Server_Name["S_1"]:
			if flag == 0:
				if unique_item not in Server_Name["S_10"]:
					Server_Name["S_10"].append(unique_item)
					Server_Name["S_1"].append(copy)
					Server_Name["S_1"].remove(unique_item)
					flag += 1
	return Server_Name

if y == "--mirror":
	mirror()
elif y == "--random":
	randomize()
else:
	print ("Some troubleshooting is required!!!")

#Now lets Compare Each server
for i in range(1,len(Server_Name)+1):
	for j in range(i+1,len(Server_Name)+1):
	#print Server_Name["S_"+str(i)], len(Server_Name["S_"+str(i)]), len(set(Server_Name["S_"+str(i)]))
	#print Server_Name["S_"+str(i+1)], len(Server_Name["S_"+str(i+1)]), len(set(Server_Name["S_"+str(i+1)]))
		if set(Server_Name["S_"+str(i)]).intersection(set(Server_Name["S_"+str(j)])):
			counter += 1

N = round((float(counter)/C)*100, 2)
#print shards
#print Server_Name["S_10"]
#for i in range(1,len(Server_Name)+1):
	#print Server_Name["S_"+str(i)]
Message = "Killing 2 arbitrary servers results in data loss in %d" % N
print (Message +" % cases")
