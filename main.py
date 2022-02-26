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
                  return
                elif matrix[row + i][col + j] == "D":
                  return
                elif isinstance(matrix[row + i][col + j] , int):
                  return
                else: matrix[row + i][col + j] = int(p[i][j])




              # if isinstance(matrix[row + i][col + j] , int) and not p[i][j] == "-": # matrix AND piece locations is int -> return
              #   return
              # if matrix[row + i][col + j] == "X" and not p[i][j] == "-": # Don't place a piece on the X's
              #   return
              # if not matrix[row + i][col + j] == "X" and not p[i][j] == "-":
              #   matrix[row + i][col + j] = int(p[i][j])
              # elif isinstance(matrix[row + i][col + j] , int) and p[i][j] == "-":
              #   continue
              # elif matrix[row + i][col + j] == "D" and p[i][j] == "-":
              #   continue
            except:
              return
      self.b.set(matrix)
      return True

    def get_order(self) -> list:
      return list(itertools.permutations([0,1,2,3,4,5,6,7,8,9],10))

    def get_rotation(self) -> list:
      indices = {}
      for i in self.pieces:
        for j in range(len(self.pieces[i])):
          indices.setdefault(i, []).append(j)
      return list(itertools.product(*indices.values()))

    def get_piece(self, key, rotation):
      return self.pieces[key][rotation]

    def place_pieces(self):
      order = self.get_order()
      rotation = self.get_rotation()

      while True:
        for i in reversed(order): # i is a tuple of the order of pieces. order is length 3628800
          for j in rotation: # tuple of the rotation pieces. rotation is length 8388608
            self.b = Board()
            order, rotation = list(i), list(j)
            #print(order, rotation)
            
            for index, key in enumerate(order):
              self.b.find_remaining()
              print("Trying piece {}".format(key), file=open('output.txt', 'a'))
              self.b.print()
              while True:
                try: 
                  location = self.b.next_location()
                except:
                  break
                #print(o)
                piece = self.get_piece(order[index], rotation[key])
              
                #print(np.array(piece))
                
                result = self.overlay_piece(location[0], location[1], piece)
                if result:
                  self.pieces.pop(i, None)
                  break
                if len(self.pieces) == 0:
                  print("Filled the board!", file=open('output.txt', 'a'))
                  self.b.print()
                  return
            

          self.b.print()
   
g = Game()
g.place_pieces()