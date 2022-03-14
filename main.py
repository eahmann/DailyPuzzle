from array import array
from inspect import stack
import random as r
import numpy as np
from copy import deepcopy
import itertools
from piece import Piece
from board import Board
import sys
print(sys.getrecursionlimit())
class Game():
    def __init__(self):
      self.pieces = {}
      self.order_permutations = list(itertools.permutations([0,1,2,3,4,5,6,7,8,9],10))
      self.generate_pieces()
      self.stack = []

      # order of the pieces
      self.order = []
      

      # index of the current piece
      self.position = 0


      self.state = {}
      

    def next_order(self) -> list:
      self.order = list(self.order_permutations.pop(r.randrange(0, len(self.order_permutations))))

    def init_state(self):
      for i in self.order:
        self.state[i] = {'cur': 0, 'max': len(self.pieces[i]) - 1}
      print(self.state)

    def generate_pieces(self):
      piece_defs = ["000|00-","11|1-|1-|1-", "22|2-|22", "333|3--","--4|444|4--", "-55|55-", "666|-6-|-6-", "7--|7--|777", "-8|88|8-|8-", "9999"]

      for i, code in enumerate(piece_defs, start=0):
        piece = Piece(code)
        self.pieces.setdefault(i, []).append(piece.get().tolist())

        pieceFlipY = deepcopy(piece)
        pieceFlipY.flipY()
        if (pieceFlipY.get().tolist() not in self.pieces[i]):
          self.pieces[i].append(pieceFlipY.get().tolist())
  
        pieceFlipX = deepcopy(piece)
        pieceFlipX.flipX()
        if (pieceFlipX.get().tolist() not in self.pieces[i]):
          self.pieces[i].append(pieceFlipX.get().tolist())
  
        pieceFlipYFlipX = deepcopy(pieceFlipY)
        pieceFlipYFlipX.flipX()
        if (pieceFlipYFlipX.get().tolist() not in self.pieces[i]):
            self.pieces[i].append(pieceFlipYFlipX.get().tolist())
  
        pieceRot90 = deepcopy(piece)
        pieceRot90.rot90()
        if (pieceRot90.get().tolist() not in self.pieces[i]):
            self.pieces[i].append(pieceRot90.get().tolist())
  
        pieceRot90FlipY = deepcopy(pieceRot90)
        pieceRot90FlipY.flipY()
        if (pieceRot90FlipY.get().tolist() not in self.pieces[i]):
            self.pieces[i].append(pieceRot90FlipY.get().tolist())
  
        pieceRot90FlipX = deepcopy(pieceRot90)
        pieceRot90FlipX.flipX()
        if (pieceRot90FlipX.get().tolist() not in self.pieces[i]):
            self.pieces[i].append(pieceRot90FlipX.get().tolist())
  
        pieceRot90FlipYFlipX = deepcopy(pieceRot90FlipY)
        pieceRot90FlipYFlipX.flipX()
        if (pieceRot90FlipYFlipX.get().tolist() not in self.pieces[i]):
            self.pieces[i].append(pieceRot90FlipYFlipX.get().tolist())
  
        # Print out the pieces
        # for k in range(len(self.pieces[i])):
        #     print(np.array(self.pieces[i][k]))
        #     print("\n")
        # print("-"*15,"\n")


    def get_piece(self, key, rotation):
      return self.pieces[key][rotation]


    def solver(self):
      self.next_order()
      self.init_state()
      self.position = 0

      # Initialize with a blank board
      if len(self.stack) == 0:
        self.stack.append(Board())


      while self.position <= len(self.pieces) - 1:
        # Get the latest board from the stack
        b = deepcopy(self.stack[-1])

        b.print()

        current_piece = self.order[self.position]
        current_rotation = self.state[self.order[self.position]]['cur']

        piece = self.get_piece(current_piece,current_rotation)

        placed = b.place_piece(piece)

        if placed: 
          self.position += 1
          self.stack.append(b)

        if not placed: 
          self.state[self.order[self.position]]['cur'] += 1

        if not placed and self.state[self.order[self.position]]['cur'] >= self.state[self.order[self.position]]['max']: # backtrack
          print("start backtracking...")
          self.set_position()

          
          self.state[self.order[self.position]]['cur'] += 1

          print("end backtrack")

      self.solver()

    def set_position(self):
      
      if self.state[self.order[self.position]]['cur'] >= self.state[self.order[self.position]]['max']:
        self.position -= 1
        self.stack.pop()
        self.set_position()

      print(self.order[self.position])
      print(self.order)
      # reset remaining to initial rotation
      pos = self.position
      while pos + 1 < len(self.order):

        self.state[self.order[pos + 1]]['cur'] = 0

        pos += 1

if __name__ == "__main__":
  g = Game()
  g.solver()


