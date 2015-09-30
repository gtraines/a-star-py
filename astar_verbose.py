__author__ = 'Graham Traines'
# 19 September 2014
# CSCI 7130
# Chapter 4 Assignment

# Requires numpy
import heapq
import numpy as np

class Location(object):
    def __init__(self, x, y, goalnumber, tile, isempty = False):
        self.x = x
        self.y = y
        self.goalnumber = goalnumber
        self.tile = tile
        self.isempty = isempty
        #self.totaldistances = 0

class Puzzle(object):
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.grid = []
        self.goal_locations = []
        return

    def generate_puzzle(self):
        self.grid = np.empty(shape = (self.width, self.height), dtype=Location)
        cellvalue = 0
        for y in range(self.height):
            for x in range(self.width):
                self.grid[x][y] = Location(x, y, cellvalue, Tile(0, False), False)
                self.goal_locations.append(self.grid[x][y])
                cellvalue = cellvalue + 1
  
        self.grid[0][0].goalnumber = " "
        self.grid[0][0].isempty = True

        #line 0:  7 2 4
        self.grid[0][0].tile.tilenumber = 7
        self.grid[1][0].tile.tilenumber = 2
        self.grid[2][0].tile.tilenumber = 4
        
        #line 1: 5   6
        self.grid[0][1].tile.tilenumber = 5
        self.grid[1][1].tile.tilenumber = " "
        self.grid[1][1].isempty = True
        self.openlocation = self.grid[1][1]
        self.grid[2][1].tile.tilenumber = 6

        #line 2: 8 3 1
        self.grid[0][2].tile.tilenumber = 8
        self.grid[1][2].tile.tilenumber = 3
        self.grid[2][2].tile.tilenumber = 1

        self.totaldistances = self.get_total_distances()

        return

    def print_goal_state(self):
        print "Goal state:"
        for y in range(self.height):
            for x in range(self.width):
                print"[ %s ]" % str(self.grid[x, y].goalnumber),
            print
        return

    def print_current_state(self):
        print "Current puzzle state:"
        for y in range(self.height):
            for x in range(self.width):
                print"[ %s ]" % str(self.grid[x, y].tile.tilenumber),
            print
        return
                 
    def get_tile(self, x, y):
        return self.grid[x][y].tile

    def get_adjacent_tiles_locations(self, location):
        locations = []
        if location.x < self.width - 1:
            locations.append(self.grid[location.x + 1][location.y])
        if location.y > 0:
            locations.append(self.grid[location.x][location.y - 1])
        if location.x > 0:
            locations.append(self.grid[location.x - 1][location.y])
        if location.y < self.height - 1:
            locations.append(self.grid[location.x][location.y + 1])
        return locations

    def update_state(self, emptylocation, locationtiletomove):
        temptile = self.grid[emptylocation.x, emptylocation.y].tile
        
        self.grid[emptylocation.x, emptylocation.y].tile = locationtiletomove.tile
        self.grid[emptylocation.x, emptylocation.y].isempty = False
        if emptylocation.goalnumber == locationtiletomove.tile.tilenumber:
            locationtiletomove.tile.isinplace = True
        else: locationtiletomove.tile.isinplace = False

        self.grid[locationtiletomove.x, locationtiletomove.y].tile = temptile
        self.grid[locationtiletomove.x, locationtiletomove.y].isempty = True
        self.emptylocation = self.grid[locationtiletomove.x, locationtiletomove.y]
        self.totaldistances = self.get_total_distances()
        return

    def get_g_value(self):

        return self.get_total_distances()
    
    def get_manhattan_distance_to_goal(self, currentlocation):
        goallocation = self.get_goal_location(currentlocation.tile)

        xdistance = abs(currentlocation.x - goallocation.x)
        ydistance = abs(currentlocation.y - goallocation.y)

        return xdistance + ydistance
    
    def get_goal_location(self, tile):
        #home = 0
        if tile.tilenumber == ' ':
            return self.goal_locations[0]
        #while home != tile.tilenumber:
        #    for x in range(self.width):
        #        for y in range(self.height):
        #            home = self.grid[x, y].goalnumber
        return self.goal_locations[int(tile.tilenumber)]


    def get_total_distances(self):
        totaldistance = 0

        for y in range(self.height):
            for x in range(self.width):
                if self.grid[x, y].tile.isinplace == False and self.grid[x, y].tile.tilenumber != ' ':
                    tempdist = self.get_manhattan_distance_to_goal(self.grid[x, y])
                    totaldistance = totaldistance + tempdist
        return totaldistance

    def get_potential_distance_sum(self, openlocation, potentialtilelocation):

        currentdistancetogoal = self.get_manhattan_distance_to_goal(potentialtilelocation)

        potentiallocation = Location(openlocation.x, openlocation.y, " ", potentialtilelocation.tile)

        potentialnewdistancetogoal = self.get_manhattan_distance_to_goal(potentiallocation)
        
        return self.totaldistances - currentdistancetogoal + potentialnewdistancetogoal

    def get_heuristic(self, openlocation, potentialtilelocation):

        return self.get_potential_distance_sum(openlocation, potentialtilelocation)

