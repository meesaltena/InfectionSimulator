class Person:
    # x and y location of the circle representing the person
    x = 0
    y = 0
    # List of neighbors, not used yet
    neighbors = []
    infected = False
    alive = True
    recovered = False

    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    # Not used yet
    def addNeighbor(self, neighbor):
        if neighbor not in self.neighbors:
            self.neighbors.append(neighbor)
    
    def move(self, x, y):
        self.x += x
        self.x += y

    def __str__(self):
        return "Person with x: " + str(self.x) + ", y: " + str(self.x) + ", no. of neighbors: " + str(len(self.neighbors))