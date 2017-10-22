# COMP3331 Assignment II
# Yikai Wang & Zhaoyang Jin
# Start: 20 Sep 17
# Finish: 

from sets import Set
from collections import defaultdict
from threading import Thread
from time import time
import sys

if (len(sys.argv) != 6):
	print "Invalid input"
	exit(1)

network = sys.argv[1]
alg = sys.argv[2]
topology = sys.argv[3]
workload = sys.argv[4]
packetRate = int(sys.argv[5])

# network = "CIRCUIT"
# alg = "SDP"
# topology = "topology.txt"
# workload = "workload.txt"
# packetRate = 1

class Graph(object):
	def __init__(self,filename):
		fo = open(filename, "r")
		self.data = fo.read()
		fo.close()
		self.load = {}
		self.edge = self.init_edge()
		self.map = self.init_map()

	def init_edge(self):
		new = self.data.split('\r\n')
		d = {}
		for i in new:
			temp = i.split()
			src1 = (temp[0], temp[1])
			src2 = (temp[1], temp[0])
			dest = [True, int(temp[2]), int(temp[3])]
			d[src1] = dest
			d[src2] = dest
			a = [0]
			self.load[src1] = a
			self.load[src2] = a
		return d

	def init_map(self):
		new = self.data.split('\r\n')
		d = defaultdict(list)
		for i in new:
			temp = i.split()
			d[temp[0]].append(temp[1])
			d[temp[1]].append(temp[0])
		return d

	def show(self):
		print "edges:\n",self.edge
		print ""
		print "load:\n", self.load
		print ""
		print "maps: \n",self.map
		print ""
		print ""

	def get_vertex(self):
		nodes = self.map.keys()
		return nodes

	# def activate_edge(self, tup): # change (this,,) one to True
	# 	self.edge[tup] = (True,) + self.edge[tup][1:]
	# 	self.edge[tup[::-1]] = (True,) + self.edge[tup[::-1]][1:]

