# Problem 1

# Detailed Solution for Calculating Equivalent Resistance Using Graph Theory

Below, I provide a comprehensive solution to calculate the equivalent resistance between two points in an electrical circuit using graph theory. This response includes a detailed theoretical foundation, a step-by-step explanation of the algorithm, a complete Python implementation, and solutions to multiple example tasks. The solution is presented in markdown format for clarity and readability.

---

## Theoretical Background

### Equivalent Resistance in Electrical Circuits
In electrical engineering, the **equivalent resistance** between two points in a circuit is the single resistance value that can replace the entire network while maintaining the same voltage-current relationship between those points, as per Ohm's Law ($V = I \cdot R$). Traditionally, this is computed by simplifying the circuit using two fundamental rules:

- **Series Combination**: When resistors are connected end-to-end, the same current flows through each, and their resistances add directly:
  $$
  R_{\text{eq}} = R_1 + R_2 + \cdots + R_n
  $$

- **Parallel Combination**: When resistors connect the same two nodes, they share the same voltage, and their equivalent resistance is found by adding their conductances (reciprocals of resistance):
  $$
  \frac{1}{R_{\text{eq}}} = \frac{1}{R_1} + \frac{1}{R_2} + \cdots + \frac{1}{R_n}
  $$
  For two resistors, this simplifies to:
  $$
  R_{\text{eq}} = \frac{R_1 \cdot R_2}{R_1 + R_2}
  $$

These rules work well for simple circuits but become cumbersome for complex or nested configurations. Graph theory offers a systematic approach to model and simplify such circuits.

### Graph Theory in Circuit Analysis
A circuit can be modeled as an **undirected multigraph**:
- **Nodes** represent junction points or terminals where wires connect.
- **Edges** represent resistors, with weights corresponding to their resistance values (in ohms, Ω).
- **Multigraph**: Allows multiple edges between the same pair of nodes, representing parallel resistors.

The goal is to reduce this graph iteratively until only the two nodes of interest (source and target) remain, connected by edges whose combined resistance equals the equivalent resistance. We achieve this using:
- **Series Reduction**: Replace a path through an intermediate node with a single edge.
- **Parallel Reduction**: Combine multiple edges between two nodes into one.

### Assumptions
- Resistances are positive ($R > 0$).
- The circuit is connected between the source and target.
- The configuration can be fully reduced using series and parallel rules (e.g., no irreducible structures like a balanced Wheatstone bridge, which would require advanced techniques like delta-star transformations).

---

## Algorithm Overview

### Representation
- Use a **multigraph** (via Python’s `networkx.MultiGraph`) to allow multiple resistors between nodes.
- Each edge has a `weight` attribute representing resistance.

### Reduction Steps
1. **Parallel Reduction**:


    - Identify pairs of nodes with multiple edges.
    - Compute the equivalent resistance using the parallel formula.
    - Replace all edges between the pair with a single edge of the computed resistance.

2. **Series Reduction**:


    - Identify nodes (not the source or target) with exactly two distinct neighbors, each connected by a single edge.
    - Remove the node and connect its neighbors with a new edge, summing the resistances of the two original edges.

3. **Iterative Process**:


    - Prioritize parallel reductions to simplify multiple edges.
    - Alternate between parallel and series reductions until only the source and target nodes remain.
    - Compute the final equivalent resistance from any edges between the source and target.

### Stopping Conditions
- Success: The graph has exactly two nodes (source and target), and their connecting edges’ parallel resistance is the answer.
- Failure: No further reductions are possible, and more than two nodes remain, indicating a complex configuration beyond series-parallel reductions.

---

## Python Implementation

Here’s the complete code, with detailed comments explaining each function:

