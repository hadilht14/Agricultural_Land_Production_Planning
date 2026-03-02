import csv
from collections import deque
import heapq
import time
import matplotlib.pyplot as plt
import networkx as nx
import seaborn as sns
from memory_profiler import memory_usage


def measure_memory_usage():
    mem_usage_before = memory_usage()[0]* 1024 * 1024
    mem_usage_after = memory_usage()[0]* 1024 * 1024
    memory_used = mem_usage_after - mem_usage_before
    return memory_used


class Product:
    def __init__(self, name, production, season, price, consumption):
        self.name = name
        self.production = production
        self.season = season
        self.price = price
        self.consumption = consumption

class Wilaya:
    def __init__(self, name):
        self.name = name
        self.products = []

    def add_product(self, product):
        self.products.append(product)

class Graph:
    def __init__(self):
        self.wilayas = {}
        self.adjacency_list = {}

    def add_wilaya(self, wilaya_name):
        if wilaya_name not in self.wilayas:
            self.wilayas[wilaya_name] = Wilaya(wilaya_name)
            self.adjacency_list[wilaya_name] = []

    def add_product_to_wilaya(self, wilaya_name, product):
        if wilaya_name in self.wilayas:
            self.wilayas[wilaya_name].add_product(product)

    def connect_wilayas(self, wilaya1, wilaya2):
        if wilaya1 in self.wilayas and wilaya2 in self.wilayas:
            self.adjacency_list[wilaya1].append(wilaya2)
            self.adjacency_list[wilaya2].append(wilaya1)

    def visualize_graph(self):
        G = nx.Graph()
        for wilaya, neighbors in self.adjacency_list.items():
            for neighbor in neighbors:
                G.add_edge(wilaya, neighbor)

        # Increase the distance between nodes
        pos = nx.spring_layout(G, k=12)  # Adjust the value of k as needed

        plt.figure(figsize=(10, 8))
        nx.draw(G, pos, with_labels=True, node_color='skyblue', node_size=50, edge_color='gray', font_size=10)
        plt.title('Wilaya Connections Graph')
        plt.show()


    def visualize_production(self, season):
        wilaya_names = []
        product_names = []
        productions = []

        for wilaya in self.wilayas.values():
            for product in wilaya.products:
                if product.season == season:
                    wilaya_names.append(wilaya.name)
                    product_names.append(product.name)
                    productions.append(product.production)

        data = {
            'Wilaya': wilaya_names,
            'Product': product_names,
            'Production': productions
        }

        plt.figure(figsize=(12, 6))
        ax = sns.barplot(x='Wilaya', y='Production', hue='Product', data=data)

        # Rotate x-axis labels vertically for better readability
        ax.set_xticklabels(ax.get_xticklabels(), rotation=90, ha='center')

        # Move the legend outside the plot
        plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')

        plt.title(f'Production Data for Season: {season}')
        plt.tight_layout()  # Adjust layout to prevent clipping of labels
        plt.yscale('log')
        plt.show()

    def dfs_search_product(self, searched_wilaya, search_season, search_by):
        if searched_wilaya not in self.wilayas:
            print("Wilaya not found in the graph.")
            return

        start_wilaya = self.wilayas[searched_wilaya]
        stack = [start_wilaya]
        visited = set()
        best_production = {}
        best_price = {}

        while stack:
            current_wilaya = stack.pop()
            if current_wilaya.name in visited:
                continue
            visited.add(current_wilaya.name)

            for product in current_wilaya.products:
                if product.season == search_season:
                    if search_by == 1:
                        if product.name not in best_production or product.production > best_production[product.name]:
                            is_best = True

                            for neighbor_name in self.adjacency_list[current_wilaya.name]:
                                neighbor_wilaya = self.wilayas[neighbor_name]
                                neighbor_production = self.get_production(neighbor_wilaya, product)
                                if neighbor_production > product.production:
                                    is_best = False
                                    break
                                for second_neighbor_name in self.adjacency_list[neighbor_wilaya.name]:
                                    second_neighbor_wilaya = self.wilayas[second_neighbor_name]
                                    second_neighbor_production = self.get_production(second_neighbor_wilaya, product)
                                    if second_neighbor_production > product.production:
                                        is_best = False
                                        break
                                if not is_best:
                                    break

                            if is_best:
                                best_production[product.name] = product.production

                    elif search_by == 2:
                        if product.name not in best_price or product.price < best_price[product.name]:
                            is_best = True

                            for neighbor_name in self.adjacency_list[current_wilaya.name]:
                                neighbor_wilaya = self.wilayas[neighbor_name]
                                neighbor_price = self.get_price(neighbor_wilaya, product)
                                if neighbor_price < product.price:
                                    is_best = False
                                    break
                                for second_neighbor_name in self.adjacency_list[neighbor_wilaya.name]:
                                    second_neighbor_wilaya = self.wilayas[second_neighbor_name]
                                    second_neighbor_price = self.get_price(second_neighbor_wilaya, product)
                                    if second_neighbor_price < product.price:
                                        is_best = False
                                        break
                                if not is_best:
                                    break

                            if is_best:
                                best_price[product.name] = product.price

            for neighbor_name in self.adjacency_list[current_wilaya.name]:
                neighbor_wilaya = self.wilayas[neighbor_name]
                if neighbor_wilaya.name not in visited:
                    stack.append(neighbor_wilaya)

        if best_production:
            print(f"{searched_wilaya} is best at producing:")
            for product, production in best_production.items():
                print(f"- {product} with production {production}")

        if best_price:
            print(f"\n{searched_wilaya} is best at providing the lowest price for:")
            for product, price in best_price.items():
                print(f"- {product} with price {price}")

        if not best_production and not best_price:
            print(f"{searched_wilaya} does not have the highest production or the lowest price for any product.")
        
        
        
    def dfs_search_wilaya(self, product_name, search_season, search_by):
        stack = list(self.wilayas.values())
        visited = set()
        best_production = {}
        best_price = {}

        while stack:
            current_wilaya = stack.pop()
            if current_wilaya.name in visited:
                continue
            visited.add(current_wilaya.name)

            for product in current_wilaya.products:
                if product.name == product_name and product.season == search_season:
                    if search_by == 1:
                        if product_name not in best_production or product.production > best_production[product_name][1]:
                            best_production[product_name] = (current_wilaya.name, product.production)

                    elif search_by == 2:
                        if product_name not in best_price or product.price < best_price[product_name][1]:
                            best_price[product_name] = (current_wilaya.name, product.price)

            for neighbor_name in self.adjacency_list[current_wilaya.name]:
                neighbor_wilaya = self.wilayas[neighbor_name]
                if neighbor_wilaya.name not in visited:
                    stack.append(neighbor_wilaya)

        if best_production:
            for product, (wilaya, production) in best_production.items():
                print(f"The wilaya with the highest production of {product} is {wilaya} with a production of {production}")

        if best_price:
            for product, (wilaya, price) in best_price.items():
                print(f"The wilaya with the lowest price of {product} is {wilaya} with a price of {price}")

        if not best_production and not best_price:
            print(f"No wilaya has the highest production or the lowest price for the product {product_name} in season {search_season}.")

        
        


    def bfs_search_product(self, searched_wilaya, searched_season, search_by):
        if searched_wilaya not in self.wilayas:
            print("Wilaya not found in the graph.")
            return

        start_wilaya = self.wilayas[searched_wilaya]
        queue = deque([start_wilaya])
        visited = set()
        best_production = {}
        best_price = {}

        while queue:
            current_wilaya = queue.popleft()
            if current_wilaya.name in visited:
                continue
            visited.add(current_wilaya.name)

            for product in current_wilaya.products:
                if product.season == searched_season:
                    if search_by == 1:
                        if product.name not in best_production or product.production > best_production[product.name]:
                            is_best = True

                            for neighbor_name in self.adjacency_list[current_wilaya.name]:
                                neighbor_wilaya = self.wilayas[neighbor_name]
                                neighbor_production = self.get_production(neighbor_wilaya, product)
                                if neighbor_production > product.production:
                                    is_best = False
                                    break
                                for second_neighbor_name in self.adjacency_list[neighbor_wilaya.name]:
                                    second_neighbor_wilaya = self.wilayas[second_neighbor_name]
                                    second_neighbor_production = self.get_production(second_neighbor_wilaya, product)
                                    if second_neighbor_production > product.production:
                                        is_best = False
                                        break
                                if not is_best:
                                    break

                            if is_best:
                                best_production[product.name] = product.production

                    elif search_by == 2:
                        if product.name not in best_price or product.price < best_price[product.name]:
                            is_best = True

                            for neighbor_name in self.adjacency_list[current_wilaya.name]:
                                neighbor_wilaya = self.wilayas[neighbor_name]
                                neighbor_price = self.get_price(neighbor_wilaya, product)
                                if neighbor_price < product.price:
                                    is_best = False
                                    break
                                for second_neighbor_name in self.adjacency_list[neighbor_wilaya.name]:
                                    second_neighbor_wilaya = self.wilayas[second_neighbor_name]
                                    second_neighbor_price = self.get_price(second_neighbor_wilaya, product)
                                    if second_neighbor_price < product.price:
                                        is_best = False
                                        break
                                if not is_best:
                                    break

                            if is_best:
                                best_price[product.name] = product.price

            for neighbor_name in self.adjacency_list[current_wilaya.name]:
                neighbor_wilaya = self.wilayas[neighbor_name]
                if neighbor_wilaya.name not in visited:
                    queue.append(neighbor_wilaya)

        if best_production:
            print(f"{searched_wilaya} is best at producing:")
            for product, production in best_production.items():
                print(f"- {product} with production {production}")

        if best_price:
            print(f"\n{searched_wilaya} is best at providing the lowest price for:")
            for product, price in best_price.items():
                print(f"- {product} with price {price}")

        if not best_production and not best_price:
            print(f"{searched_wilaya} does not have the highest production or the lowest price for any product.")

        
        



    def bfs_search_wilaya(self, product_name, search_season, search_by):
        queue = deque(self.wilayas.values())
        visited = set()
        best_production = {}
        best_price = {}

        while queue:
            current_wilaya = queue.popleft()
            if current_wilaya.name in visited:
                continue
            visited.add(current_wilaya.name)

            for product in current_wilaya.products:
                if product.name == product_name and product.season == search_season:
                    if search_by == 1:
                        if product_name not in best_production or product.production > best_production[product_name][1]:
                            best_production[product_name] = (current_wilaya.name, product.production)

                    elif search_by == 2:
                        if product_name not in best_price or product.price < best_price[product_name][1]:
                            best_price[product_name] = (current_wilaya.name, product.price)

            for neighbor_name in self.adjacency_list[current_wilaya.name]:
                neighbor_wilaya = self.wilayas[neighbor_name]
                if neighbor_wilaya.name not in visited:
                    queue.append(neighbor_wilaya)

        if best_production:
            for product, (wilaya, production) in best_production.items():
                print(f"The wilaya with the highest production of {product} is {wilaya} with a production of {production}")

        if best_price:
            for product, (wilaya, price) in best_price.items():
                print(f"The wilaya with the lowest price of {product} is {wilaya} with a price of {price}")

        if not best_production and not best_price:
            print(f"No wilaya has the highest production or the lowest price for the product {product_name} in season {search_season}.")

        
        




    def hill_climbing_search_product(self, searched_wilaya, searched_season, search_by):
        if searched_wilaya not in self.wilayas:
            print("Wilaya not found in the graph.")
            return

        selected_wilaya = self.wilayas[searched_wilaya]
        best_production = {}
        best_price = {}

        if search_by == 1:
            max_production = 0
            best_product = None

            for product in selected_wilaya.products:
                if product.season == searched_season:
                    product_production = product.production
                    if product_production > max_production:
                        max_production = product_production
                        best_product = product

            if best_product is not None:
                is_best = True

                for neighbor_name in self.adjacency_list[searched_wilaya]:
                    neighbor_wilaya = self.wilayas[neighbor_name]
                    neighbor_production = self.get_production(neighbor_wilaya, best_product)
                    if neighbor_production > max_production:
                        is_best = False
                        break
                    for second_neighbor_name in self.adjacency_list[neighbor_wilaya.name]:
                        second_neighbor_wilaya = self.wilayas[second_neighbor_name]
                        second_neighbor_production = self.get_production(second_neighbor_wilaya, best_product)
                        if second_neighbor_production > max_production:
                            is_best = False
                            break
                    if not is_best:
                        break

                if is_best:
                    best_production[best_product.name] = max_production
            else:
                print(f"{searched_wilaya} does not have the highest production for any product.")

        elif search_by == 2:
            min_price = float('inf')
            best_product = None

            for product in selected_wilaya.products:
                if product.season == searched_season:
                    product_price = product.price
                    if product_price < min_price:
                        min_price = product_price
                        best_product = product

            if best_product is not None:
                is_best = True

                for neighbor_name in self.adjacency_list[searched_wilaya]:
                    neighbor_wilaya = self.wilayas[neighbor_name]
                    neighbor_price = self.get_price(neighbor_wilaya, best_product)
                    if neighbor_price < min_price:
                        is_best = False
                        break
                    for second_neighbor_name in self.adjacency_list[neighbor_wilaya.name]:
                        second_neighbor_wilaya = self.wilayas[second_neighbor_name]
                        second_neighbor_price = self.get_price(second_neighbor_wilaya, best_product)
                        if second_neighbor_price < min_price:
                            is_best = False
                            break
                    if not is_best:
                        break

                if is_best:
                    best_price[best_product.name] = min_price
            else:
                print(f"{searched_wilaya} does not have the lowest price for any product.")

        if best_production:
            print(f"{searched_wilaya} is best at producing:")
            for product, production in best_production.items():
                print(f"- {product} with production {production}")

        if best_price:
            print(f"\n{searched_wilaya} is best at providing the lowest price for:")
            for product, price in best_price.items():
                print(f"- {product} with price {price}")

        if not best_production and not best_price:
            print(f"{searched_wilaya} does not have the highest production or the lowest price for any product.")

        
        

    def hill_climbing_search_wilaya(self, product_name, search_season, search_by):
        best_production = {}
        best_price = {}

        for wilaya in self.wilayas.values():
            if search_by == 1:
                max_production = 0
                best_product = None

                for product in wilaya.products:
                    if product.name == product_name and product.season == search_season:
                        product_production = product.production
                        if product_production > max_production:
                            max_production = product_production
                            best_product = product

                if best_product is not None:
                    best_production[best_product.name] = (wilaya.name, max_production)

            elif search_by == 2:
                min_price = float('inf')
                best_product = None

                for product in wilaya.products:
                    if product.name == product_name and product.season == search_season:
                        product_price = product.price
                        if product_price < min_price:
                            min_price = product_price
                            best_product = product

                if best_product is not None:
                    best_price[best_product.name] = (wilaya.name, min_price)

        if best_production:
            for product, (wilaya, production) in best_production.items():
                print(f"The wilaya with the highest production of {product} is {wilaya} with a production of {production}")

        if best_price:
            for product, (wilaya, price) in best_price.items():
                print(f"The wilaya with the lowest price of {product} is {wilaya} with a price of {price}")

        if not best_production and not best_price:
            print(f"No wilaya has the highest production or the lowest price for the product {product_name} in season {search_season}.")

        
        



    def a_star_search_product(self, searched_wilaya, searched_season, search_by):
        if searched_wilaya not in self.wilayas:
            print("Wilaya not found in the graph.")
            return

        def heuristic(wilaya, product, search_by):
            if search_by == 1:
                return -product.production
            elif search_by == 2:
                return product.price

        start_wilaya = self.wilayas[searched_wilaya]
        priority_queue = []
        heapq.heappush(priority_queue, (0, start_wilaya.name))
        visited = set()
        best_production = {}
        best_price = {}

        while priority_queue:
            _, current_wilaya_name = heapq.heappop(priority_queue)
            if current_wilaya_name in visited:
                continue
            visited.add(current_wilaya_name)
            current_wilaya = self.wilayas[current_wilaya_name]

            for product in current_wilaya.products:
                if product.season == searched_season:
                    if search_by == 1:
                        if product.name not in best_production or product.production > best_production[product.name]:
                            is_best = True

                            for neighbor_name in self.adjacency_list[current_wilaya_name]:
                                neighbor_wilaya = self.wilayas[neighbor_name]
                                neighbor_production = self.get_production(neighbor_wilaya, product)
                                if neighbor_production > product.production:
                                    is_best = False
                                    break
                                for second_neighbor_name in self.adjacency_list[neighbor_wilaya.name]:
                                    second_neighbor_wilaya = self.wilayas[second_neighbor_name]
                                    second_neighbor_production = self.get_production(second_neighbor_wilaya, product)
                                    if second_neighbor_production > product.production:
                                        is_best = False
                                        break
                                if not is_best:
                                    break

                            if is_best:
                                best_production[product.name] = product.production
                                for neighbor_name in self.adjacency_list[current_wilaya_name]:
                                    heapq.heappush(priority_queue, (heuristic(self.wilayas[neighbor_name], product, search_by), neighbor_name))

                    elif search_by == 2:
                        if product.name not in best_price or product.price < best_price[product.name]:
                            is_best = True

                            for neighbor_name in self.adjacency_list[current_wilaya_name]:
                                neighbor_wilaya = self.wilayas[neighbor_name]
                                neighbor_price = self.get_price(neighbor_wilaya, product)
                                if neighbor_price < product.price:
                                    is_best = False
                                    break
                                for second_neighbor_name in self.adjacency_list[neighbor_wilaya.name]:
                                    second_neighbor_wilaya = self.wilayas[second_neighbor_name]
                                    second_neighbor_price = self.get_price(second_neighbor_wilaya, product)
                                    if second_neighbor_price < product.price:
                                        is_best = False
                                        break
                                if not is_best:
                                    break

                            if is_best:
                                best_price[product.name] = product.price
                                for neighbor_name in self.adjacency_list[current_wilaya_name]:
                                    heapq.heappush(priority_queue, (heuristic(self.wilayas[neighbor_name], product, search_by), neighbor_name))

        if best_production:
            print(f"{searched_wilaya} is best at producing:")
            for product, production in best_production.items():
                print(f"- {product} with production {production}")

        if best_price:
            print(f"\n{searched_wilaya} is best at providing the lowest price for:")
            for product, price in best_price.items():
                print(f"- {product} with price {price}")

        if not best_production and not best_price:
            print(f"{searched_wilaya} does not have the highest production or the lowest price for any product.")

        
        


    def a_star_search_wilaya(self, product_name, search_season, search_by):
        def heuristic(wilaya, product, search_by):
            if search_by == 1:
                return -product.production
            elif search_by == 2:
                return product.price

        priority_queue = []
        for wilaya_name in self.wilayas:
            heapq.heappush(priority_queue, (0, wilaya_name))

        visited = set()
        best_production = {}
        best_price = {}

        while priority_queue:
            _, current_wilaya_name = heapq.heappop(priority_queue)
            if current_wilaya_name in visited:
                continue
            visited.add(current_wilaya_name)
            current_wilaya = self.wilayas[current_wilaya_name]

            for product in current_wilaya.products:
                if product.name == product_name and product.season == search_season:
                    if search_by == 1:
                        if product_name not in best_production or product.production > best_production[product_name][1]:
                            best_production[product_name] = (current_wilaya.name, product.production)

                    elif search_by == 2:
                        if product_name not in best_price or product.price < best_price[product_name][1]:
                            best_price[product_name] = (current_wilaya.name, product.price)

            for neighbor_name in self.adjacency_list[current_wilaya_name]:
                heapq.heappush(priority_queue, (heuristic(self.wilayas[neighbor_name], product, search_by), neighbor_name))

        if best_production:
            for product, (wilaya, production) in best_production.items():
                print(f"The wilaya with the highest production of {product} is {wilaya} with a production of {production}")

        if best_price:
            for product, (wilaya, price) in best_price.items():
                print(f"The wilaya with the lowest price of {product} is {wilaya} with a price of {price}")

        if not best_production and not best_price:
            print(f"No wilaya has the highest production or the lowest price for the product {product_name} in season {search_season}.")

        
        


    def get_production(self, wilaya, product):
        for p in wilaya.products:
            if p.name == product.name and p.season == product.season:
                return p.production
        return 0

    def get_price(self, wilaya, product):
        for p in wilaya.products:
            if p.name == product.name and p.season == product.season:
                return p.price
        return float('inf')  # Return infinity if price not found
    
    def calculate_self_sufficiency(graph, product_name):
        total_production = 0
        total_consumption = 0

        for wilaya in graph.wilayas.values():
            for product in wilaya.products:
                if product.name == product_name:
                    total_production += product.production
                    total_consumption += product.consumption

        difference = total_production - total_consumption

        if difference > 0:
            print(f"Algeria was self-sufficient in {product_name} in the given year.")
            print(f"Total production: {total_production}")
            print(f"Total consumption: {total_consumption}")
            print(f"Difference (Production - Consumption): {difference}")
        else:
            print(f"Algeria was not self-sufficient in {product_name} in the given year.")
            print(f"Total production: {total_production}")
            print(f"Total consumption: {total_consumption}")
            print(f"Difference (Production - Consumption): {difference}")

    def sum_consumption(graph, product_name):
        total_consumption = 0

        for wilaya in graph.wilayas.values():
            for product in wilaya.products:
                if product.name == product_name:
                    total_consumption += product.consumption

        return total_consumption





