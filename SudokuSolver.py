#!/usr/bin/env python
###########################################################################
#
# Copyright (c) 2009, Eric W. Wallace <e@ewall.org>
#
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License version 2 as published by
# the Free Software Foundation.
# (See http://www.fsf.org/licensing/licenses/info/GPLv2.html)
#
###########################################################################

debug = False

examplePuzzle1 = [ [0,8,6, 5,0,0, 0,0,7],
                   [7,0,0, 6,0,0, 3,0,0],
                   [0,5,3, 1,7,4, 0,6,0],
                   [1,0,0, 2,0,6, 0,0,0],
                   [4,7,0, 0,0,0, 0,2,3],
                   [0,0,0, 7,0,5, 0,0,4],
                   [0,1,0, 3,5,2, 7,9,0],
                   [0,0,9, 0,0,7, 0,0,5],
                   [5,0,0, 0,0,8, 4,3,0] ]

examplePuzzle2 = [ [1,7,6, 0,0,3, 4,0,8],
                   [5,8,0, 0,0,0, 0,0,0],
                   [0,2,0, 8,0,4, 0,0,1],
                   [0,0,5, 0,0,1, 2,8,4],
                   [0,0,0, 9,0,2, 0,0,0],
                   [7,1,2, 4,0,0, 5,0,0],
                   [6,0,0, 7,0,5, 0,3,0],
                   [0,0,0, 0,0,0, 0,4,6],
                   [8,0,3, 1,0,0, 9,7,5] ]

unsolvablePuzzle = [ [0,0,0, 0,0,0, 0,0,0],
                     [0,0,0, 0,0,0, 0,0,0],
                     [0,0,0, 0,0,0, 0,0,0],
                     [0,0,0, 0,0,0, 0,0,0],
                     [0,0,0, 0,0,0, 0,0,0],
                     [0,0,0, 0,0,0, 0,0,0],
                     [0,0,0, 0,0,0, 0,0,0],
                     [0,0,0, 0,0,0, 0,0,0],
                     [0,0,0, 0,0,0, 0,0,0] ]

class SudokuPuzzle():

    """
        This class represents and solves a 9x9 matrix Sudoku puzzle.

        Puzzles are 9x9 matrices as nested lists, like this:
            puzzle = [ [0,0,0, 0,0,0, 0,0,0],
                       [0,0,0, 0,0,0, 0,0,0],
                       [0,0,0, 0,0,0, 0,0,0],
                       [0,0,0, 0,0,0, 0,0,0],
                       [0,0,0, 0,0,0, 0,0,0],
                       [0,0,0, 0,0,0, 0,0,0],
                       [0,0,0, 0,0,0, 0,0,0],
                       [0,0,0, 0,0,0, 0,0,0],
                       [0,0,0, 0,0,0, 0,0,0] ]
        
        A few notes on the variables in the code...
        x will always represent the x-axis position / column number ordinally
        y will always represent the y-axis position / row number ordinally
        z will always represent the number of the square,
            assigned 1-9 from left-to-right and top-to-bottom
    """

    fullset = set(range(1,10))

    puzzle = None #will be assinged by __init__
    
    def __init__(self, puzzle):
        """ you must pass in a 9x9 nested-list matrix as the puzzle """
        self.puzzle = puzzle
        
    def point(self, x,y):
        """ return value at a coordinate in the puzzle """
        #first cardinalize the coordinates...
        x -= 1
        y -= 1
        return self.puzzle[y][x]

    def row(self,y):
        """ return ordinal row of puzzle as a set """
        return set( self.puzzle[y-1] )

    def col(self,x):
        """ return ordinal column of puzzle as a set """
        return set( [ col[x-1] for col in self.puzzle ] )

    def square(self,z):
        """ return ordinal square number of puzzle as a set """
        z -= 1
        boxCol = (z%3) * 3
        boxRow = (z/3) * 3
        return set( [ m[n] for m in self.puzzle[boxRow:boxRow+3] for n in range(boxCol,boxCol+3) ] )
        
    def squareNum(self,x,y):
        """ return square number from the given coordinates """
        #first cardinalize the coordinates...
        x -= 1
        y -= 1
        boxCol = 3 * int(y/3) #add 3 for each row
        boxRow = int(x/3) + 1 #add this (cardinal) for the row number
        return boxRow + boxCol

    def setPoint(self,x,y,value):
        """ set the value at the given coordinates """
        #first cardinalize the coordinates...
        x -= 1
        y -= 1
        self.puzzle[y][x]=value

    def checkPoint(self,x,y):
        """ calculate a single coordinate,
            assign the value if an answer is found,
            return True if this point is done """
        if (debug): print "Processing: ",x,",",y

        #exit if point is already done
        if (self.point(x,y) > 0): return True

        #get sets
        myRow = self.row(y)
        myCol = self.col(x)
        z = self.squareNum(x,y)
        mySquare = self.square(z)

        #get available values for the row
        rowNeeds = self.fullset.difference(myRow)
        if (debug): print "rowNeeds = ",rowNeeds
        if len(rowNeeds)==1:
            self.setPoint(x,y,rowNeeds.pop())
            return True

        #get available values for the column
        colNeeds = self.fullset.difference(myCol)
        if (debug): print "colNeeds = ",colNeeds
        if len(colNeeds)==1:
            self.setPoint(x,y,colNeeds.pop())
            return True

        #get available values for the square
        squareNeeds = self.fullset.difference(mySquare)
        if (debug): print "squareNeeds = ",squareNeeds
        if len(squareNeeds)==1:
            self.setPoint(x,y,squareNeeds.pop())
            return True

        #get intersection of the three sets
        possibilities = rowNeeds.intersection(colNeeds).intersection(squareNeeds)
        if (debug): print "possibilities = ",possibilities
        if len(possibilities)==1:
            self.setPoint(x,y,possibilities.pop())
            return True

        return False #if we got this far, we didn't answer this one

    def checkAllPoints(self):
        """ loop through all points, return True if puzzle is solved """
        #[ self.checkPoint(x,y) for x in range(1,10) for y in range(1,10) ]
        solved=True #assume true until proved otherwise
        for x in range(1,10):
            for y in range(1,10):
                if self.checkPoint(x,y)==False: solved=False
        return solved

    def solve(self):
        """ keep checking all points until either it's solved
            or 1000 loops have passed and we can't solve it """
        for i in range(1000):
            if self.checkAllPoints()==True: return True #quit as soon as its solved
        #stop infinite loop if we can't solve it
        print "Too many tries--cannot solve this one!"
        return False

    def tripleCheck(self):
        """ go over each row, column, and square to be sure it's solved """
        for i in range(1,10):
            if self.row(i)!=self.fullset: return False
            if self.col(i)!=self.fullset: return False
            if self.square(i)!=self.fullset: return False
        return True
            
    def prettyPrint(self):
        """ stdout printing of the puzzle """
        prettify = (lambda printRow: " | ".join([str(i) for i in printRow]))
        print "-" * 37
        for i in range(0,9):
            print "|",prettify(self.puzzle[i]),"|"
            print "-" * 37
    
def main():
    sp = SudokuPuzzle(examplePuzzle2)
    print "\nStarting Puzzle:"
    sp.prettyPrint()
    if sp.solve():
        if sp.tripleCheck()==True: print "\nSolved!"
        print "\nSolved Puzzle:"
        sp.prettyPrint()

if __name__ == "__main__":
    main()
