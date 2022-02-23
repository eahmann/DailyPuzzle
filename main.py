import numpy as np
import random as r

class Piece():
  def __init__(self, code):
    self.piece = []
    self.create(code)

  def create(self, code):
    # Split the piece code string into rows
    row_delimiter = "|"
    split_code = code.split(row_delimiter)

    # for each row, split the string and create 2d array
    for i in range(len(split_code)):
      row = split_code[i].split()
      self.piece.append(list(row[0]))

  def get(self):
    return np.array(self.piece)

  def print(self):
    for i in range(len(self.piece)):
      for j in range(len(self.piece[0]) ):
        print(self.piece[i][j], end=" ")
      print("")

  def flipX(self):
    self.piece = np.fliplr(self.get())

  def flipY(self):
    self.piece = np.flipud(self.get())

  def rot90(self):
    self.piece = np.rot90(self.get())

piece_defs = ["000|00-","11|1-|1-|1-", "22|2-|22", "333|3--","--4|444|4--", "-55|55-", "666|-6-|-6-", "7--|7--|777", "-8|88|8-|8-", "9999"]

# pieces = [Piece(i) for i in piece_defs]

# for i in range(len(pieces)): 
#     print("\nnormal")
#     #pieces[i].print()
#     print(pieces[i].get())

    # print("\nflipY 1")
    # pieces[i].flipY()
    # print(pieces[i].get())

    # print("\nrot90 1")
    # pieces[i].rot90()
    # print(pieces[i].get())

    # print("\nflipX 1")
    # pieces[i].flipX()
    # print(pieces[i].get())

    # print("\nrot90 2")
    # pieces[i].rot90()
    # print(pieces[i].get())

    # print("\nrot90 3")
    # pieces[i].rot90()
    # print(pieces[i].get())

pieces = {}

for i, code in enumerate(piece_defs, start=0):
    print(code)
    piece = Piece(code)
    print(type(piece))
    pieces.setdefault(i, []).append(piece)
    pieces[i].append(piece.flipY())
    pieces[i].append(piece.flipX())
    print(pieces[i])
    print(pieces[i][0].get())


for i in range(len(pieces)): 
    for j in range(len(pieces[i])):
        print(pieces[i][j].get())

class Board():
  matrix = []

  def __init__(self):
    for i in range(8):
        row = []
        for j in range(7):
            value = "X"
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

  def get(self):
    return self.matrix

  def print(self):
    for i in range (8):
      for j in range(7):
          print(self.matrix[i][j], end=" ")
      print("")

  def get_random_piece(self):
    return pieces.pop(r.randint(0,9))

b = Board()
# b.print()

# p = b.get_random_piece()
# p.print()
# p = b.get_random_piece()
# p.print()

# print(len(pieces))

def solve():
  b = Board()
#   b.print()

#   print(b.get())

  # TODO: find next available spot
  for i in range(8):
        row = []
        for j in range(7):
            value = "X"
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

  # TODO: see if piece fits on board

  # TODO: rotate piece if it doesn't fit

solve()