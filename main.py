import numpy as np
import random as r
from copy import deepcopy
import itertools

class Piece():
  def __init__(self, code):
    self.piece = []
    self.create(code)

  def create(self, code):
    """ 
    Purpose: To allow easy creation of all the puzzle pieces

    Input: String containing data to create a puzzle piece
    Output: 2d array containing the layout of the puzzle piece
    """
    # Split the piece code string into rows
    row_delimiter = "|"
    split_code = code.split(row_delimiter)
    # for each row, split the string and create 2d array
    for i in range(len(split_code)):
      row = split_code[i].split()
      self.piece.append(list(row[0]))

  def get(self):
    """ 
    Purpose: To allow for array transformations using numpy
    
    Input: self
    Output: numpy array
    """
    return np.array(self.piece)

  """numpy tranformation helpers"""
  def flipX(self):
    self.piece = np.fliplr(self.get())

  def flipY(self):
    self.piece = np.flipud(self.get())

  def rot90(self):
    self.piece = np.rot90(self.get())

class Board():
  months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
  dates = [i for i in range(1, 32)]
  days = ["Sun", "Mon", "Tues", "Wed", "Thurs", "Fri", "Sat"]

  labels = months + dates + days

  def __init__(self):
    self.matrix = []
    # label_index = 0
    for i in range(8):
        row = []
        for j in range(7):
            value = "X"
            # first 2 rows
            if i <= 1 and not j >= 6:
                value = "-"
                # value = self.labels[label_index]
                # label_index += 1
            # middle rows
            if i > 1 and not i > 6:
                value = "-"
                # value = self.labels[label_index]
                # label_index += 1
            # last row
            if i == 7 and not j <= 3:
                value = "-"
                # value = self.labels[label_index]
                # label_index += 1
            row.append(value)
        self.matrix.append(row)

  def get(self):
    return self.matrix

  def set(self, matrix):
    self.matrix = matrix

  def next_location(self):
    for i in range(8):
      for j in range(7):
          if self.matrix[i][j] == "-":
            return i, j

  def print(self):
    for i in range(8):
      for j in range(7):
          print(self.matrix[i][j], end=" ")
      print("")


class Game():
    def __init__(self):
      self.pieces = {}
      self.permutations = []
      self.b = Board()
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
        for k in range(len(self.pieces[i])):
            print(np.array(self.pieces[i][k]))
            print("\n")
        print("-"*15,"\n")

    def remove_piece(self, i):
      self.pieces.pop(i)

    def overlay_piece(self, row, col, p):
      matrix = deepcopy(self.b.get())
      
      for i in range(len(p)):
          for j in range(len(p[0])):
            try:
              if matrix[row + i][col + j] == "-":
                matrix[row + i][col + j] = int(p[i][j])
                self.b.set(matrix)
            except:
              continue


    def piece_permutations(self):
      indices = []
      for i in self.pieces:
        print(len(self.pieces[i]))
        for j in range(len(self.pieces[i])):
          indices.append([i,j])

      print(indices)
      
      self.permutations = list(itertools.product(*indices))

      print(len(self.permutations))


    def get_piece(self):
      # get a remaining piece
      key = r.choice(list(self.pieces.keys()))
      return self.pieces[key]

    def place_pieces(self):
      row, col = self.b.next_location()
      
      self.b.print()
        
      p = self.get_piece()
      self.overlay_piece(row, col, p[0])
      # print(p[0])
      # for i in range (8):
      #   for j in range(7):
      #     print("Trying to overlay pice at row {} and column {}".format(i,j))
      #     self.b.overlay_piece(i, j, p)
      #     if i == 7 and j == 6:
      #       break
      row, col = self.b.next_location()
      p = self.get_piece()
      self.overlay_piece(row, col, p[0])


      # p = self.pieces[(r.randint(0,9))]

      # self.b.overlay_piece(0,0,p[1])

      self.b.print()
                
g = Game()
g.piece_permutations()




