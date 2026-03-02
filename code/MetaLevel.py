import csv
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import time
from memory_profiler import memory_usage

def measure_memory_usage():
    mem_usage_before = memory_usage()[0]* 1024 * 1024
    mem_usage_after = memory_usage()[0]* 1024 * 1024
    memory_used = mem_usage_after - mem_usage_before
    return memory_used

class Product:
    def __init__(self, name, production, season, price, consumption, size_of_land_used):
        self.name = name
        self.production = production
        self.season = season
        self.price = price
        self.consumption = consumption
        self.size_of_land_used = size_of_land_used

class Wilaya:
    def __init__(self, name):
        self.name = name.capitalize()  # Capitalize the first letter
        self.products = []

    def add_product(self, product):
        self.products.append(product)

class Graph:
    def __init__(self):
        self.wilayas = {}
        self.adjacency_list = {}

    def add_wilaya(self, wilaya_name):
        wilaya_name = wilaya_name.lower()  # Convert to lowercase
        wilaya_name = wilaya_name.capitalize()  # Capitalize the first letter
        if wilaya_name not in self.wilayas:
            self.wilayas[wilaya_name] = Wilaya(wilaya_name)
            self.adjacency_list[wilaya_name] = []

    def add_product_to_wilaya(self, wilaya_name, product):
        wilaya_name = wilaya_name.lower()  # Convert to lowercase
        wilaya_name = wilaya_name.capitalize()  # Capitalize the first letter
        if wilaya_name in self.wilayas:
            self.wilayas[wilaya_name].add_product(product)

    def connect_wilayas(self, wilaya1, wilaya2):
        wilaya1 = wilaya1.lower()  # Convert to lowercase
        wilaya1 = wilaya1.capitalize()  # Capitalize the first letter
        wilaya2 = wilaya2.lower()  # Convert to lowercase
        wilaya2 = wilaya2.capitalize()  # Capitalize the first letter
        if wilaya1 in self.wilayas and wilaya2 in self.wilayas:
            self.adjacency_list[wilaya1].append(wilaya2)
            self.adjacency_list[wilaya2].append(wilaya1)


class TreeNode:
    def __init__(self, graph, name, year):
        self.graph = graph
        self.name = name
        self.year = year
        self.children = []

    def add_child(self, child_node):
        self.children.append(child_node)

class Tree:
    def __init__(self, root=None):
        self.root = root

    def add_node(self, parent_name, graph, name, year):
        parent_node = self.find_node(self.root, parent_name)
        if parent_node is not None:
            new_node = TreeNode(graph, name, year)
            parent_node.add_child(new_node)
        else:
            print(f"Parent node '{parent_name}' not found.")

    def find_node(self, node, name):
        if node is None:
            return None
        if node.name == name:
            return node
        for child in node.children:
            result = self.find_node(child, name)
            if result is not None:
                return result
        return None

    def traverse(self, node, level=0):
        if node is not None:
            print(" " * level * 2 + node.name)
            for child in node.children:
                self.traverse(child, level + 1)

    def search_product(self, product_name):
        highest_production_by_wilaya = {}

        def search_node(node):
            for wilaya in node.graph.wilayas.values():
                for product in wilaya.products:
                    if product.name == product_name:
                        if wilaya.name not in highest_production_by_wilaya:
                            highest_production_by_wilaya[wilaya.name] = {
                                "highest_production": product.production,
                                "year": node.year,
                                "land_used": product.size_of_land_used
                            }
                        else:
                            if product.production > highest_production_by_wilaya[wilaya.name]["highest_production"]:
                                highest_production_by_wilaya[wilaya.name] = {
                                    "highest_production": product.production,
                                    "year": node.year,
                                    "land_used": product.size_of_land_used
                                }
            for child in node.children:
                search_node(child)

        search_node(self.root)

        return highest_production_by_wilaya

def load_wilaya_data_from_csv(filename, year, graph):
    with open(filename, mode='r', newline='', encoding='utf-8') as file:
        csv_reader = csv.reader(file, delimiter=',')
        headers = next(csv_reader)
        for row in csv_reader:
            if len(row) >= 7:  
                wilaya_name = row[0].strip().lower()  # Convert to lowercase
                wilaya_name = wilaya_name.capitalize()  # Capitalize the first letter
                product_name = row[1].strip()
                production = float(row[2]) if row[2].strip() else 0.0
                season = row[4].strip()
                try:
                    size_of_land_used = float(row[3])
                except ValueError:
                    size_of_land_used = 0.0
                price = float(row[5])
                consumption = float(row[6])
                product = Product(product_name, production, season, price, consumption, size_of_land_used)
                graph.add_wilaya(wilaya_name)
                graph.add_product_to_wilaya(wilaya_name, product)

def load_graph_from_csv(filename):
    graph = Graph()
    with open(filename, mode='r', newline='', encoding='utf-8') as file:
        csv_reader = csv.reader(file, delimiter=',')
        for row in csv_reader:
            if row and row[0]:  
                wilaya = row[0].strip().lower()  # Convert to lowercase
                wilaya = wilaya.capitalize()  # Capitalize the first letter
                if len(row) > 1:
                    neighbors_raw = row[1].strip().strip('"')  
                    neighbors = [neighbor.strip().lower().capitalize() for neighbor in neighbors_raw.split(',')]  # Convert to lowercase and capitalize the first letter
                    graph.add_wilaya(wilaya)
                    for neighbor in neighbors:
                        graph.add_wilaya(neighbor)
                        graph.connect_wilayas(wilaya, neighbor)  

    return graph

def main():

    start_time = time.time()

    graph_2016 = Graph()
    load_wilaya_data_from_csv('Data/2016.csv', 2016, graph_2016)
    graph_2017 = Graph()
    load_wilaya_data_from_csv('Data/2017.csv', 2017, graph_2017)
    graph_2018 = Graph()
    load_wilaya_data_from_csv('Data/2018.csv', 2018, graph_2018)
    graph_2019 = Graph()
    load_wilaya_data_from_csv('Data/2019.csv', 2019, graph_2019)

    root_node = TreeNode(graph_2016, "Graph 2016", 2016)
    tree = Tree(root_node)

    tree.add_node("Graph 2016", graph_2017, "Graph 2017", 2017)
    tree.add_node("Graph 2016", graph_2018, "Graph 2018", 2018)
    tree.add_node("Graph 2016", graph_2019, "Graph 2019", 2019)

    print("Welcome to the Meta Level side of the Production Analysis and Optimization System!")
    # Example of searching for a product
    product_name = input("Enter product name to search: ")
    result = tree.search_product(product_name)
    print("THE BEST PRODUCTION SCENARIO OF ", product_name, " :")
    for wilaya, data in result.items():
        print(f"Wilaya: {wilaya}, Year: {data['year']}, Highest Production: {data['highest_production']}, Land Used: {data['land_used']}")

    execution_time = time.time() - start_time
    print(f"Execution time: {execution_time:.2f} seconds")
    memory_usage = measure_memory_usage()
    print("Memory Usage (bytes):", memory_usage)

if __name__ == "__main__":
    main()
