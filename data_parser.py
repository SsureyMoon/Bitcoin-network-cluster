import re
import pprint
import math
import requests
import pickle
import json
import os.path
import random
import operator
import networkx as nx
import matplotlib.pyplot as plt
import community

MAX_DEPTH = 2
MAX_HEIGHT = 1000
MAX_WIDTH = 1000

#dictionary = requests.get("https://blockchain.info/address/"+origin+"?format=json").json()
#txs = dictionary[u'txs']
#del dictionary

class BTCNetwork:

    def __init__(self):
        self.full_set = set()
        self.associated_addr = list()

    def get_associated_addr(self, source_addr, depth):

        if source_addr in self.full_set:
            return
        else:
            self.full_set.add(source_addr)
            dictionary = requests.get("https://blockchain.info/address/"+source_addr+"?format=json").json()
            txs = dictionary[u'txs']
            local_set = set()
            for tx in txs:
                inputs = tx[u'inputs']
                for input in inputs:
                    addr = str(input[u'prev_out'][u'addr'])
                    if addr != source_addr:
                        self.associated_addr.append((source_addr, addr, depth))
                        local_set.add(addr)

                outputs = tx[u'out']
                for output in outputs:
                    addr = str(output[u'addr'])
                    if addr != source_addr:
                        self.associated_addr.append((source_addr, addr, depth))
                        local_set.add(addr)

            if depth == MAX_DEPTH:
                return
            else:
                for local_addr in local_set:
                    self.get_associated_addr(local_addr, depth+1)

    def PointsInCircum(self, c=None, r=25,n=100):
        if not c:
            c = (500, 500)
        circular_points = [((math.cos(2* math.pi /n*x)*r+c[0]), (math.sin(2*math.pi/n*x)*r)+c[1]) for x in xrange(0, n+1)]
        return circular_points

    def get_nodes(self, center):
            while True:
                x = random.random()*1000
                y = random.random()*1000
                dist = math.hypot(center[0]-x, center[1]-y)
                if dist > (MAX_WIDTH/8+10):
                    break
            return x, y

    def data_parse(self, origin):


        if os.path.exists('data/'+origin+'.pkl'):
            pkl_file = open('data/'+origin+'.pkl', 'rb')
            self.associated_addr = data = pickle.load(pkl_file)
        else:
            self.get_associated_addr(origin, 0)
            output = open('data/'+origin+'.pkl', 'wb')
            pickle.dump(self.associated_addr, output)

        counter_depth2 = 0
        for addr_tuple in self.associated_addr:
            if addr_tuple[2] == 1:
                counter_depth2 += 1



        CENTER = (MAX_WIDTH/2, MAX_HEIGHT/2)
        axis = dict()
        axis[origin] = (0, CENTER)
        index = 1

        points_depth2 = self.PointsInCircum(CENTER, (MAX_WIDTH/8), counter_depth2)
        for addr_tuple in self.associated_addr:
            if addr_tuple[1] not in axis:
                axis[addr_tuple[1]] = (index, points_depth2.pop() if addr_tuple[2] == 1 else self.get_nodes(CENTER))
                index += 1

        links = list()
        #get links list
        for addr_tuple in self.associated_addr:
            links.append({"source":axis[addr_tuple[0]][0],\
                   "target": axis[addr_tuple[1]][0]})

        nodes = list()

        sorted_x = sorted(axis.items(), key=operator.itemgetter(1))
        for key, index_xy_tuple in sorted_x:
            xy_tuple = index_xy_tuple[1]
            nodes.append({"x":xy_tuple[0], "y":xy_tuple[1], "address":key})

        return nodes, links

    def data_clust(self, origin, nodes, links):

        edge_list = [tuple(elem.values()) for elem in links]

        g = nx.Graph()
        g.add_edges_from(edge_list)

        #clust_coefficients = nx.clustering(g)
        partition = community.best_partition(g)

        clustered_nodes = nodes


        part_set = set()
        number_of_clusters = 0
        for i, node in enumerate(clustered_nodes):
            node['cluster'] = partition[i]
            if partition[i] not in part_set:
                part_set.add(partition[i])
                number_of_clusters += 1

        return clustered_nodes, links, number_of_clusters



