class Graph(object):
	"""
		initialize a graph object
		if no dictionary or none is given,
		an empty dictionary will be used	
	"""
	def __init__(self, graph_dict = None):
		if graph_dict == None:
			graph_dict = {}
		self.__graph_dict = graph_dict

	def Node(self):
		return list(self.__graph_dict.keys())

	def edge(self):
		return self.__generate_edge()

	def InsertNode(self, node):
		if node not in self.__graph_dict:
			self.__graph_dict[node] = []

	def add_edge(self, edge):
		edge = set(edge)
		(node1, node2) = tuple(edge)
		if node1 in self.__graph_dict:
			self.__graph_dict[node1].append(node2)
		else:
			self.__graph_dict[node1] = [node2]

	def __generate_edge(self):
		edge = []
		for node in self.__graph_dict:
			for neighbour in self.__graph_dict[node]:
				if {neighbour, node} not in edge:
					edge.append({node, neighbour})
		return edge

	def __str__(self):
		res = "Node: "
		for k in self.__graph_dict:
			res += str(k) + " "
		res += "\nedge: "
		for edge in self.__generate_edge():
			res += str(edge) + " "
		return res

	def find_path(self, start_node, end_node, path = None):
		if path == None: # if no path/link then set up a new set
			path = []
		graph = self.__graph_dict 
		path = path + [start_node] # put the current starting node to the list
		if start_node == end_node: # if 2 nodes passed in are the same node
			return path
		if start_node not in graph: # if the node is not in graph at all, then there will be no path at all
			return None
		for node in graph[start_node]: # 这里怎么理解好
			if node not in path:
				extended_path = self.find_path(node, end_node, path)
				if extended_path:
					return extended_path
		return None