def load_graph_from_csv(filename):
    graph = Graph()
    
    with open(filename, mode='r', newline='', encoding='utf-8') as file:
        csv_reader = csv.reader(file, delimiter=',')
        for row in csv_reader:
            if row and row[0]:  # Check if the row is not empty and the first element exists
                wilaya = row[0].strip()  # The first item is the wilaya
                if len(row) > 1:
                    neighbors_raw = row[1].strip().strip('"')  # Strip the outer quotes
                    neighbors = [neighbor.strip() for neighbor in neighbors_raw.split(',')]
                    graph.add_wilaya(wilaya)
                    for neighbor in neighbors:
                        graph.add_wilaya(neighbor)
                        graph.connect_wilayas(wilaya, neighbor)  # Establish connections between wilaya and its neighbors

    return graph

def load_wilaya_data_from_csv(filename, year, graph):
    with open(filename, mode='r', newline='', encoding='utf-8') as file:
        csv_reader = csv.reader(file, delimiter=',')
        headers = next(csv_reader)
        for row in csv_reader:
            if len(row) >= 7:  # Ensure the row has enough elements
                wilaya_name = row[0].strip()
                product_name = row[1].strip()
                try:
                    production = float(row[2]) if row[2] else 0.0
                    price = float(row[5]) if row[5] else 0.0
                    consumption = float(row[6]) if row[6] else 0.0
                except ValueError:
                    # Skip the row if conversion fails
                    print(f"Skipping row due to invalid data: {row}")
                    continue
                season = row[4].strip()
                product = Product(product_name, production, season, price, consumption)
                graph.add_wilaya(wilaya_name)
                graph.add_product_to_wilaya(wilaya_name, product)


