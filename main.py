import random as r
import numpy as np
from copy import deepcopy
import itertools
from piece import Piece
from board import Board

class Game():
    def __init__(self):
      self.pieces = {}
      self.generate_pieces()
      self.order_permutations = list(itertools.permutations([i for i in range(len(self.pieces))],len(self.pieces)))
      self.stack = []
      # Contains a list of 2d list for maintaining the state of the game
      # [[{piece number}, {current rotation (0..n)}, {max rotation (n)}]]
      self.state = []
      

    def get_order(self) -> list:
      return list(self.order_permutations.pop(r.randrange(0, len(self.order_permutations))))

    def do_next(self):
      self.state = []
      for i in self.get_order():
        self.state.append([i, 0, len(self.pieces[i]) - 1])
      

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
      self.do_next()

      # hotwire game
      #self.state = [[5, 3, 3], [7, 3, 3], [4, 3, 3], [1, 3, 7], [9, 1, 1], [0, 6, 7], [3, 5, 7], [8, 5, 7], [6, 0, 3], [2, 0, 3]]
      print(self.state, file=open('output.txt', 'a'))


      index = 0
      self.stack = []
      self.stack.append(Board())


      while index > -1:
        # Get the latest board from the stack
        b = deepcopy(self.stack[-1])

        #print("\nstate:",self.state)
        #b.print()

        piece = self.get_piece(self.state[index][0], self.state[index][1])
        placed = b.place_piece(piece)

        if placed: # move (index) to the next piece in the order and addd the board to stack
          if b.is_solvable():
            index += 1
            self.stack.append(b)
          else:
            placed = False

        if index == len(self.state):
          print("\nWinner!",self.state, file=open('output.txt', 'a'))
          b.print()
          index -= 1

          index = self.move_index(index)
          self.state[index][1] += 1

        if not placed: # try the next rotation
          self.state[index][1] += 1

        if not placed and self.state[index][1] > self.state[index][2]: # backtrack
          index = self.move_index(index)
          self.state[index][1] += 1

      self.solver()

    def move_index(self, index):
      # move the index to where the current rotation is not yet max
      while self.state[index][1] >= self.state[index][2]:
        index -= 1
        # print(index)
        self.stack.pop()

      # reset state
      for i in range(index + 1, len(self.state)):
        self.state[i][1] = 0

      return index

if __name__ == "__main__":
  g = Game()
  g.solver()


