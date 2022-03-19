from copy import deepcopy
import numpy as np


class Board():
  
  # months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
  # dates = [i for i in range(1, 32)]
  # days = ["Sun", "Mon", "Tues", "Wed", "Thurs", "Fri", "Sat"]
  # labels = months + dates + days

  def __init__(self):
    self.remaining_locations = []
    self.matrix = []
    self.matrix2 = []
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
    self.matrix[0][2] = "D"
    self.matrix[4][1] = "D"
    self.matrix[6][6] = "D"
    #self.print()


  def get(self):
    return self.matrix

  def set(self, matrix):
    self.matrix = matrix

  def place_piece(self, piece):
    self.find_remaining()
    placed = False
    while not placed:
      try: 
          loc = self.next_location()
      except:
        break
      placed = self.overlay_piece(loc[0], loc[1], piece)
    return placed

  def overlay_piece(self, row: int, col: int, p):
      # make a copy so we can undo if the piece doesn't fit in the row, col
      matrix = deepcopy(self.get())
      
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
              return False

      # self.set(matrix)
      # return True
      if self.is_solvable():
        self.set(matrix)
        return True 
      else:
        return False



  def find_remaining(self):
    self.remaining_locations = []
    for i in range(0, 8):
      for j in range(0, 7):
        self.remaining_locations.append([i, j])
          # if self.matrix[i][j] == "-":
          #   self.remaining_locations.append([i, j])
          # if self.matrix[i][j] == "D":
          #   self.remaining_locations.append([i, j])

  def is_solvable(self):
    
    self.matrix2 = deepcopy(self.matrix)
    # Mask all the filled pieces
    for i in range(8):
      for j in range(7):
        if isinstance(self.matrix2[i][j], int) or self.matrix2[i][j] == "D" or self.matrix2[i][j] == "X":
          self.matrix2[i][j] = -1

    color = 0
    # color the empty spaces
    for i in range(8):
      for j in range(7):
        if self.matrix2[i][j] == "-":
          if self.fill(i, j, self.matrix2[i][j], color):
            color += 1

    totals = {}
    for i in range(8):
      for j in range(7):
        if self.matrix2[i][j] != -1:
          totals[self.matrix2[i][j]] = totals.setdefault(self.matrix2[i][j], 0) + 1
   # print(np.array(self.matrix2))
   # print(totals)

    for i in totals:
      #print(totals[i])
      if totals[i] < 4:
        return False

    return True

  def fill(self, row, col, initial, color):
    if row < 0 or row >= len(self.matrix2) or col < 0 or col >= len(self.matrix2[0]) or self.matrix2[row][col] != initial:
      return False
    self.matrix2[row][col] = color
    self.fill(row - 1, col, initial, color)
    self.fill(row + 1, col, initial, color)
    self.fill(row, col - 1, initial, color)
    self.fill(row, col + 1, initial, color)
    return True
          

  def IsIsolated(self, matrix, row, col):
    # check the corner
    if row == 0:
      if col == 0:
        if matrix[row][col] == "-" and matrix[row + 1][col] == "X" and matrix[row][col + 1] == "X":
          return True
      # check the rest of top row
      if matrix[row][col] == "-" and matrix[row + 1][col] == "X" and matrix[row - 1][col] == "X" and matrix[row][col + 1] == "X":
          return True
    # if row > 0 and row < len(matrix[0]):
    #     if matrix[row][col] == "-" and matrix[row + 1][col] == "X" and matrix[row][col + 1] == "X":
    #       return True



  def next_location(self):
    return self.remaining_locations.pop(0)

  def print(self):
    for i in range(8):
      for j in range(7):
          print(self.matrix[i][j], end=" ", file=open('output.txt', 'a'))
      print("", file=open('output.txt', 'a'))
    print("\n", file=open('output.txt', 'a'))
    #     print(self.matrix[i][j], end=" ")
    #   print("")
    # print("\n")