import os
import pickle
import numpy as np
import logging

import constants
from timing_maze_state import TimingMazeState

##### Frank (9/16):
# For exploration algorithm
from experience import Experience
#################

##### Tom (9/15):
# For heap in a*
import heapq
#################


class Player:
    def __init__(self, rng: np.random.Generator, logger: logging.Logger,
                 precomp_dir: str, maximum_door_frequency: int, radius: int) -> None:
        """Initialise the player with the basic amoeba information

            Args:
                rng (np.random.Generator): numpy random number generator, use this for same player behavior across run
                logger (logging.Logger): logger use this like logger.info("message")
                maximum_door_frequency (int): the maximum frequency of doors
                radius (int): the radius of the drone
                precomp_dir (str): Directory path to store/load pre-computation
        """

        # precomp_path = os.path.join(precomp_dir, "{}.pkl".format(map_path))

        # # precompute check
        # if os.path.isfile(precomp_path):
        #     # Getting back the objects:
        #     with open(precomp_path, "rb") as f:
        #         self.obj0, self.obj1, self.obj2 = pickle.load(f)
        # else:
        #     # Compute objects to store
        #     self.obj0, self.obj1, self.obj2 = _

        #     # Dump the objects
        #     with open(precomp_path, 'wb') as f:
        #         pickle.dump([self.obj0, self.obj1, self.obj2], f)

        self.rng = rng
        self.logger = logger
        self.maximum_door_frequency = maximum_door_frequency
        self.radius = radius

        ########## Tom (9/15):
        self.frontier = []
        self.explored = set()
        self.path = []
        ######################

        ########## Frank (9/16):
        self.experience = Experience(self.maximum_door_frequency, self.radius)
        ######################


    def move(self, current_percept) -> int:
        """Function which retrieves the current state of the amoeba map and returns an amoeba movement

            Args:
                current_percept(TimingMazeState): contains current state information
            Returns:
                int: This function returns the next move of the user:
                    WAIT = -1
                    LEFT = 0
                    UP = 1
                    RIGHT = 2
                    DOWN = 3
        """
        ################################ Tom (9/15): Comment this chunk to go back to default player
        # If there's no path, run A* to find one
        if not self.path:
            #print("not self.path")
            self.path = self.a_star(current_percept)
        
        # If A* found a path, execute the next move
        else:
            # Get the next move from the path
            #print("yes self.path")
            next_move = self.path.pop(0) 
            #print("next move is")
            #print(next_move)
            return next_move
        ############################################ Comment this chunk to go back to default player

        # default_player:
        # The condition of the four doors at the current cell
        direction = [0, 0, 0, 0] # [left, up, right, down]; 1 is closed, 2 is open, 3 is boundary
        for maze_state in current_percept.maze_state: # looping through all the cells visible by the drone
            if maze_state[0] == 0 and maze_state[1] == 0: # (0,0) is the current loc; -> Looking to see the conditions of the four doors at the current location.
                direction[maze_state[2]] = maze_state[3] # import that information into direction

        if current_percept.is_end_visible:
            if abs(current_percept.end_x) >= abs(current_percept.end_y): # huhh???
                if (current_percept.end_x > 0 # if goal is on the right side
                    and direction[constants.RIGHT] == constants.OPEN # if the door on the right is open
                    ):
                    for maze_state in current_percept.maze_state: # looping through all the cells visible by the drone
                        if (maze_state[0] == 1 and maze_state[1] == 0 # (1,0) is the cell on the right; -> Looking to see the conditions of the four doors at the cell on the right.
                            and maze_state[2] == constants.LEFT and maze_state[3] == constants.OPEN # if the left door of the cell on the right (the adjacent door to the current cell) is open
                            ):
                            return constants.RIGHT # goes right -> returning 2
                        
                if (current_percept.end_x < 0 # if goal is on the left side
                    and direction[constants.LEFT] == constants.OPEN # if the door on the left is open
                    ):
                    for maze_state in current_percept.maze_state: # looping through all the cells visible by the drone
                        if (maze_state[0] == -1 and maze_state[1] == 0 # (-1,0) is the cell on the left; -> Looking to see the conditions of the four doors at the cell on the left.
                            and maze_state[2] == constants.RIGHT and maze_state[3] == constants.OPEN # if the right door of the cell on the left (the adjacent door to the current cell) is open
                            ):
                            return constants.LEFT # goes left -> returning 0
                        
                if (current_percept.end_y < 0 # if goal is above
                    and direction[constants.UP] == constants.OPEN # if the door above is open
                    ):
                    for maze_state in current_percept.maze_state: # looping through all the cells visible by the drone
                        if (maze_state[0] == 0 and maze_state[1] == -1 # (0,-1) is the cell above; -> Looking to see the conditions of the four doors at the cell above.
                            and maze_state[2] == constants.DOWN and maze_state[3] == constants.OPEN # if the down door of the cell above (the adjacent door to the current cell) is open
                            ):
                            return constants.UP # goes up -> returning 1
                        
                if (current_percept.end_y > 0 # if goal is below
                    and direction[constants.DOWN] == constants.OPEN # if the door below is open
                    ):
                    for maze_state in current_percept.maze_state: # looping through all the cells visible by the drone
                        if (maze_state[0] == 0 and maze_state[1] == 1 # (0,1) is the cell below; -> Looking to see the conditions of the four doors at the cell below.
                            and maze_state[2] == constants.UP and maze_state[3] == constants.OPEN # if the above door of the cell below (the adjacent door to the current cell) is open
                            ): 
                            return constants.DOWN # goes down -> returning 3
                        
                return constants.WAIT # return -1
            
            else:
                if (current_percept.end_y < 0 # if goal is above
                    and direction[constants.UP] == constants.OPEN # if the door above is open
                    ):
                    for maze_state in current_percept.maze_state: # looping through all the cells visible by the drone
                        if (maze_state[0] == 0 and maze_state[1] == -1 # (0,-1) is the cell above; -> Looking to see the conditions of the four doors at the cell above.
                            and maze_state[2] == constants.DOWN and maze_state[3] == constants.OPEN # if the down door of the cell above (the adjacent door to the current cell) is open
                            ):
                            return constants.UP # return 1
                        
                if (current_percept.end_y > 0 # if goal is below
                    and direction[constants.DOWN] == constants.OPEN # if the door below is open
                    ):
                    for maze_state in current_percept.maze_state: # looping through all the cells visible by the drone
                        if (maze_state[0] == 0 and maze_state[1] == 1 # (0,1) is the cell below; -> Looking to see the conditions of the four doors at the cell below.
                            and maze_state[2] == constants.UP and maze_state[3] == constants.OPEN # if the above door of the cell below (the adjacent door to the current cell) is open
                            ):
                            return constants.DOWN # return 3
                        
                if (current_percept.end_x > 0 # if goal is on the right side
                    and direction[constants.RIGHT] == constants.OPEN # if the door on the right is open
                    ):
                    for maze_state in current_percept.maze_state: # looping through all the cells visible by the drone
                        if (maze_state[0] == 1 and maze_state[1] == 0 # (1,0) is the cell on the right; -> Looking to see the conditions of the four doors at the cell on the right.
                            and maze_state[2] == constants.LEFT and maze_state[3] == constants.OPEN # if the left door of the cell on the right (the adjacent door to the current cell) is open
                            ):
                            return constants.RIGHT # return 2
                        
                if (current_percept.end_x < 0 # if goal is on the left side
                    and direction[constants.LEFT] == constants.OPEN # if the door on the left is open
                    ):
                    for maze_state in current_percept.maze_state: # looping through all the cells visible by the drone
                        if (maze_state[0] == -1 and maze_state[1] == 0 # (-1,0) is the cell on the left; -> Looking to see the conditions of the four doors at the cell on the left.
                            and maze_state[2] == constants.RIGHT and maze_state[3] == constants.OPEN # if the right door of the cell on the left (the adjacent door to the current cell) is open
                            ):
                            return constants.LEFT #return 0
                        
                return constants.WAIT # return -1
            
        else: # If End is not visible

            ########## Frank (9/16):
            move = self.experience.move(current_percept)

            if self.experience.is_valid_move(current_percept, move):
                return move

            self.experience.wait()
            return constants.WAIT
            ###########################
    

    ########################################## Tom (9/15):
    def a_star (self, current_percept):
        # Reset frontier and explored set
        self.frontier = []
        self.explored = set()

        # Start position and goal position
        start = (0, 0)  # (x, y) relative position
        #print("start is: ")
        #print(start)
        goal = (current_percept.end_x, current_percept.end_y)
        #print("goal is:")
        #print(goal)

        # Push the start state to the frontier with a cost of 0
        heapq.heappush(self.frontier, (0, start))
        came_from = {start: None}
        cost_so_far = {start: 0}

        while self.frontier:
            _, current = heapq.heappop(self.frontier)
            #print ("current is:")
            #print (current)
            # Loop until the current state is the goal;
            # Once the current state is the goal, we know that the path is found;
            # then call the reconstruct_path function to construct a path.
            if current == goal:
                
                return self.reconstruct_path(came_from, start, goal)

            self.explored.add(current)
            
            # Get the possible moves from the current position
            neighbors = self.get_neighbors(current, current_percept)
            #print("neighbors are:")
            #print(neighbors)
            for direction, neighbor in neighbors:
                new_cost = cost_so_far[current] + 1  # Assume each move costs 1
                if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                    cost_so_far[neighbor] = new_cost
                    priority = new_cost + self.heuristic(neighbor, goal)
                    heapq.heappush(self.frontier, (priority, neighbor))
                    came_from[neighbor] = (current, direction)
        
        return None  # No path found
    

    # Manhattan distance heuristic for A*
    def heuristic(self, current, goal):
        return abs(current[0] - goal[0]) + abs(current[1] - goal[1])


    # Get neighbors and their movement directions based on door states.
    def get_neighbors(self, current, current_percept):
        x, y = current
        #directions = [constants.LEFT, constants.UP, constants.RIGHT, constants.DOWN]
        #moves = [(-1, 0), (0, -1), (1, 0), (0, 1)]  # left, up, right, down
        neighbors = []

        # The condition of the four doors at the current cell
        counter1 = 0
        direction = [0, 0, 0, 0] # [left, up, right, down]; 1 is closed, 2 is open, 3 is boundary
        for maze_state in current_percept.maze_state: # looping through all the cells visible by the drone
            if maze_state[0] == x and maze_state[1] == y: # (x,y) is the current loc; -> Looking to see the conditions of the four doors at the current location.
                direction[maze_state[2]] = maze_state[3] # import that information into direction
                counter1 += 1
            # Meaning we have gathered everything needed for the variable direction; no need to keep going
            if counter1 == 4: 
                break

        # Check if "moving to right" is a legit move: checking 1). the right door is open; 2) the left door on the cell to the right is open 
        if (direction[constants.RIGHT] == constants.OPEN): # if the door on the right is open
            for maze_state in current_percept.maze_state: # looping through all the cells visible by the drone
                        if (maze_state[0] == x+1 and maze_state[1] == y+0 # (x+1,y+0) is the cell on the right; -> Looking to see the conditions of the four doors at the cell on the right.
                            and maze_state[2] == constants.LEFT and maze_state[3] == constants.OPEN # if the left door of the cell on the right (the adjacent door to the current cell) is open
                            ):
                            neighbors.append((constants.RIGHT, (x + 1, y)))
                            break

        # Check if "moving to left" is a legit move: checking 1). the left door is open; 2) the right door on the cell to the left is open 
        if (direction[constants.LEFT] == constants.OPEN): # if the door on the left is open
            for maze_state in current_percept.maze_state: # looping through all the cells visible by the drone
                        if (maze_state[0] == x-1 and maze_state[1] == y+0 # (x-1,y+0) is the cell on the left; -> Looking to see the conditions of the four doors at the cell on the left.
                            and maze_state[2] == constants.RIGHT and maze_state[3] == constants.OPEN # if the right door of the cell on the left (the adjacent door to the current cell) is open
                            ):
                            neighbors.append((constants.LEFT, (x - 1, y)))
                            break
                
        # Check if "moving up" is a legit move: checking 1). the up door is open; 2) the down door on the cell above is open 
        if (direction[constants.UP] == constants.OPEN): # if the door above is open
            for maze_state in current_percept.maze_state: # looping through all the cells visible by the drone
                        if (maze_state[0] == x+0 and maze_state[1] == y-1 # (x+0,y-1) is the cell above; -> Looking to see the conditions of the four doors at the cell above.
                            and maze_state[2] == constants.DOWN and maze_state[3] == constants.OPEN # if the down door of the cell above (the adjacent door to the current cell) is open
                            ):
                            neighbors.append((constants.UP, (x, y - 1)))
                            break

        # Check if "moving down" is a legit move: checking 1). the down door is open; 2) the up door on the cell to the below is open 
        if (direction[constants.DOWN] == constants.OPEN): # if the door below is open
            for maze_state in current_percept.maze_state: # looping through all the cells visible by the drone
                        if (maze_state[0] == x+0 and maze_state[1] == y+1 # (x+0,y+1) is the cell below; -> Looking to see the conditions of the four doors at the cell below.
                            and maze_state[2] == constants.UP and maze_state[3] == constants.OPEN # if the up door of the cell below (the adjacent door to the current cell) is open
                            ):
                            neighbors.append((constants.DOWN, (x, y + 1)))
                            break

        # Finally return the neighbors that we can possibly move to.
        return neighbors


    def reconstruct_path(self, came_from, start, goal):
        """Reconstruct the path from start to goal."""
        path = []
        current = goal
        while current != start:
            current, direction = came_from[current]
            path.append(direction)
        path.reverse()
        #print("path is:")
        #print(path)
        return path
    ##########################################