from room import Room
from player import Player
from world import World

import random
from ast import literal_eval

class Queue():
    def __init__(self):
        self.queue = []
    def enqueue(self, value):
        self.queue.append(value)
    def dequeue(self):
        if self.size() > 0:
            return self.queue.pop(0)
        else:
            return None
    def size(self):
        return len(self.queue)

class TraversalGraph:
    def __init__(self):
        self.rooms = {}
    
    def add_room(self, room):
        self.rooms[room.id] = {}
        for i in room.get_exits():
            self.rooms[room.id][i] = '?'

    def add_connection(self, room_1, room_2, direction):
        opp_direction = {'n': 's', 's': 'n', 'e': 'w', 'w': 'e'}
        self.rooms[room_1.id][direction] = room_2.id
        self.rooms[room_2.id][opp_direction[direction]] = room_1.id
    
    def get_neighbor_rooms(self, room_id):
        return self.rooms[room_id]

    def bfs(self, starting_room):
        q = Queue()
        path = [starting_room]
        q.enqueue(path)
        visited = set()
        while q.size() > 0:
            current_path = q.dequeue()
            current_room = current_path[-1]
            if current_room == '?':
                return current_path
            if current_room not in visited:
                visited.add(current_room)
                room_neighbors = self.get_neighbor_rooms(current_room).values()
                for room_neighbor in room_neighbors:
                    path_copy = current_path[:]
                    path_copy.append(room_neighbor)
                    q.enqueue(path_copy)

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "C:/Users/nchib/DS5/Graphs/projects/adventure/maps/test_line.txt"
# map_file = "C:/Users/nchib/DS5/Graphs/projects/adventure/maps/test_cross.txt"
# map_file = "C:/Users/nchib/DS5/Graphs/projects/adventure/maps/test_loop.txt"
# map_file = "C:/Users/nchib/DS5/Graphs/projects/adventure/maps/test_loop_fork.txt"
map_file = "C:/Users/nchib/DS5/Graphs/projects/adventure/maps/main_maze.txt"

# Loads the map into a dictionary
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []
graph = TraversalGraph()
directions = ['n','s','e','w']

while len(graph.rooms) < 500:
    room_1 = player.current_room
    if room_1.id not in graph.rooms:
        graph.add_room(room_1)
    current_exits = player.current_room.get_exits()
    direction = random.choice(current_exits)
    while player.current_room.get_room_in_direction(direction).id in \
        graph.rooms and '?' not in \
        graph.get_neighbor_rooms(player.current_room.get_room_in_direction(direction).id).values():
        direction = random.choice(current_exits)
    player.travel(direction)
    room_2 = player.current_room
    if room_2.id not in graph.rooms:
        graph.add_room(room_2)
    traversal_path.append(direction)
    if room_2.id not in graph.get_neighbor_rooms(room_1.id).values():
        graph.add_connection(room_1, room_2, direction)
    if '?' not in graph.get_neighbor_rooms(room_2.id).values() and graph.bfs(room_2.id) is not None:
        path_nearest_room = graph.bfs(room_2.id)
        path_nearest_room = path_nearest_room[1:-1]
        for p in path_nearest_room:
            for d in directions:
                room_in_dir = player.current_room.get_room_in_direction(d)
                if room_in_dir and room_in_dir.id == p:
                    traversal_path.append(d)
                    player.travel(d)
                    if player.current_room.id not in graph.rooms:
                        graph.add_room(player.current_room)

# TRAVERSAL TEST
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")



#######
# UNCOMMENT TO WALK AROUND
#######
# player.current_room.print_room_description(player)
# while True:
#     cmds = input("-> ").lower().split(" ")
#     if cmds[0] in ["n", "s", "e", "w"]:
#         player.travel(cmds[0], True)
#     elif cmds[0] == "q":
#         break
#     else:
#         print("I did not understand that command.")

