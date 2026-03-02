#  Agricultural Land Production Planning (ALPP)

Artificial Intelligence Mini Project
May 2024

##  Project Overview

The **Agricultural Land Production Planning (ALPP)** project focuses on optimizing agricultural production across Algerian Wilayas using Artificial Intelligence search algorithms.

The main objective is to:

* Identify the best product produced by each Wilaya.
* Optimize agricultural planning scenarios using historical data.
* Improve food security, production efficiency, and economic sustainability in Algeria.

The project applies **graph search algorithms** and a **meta-level optimization framework** to analyze agricultural data from 2016 to 2019.

---

##  Objectives

1. Determine the strongest agricultural product for each Wilaya.
2. Compare different AI search strategies.
3. Build an optimized agricultural scenario using historical data.
4. Improve farming efficiency and strategic production planning.

---

##  Dataset Description

The dataset covers **4 years (2016–2019)** and contains agricultural data for multiple Algerian Wilayas.

### Data Attributes

* **Wilaya** – Administrative region in Algeria
* **Product** – Agricultural product (wheat, barley, potatoes, etc.)
* **Production (prod)** – Quantity produced
* **Land Size (Superficie emblavée)** – Cultivated area (hectares)
* **Season** – Growing season (Spring, Fall, etc.)
* **Price** – Market price
* **Consumption** – Local consumption

### Data Source

Official agricultural reports from the Algerian Ministry:

* 2016 Report
* 2017 Report
* 2018 Report
* 2019 Report

(Referenced in the appendix of the project report )

---

# Project Structure

The project is divided into two main parts:

---

##  Part 1: Graph Search for Best Products

This part models Wilayas as nodes in a graph.

### Problem Formulation

* **States:** Wilayas
* **Initial State:** User-selected Wilaya
* **Actions:** Compare production with other Wilayas
* **Goal State:** Identify the Wilaya that produces the highest quantity of a product
* **Path Cost:** Production difference

### Implemented Algorithms

* Breadth-First Search (BFS)
* Depth-First Search (DFS)
* A* Search
* Hill Climbing

Each algorithm traverses the graph to determine the best-performing product per Wilaya.

---

##  Part 2: Scenario Optimization (Meta-Level Tree)

This part builds a **meta-level tree structure** to optimize agricultural strategies.

### Concept

Each node in the meta-tree represents:

* A combination of search algorithms
* Different heuristics
* Different optimization configurations

### Goal

Find the best combination of:

* Search strategy
* Parameters
* Heuristic functions

To maximize:

* Production efficiency
* Agricultural performance
* National food security

---

##  Running Time Comparison

| Algorithm          | Execution Time |
| ------------------ | -------------- |
| A* Search          | 13.19 sec      |
| Best First Search  | 16.20 sec      |
| Hill Climbing      | 18.04 sec      |
| Depth First Search | 41.25 sec      |

### Observation

* **A*** performed best in terms of speed and balance.
* **DFS** was the slowest.
* **Hill Climbing** quickly finds local optima but may miss global ones.

---

##  Visualization

The project includes:

* Graph visualization of Wilayas
* Attribute comparison charts
* Relationships between production, land size, and price
* Scenario comparison outputs

---

##  Technologies Used

* Python
* Graph Data Structures
* AI Search Algorithms
* CSV Data Processing
* Data Visualization

---

## Team Members & Contributions

###  KHEFFACHE Semhane (Leader)

* BFS implementation
* data2019.csv generation
* Product class coding
* Report writing
* Testing & Debugging
* Visualization

###  HATTABI Hadil

* DFS implementation
* data2017.csv generation
* Main function coding
* Report writing
* Testing & Debugging
* Visualization

###  SOUAK Maroua

* Hill Climbing implementation
* data2018.csv generation
* Wilaya class coding
* Report writing
* Testing & Debugging
* Visualization

### MAHFOUDIA Nour el houda Imene

* A* implementation
* data2016.csv generation
* Graph & Meta-Level classes
* Report writing
* Testing & Debugging
* Visualization

---

##  How to Run the Project

1. Clone the repository.
2. Make sure all CSV data files (2016–2019) are in the project directory.
3. Run the main file:

```bash
python main.py
```

4. Select:

   * Year
   * Wilaya
   * Search Algorithm

5. View results and optimization outputs.

---

## 📌 Conclusion

This project demonstrates how Artificial Intelligence search algorithms can solve real-world agricultural optimization problems.

By combining:

* Graph search techniques
* Heuristic optimization
* Meta-level tree exploration

We successfully identified:

* The strongest agricultural products per Wilaya
* The most efficient search strategy (A*)
* Optimized national-level production scenarios

This work highlights the power of AI in improving agricultural planning, sustainability, and food security in Algeria.