```python
import networkx as nx

def parallel_resistance(resistances):
    """
    Compute the equivalent resistance of resistors in parallel.
    
    Args:
        resistances (list): List of resistance values (floats).
    
    Returns:
        float: Equivalent resistance. Returns inf for an open circuit (no resistors),
               0 for a short circuit (any resistance is 0).
    """
    if not resistances:
        return float('inf')  # Open circuit
    inv_sum = sum(1 / r for r in resistances if r != 0)  # Sum of conductances
    return 1 / inv_sum if inv_sum != 0 else 0  # Handle short circuit

def find_series(G, source, target):
    """
    Perform one series reduction if possible.
    
    Args:
        G (nx.MultiGraph): The circuit graph.
        source (node): Starting node (protected from removal).
        target (node): Ending node (protected from removal).
    
    Returns:
        bool: True if a reduction was made, False otherwise.
    """
    for node in list(G.nodes()):
        if node != source and node != target:
            neighbors = list(set(G.neighbors(node)))
            # Check for exactly two distinct neighbors, each with one edge
            if len(neighbors) == 2 and all(len(G[node][nbr]) == 1 for nbr in neighbors):
                u, v = neighbors
                r1 = list(G[node][u].values())[0]['weight']
                r2 = list(G[node][v].values())[0]['weight']
                G.remove_node(node)
                G.add_edge(u, v, weight=r1 + r2)
                return True
    return False

def find_parallel(G):
    """
    Perform one parallel reduction if possible.
    
    Args:
        G (nx.MultiGraph): The circuit graph.
    
    Returns:
        bool: True if a reduction was made, False otherwise.
    """
    for u in G:
        for v in G[u]:
            if len(G[u][v]) > 1:  # Multiple edges between u and v
                resistances = [data['weight'] for data in G[u][v].values()]
                R_eq = parallel_resistance(resistances)
                G.remove_edges_from([(u, v, key) for key in G[u][v].keys()])
                G.add_edge(u, v, weight=R_eq)
                return True
    return False

def equivalent_resistance(G_input, source, target):
    """
    Calculate the equivalent resistance between source and target nodes.
    
    Args:
        G_input (nx.MultiGraph): Input circuit graph.
        source (node): Starting node.
        target (node): Ending node.
    
    Returns:
        float: Equivalent resistance between source and target.
    
    Raises:
        ValueError: If the graph cannot be reduced to two nodes.
    """
    G = G_input.copy()  # Work on a copy to preserve the original graph
    while len(G.nodes()) > 2:
        if find_parallel(G):
            continue
        elif find_series(G, source, target):
            continue
        else:
            raise ValueError("Cannot reduce further. Complex configuration detected.")
    if set(G.nodes()) == {source, target}:
        resistances = [data['weight'] for data in G[source][target].values()]
        return parallel_resistance(resistances)
    else:
        raise ValueError("Graph not reduced to source and target nodes.")
```

---

## Solving Example Tasks

Let’s apply this implementation to several circuit configurations, walking through each reduction step-by-step and verifying the results.

### Task 1: Simple Series Circuit
**Circuit**: $A \xrightarrow{2Ω} B \xrightarrow{3Ω} C$  
**Objective**: Find the equivalent resistance between $A$ and $C$.

#### Graph Setup
```python
G_series = nx.MultiGraph()
G_series.add_edge('A', 'B', weight=2)
G_series.add_edge('B', 'C', weight=3)
```

#### Reduction Steps
1. **Initial Graph**: Nodes = {A, B, C}, Edges = {A-B (2Ω), B-C (3Ω)}
   - B has degree 2, neighbors = {A, C}, one edge each.
2. **Series Reduction**:
   - Remove B.
   - Add edge A-C with weight = 2 + 3 = 5Ω.
3. **Reduced Graph**: Nodes = {A, C}, Edges = {A-C (5Ω)}

#### Result
```python
eq_series = equivalent_resistance(G_series, 'A', 'C')
print(f"Series Circuit (A to C): {eq_series} ohms")  # Output: 5.0 ohms
```
**Verification**: $R_{\text{eq}} = 2 + 3 = 5Ω$, correct.

---

### Task 2: Simple Parallel Circuit
**Circuit**: $A$ connected to $B$ by two resistors (2Ω and 3Ω in parallel).  
**Objective**: Find the equivalent resistance between $A$ and $B$.

#### Graph Setup
```python
G_parallel = nx.MultiGraph()
G_parallel.add_edge('A', 'B', weight=2)
G_parallel.add_edge('A', 'B', weight=3)
```

#### Reduction Steps

1. **Initial Graph**: 

    - Nodes = {A, B}, Edges = {A-B (2Ω), A-B (3Ω)}
    - A and B have multiple edges.
2. **Parallel Reduction**:

    - Resistances = [2, 3].
    - $R_{\text{eq}} = \frac{2 \cdot 3}{2 + 3} = \frac{6}{5} = 1.2Ω$.
    - Remove both edges, add A-B (1.2Ω).
3. **Reduced Graph**:

    - Nodes = {A, B}, Edges = {A-B (1.2Ω)}

