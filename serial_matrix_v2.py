#!/usr/bin/env python3
########################################
# Name:        Jennifer Sanchez
# ID:          88505016
# Course:      Parallel Computing
# Assignment:  HomeWork #1 Part 2
#
########################################
import random, time, pymp

class MatrixIncompatibleError(Exception):
    def __init__(self, message):
        super().__init__(message)

class Matrix(object):
    __doc__ = ''''''
    def __init__(self, rows, cols, randGen=False):
        self.rows = rows
        self.cols = cols
        # Overhead of the pymp shared array requires that
        # both serial and parallel versions use the same data structure
        # for accurate time differences
        self.table = pymp.shared.array((rows,cols), dtype='int')
        if randGen:
            for i in range(self.rows):
                for j in range(self.cols):
                    self.table[i][j] = random.randint(1,6)

    #Matrix Multiply python function
    def __matmul__(self, target):
        if not self.rows == target.cols:
            raise MatrixIncompatibleError("Matrix row count does not match target Matrix column count!\n")
        resultMatrix = Matrix(self.rows, target.cols)
        #_row: row of initial matrix, row: target matrix, rows: # of rows/cols

        for _row in range(self.rows):
            for col in range(target.cols):
                for row in range(target.rows):
                    resultMatrix.table[_row][col] += self.table[_row][row] * target.table[row][col]
        return resultMatrix
    #Table format
    def __str__(self):
        resultMatrix = ''
        for row in self.table:
            for i in row:
                resultMatrix += str(i) + ' '
            resultMatrix += ' \n'
        return resultMatrix
    #Safeguarding main function
if __name__ == '__main__':
    m = Matrix(10, 100000, True)
    n = Matrix(100000, 10, True)
    # @ m.__matmul__(n)
    print('Begin\n')
    start = time.time()
    result = m @ n
    end = time.time()
    print(result)
    print('Time Taken: ' + str(end-start) + 's')
