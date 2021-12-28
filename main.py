import numpy as np

class Piece():
  def __init__(self, code):
    self.piece = []
    self.create(code)

  def create(self, code):
    index = 0
    for i in range(4):
      row = []
      for j in range(4):
          row.append(code[index])
          index += 1
      self.piece.append(row)

  def get(self):
    return self.piece

  def print(self):
    print("print piece")
    for i in range (4):
      for j in range(4):
        print(self.piece[i][j], end=" ")
      print("")

  def flipX(self):
    self.piece = np.fliplr(self.piece)

  def flipY(self):
    self.piece = np.flipud(self.piece)

  def rot90(self):
    self.piece = np.rot90(self.piece)

piece_defs = ["000-00----------","11--1---1---1---", "22--2---22------", "333---3---------","--4-444-4-------", "-55-55----------", "666---6---------", "7---7---777-----", "--8-888---8-----", "9999------------"]

pieces = [Piece(i) for i in piece_defs]

for i in range(len(pieces)): pieces[i].print()

pieces[5].print()
pieces[5].flipY()

pieces[5].print()
pieces[5].flipY()
pieces[5].flipX()

pieces[5].print()
pieces[5].flipY()
pieces[5].print()
pieces[5].rot90()
pieces[5].print()

class Board():
  matrix = []

  def __init__(self):
    for i in range(8):
        row = []
        value = "X"
        for j in range(7):
            # first 2 rows
            if i <= 1 and not j >= 6:
                value = "-"
            # middle rows
            if i > 1 and not i > 6:
                value = "-"
            # last row
            if i == 7 and not j <= 3:
                value = "-"
            row.append(value)
        self.matrix.append(row)

  def print(self):

    print("Puzzle matrix is")

    for i in range (8):
      for j in range(7):
          print(self.matrix[i][j], end=" ")
      print("")