#### Result
```python
eq_parallel = equivalent_resistance(G_parallel, 'A', 'B')
print(f"Parallel Circuit (A to B): {eq_parallel} ohms")  # Output: 1.2 ohms
```
**Verification**: $\frac{1}{R_{\text{eq}}} = \frac{1}{2} + \frac{1}{3} = \frac{3}{6} + \frac{2}{6} = \frac{5}{6}$, so $R_{\text{eq}} = \frac{6}{5} = 1.2Ω$, correct.

---

### Task 3: Nested Series-Parallel Circuit
**Circuit**: $A \xrightarrow{2Ω} B \xrightarrow{3Ω} C$, and $A \xrightarrow{4Ω} C$.  
**Objective**: Find the equivalent resistance between $A$ and $C$.

#### Graph Setup
```python
G_nested = nx.MultiGraph()
G_nested.add_edge('A', 'B', weight=2)
G_nested.add_edge('B', 'C', weight=3)
G_nested.add_edge('A', 'C', weight=4)
```

#### Reduction Steps
1. **Initial Graph**: 

    - Nodes = {A, B, C}, Edges = {A-B (2Ω), B-C (3Ω), A-C (4Ω)}
    - B has degree 2, neighbors = {A, C}, one edge each.
2. **Series Reduction**:
    
    - Remove B.
    - Add edge A-C with weight = 2 + 3 = 5Ω.
3. **Intermediate Graph**: 
    
    - Nodes = {A, C}, Edges = {A-C (4Ω), A-C (5Ω)}
    - Multiple edges between A and C.
4. **Parallel Reduction**:
    
    - Resistances = [4, 5].
    - $R_{\text{eq}} = \frac{4 \cdot 5}{4 + 5} = \frac{20}{9} \approx 2.222Ω$.
    - Remove both edges, add A-C (20/9 Ω).
5. **Final Graph**: 
    
    - Nodes = {A, C}, Edges = {A-C (20/9 Ω)}

#### Result
```python
eq_nested = equivalent_resistance(G_nested, 'A', 'C')
print(f"Nested Circuit (A to C): {eq_nested} ohms")  # Output: 2.222... ohms
```
**Verification**: Series from A to C via B is 5Ω, in parallel with 4Ω: $\frac{1}{R_{\text{eq}}} = \frac{1}{5} + \frac{1}{4} = \frac{4}{20} + \frac{5}{20} = \frac{9}{20}$, so $R_{\text{eq}} = \frac{20}{9} \approx 2.222Ω$, correct.

---

### Task 4: Complex Ladder Network
**Circuit**: $A \xrightarrow{1Ω} B \xrightarrow{1Ω} C$, with $A \xrightarrow{2Ω} C$ and $B \xrightarrow{2Ω} C$.  
**Objective**: Find the equivalent resistance between $A$ and $C$.

#### Graph Setup
```python
G_ladder = nx.MultiGraph()
G_ladder.add_edge('A', 'B', weight=1)
G_ladder.add_edge('B', 'C', weight=1)
G_ladder.add_edge('A', 'C', weight=2)
G_ladder.add_edge('B', 'C', weight=2)
```

#### Reduction Steps
1. **Initial Graph**: 
    
    - Nodes = {A, B, C}, Edges = {A-B (1Ω), B-C     (1Ω), A-C (2Ω), B-C (2Ω)}
    - B-C has multiple edges: [1Ω, 2Ω].
2. **Parallel Reduction (B-C)**:
    
    - $R_{\text{eq}} = \frac{1 \cdot 2}{1 + 2} = \frac{2}{3} \approx 0.6667Ω$.
    - Replace B-C edges with B-C (2/3 Ω).
3. **Intermediate Graph**: 
    
    - Nodes = {A, B, C}, Edges = {A-B (1Ω), B-C (2/3 Ω), A-C (2Ω)}
    - B has degree 2, neighbors = {A, C}, one edge each.
4. **Series Reduction**:
   
    - Remove B.
    - Add edge A-C with weight = 1 + 2/3 = 3/3 + 2/3 = 5/3 Ω.
5. **Intermediate Graph**: 
    
    - Nodes = {A, C}, Edges = {A-C (2Ω), A-C (5/3 Ω)}
    - Multiple edges between A and C.
6. **Parallel Reduction (A-C)**:
   
    - Resistances = [2, 5/3].
    - $\frac{1}{R_{\text{eq}}} = \frac{1}{2} + \frac{3}{5} = \frac{5}{10} + \frac{6}{10} = \frac{11}{10}$.
    - $R_{\text{eq}} = \frac{10}{11} \approx 0.9091Ω$.

