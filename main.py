from datetime import datetime
import random as r
from copy import deepcopy
import itertools
from piece import Piece
from board import Board
import os


class Game():
    def __init__(self, year=datetime.now().year,
                 month=datetime.now().month, day=datetime.now().day):
        self.year, self.month, self.day = year, month, day
        
        # Setup output path
        self.output_filename = "output/" + "_".join(
            [str(self.year), str(self.month), str(self.day)]) + ".txt"
        if not os.path.exists('output'):
            os.makedirs('output')

        # Dictionary for pieces and their rotations
        self.pieces = {}
        self.generate_pieces()

        # A list of all possible ways to order the pieces (10 digits, 0 to 9)
        self.order_permutations = list(itertools.permutations(
            [i for i in range(len(self.pieces))], len(self.pieces)))

        self.stack = []
        # Initialize the blank board here so we can print it only once per run
        self.stack.append(
            Board(
                self.year,
                self.month,
                self.day,
                self.output_filename))
        print("Solving for date:", self.year, self.month, self.day, file=open(
            self.output_filename, 'a'))
        self.stack[0].print()

        # Contains a list of 2d list for maintaining the state of the game
        # [[{piece number}, {current rotation (0..n)}, {max rotation (n)}]]
        self.state = []
        self.solutions = []

    def get_order(self) -> list:
        '''
        Return a randomly selected order permutation
        '''
        return list(self.order_permutations.pop(
            r.randrange(0, len(self.order_permutations))))

    def init_next_order(self):
        '''
        Initialize the state of the game with a new order
        '''
        self.state = []
        for i in self.get_order():
            self.state.append([i, 0, len(self.pieces[i]) - 1])

    def generate_pieces(self):
        '''
        Generate all possible rotations/reflections of each piece and add it to the dictionary
        '''
        piece_defs = [
            "000|00-",
            "11|1-|1-|1-",
            "22|2-|22",
            "333|3--",
            "--4|444|4--",
            "-55|55-",
            "666|-6-|-6-",
            "7--|7--|777",
            "-8|88|8-|8-",
            "9999"]

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

    def get_piece(self, key, rotation):
        '''
        Return a specific piece
        '''
        return self.pieces[key][rotation]

    def solver(self):
        while self.order_permutations:
            self.init_next_order()
            count = 0

            print(
                "New order:",
                [i[0] for i in self.state], file=open(
                    self.output_filename, 'a'), end=" ")

            index = 0  # current index in the order of pieces
            if len(self.stack) == 0:
                self.stack.append(
                    Board(
                        self.year,
                        self.month,
                        self.day,
                        self.output_filename))

            while index > -1:
                # Get the latest board from the stack
                b = deepcopy(self.stack[-1])

                # Get the next piece
                piece = self.get_piece(
                    self.state[index][0], self.state[index][1])

                # Try to place the piece on the board
                placed = b.place_piece(piece)

                # add the board to stack and move to the next piece
                if placed:
                    if b.is_solvable():
                        index += 1
                        self.stack.append(b)
                        count += 1
                    else:
                        placed = False

                # Wiining solution
                if index == len(self.state):
                    if b.get() not in self.solutions:
                        print("Solution found after {} piece placements.".format(count), file=open(
                            self.output_filename, 'a'))
                        self.solutions.append(b.get())
                        print(
                            "Solution #{}".format(
                                len(self.solutions)), self.state, file=open(
                                self.output_filename, 'a'))
                        b.print()

                        print(
                            "Continueing with state:",
                            self.state, file=open(
                                self.output_filename, 'a'), end=" ")
                    else:
                        print(
                            "Duplicate solution found after {} piece placements.".format(count), file=open(
                                self.output_filename, 'a'))
                        print("With state: {}".format(self.state), file=open(
                                self.output_filename, 'a'))
                        b.print()
                    index -= 1
                    count = 0

                    index = self.move_index(index)
                    self.state[index][1] += 1

                # try the next rotation
                if not placed:
                    self.state[index][1] += 1
                    count += 1

                # backtrack if no more rotations on the current piece
                if not placed and self.state[index][1] > self.state[index][2]:
                    index = self.move_index(index)
                    self.state[index][1] += 1

            print("Failed after {} piece placements.".format(count), file=open(
                self.output_filename, 'a'))

    def move_index(self, index):
        # move the index to where the current rotation is not yet max
        while self.state[index][1] >= self.state[index][2]:
            index -= 1
            self.stack.pop()

        # reset state
        for i in range(index + 1, len(self.state)):
            self.state[i][1] = 0

        return index


if __name__ == "__main__":
    g = Game()
    g.solver()
