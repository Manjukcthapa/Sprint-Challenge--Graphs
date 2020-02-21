from room import Room
from player import Player
from world import World

import random
from ast import literal_eval

class Stack():
    def __init__(self):
        self.stack = []
    def push(self, value):
        self.stack.append(value)
    def pop(self):
        if self.size() > 0:
            return self.stack.pop()
        else:
            return None
    def size(self):
        return len(self.stack)   

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []

#the plan is to move player throw the rooms in a given direction (say n)
#ever room that is visited is added to the visited dictionary, every room visited is added to the
#traveral path. #the player will continue in this direction keeping ttravel back to this room
# and 1 is an array of other directions it could have traveled
#  (so if you are going N then S would be the way back)
#when player hits a room with no connections (ie a dead end) it will travel backwards
#till it hits a room where a cached direction is stored (it will check to see if that
#  room has been visited, if not it will
# continue that way till the text dead end)
#when a dead end occurs we will walk back until we find a connection, meaning there was a
#  new way to
#go that we have not travel. We will varify we havent gone to the room connected
#  in this driection, then we will continue in that direction until  the next
#dead end.

# fetch the opposite direction for when we're moving bacward
opposites_dir = {'n': 's', 'e': 'w', 's': 'n', 'w': 'e'}
# back to room with exit
previousRoom = [None]
#create a empty dictionary
roomTrack = {}
visited = {}
# Check each direction and make sure there is an exit
def checkDirections(roomId):
    #create direction as empty array 
    directions = []
    if 'n' in room_graph[roomId][1].keys():
        directions.append('n')
    if 'e' in room_graph[roomId][1].keys():
        directions.append('e')
    if 's' in room_graph[roomId][1].keys():
        directions.append('s')
    if 'w' in room_graph[roomId][1].keys():
        directions.append('w')
    return directions
    #check wheather length of visited less than len room_graph
while len(visited) < len(room_graph):
    roomid = player.current_room.id
    #if roomid is not in roomtrack
    if roomid not in roomTrack:
        # Put an array of room directions into roomTracking dict
        # append/add to visited so we can know when we have to visited all rooms
        visited[roomid] = roomid
        # add all directions using our direction finding algo
        roomTrack[roomid] = checkDirections(roomid)
    # check whethere any more directions to traverse
    if len(roomTrack[roomid]) < 1:
        previousDirection = previousRoom.pop()
        #add the previousDirection
        traversal_path.append(previousDirection)
        # send player into previous direction
        player.travel(previousDirection)
    else:
        # New direction to travel into. Pulled from list of directions
        nextDirection = roomTrack[roomid].pop(0)
        traversal_path.append(nextDirection)
        # Keep track in oppositie direction
        previousRoom.append(opposites_dir[nextDirection])
        player.travel(nextDirection)

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
