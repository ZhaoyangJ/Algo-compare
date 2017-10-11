# COMP3331 Assignment II
# Yikai Wang & Zhaoyang Jin
# Start: 20 Sep 17
# Finish: 

from sets import Set
from collections import defaultdict
from threading import Thread
from time import time

class Graph(object):
	def __init__(self,filename):
		fo = open(filename, "r")
		self.data = fo.read()
		fo.close()
		self.edge = self.init_edge()
		self.map = self.init_map()


	def init_edge(self):
		new = self.data.split('\r\n')
		d = {}
		for i in new:
			temp = i.split()
			src1 = (temp[0], temp[1])
			src2 = (temp[1], temp[0])
			dest = (False, temp[2], temp[3])
			d[src1] = dest
			d[src2] = dest
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
		print ""
		print "maps: \n",self.map

	def activate_edge(self, tup):
		self.edge[tup] = (True,) + self.edge[tup][1:]
		self.edge[tup[::-1]] = (True,) + self.edge[tup[::-1]][1:]

def count_time(e, g):
	if time()-start == e[0]:
		(e[1],e[2])



g = Graph("topology.txt")
g.show()
g.activate_edge(("G", "H"))
g.show()

start = time()

s = Thread()
s.start()


# class Graph(object):
# 	"""
# 		initialize a graph object
# 		if no dictionary or none is given,
# 		an empty dictionary will be used	
# 	"""
# 	def __init__(self, graph_dict = None):
# 		if graph_dict == None:
# 			graph_dict = {}
# 		self.__graph_dict = graph_dict

# 	def Node(self):
# 		return list(self.__graph_dict.keys())

# 	def edge(self):
# 		return self.__generate_edge()

# 	def InsertNode(self, node):
# 		if node not in self.__graph_dict:
# 			self.__graph_dict[node] = []

# 	def add_edge(self, edge):
# 		edge = set(edge)
# 		(node1, node2) = tuple(edge)
# 		if node1 in self.__graph_dict:
# 			self.__graph_dict[node1].append(node2)
# 		else:
# 			self.__graph_dict[node1] = [node2]

# 	def __generate_edge(self):
# 		edge = []
# 		for node in self.__graph_dict:
# 			for neighbour in self.__graph_dict[node]:
# 				if {neighbour, node} not in edge:
# 					edge.append({node, neighbour})
# 		return edge

# 	def __str__(self):
# 		res = "Node: "
# 		for k in self.__graph_dict:
# 			res += str(k) + " "
# 		res += "\nedge: "
# 		for edge in self.__generate_edge():
# 			res += str(edge) + " "
# 		return res

# 	def find_path(self, start_node, end_node, path = None):
# 		if path == None: # if no path/link then set up a new set
# 			path = []
# 		graph = self.__graph_dict 
# 		path = path + [start_node] # put the current starting node to the list
# 		if start_node == end_node: # if 2 nodes passed in are the same node
# 			return path
# 		if start_node not in graph: # if the node is not in graph at all, then there will be no path at all
# 			return None
# 		for node in graph[start_node]:
# 			if node not in path:
# 				extended_path = self.find_path(node, end_node, path)
# 				if extended_path:
# 					return extended_path
# 		return None
