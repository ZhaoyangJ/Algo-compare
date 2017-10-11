from time import time, sleep

fo = open("workload.txt", "r")
data = fo.read()
fo.close()

new = data.split('\r\n')
a = 0
i = new[0]
start = time()
print (float)i[0]
while 1:
	if i[0] == (time()-start):
		print i[0], " passed\n"
		a += 1
		i = new[a]