def main():

    start_time = time.time()
    # Load the graph structure from neighbors CSV
    graph = load_graph_from_csv('Data\wilayas_and_neighbors.csv')

    # Prompt user for the year and load the corresponding data
    print("Welcome to the Production Analysis and Optimization System!")
    year = int(input("please choose the year you wish to perform a search on (2016 - 2019): "))
    if year in [2016, 2017, 2018, 2019]:
        load_wilaya_data_from_csv(f'Data\{year}.csv', year, graph)
    else:
        print("Enter a valid year between 2016 and 2019!")
        return

    print("Please choose an option:")
    print("1. Best product production in a given wilaya.")
    print("2. Highest production in a given product.")
    print("3. Does Algeria achieve self-sufficiency in a given product?")
    print("4. What is the country's consumption of a given product?")
    print("5. Check the visualization of wilaya connections graph.")
    print("6. Check the visualization of production by season.")
    choice = input("Enter the number of your choice: ")

    if choice == "1":

        # Example usage
        start_wilaya_name = input("Enter wilaya whose products will be searched: ")
        season = input("Enter season of search: ")

        print("1_ Breadth-First Search (BFS).")
        print("2_ Deapth-First Search (DFS).")
        print("3_ Hill Climbing Search.")
        print("4_ A* Search.")
        print("5_ All at once.")
        option=input("Enter search to be performed: ")

        if option == "1":
            print("Enter search parameter to be performed: ")
            print("Enter 1 to find the best wilaya production wise.")
            print("Enter 2 to find the best wilaya price wise.")
            option1 = int(input("Enter choice: "))
            print('Result of DFS Search: ')
            graph.dfs_search_product(start_wilaya_name, season, option1)
            execution_time = time.time() - start_time
            print(f"Execution time: {execution_time:.2f} seconds")
            memory_usage = measure_memory_usage()
            print("Memory Usage (bytes):", memory_usage)
        if option == "2":
            print("Enter search parameter to be performed: ")
            print("Enter 1 to find the best wilaya production wise.")
            print("Enter 2 to find the best wilaya price wise.")
            option1 = int(input("Enter choice: "))
            print('BFS Search Result: ')
            graph.bfs_search_product(start_wilaya_name, season, option1)
            execution_time = time.time() - start_time
            print(f"Execution time: {execution_time:.2f} seconds")
            memory_usage = measure_memory_usage()
            print("Memory Usage (bytes):", memory_usage)
        if option == "3":
            print("Enter search parameter to be performed: ")
            print("Enter 1 to find the best wilaya production wise.")
            print("Enter 2 to find the best wilaya price wise.")
            option1 = int(input("Enter choice: "))
            print('Hill Climbing Search Result: ')
            graph.hill_climbing_search_product(start_wilaya_name, season, option1)
            execution_time = time.time() - start_time
            print(f"Execution time: {execution_time:.2f} seconds")
            memory_usage = measure_memory_usage()
            print("Memory Usage (bytes):", memory_usage)
        if option == "4":
            print("Enter search parameter to be performed: ")
            print("Enter 1 to find the best wilaya production wise.")
            print("Enter 2 to find the best wilaya price wise.")
            option1 = int(input("Enter choice: "))
            print('A* Search Result: ')
            graph.a_star_search_product(start_wilaya_name, season, option1)
            execution_time = time.time() - start_time
            print(f"Execution time: {execution_time:.2f} seconds")
            memory_usage = measure_memory_usage()
            print("Memory Usage (bytes):", memory_usage)
        if option == "5":
            print("Enter search parameter to be performed: ")
            print("Enter 1 to find the best wilaya production wise.")
            print("Enter 2 to find the best wilaya price wise.")
            option1 = int(input("Enter choice: "))
            print("-------------------------")
            print('Result of DFS Search:')
            graph.dfs_search_product(start_wilaya_name, season, option1)
            print("-------------------------")
            print('BFS Search Result: ')
            graph.bfs_search_product(start_wilaya_name, season, option1)
            print("-------------------------")
            print('Hill Climbing Search Result: ')
            graph.hill_climbing_search_product(start_wilaya_name, season, option1)
            print("-------------------------")
            print('A* Search Result: ')
            graph.a_star_search_product(start_wilaya_name, season, option1)
            print("-------------------------")
            execution_time = time.time() - start_time
            print(f"Execution time: {execution_time:.2f} seconds")
            memory_usage = measure_memory_usage()
            print("Memory Usage (bytes):", memory_usage)

    if choice == "2":
        given_product = input("Enter product that will have its wilayas searched: ")
        season = input("Enter season of search: ")

        print("1_ Breadth-First Search (BFS).")
        print("2_ Deapth-First Search (DFS).")
        print("3_ Hill Climbing Search.")
        print("4_ A* Search.")
        print("5_ All at once.")
        option=input("Enter search to be performed: ")

        if option == "1":
            print("Enter search parameter to be performed: ")
            print("Enter 1 to find the best wilaya production wise.")
            print("Enter 2 to find the best wilaya price wise.")
            option1 = int(input("Enter choice: "))
            print('Result of DFS Search: ')
            graph.dfs_search_wilaya(given_product, season, option1)
            execution_time = time.time() - start_time
            print(f"Execution time: {execution_time:.2f} seconds")
            memory_usage = measure_memory_usage()
            print("Memory Usage (bytes):", memory_usage)
        if option == "2":
            print("Enter search parameter to be performed: ")
            print("Enter 1 to find the best wilaya production wise.")
            print("Enter 2 to find the best wilaya price wise.")
            option1 = int(input("Enter choice: "))
            print('BFS Search Result: ')
            graph.bfs_search_wilaya(given_product, season, option1)
            execution_time = time.time() - start_time
            print(f"Execution time: {execution_time:.2f} seconds")
            memory_usage = measure_memory_usage()
            print("Memory Usage (bytes):", memory_usage)
        if option == "3":
            print("Enter search parameter to be performed: ")
            print("Enter 1 to find the best wilaya production wise.")
            print("Enter 2 to find the best wilaya price wise.")
            option1 = int(input("Enter choice: "))
            print('Hill Climbing Search Result: ')
            graph.hill_climbing_search_wilaya(given_product, season, option1)
            execution_time = time.time() - start_time
            print(f"Execution time: {execution_time:.2f} seconds")
            memory_usage = measure_memory_usage()
            print("Memory Usage (bytes):", memory_usage)
        if option == "4":
            print("Enter search parameter to be performed: ")
            print("Enter 1 to find the best wilaya production wise.")
            print("Enter 2 to find the best wilaya price wise.")
            option1 = int(input("Enter choice: "))
            print('A* Search Result: ')
            graph.a_star_search_wilaya(given_product, season, option1)
            execution_time = time.time() - start_time
            print(f"Execution time: {execution_time:.2f} seconds")
            memory_usage = measure_memory_usage()
            print("Memory Usage (bytes):", memory_usage)
        if option == "5":
            print("Enter search parameter to be performed: ")
            print("Enter 1 to find the best wilaya production wise.")
            print("Enter 2 to find the best wilaya price wise.")
            option1 = int(input("Enter choice: "))
            print("-------------------------")
            print('Result of DFS Search:')
            graph.dfs_search_wilaya(given_product, season, option1)
            print("-------------------------")
            print('BFS Search Result: ')
            graph.bfs_search_wilaya(given_product, season, option1)
            print("-------------------------")
            print('Hill Climbing Search Result: ')
            graph.hill_climbing_search_wilaya(given_product, season, option1)
            print("-------------------------")
            print('A* Search Result: ')
            graph.a_star_search_wilaya(given_product, season, option1)
            print("-------------------------")
            execution_time = time.time() - start_time
            print(f"Execution time: {execution_time:.2f} seconds")
            memory_usage = measure_memory_usage()
            print("Memory Usage (bytes):", memory_usage)

    if choice == "3":        
        product=input("Enter product whose self-sufficiency will be checked: ")
        graph.calculate_self_sufficiency(product)
        execution_time = time.time() - start_time
        print(f"Execution time: {execution_time:.2f} seconds")
        memory_usage = measure_memory_usage()
        print("Memory Usage (bytes):", memory_usage)

    if choice == "4":
        product1 = input("Enter product whose total consumption will be summed: ")
        print("Total consumption of ", product1, " in the year ", year, " : ", graph.sum_consumption(product1))
        execution_time = time.time() - start_time
        print(f"Execution time: {execution_time:.2f} seconds")
        memory_usage = measure_memory_usage()
        print("Memory Usage (bytes):", memory_usage)

    if choice == "5":
        graph.visualize_graph()

    if choice == "6":
        seasonPlot = input("Enter season whose production will be plotted: ")
        graph.visualize_production(seasonPlot)


if __name__ == "__main__":
    main()