class Tile(object):
    def __init__(self, tilenumber, isinplace):
        """
        Initialize a new tile
        @param tilenumber number of tile
        @param isinplace
        :rtype : object
        :return:void
        """
        self.isinplace = isinplace
        #self.parent = None
        self.tilenumber = tilenumber
        # value of G
        self.g = 0
        #value of H
        self.h = 0
        #sum of F
        self.f = 0



class AStar(object):
    def __init__(self):
        self.opened = []
        heapq.heapify(self.opened)
        self.closed = set()
        self.tiles = []
        self.iterations = 0

    def set_puzzle(self, puzzle):
        self.puzzle = puzzle
        self.start = self.puzzle.openlocation
        return

    def get_g_value(self):
        """
        Compute the actual state of the puzzle
        """
        return self.puzzle.get_g_value()

    def get_heuristic(self, currentlocation):
        return self.puzzle.get_heuristic(self.puzzle.openlocation, currentlocation)

    def move_tile(self, openlocation, tilelocation):
        """
        Move tile to open location
        :param openlocation: Open tile location
        :param tilelocation: Tile being processed
        :return:
        """
        self.puzzle.update_state(openlocation, tilelocation)
        return

    def display_option_value(self, potentialtile, newvalue):
        print("Considering %s -> Potential new value: %d" % (str(potentialtile.tilenumber), newvalue))
        return

    def process(self):
        
        print("Iteration %d" % self.iterations)
        self.iterations = self.iterations + 1
        
        # add starting tile to open heap queue
        adj_locations = self.puzzle.get_adjacent_tiles_locations(self.start)
        for adj_location in adj_locations:
            adj_location.f = self.get_heuristic(adj_location)
            heapq.heappush(self.opened, (adj_location.f, adj_location))
            self.display_option_value(adj_location.tile, adj_location.f)

        lasttilemoved = 0
        while len(self.opened):

            raw_input("Press Enter to advance to next step")
            print
            print("********************************")
            print("Iteration %d" % self.iterations)
            self.iterations = self.iterations + 1
            #pop tile from heap queue
            f, currentlocation = heapq.heappop(self.opened)
            #add tile to closed list so we don't process it twice
            lasttilemoved  = currentlocation.tile.tilenumber
            print
            print ("Chose %s" % currentlocation.tile.tilenumber)
            
            #swap empty tile for chosen tile
            self.opened = []
            self.move_tile(self.puzzle.openlocation, currentlocation)
            self.puzzle.openlocation = currentlocation
            self.puzzle.print_current_state()
             
            #if puzzle solved, display completed puzzle
            if self.puzzle.get_g_value() == 0:
                print("Puzzle solved!")
                self.puzzle.print_current_state()
                break

            #get adjacent tiles to current open tile
            adj_locations = self.puzzle.get_adjacent_tiles_locations(self.puzzle.openlocation)
            for adj_location in adj_locations:
                if adj_location.tile.tilenumber != lasttilemoved:
                    adj_location.f = self.get_heuristic(adj_location)
                    heapq.heappush(self.opened, (adj_location.f, adj_location))
                    self.display_option_value(adj_location.tile, adj_location.f)
                


puzzle = Puzzle(3, 3)
puzzle.generate_puzzle()
puzzle.print_goal_state()
puzzle.print_current_state()

a_star = AStar()
a_star.set_puzzle(puzzle)
a_star.process()
