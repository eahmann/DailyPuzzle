from xmlrpc.client import boolean
from copy import deepcopy

class Board():
  # months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
  # dates = [i for i in range(1, 32)]
  # days = ["Sun", "Mon", "Tues", "Wed", "Thurs", "Fri", "Sat"]
  # labels = months + dates + days

  def __init__(self):
    self.remaining_locations = []
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
    # self.matrix[0][1] = "D"
    # self.matrix[5][3] = "D"
    # self.matrix[7][5] = "D"
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
          location = self.next_location()
      except:
        break
      placed = self.overlay_piece(location[0], location[1], piece)
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
              return

      # Add function to check for void state and return boolean

      self.set(matrix)
      return True

  def find_remaining(self):
    self.remaining_locations = []
    for i in range(0, 8):
      for j in range(0, 7):
        self.remaining_locations.append([i, j])
          # if self.matrix[i][j] == "-":
          #   self.remaining_locations.append([i, j])
          # if self.matrix[i][j] == "D":
          #   self.remaining_locations.append([i, j])

  def is_isolated(self, copy) -> boolean:
    pass


  def mark_filled(self):
    copy = deepcopy(self.matrix)
    for i in range(8):
      for j in range(7):
        if isinstance(copy[i][j], int) or copy[i][j] == "D":
          copy[i][j] = "X"

    for i in range(8):
      for j in range(7):
          print(copy[i][j], end=" ")
      print("")
    print("\n")

    for i in range(1,8): #row
      for j in range(0,7): #cols
        if (j + 1) < 7:
          if copy[i][j] == "X" and copy[i][j + 1] == "X" and copy[i - 1][j + 1] == "X":
            if copy[i - 1][j] == "-":
              print("Found a void at {}:{}".format(i-1,j))

          


  def next_location(self):
    return self.remaining_locations.pop(0)

  def print(self):
    for i in range(8):
      for j in range(7):
          print(self.matrix[i][j], end=" ")
      print("")
    print("\n")