class routing(object):

	def __init__(self, g, workload, alg, rate):
		self.ttlrq=0
		self.ttlp=0
		self.numsp=0
		self.percsp=0.00
		self.numbp=self.ttlp-self.numsp
		self.percbp=100-self.percsp
		self.ttlhpc=0
		self.ttlpdpc=0
		self.ttlsrq=0
		self.ttlbrq=0

		self.p={} # p[finish time] -> paths need to be reactivated
		self.rate = rate
		self.start(g, workload, alg)

	def start(self, g, workload, alg):
		txt = open(workload)
		content = txt.readlines()
		txt.close()

		S={} # S[start_time] -> [src, dest, duration]
		T={} # T[stop_time] -> [src, dest]
		start_t=[]
		stop_t=[]
		self.ttlrq=len(content)
		for i in range(len(content)):
			content[i] = content[i].strip().split()

		for i in range(len(content)):
			self.ttlp += int(float(content[i][3])*self.rate)

			start = float(content[i][0])
			S[start] = [content[i][1], content[i][2], content[i][3]]
			start_t.append(start)

			stop = float(content[i][3]) + float(content[i][0])
			T[stop] = [content[i][1], content[i][2]]
			stop_t.append(stop)

		stop_t = sorted(stop_t)

		org = time()
		while len(start_t) != 0 or len(stop_t) != 0:
			current = time()
			if len(start_t) != 0:
				if (current-org) >= start_t[0]/float(100):
					# print "enable: ", S[start_t[0]], " at ", current-org
					if self.enable(g, alg, S[start_t[0]], start_t[0] + float(S[start_t[0]][2])) == False:
						stop_t.remove(start_t[0] + float(S[start_t[0]][2]))
						# print "Removed"
					start_t.remove(start_t[0])
					# print " "
			if len(stop_t) != 0:
				if current-org >= stop_t[0]/float(100):
					# print "disable:", T[stop_t[0]], " at ", current-org
					self.disable(g, stop_t[0])
					stop_t.remove(stop_t[0])
					# print ""

	def enable(self, g, alg, nodes, t):

		s = solution(g, alg, nodes[0], nodes[1])
		# if alg=="LLP":
		# 	path = self.find_minLoad(g, s.paths)
		# else:
		path = self.path_split(s.path)

		if self.path_valid(path):
			self.ttlsrq+=1
			self.ttlhpc += (len(path))
			ppgd=0
			for i in path: 
				ppgd += g.edge[i][1]
			self.ttlpdpc += ppgd
			self.numsp += int(float(nodes[2])*self.rate)

			for i in path:
				# if g.edge[i][0]:
				if g.load[i][0] == g.edge[i][2]-1:
					# print "Blocking the path: ", i, " lasts ", nodes[2]
					g.edge[i][0] = False
				g.load[i][0] += 1
			self.p[round(t,6)] = path 	
		else:
			# print "Blocked"
			self.numbp += int(float(nodes[2])*self.rate)
			self.ttlbrq+=1
			return False

	def path_valid(self, pathSplited):
		for i in pathSplited:
			if g.edge[i][0] == False:
				return 0
		return 1

	def find_minLoad(self, g, paths):
		minLoad=[]
		min = 1
		# print ""
		# print "all possible paths:"
		for i in paths:
			# print i
			new = self.path_split(i)
			m = []
			for l in new:
				m.append(float(g.load[l][0])/float(g.edge[l][2]))
			m=sorted(m)
			# print m[-1]
			if m[-1] <= min:
				min=m[-1]
				minLoad=new
			# print ""
		# print "minLoad = ", minLoad
		return minLoad

	def path_split(self, path):
		pathSplited = []
		c=0
		while c + 1 < len(path):
			pathSplited.append((path[c], path[c+1]))
			c += 1
		return pathSplited



	def disable(self, g, t):

		path = self.p[round(t,6)]
		for i in path:
			g.load[i][0] -= 1
			if g.load[i][0] < g.edge[i][2]:
				g.edge[i][0] = True
				# print "reactivated : ", i
			

		# print g.edge

	def show(self):
		self.percsp = 100 * float(self.numsp)/float(self.ttlp)
		print "total number of virtual connection requests: ", self.ttlrq
		print "total number of packets: ", self.ttlp
		print "number of successfully routed packets: ", self.numsp
		print "percentage of successfully routed packets:", self.percsp
		print "number of blocked packets: ", self.numbp
		print "percentage of blocked packets: ", 100 - self.percsp
		print "average number of hops per circuit: ", float(self.ttlhpc)/float(self.ttlsrq)
		print "average cumulative propagation delay per circuit: ", float(self.ttlpdpc)/float(self.ttlsrq)
		print "succesful request : ", self.ttlsrq
		print "blocked request : ", self.ttlbrq

class solution(object):

	def __init__(self, g, alg, src, dest):
		self.maps = g.map
		self.edge = g.edge
		self.path = self.dijkstra(g, src, dest, alg)

	def dijkstra(self, g, src, dest, alg):
		D={}
		Pred = {}
		visited = []
		unvisited=g.get_vertex()

		for i in unvisited:
			D[i]=999
		D[src]=0
		Pred[src] = None
		# q = [src]
		cur = self.get_min(unvisited, D)
		while len(unvisited) != 0 and cur != dest:
			# q.remove(cur)
			for v in g.map[cur]:
				if v in visited:
					continue
				if alg == "SHP":
					temp=D[cur]+1
				elif alg == "SDP":
					temp=D[cur] + g.edge[(cur, v)][1]
				elif alg == "LLP":
					temp = float(g.load[(cur, v)][0])/float(g.edge[(cur, v)][2])
					if temp < D[cur]:
						temp = D[cur]
				if temp < D[v]:
					D[v] = temp
					Pred[v]=cur
					# q.append(v)

			unvisited.remove(cur)
			visited.append(cur)
			cur = self.get_min(unvisited, D)
			# print "v = ", visited
			# print "q = ", q

		path = []
		v = dest
		while v != None:
			path.append(v)
			v = Pred[v]

		path.reverse()
		return path

	# def SHP(self, g, src, dest):
	# 	return
				
	def get_min(self, l, D):
		min = D[l[0]]
		value = l[0]
		for i in l:
			if D[i] < min:
				min=D[i]
				value=i
		return value

g = Graph(topology)
g.show()
g.get_vertex()

r = routing(g, workload, alg, packetRate)
r.show()