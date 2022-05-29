# ReemAqra_1181818
from abc import ABC, abstractmethod
import time
import random


class Sudoku:
    def __init__(self):
        self._data = [["" for _ in range(9)] for _ in range(9)]

    # read data from file and store it in array
    def readFromFile(self):
        self._data = []
        with open('Input.txt', 'r') as file:
            for row in file:
                row = row.replace("\n", "")

                row = row.split(',')
                self._data.append(row)

        for row in range(len(self._data)):
            for col in range(len(self._data)):
                if (self._data[row][col] == ""):
                    self._data[row][col] = "0"
                self._data[row][col] = int(self._data[row][col])

    def fillValues(self):
        print("1. Easy")
        print("2. Medium")
        print("3. Difficult")
        print()
        print("Enter your choice: ", end="")
        choice = int(input())

        K = 30

        if (choice == 1):
        #Easy (E)
            K = 81 * 60 // 100
            #48  number to fill
        elif (choice == 2):
        #Medium(M)
            K = 81 * 75 // 100
            #60 number to fill
        elif (choice == 3):
        #Difficult(D)
            K = 81 * 90 // 100
            #72 number to fill


        self.fillDiagonal()
        self.fillRemaining(0, 3)
        self.removeKDigits(K)
        self.printSudoku()

    # fill diagonal Boxes
    def fillDiagonal(self):
        for i in range(0, 9, 3):
            self.fillBox(i, i)

    # check is the Box is unused
    def unUsedInBox(self, rowStart, colStart, num):
        for i in range(3):
            for j in range(3):
                if (self._data[rowStart + i][colStart + j] == num):
                    return False

        return True
   # fill Box
    def fillBox(self, row, col):
        num = 0
        #3 * 3 Box
        for i in range(3):
            for j in range(3):
                num = self.randomGenerator(9)
                while (not self.unUsedInBox(row, col, num)):
                    num = self.randomGenerator(9)
                self._data[row + i][col + j] = num;

    #get a random number from 1 -  num
    def randomGenerator(self, num):
        return random.randint(1, num)

    # check if the number position is safe
    def CheckIfSafe(self, i, j, num):
        SRN = 3
        return (self.unUsedInRow(i, num) and self.unUsedInCol(j, num) and self.unUsedInBox(i - i % SRN, j - j % SRN,num))

   #check if the number not repeated in the Row
    def unUsedInRow(self, i, num):
        for j in range(9):
            if (self._data[i][j] == num):
                return False
        return True

    # check if the number not repeated in the one colom
    def unUsedInCol(self, j, num):
        for i in range(9):
            if (self._data[i][j] == num):
                return False
        return True


    def fillRemaining(self, i, j):
        SRN = 3 # 3*3 Boxes
        N = 9 # for 9*9 suduko

        if (j >= N and i < N - 1):
            # then move to the next Row
            i = i + 1;
            j = 0;

        if (i >= N and j >= N):
            # the end of suduko
            return True

        if (i < SRN):
            if (j < SRN):
                #j=3
                j = SRN
        elif (i < N - SRN):
            if (j == (i // SRN) * SRN):
                # j=6
                j = j + SRN
        else:
            if (j == N - SRN):
                i = i + 1
                j = 0
                if (i >= N):
                    return True

        for num in range(1, N + 1):
            if (self.CheckIfSafe(i, j, num)):
                self._data[i][j] = num;
                if (self.fillRemaining(i, j + 1)):
                    return True
                self._data[i][j] = 0

        return False

    #remove digite by Level of difficulty
    def removeKDigits(self, K):
        count = K
        N = 9
        while (count != 0):
            #get a random number form 1 to 81
            cellId = self.randomGenerator(N * N);

            # Determine which cell it is located in
            i = (cellId // N) % N
            j = cellId % 9

            if (self._data[i][j] != 0):
                count = count - 1
                self._data[i][j] = 0

    # this function to find a hint if the user order
    def findHint(self):
        data = [[d for d in row] for row in self._data]
        self.solveSuduko(0, 0)

        t = None

        for row in range(len(self._data)):
            for col in range(len(self._data[0])):
                if (data[row][col] == 0):
                    t = (row + 1, col + 1, self._data[row][col])
                    break

        self._data = data

        return t
    #print sudoku to user
    def printSudoku(self):
        rows = 'ABCDEFGHI'
        cols = '123456789'
        for i, _ in enumerate(rows):
            if i in [3, 6]:
                print('------+------+------')
            for j, _ in enumerate(cols):
                if j in [3, 6]:
                    print('|', end="")
                if (self._data[i][j] == 0):
                    print(' ', end=" ")
                else:
                    print(self._data[i][j], end=" ")
            print()

    def isSafe(self, row, col, num):
        for x in range(9):
            if self._data[row][x] == num:
                return False

        for x in range(9):
            if self._data[x][col] == num:
                return False

        startRow = row - row % 3
        startCol = col - col % 3

        for i in range(3):
            for j in range(3):
                if self._data[i + startRow][j + startCol] == num:
                    return False
        return True

    def solveSuduko(self, row, col):

        N = len(self._data)
        if (row == N - 1 and col == N):
            return True

        if col == N:
            row += 1
            col = 0

        if self._data[row][col] > 0:
            # the feild is full go to the next
            return self.solveSuduko(row, col + 1)

        for num in range(1, N + 1, 1):
            if self.isSafe(row, col, num):
                self._data[row][col] = num
                if self.solveSuduko(row, col + 1):
                    return True
            self._data[row][col] = 0

        return False

    def fill(self):
        value = input("Enter [row column value] to fill: ")
        value = value.split(" ")

        if (len(value) != 3):
            return False

        if (not (value[0].isdigit() and value[1].isdigit() and value[2].isdigit())):
            return False

        row = int(value[0])
        column = int(value[1])
        if (row in range(1, 10) and column in range(1, 10) and int(value[2]) in range(1, 10)):
            data = [[d for d in row] for row in self._data]
            self.solveSuduko(0, 0)
            if (self._data[row - 1][column - 1] == int(value[2])):
                self._data = data
                self._data[row - 1][column - 1] = int(value[2])
                return True
            self._data = data
        return False

    def sudokuisSolved(self):
        for row in range(len(self._data)):
            for col in range(len(self._data)):
                if self._data[row][col] < 1 or type(self._data[row][col]) is not type(1):
                    return False
                elif self._data[row][col] > len(self._data):
                    return False

        for row in self._data:
            if sorted(list(set(row))) != sorted(row):
                return False

        cols = []
        for col in range(len(self._data)):
            for row in self._data:
                cols += [row[col]]

            if sorted(list(set(cols))) != sorted(cols):
                return False
            cols = []

        return True


class Player(ABC):
    def __init__(self, number):
        self._playerNumber = number

    @abstractmethod
    def addPoint(self):
        pass

    @abstractmethod
    def substractPoint(self):
        pass


class OnePlayerMode(Player):
    def __init__(self, number):
        super().__init__(number)
        self._points1 = 0
        self._totalTime1 = 0

    def addPoint(self, point, turn):
        if turn == 1:
            self._points1 = self._points1 + point

    def substractPoint(self, point, turn):
        if turn == 1:
            self._points1 = self._points1 - point

    def addTime(self, time, turn):

        if turn == 1:
            self._totalTime1 += time

    def getTime(self):
        return self._totalTime1

    def getScore(self):
        return self._points1

    def printScore(self):
        # calculate the score of the player
        print("Player 1 Score: ", end="")
        player1Score = 0
        if (self.getTime() != 0):
            player1Score = self.getScore() * (3600)
            player1Score = player1Score / (81 * (self.getTime()))

        if (self.getScore() <= 0):
            player1Score = 0

        print(player1Score)

    def playGame(self, sudoku):
        turn = 1
        while (not sudoku.sudokuisSolved()):
            print("1. Fill")
            print("2. Hint")
            print("3. Solve")
            print()

            print("Enter your choice: ", end="")
            choice = int(input())

            start_time = time.time()

            if (choice == 1):
            #fill a specific cell (row, column) by a specific value (value
                if (sudoku.fill()):
                    self.addPoint(1, turn)
                else:
                    print("Invalid Option Selected. Minus One point..")
                    self.substractPoint(1, turn)
            elif (choice == 2):
                #fill one cell and print on the screen a tuple (row, column, value)
                hint = sudoku.findHint()

                if (hint is not None):
                    print("Hint")
                    print("Row    : ", hint[0])
                    print("Column : ", hint[1])
                    print("Value  : ", hint[2])
                else:
                    print("No Hint Found")

            elif (choice == 3):
            #solve the whole puzzle
                if (not sudoku.solveSuduko(0, 0)):
                    print("No solution  exists ")
            else:
                print("Invalid Option. Try again..")

            end_time = time.time()
            sudoku.printSudoku()

            print("Player took ", (end_time - start_time), " seconds to select option", choice)
            self.addTime(end_time - start_time, turn)
        self.printScore()

# class of Tow player mode
class TwoPlayerMode(OnePlayerMode):
    def __init__(self, number):
        super().__init__(number)

        self._points2 = 0
        self._totalTime2 = 0

    def addTime(self, time, turn):
        if (turn == 1):
            # then player number 1 is playing
            super().addTime(time, turn)
        else:
            #Turn for the second player
            self._totalTime2 += time

    # if player score add point
    def addPoint(self, point, turn):
        if turn == 1:
            #player num 1
            super().addPoint(point, turn)
        else:
            #turn =2
            self._points2 = self._points2 + point


    # if player didnt scoure right substract point
    def substractPoint(self, point, turn):
        if turn == 1:
            super().substractPoint(point, turn)
        else:
            # turn = 2
            self._points2 = self._points2 - point

    #print scoure of each player
    def printScore(self):
        # scoure of the first player
        print("Player 1 Score: ", end="")
        player1Score = 0
        if (super().getTime() != 0):
            player1Score = super().getScore() * (self._totalTime2 + super().getTime())
            player1Score = player1Score / ( 81 * (super().getTime()))


        if (super().getScore() <= 0):
            player1Score = 0

        print(player1Score)

        # scoure of the secound player
        print("Player 2 Score: ", end="")

        player2Score = 0
        if (self._totalTime2 != 0):
            player2Score = self._points2 * (self._totalTime2 + super().getTime())
            player2Score = player2Score / ( 81  * self._totalTime2)

        if (self._points2 <= 0):
            player2Score = 0
        print(player2Score)

    def playGame(self, sudoku):
        turn = 1
        player1AlreadyPass = False
        player2AlreadyPass = False

        while (not sudoku.sudokuisSolved()):
            print("Turn of Player", turn)
            print()
            print("1. Fill")
            print("2. Pass")
            print("3. Solve")
            print()

            print("Enter your choice: ", end="")
            choice = int(input())

            start_time = time.time()

            if (choice == 1):
            #fill sudoku
                if (sudoku.fill()):
                    # the player fill right add point
                    self.addPoint(1, turn)
                else:
                    print("Invalid Option Selected. Minus One point..")
                    # un correct answer
                    self.substractPoint(1, turn)

                if (turn == 1):
                    player1AlreadyPass = False
                else:
                    player2AlreadyPass = False

            elif (choice == 2):
            # give the player hint
                if (turn == 1 and player1AlreadyPass):
                    hint = sudoku.findHint()

                    if (hint is not None):
                        print("Hint")
                        print("Row    : ", hint[0])
                        print("Column : ", hint[1])
                        print("Value  : ", hint[2])
                    else:
                        print("No Hint Found")
                elif (turn == 1):
                    player1AlreadyPass = True
                elif (turn == 2 and player2AlreadyPass):
                    hint = sudoku.findHint()

                    if (hint is not None):
                        print("Hint")
                        print("Row    : ", hint[0])
                        print("Column : ", hint[1])
                        print("Value  : ", hint[2])
                    else:
                        print("No Hint Found")
                elif (turn == 2):
                    player2AlreadyPass = True

                if (turn == 1):
                    turn = 2
                else:
                    turn = 1

                self.substractPoint(1, turn)
            elif (choice == 3):
                #solve the sudoko
                if (not sudoku.solveSuduko(0, 0)):
                    print("No solution  exists ")
            else:
                print("Invalid Option. Try again..")

            sudoku.printSudoku()
            end_time = time.time()

            print("Player ", turn, " took ", (end_time - start_time), " seconds to select option", choice)
            self.addTime(end_time - start_time, turn)
        self.printScore()


def main():
    exitFlag = False
    sudoku = Sudoku()

    while (not exitFlag):
        print("===============================")
        print("            MENU               ")
        print("===============================")
        print("1. Load a puzzle from a text file")
        print("2. Start a random puzzle")
        print("3. Exit")
        print()
        print("Enter your choice: ", end="")
        choice = int(input())
        # choice = 1

        if (choice == 1):
            sudoku.readFromFile()
            sudoku.printSudoku()
        elif (choice == 2):
            sudoku.fillValues()
        elif (choice == 3):
            exitFlag = True
            break

        print("1. One player mode")
        print("2. Two Player mode")
        print()
        print("Enter your choice: ", end="")
        choice = int(input())

        mode = OnePlayerMode("One Player Mode")
        if (choice == 2):
            mode = TwoPlayerMode("Two Player Mode")

        mode.playGame(sudoku)


if __name__ == "__main__":
    main()
