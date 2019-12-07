# Lab 6 - Kruskal's & Topological Sort
# GeeksForGeeks was used to assist on implementations for both algorithms:
# Union by rank, path compression,

class Subset:  # Using the union by rank and compress algorithm
    def __init__(self, parent, rank):
        self.parent = parent
        self.rank = rank


class Edge:
    def __init__(self, src, dest, weight=1):
        self.src = src
        self.dest = dest
        self.weight = weight

    def print_edge(self):
        print("Src: %d --\tDest: %d --\tWeight: %d" % (self.src, self.dest, self.weight))


class Graph:
    # Constructor
    def __init__(self, vertices, weighted=False):
        # self.al = [[] for i in range(vertices)]
        self.edges = []
        self.V = vertices
        self.weighted = weighted

    def is_valid_vertex(self, u):
        return 0 <= u < self.V

    # adds an edge to the graph
    def add_edge(self, source, dest, weight=1):
        if not self.is_valid_vertex(source) or not self.is_valid_vertex(dest):
            print('Error, vertex number out of range')
        elif weight != 1 and not self.weighted:
            print('Error, inserting weighted edge to unweighted graph')
        else:
            self.edges.append(Edge(source, dest, weight))

    # find set of element i, through path compression
    def find(self, subsets, i):

        # find root and make root as parent of i (path compression)
        # path compression: "flattens tree"
        if subsets[i].parent != i:
            subsets[i].parent = self.find(subsets, subsets[i].parent)

        return subsets[i].parent

    # unions 2 sets (by rank)
    # rank: attaching a smaller depth tree under root of bigger depth tree
    def union(self, subsets, x, y):
        root_x = self.find(subsets, x)
        root_y = self.find(subsets, y)

        # union by rank
        if subsets[root_x].rank < subsets[root_y].rank:
            subsets[root_x].parent = root_y
        elif subsets[root_x].rank > subsets[root_y].rank:
            subsets[root_y].parent = root_x

        # trees have same rank
        # 1) one tree becomes root
        # 2) depth (rank) increased by 1
        else:
            subsets[root_y].parent = root_x
            subsets[root_x].rank += 1

    # creates minimum spanning tree (MST)
    def kruskal(self):
        mst = []
        e = 0
        i = 0

        #  sort edges by increasing order
        self.edges = sorted(self.edges, key=lambda edge: edge.weight)

        subset = []

        for i_vertex in range(self.V):
            subset.append(Subset(i_vertex, 0))

        # traverse through all the expected vertices and edges that have been added
        while e < self.V - 1 and i < len(self.edges):
            tmp_edge = self.edges[i]
            i += 1
            x = self.find(subset, tmp_edge.src)
            y = self.find(subset, tmp_edge.dest)

            # If a cycle isn't formed we append
            # add one to e for the next edge found
            if x != y:
                e += 1
                mst.append(tmp_edge)
                self.union(subset, x, y)

        for e in mst:
            e.print_edge()
        print()

    def print_graph(self):
        for v in self.edges:
            v.print_edge()
        print()

    # helper method used by topological sort method
    def topological_sort_util(self, source, visited, stack):

        # used to track current node
        visited[source] = True

        # recursive call for adjacent vertices
        for e in self.edges:
            if e.src == source and not visited[e.dest]:
                self.topological_sort_util(e.dest, visited, stack)

        # stores vertex in stack
        stack.insert(0, source)

    # carries out topological sort
    def topological_sort(self):

        # vertices set to false = not visited
        visited = [False] * self.V
        stack = []

        # calls helper method to store resulting order of all vertices
        for vertex in range(self.V):
            if not visited[vertex]:
                self.topological_sort_util(vertex, visited, stack)

        print(stack)
        print()


if __name__ == "__main__":
    g = Graph(4)
    g.add_edge(2, 3)
    g.add_edge(0, 1)
    g.add_edge(0, 2)
    g.add_edge(0, 3)
    g.add_edge(1, 3)

    # All the nodes in the graph
    print("All nodes found in graph")
    g.print_graph()

    # Minimum Spanning Tree
    print("Nodes needed for a MST")
    g.kruskal()

    print("Topological Map")
    g.topological_sort()

    gg = Graph(6, weighted=True)
    gg.add_edge(0, 1, 4)
    gg.add_edge(0, 2, 3)
    gg.add_edge(1, 2, 2)
    gg.add_edge(2, 3, 1)
    gg.add_edge(3, 4, 5)
    gg.add_edge(4, 1, 4)

    # All the nodes in the graph
    print("All nodes found in graph")
    gg.print_graph()

    # Minimum Spanning Tree
    print("Nodes needed for a MST")
    gg.kruskal()

    print("Topological Map")
    gg.topological_sort()
