class Board():
  months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
  dates = [i for i in range(1, 32)]
  days = ["Sun", "Mon", "Tues", "Wed", "Thurs", "Fri", "Sat"]
  labels = months + dates + days

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
    self.matrix[0][1] = "D"
    self.matrix[5][3] = "D"
    self.matrix[7][5] = "D"
    #self.print()


  def get(self):
    return self.matrix

  def set(self, matrix):
    self.matrix = matrix

  def find_remaining(self):
    self.remaining_locations = []
    for i in range(0, 8):
      for j in range(0, 7):
          if self.matrix[i][j] == "-":
            self.remaining_locations.append([i, j])
          if self.matrix[i][j] == "D":
            self.remaining_locations.append([i, j])

  def detect_bad_state(self):
    for i in range(8):
      for j in range(7):
        if i == 0:
          # check 1x1 blocked off location
          if self.matrix[i][j] == "-" and \
           (isinstance(self.matrix[i][j + 1], int) or self.matrix[i][j + 1] == "D") and \
             (isinstance(self.matrix[i + 1][j], int) or self.matrix[i + 1][j] == "D"):
            print("Found an issue")


  def next_location(self):
    return self.remaining_locations.pop(0)

  def print(self):
    for i in range(8):
      for j in range(7):
          print(self.matrix[i][j], end=" ", file=open('output.txt', 'a'))
      print("", file=open('output.txt', 'a'))
    print("\n", file=open('output.txt', 'a'))