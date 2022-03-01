import random as r
import numpy as np
from copy import deepcopy
import itertools
from piece import Piece
from board import Board

class Game():
    def __init__(self, order):
      self.pieces = {}
      self.order = order
      self.generate_pieces()
      self.order_rotations = self.generate_order_rotations()

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

    def remove_piece(self, i):
      self.pieces.pop(i)

    def overlay_piece(self, row, col, p):
      matrix = deepcopy(self.b.get())
      
      for i in range(len(p)):
          for j in range(len(p[0])):
            try: # this should catch invalid matrix locations (ie.. placing a piece too close to the edge)
              if p[i][j] == "-":
                continue
              else:
                if matrix[row + i][col + j] == "X":
                  return False
                elif matrix[row + i][col + j] == "D":
                  return False
                elif isinstance(matrix[row + i][col + j] , int):
                  return False
                else: matrix[row + i][col + j] = int(p[i][j])
            except:
              return
      self.b.set(matrix)
      return True

    def get_order(self) -> list:
      return list(self.piece_order_permutations.pop(r.randrange(0, len(self.piece_order_permutations))))

    def generate_order_rotations(self) -> list:
      indices = {}
      for i in self.pieces:
        for j in range(len(self.pieces[i])):
          indices.setdefault(i, []).append(j)
      return list(itertools.product(*indices.values()))

    def get_piece(self, key, rotation):
      return self.pieces[key][rotation]


    def place_pieces(self, runs = 1):
      print("Call #{} with order {}".format(runs, self.order), file=open('output.txt', 'a'))
      rotations = self.order_rotations
      

      #print("order: ", order)
      for j in rotations: # j is a list
        # print("With piece rotation {}".format(j), file=open('output.txt', 'a'))
        self.b = Board()
        remaining = deepcopy(self.order)
        for i in self.order: # i is an int
          self.b.find_remaining()
          piece = self.get_piece(i, j[i])
          placed = False
          while not placed:
            try: 
                location = self.b.next_location()
            except:
              break
            placed = self.overlay_piece(location[0], location[1], piece)
          if (placed):
            self.b.print()
            self.b.mark_filled()
            remaining.pop(remaining.index(i))
          if len(remaining) == 0:
            print("Winner! With piece order {} and rotation {}".format(j, self.order), file=open('output.txt', 'a'))
            self.b.print()
          #print(np.array(piece))

      self.place_pieces(runs + 1)         




if __name__ == "__main__":
  piece_order_permutations = list(itertools.permutations([0,1,2,3,4,5,6,7,8,9],10))

  def get_order() -> list:
    return list(piece_order_permutations.pop(r.randrange(0, len(piece_order_permutations))))
    #return list(piece_order_permutations.pop())

  def do_game():
    g = Game(get_order())
    g.place_pieces()

  while piece_order_permutations:
    do_game()

