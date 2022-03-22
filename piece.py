import numpy as np


class Piece():
    def __init__(self, code):
        self.piece = []
        self.create(code)

    def create(self, code):
        """
        Convert delimited string to 2d array

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
        Helper function to return a np array of the piece

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