#### Result
```python
eq_ladder = equivalent_resistance(G_ladder, 'A', 'C')
print(f"Ladder Circuit (A to C): {eq_ladder} ohms")  # Output: 0.909090... ohms
```
**Verification**: Manual calculation confirms $R_{\text{eq}} = \frac{10}{11}Ω$, correct.

---

## Complete Test Code

Here’s the full code with all test cases:

```python
import networkx as nx

def parallel_resistance(resistances):
    if not resistances:
        return float('inf')
    inv_sum = sum(1 / r for r in resistances if r != 0)
    return 1 / inv_sum if inv_sum != 0 else 0

def find_series(G, source, target):
    for node in list(G.nodes()):
        if node != source and node != target:
            neighbors = list(set(G.neighbors(node)))
            if len(neighbors) == 2 and all(len(G[node][nbr]) == 1 for nbr in neighbors):
                u, v = neighbors
                r1 = list(G[node][u].values())[0]['weight']
                r2 = list(G[node][v].values())[0]['weight']
                G.remove_node(node)
                G.add_edge(u, v, weight=r1 + r2)
                return True
    return False

def find_parallel(G):
    for u in G:
        for v in G[u]:
            if len(G[u][v]) > 1:
                resistances = [data['weight'] for data in G[u][v].values()]
                R_eq = parallel_resistance(resistances)
                G.remove_edges_from([(u, v, key) for key in G[u][v].keys()])
                G.add_edge(u, v, weight=R_eq)
                return True
    return False

def equivalent_resistance(G_input, source, target):
    G = G_input.copy()
    while len(G.nodes()) > 2:
        if find_parallel(G):
            continue
        elif find_series(G, source, target):
            continue
        else:
            raise ValueError("Cannot reduce further. Complex configuration detected.")
    if set(G.nodes()) == {source, target}:
        resistances = [data['weight'] for data in G[source][target].values()]
        return parallel_resistance(resistances)
    else:
        raise ValueError("Graph not reduced to source and target nodes.")

def test_circuits():
    # Task 1: Series Circuit
    G_series = nx.MultiGraph()
    G_series.add_edge('A', 'B', weight=2)
    G_series.add_edge('B', 'C', weight=3)
    print(f"Series Circuit (A to C): {equivalent_resistance(G_series, 'A', 'C')} ohms")

    # Task 2: Parallel Circuit
    G_parallel = nx.MultiGraph()
    G_parallel.add_edge('A', 'B', weight=2)
    G_parallel.add_edge('A', 'B', weight=3)
    print(f"Parallel Circuit (A to B): {equivalent_resistance(G_parallel, 'A', 'B')} ohms")

    # Task 3: Nested Circuit
    G_nested = nx.MultiGraph()
    G_nested.add_edge('A', 'B', weight=2)
    G_nested.add_edge('B', 'C', weight=3)
    G_nested.add_edge('A', 'C', weight=4)
    print(f"Nested Circuit (A to C): {equivalent_resistance(G_nested, 'A', 'C')} ohms")

    # Task 4: Ladder Network
    G_ladder = nx.MultiGraph()
    G_ladder.add_edge('A', 'B', weight=1)
    G_ladder.add_edge('B', 'C', weight=1)
    G_ladder.add_edge('A', 'C', weight=2)
    G_ladder.add_edge('B', 'C', weight=2)
    print(f"Ladder Circuit (A to C): {equivalent_resistance(G_ladder, 'A', 'C')} ohms")

if __name__ == "__main__":
    test_circuits()
```

### Output
```
Series Circuit (A to C): 5.0 ohms
Parallel Circuit (A to B): 1.2 ohms
Nested Circuit (A to C): 2.222222222222222 ohms
Ladder Circuit (A to C): 0.9090909090909091 ohms
```

---

## Additional Notes

### Limitations
- The algorithm assumes the circuit can be reduced using series and parallel rules. Complex configurations (e.g., Wheatstone bridge) may require additional techniques.
- Resistances are assumed positive, though the code handles zero (short circuit) and empty edge sets (open circuit).

### Efficiency
- Time complexity is approximately $O(N \cdot E)$ per iteration, where $N$ is the number of nodes and $E$ is the number of edges, due to scanning for reductions. Total complexity depends on the number of reductions, typically $O(N^2 \cdot E)$ in the worst case.


---
