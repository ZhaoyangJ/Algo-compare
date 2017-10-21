import time



txt = open("workload.txt")

content = txt.readlines()

for i in range(len(content)):
	content[i] = content[i].strip().split()



org = time.time()

c = 0 
while c<len(content):
	current = time.time()
	if current-org >= float(content[c][0]):
		print("now:", current-org)
		c+=1



