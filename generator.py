import random
import math
import copy


class Generator:

    def __init__(self, height, depth, cnt_nodes, capacity):
        self.height = height
        self.depth = depth
        self.cnt_nodes = cnt_nodes
        self.capacity = capacity

    def build_graph(self):
        nodelist, node_candidate_list = self.get_distance_list()
        edges = []
        hmap = {}
        for node,candidate_list in node_candidate_list:
            hmap[node] = candidate_list

        while True:

            overall_added=False
            for node in nodelist:
                for candidate in hmap[node]:
                    intersection=False

                    for edge in edges:
                        left,right=self.check_double_occurence(node,candidate,edge)
                        if left or right: continue
                        if self.intersect(node,candidate,edge.source,edge.target):
                            intersection=True
                            break

                    if not intersection:
                        weight = random.randint(0,self.capacity)
                        edge = Edge(weight,node,candidate)
                        edges.append(edge)
                        hmap[candidate].remove(node)
                        hmap[node].remove(candidate)
                        node.edges.append(edge)
                        overall_added=True
                        break
            if not overall_added:break

        for edge in copy.deepcopy(edges):
            new_edge = Edge(edge.weight, edge.target, edge.source)
            edge.target.edges.append(new_edge)
            edges.append(new_edge)

        graph = Graph(nodelist, edges)
        return graph

    def check_double_occurence(self,node,candidate,edge):
        target_edge = edge.target
        source_edge = edge.source
        left=right=False
        if node == target_edge or node == source_edge:left=True
        if candidate==target_edge or candidate==source_edge: right=True
        return left,right


    def get_distance_list(self):
        nodelist = []

        for cntr in range(self.cnt_nodes):
            xcoord = random.randint(0, self.depth)
            ycoord = random.randint(0, self.height)

            node = Node(xcoord, ycoord,cntr)
            nodelist.append(node)

        node_candidate_list = []
        for node in nodelist:
            node_dist = []
            for target_node in nodelist:
                dist = self.get_distance(node, target_node)
                if dist==0: continue
                node_dist.append((dist, target_node))
            node_dist.sort(key=lambda x: x[0])
            node_candidate_list.append((node, [x[1]for x in node_dist]))
        return nodelist, node_candidate_list

    def ccw(self, A, B, C):
        return (C.y - A.y) * (B.x - A.x) > (B.y-1 - A.y-1) * (C.x - A.x)

    # Return true if line segments AB and CD intersect
    def intersect(self, A, B, C, D):
        return self.ccw(A, C, D) != self.ccw(B, C, D) and self.ccw(A, B, C) != self.ccw(A, B, D)

    def get_distance(self, node1, node2):
        dist = math.sqrt((node1.x - node2.x) ** 2 + (node1.y - node2.y) ** 2)
        return dist


class Node:
    def __init__(self, x, y,i):
        self.i = i
        self.x = x
        self.y = y
        self.edges = []


class Edge:
    def __init__(self, weight, node1, node2):
        self.weight = weight
        self.source = node1
        self.target = node2


class Graph:
    def __init__(self, nodes, edges):
        self.nodes = nodes
        self.edges = edges
