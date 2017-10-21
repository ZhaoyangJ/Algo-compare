# COMP3331 Assignment II
# Yikai Wang & Zhaoyang Jin
# Start: 20 Sep 17
# Finish: 

from sets import Set
from collections import defaultdict
from threading import Thread
from time import time
import Queue

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
			self.load[src1] = 0
			self.load[src2] = 0
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

	def get_vertex(self):
		nodes = self.map.keys()
		return nodes

	# def activate_edge(self, tup): # change (this,,) one to True
	# 	self.edge[tup] = (True,) + self.edge[tup][1:]
	# 	self.edge[tup[::-1]] = (True,) + self.edge[tup[::-1]][1:]

class send(object):

	def __init__(self, g, rate):
		self.ttlrq=0
		self.ttlp=0
		self.numsp=0
		self.percsp=0.00
		self.numbp=self.ttlp-self.numsp
		self.percbp=100-self.percsp
		self.avghpc=0
		self.avgpdpc=0

		self.p={}
		self.rate = rate
		# self.enable(g, "LLP", ["A", "D", 0.88887])
		self.start(g, "LLP")

	def start(self, g, alg):
		txt = open("workload.txt")
		content = txt.readlines()
		S={}
		T={}
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

		print start_t[0]
		print stop_t

		org = time()
		while len(start_t) != 0 or len(stop_t) != 0:
			current = time()
			if len(start_t) != 0:
				if (current-org) >= start_t[0]:
					print("enable: ", S[start_t[0]], current-org)
					if self.enable(g, alg, S[start_t[0]]) == False:
						stop_t.remove(float(start_t[0]) + float(S[start_t[0]][2]))
					start_t.remove(start_t[0])
					print " "
			if len(stop_t) != 0:
				if current-org >= stop_t[0]:
					print("disable:", T[stop_t[0]], current-org)
					self.disable(g, T[stop_t[0]])
					stop_t.remove(stop_t[0])
					print ""

	def enable(self, g, alg, nodes):

		s = solution(g, alg, nodes[0], nodes[1])
		if alg=="LLP":
			path = self.find_minLoad(g, s.paths)
		else:
			path = self.path_split(s.path)
		# print "path for ", nodes, " = ", path
		if self.path_valid(path):
			self.numsp += int(float(nodes[2])*self.rate)
			for i in path:
				if g.edge[i][0]:
					if g.load[i] == g.edge[i][2]-1:
						print "Blocking the path: ", i
						g.edge[i][0] = False
					g.load[i] += 1
					self.p[(nodes[0], nodes[1])] = path
			print nodes[2]
		else:
			print "Blocked"
			print nodes[2]
			self.numbp += int(float(nodes[2])*self.rate)
			return False

	def find_minLoad(self, g, paths):
		minLoad=[]
		min = 1
		for i in paths:
			print i
			new = self.path_split(i)
			m = []
			for l in new:
				m.append(float(g.load[l])/float(g.edge[l][2]))
			m=sorted(m)
			print m
			if m[-1] <= min:
				min=m[0]
				minLoad=new
			print ""
		print minLoad
		return minLoad

	def path_split(self, path):
		pathSplited = []
		c=0
		while c + 1 < len(path):
			pathSplited.append((path[c], path[c+1]))
			c += 1
		return pathSplited

	def path_valid(self, pathSplited):
		det = 1
		for i in pathSplited:
			if g.edge[i][0] == False:
				det = 0
		return det

	def disable(self, g, nodes):

		path = self.p[(nodes[0], nodes[1])]
		for i in path:
			g.load[i] -= 1
			if g.load[i] < g.edge[i][2]:
				g.edge[i][0] = True
				print "reactivated"

		# print g.edge

	def show(self):
		self.percsp = 100 * float(self.numsp)/float(self.ttlp)
		print "total number of virtual connection requests: ", self.ttlrq
		print "total number of packets: ", self.ttlp
		print "number of successfully routed packets: ", self.numsp
		print "percentage of successfully routed packets:", self.percsp
		print "number of blocked packets: ", self.numbp
		print "percentage of blocked packets: ", 100 - self.percsp
		print "average number of hops per circuit: ", self.avghpc
		print "average number of hops per circuit: ", self.avgpdpc

		

class solution(object):

	def __init__(self, g, alg, src, dest):
		self.maps = g.map
		self.edge = g.edge
		if alg == "SHP":
			self.path = self.SHP(g, src, dest)
		elif alg == "SDP":
			self.path = self.SDP(g, src, dest)
		elif alg == "LLP":
			self.paths = self.LLP(g, src, dest)
			print self.paths

	def SHP(self, g, src, dest):
		D={}
		Pred = {}
		visited = []
		unvisited=g.get_vertex()

		for i in unvisited:
			D[i]=999
		D[src]=0
		Pred[src] = None
		q = [src]

		while len(unvisited) != 0: #while unvisited is not empty
			# for unvisited nearby vertex
			#print "uv = ", unvisited
			
			cur = self.get_min(unvisited, D)
			q.remove(cur)
			for v in self.maps[cur]:
				if v in visited:
					continue
				temp=D[cur]+1#<- 1 could be replaced by weight
				if temp < D[v]:
					D[v] = temp
					Pred[v]=cur
					q.append(v)

			unvisited.remove(cur)
			visited.append(cur)
			# print "v = ", visited
			# print "q = ", q

		path = []
		v = dest
		while v != None:
			path.append(v)
			v = Pred[v]

		path.reverse()
		return path
				
	def get_min(self, l, D):
		min = D[l[0]]
		value = l[0]
		for i in l:
			if D[i] < min:
				min=D[i]
				value=i
		return value

	def SDP(self, g, src, dest):

		D={}
		Pred = {}
		visited = []
		unvisited=g.get_vertex()

		for i in unvisited:
			D[i]=999
		D[src]=0
		Pred[src] = None
		q = [src]

		while len(unvisited) != 0: #while unvisited is not empty
			# for unvisited nearby vertex
			cur = self.get_min(unvisited, D)
			q.remove(cur)
			for v in self.maps[cur]:
				if v in visited:
					continue
				temp=D[cur] + g.edge[(cur, v)][1]#<- 1 could be replaced by weight
				if temp < D[v]:
					D[v] = temp
					Pred[v]=cur
					if v not in q:
						q.append(v)

			unvisited.remove(cur)
			visited.append(cur)
			# print "uv = ", unvisited
			# print "v = ", visited
			# print "q = ", q

		path = []
		v = dest
		while v != None:
			path.append(v)
			v = Pred[v]

		path.reverse()
		return path

	def LLP(self, g, src, dest, path=[]):
		path = path + [src]
		if src == dest:
			return [path]
		# if not g.maps[src]:
		#     return []
		paths = []
		for node in g.map[src]:
			if node not in path:
				newpaths = self.LLP(g, node, dest, path)
				for newpath in newpaths:
					paths.append(newpath)
		return paths


packetRate = 2

g = Graph("topology.txt")
g.show()
# g.activate_edge(("G", "H"))
g.show()
g.get_vertex()
s = send(g, 2)
# s = send(g, packetRate)
# s.show()
