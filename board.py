from copy import deepcopy
import numpy as np
import datetime

class Board():
  
  months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
  dates = [str(i) for i in range(1, 32)]
  days = ["Sun", "Mon", "Tues", "Wed", "Thurs", "Fri", "Sat"]
  labels = months + dates + days

  dt_days = ["Mon", "Tues", "Wed", "Thurs", "Fri", "Sat", "Sun"]

  def __init__(self, year, month, day):
    self.weekday = self.dt_days[datetime.date(year,month,day).weekday()]
    self.month = self.months[month - 1]
    self.day = day
    self.date = [self.weekday, self.month, str(self.day)]

    self.matrix = [] # 2d array for main game
    self.matrix_labeled = [] # labeled 2d array for blocking given year, month, day 
    self.matrix_colored = []
    label_index = 0
    for i in range(8):
        row = []
        row_labeled = []
        for j in range(7):
            value = label = "X"
            # first 2 rows
            if i <= 1 and not j >= 6:
                value = "-"
                label = self.labels[label_index]
                label_index += 1
            # middle rows
            if i > 1 and not i > 6:
                value = "-"
                label = self.labels[label_index]
                label_index += 1
            # last row
            if i == 7 and not j <= 3:
                value = "-"
                label = self.labels[label_index]
                label_index += 1
            if label in self.date:
                value = "D"
            row.append(value)
            row_labeled.append(label.center(4))
        self.matrix.append(row)
        self.matrix_labeled.append(row_labeled)


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
    for i in range(8):
      for j in range(7):
        self.remaining_locations.append([i, j])

  def is_solvable(self):
    
    self.matrix_colored = deepcopy(self.matrix)
    # Mask all the filled pieces
    for i in range(8):
      for j in range(7):
        if isinstance(self.matrix_colored[i][j], int) or self.matrix_colored[i][j] == "D" or self.matrix_colored[i][j] == "X":
          self.matrix_colored[i][j] = -1

    color = 0
    # color the empty spaces
    for i in range(8):
      for j in range(7):
        if self.matrix_colored[i][j] == "-":
          if self.fill(i, j, self.matrix_colored[i][j], color):
            color += 1

    totals = {}
    for i in range(8):
      for j in range(7):
        if self.matrix_colored[i][j] != -1:
          totals.setdefault(self.matrix_colored[i][j], []).append((i,j))

    for i in totals:
      if len(totals[i]) == 4:
        # check for 2x2 void
        if totals[i][0][1] == totals[i][2][1]: # left is same col
          if totals[i][1][1] == totals[i][3][1]: # right is same col
            if totals[i][0][0] == totals[i][1][0]: # top is same row
              if totals[i][2][0] == totals[i][3][0]: # bottom is same row
                # print("Eeek! Found a 2x2 void!", file=open('output.txt', 'a'))
                # self.print()
                return False
      if len(totals[i]) < 4:
        return False

    return True

  def fill(self, row, col, initial, color):
    if row < 0 or row >= len(self.matrix_colored) or col < 0 or col >= len(self.matrix_colored[0]) or self.matrix_colored[row][col] != initial:
      return False
    self.matrix_colored[row][col] = color
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

  def print_labeled(self):
    for i in range(8):
      for j in range(7):
          print(self.matrix_labeled[i][j], end=" ", file=open('output.txt', 'a'))
      print("", file=open('output.txt', 'a'))
    print("\n", file=open('output.txt', 'a'))

  def print_colored(self):
    for i in range(8):
      for j in range(7):
          print(self.matrix_colored[i][j], end=" ", file=open('output.txt', 'a'))
      print("", file=open('output.txt', 'a'))
    print("\n", file=open('output.txt', 'a'))