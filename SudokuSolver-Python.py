# The comments I am about to put are mixed with my understanding of Lee Hsien Loong's code.
# He has his own explanations via comments in his original code, which was written in C++ - C style.
# I will try my best to understand his whole logic as I put my own comments along the way.
# My comments are still flawed in terms of the logic. I will update them as soon as I understand more about how his solver works.

# Some stuff to know regarding on syntax used in the code
# & = bitwise AND (different from logical AND, which is and)
# | = bitwise OR (different from logical OR, which is or)
# << = bitwise shift left (equivalent to multiplying by 2 actually)
# ~ = bitwise NOT (flipping all the bits)
# // = integer divison (if only a single forward-slash, it is float division)

# these initializations are referred to squares that have values on input
inBlock = [0] * 81
inRow = [0] * 81
inCol = [0] * 81

# initializations of constants
CONST_BLANK = 0
CONST_ONES = 1022 # also int(hex(0b1111111110), 16), this is to show that this integer is 9 bits

entry = [0] * 81 # mini-squares in a Sudoku puzzle for console input
block = [0] * 9 # 9 blocks consisting of 3x3 mini-squares
row = [0] * 9 # 9 rows of 9 mini-squares per row
col = [0] * 9 # 9 columns of 9 mini-squares per column

# initializations for Sudoku sequence - process of knowing what value to put in the empty mini-squares
seqPtr = 0
sequence = [0] * 81

count = 0 # initialization for overall count of how many guesses overall
levelCount = [0] * 81 # initialization of the array containing of how many placements/guesses were made in a mini-square

class SudokuSolver:

    # basically swapping elements based on index in the sequence array
    def swapSeqEntries(self, S1, S2):
        temp = sequence[S2]
        sequence[S2] = sequence[S1]
        sequence[S1] = temp

    # method for putting mini-squares with given values based on the input
    def initEntry(self, i, j, val):
        square = 9 * i + j # i = row, j = column; basically the formula on which mini-square to put
        valbit = 1 << val # left-shift 1 bit to the left, equivalent to multiplying by 2

        entry[square] = valbit # putting to the mini-square twice the value of the input
        block[inBlock[square]] &= ~valbit 
        col[j] &= ~valbit # can be in this way also: col[inCol[square]] &= ~valbit
        row[i] &= ~valbit # can be in this way also: row[inRow[square]] &= ~valbit

        global seqPtr # this is actually frowned upon by Python developers: putting the global keyword :)
        seqPtr2 = seqPtr # initializing a second sequence pointer based on the current global sequence pointer

        while (seqPtr2 < 81 and sequence[seqPtr2] != square):
            seqPtr2 += 1

        self.swapSeqEntries(seqPtr, seqPtr2)
        seqPtr += 1

    # method of printing the current state of the Sudoku puzzle on input and when solved
    def printArray(self):
        val = 1
        square = 0
        ch = ''

        # whole block of code is for printing the Sudoku puzzle neatly and nicely
        for i in range(9):
            if (i % 3 == 0):
                print()
            for j in range(9):
                if (j % 3 == 0):
                    print(f' ', end='') # not printing a new line, just a space
                valbit = entry[square]
                square += 1
                if (valbit == 0):
                    ch = '-'
                else:
                    for val in range (10):
                        if (valbit == (1 << val)):
                            ch = str(val)
                            break
                print(f'{ch}', end=' ')
            print()

    # method for duplicate checking of numbers in an input string
    def duplicateCheck(self, string):
        hasDuplicate = False

        if(len(string) == 9):
            if(string.count('1') > 1 or string.count('2') > 1 or string.count('3') > 1 or string.count('4') > 1 or string.count('5') > 1 or string.count('6') > 1 or string.count('7') > 1 or string.count('8') > 1 or string.count('9') > 1):
                hasDuplicate = True
        else:
            hasDuplicate = True

        return hasDuplicate

    # method for checking if there is a non-numeric character in an input string
    def nonNumericCheck(self, string):
        hasNonNumeric = False

        if(len(string) == 9):
            for char in string:
                if(not char.isnumeric() and char != '-'):
                    hasNonNumeric = True
                    break
        else:
            hasNonNumeric = True
        
        return hasNonNumeric

    # method for console input of the Sudoku puzzle
    def consoleInput(self):
        inputString = [''] * 9 # no buffer overflows should be allowed

        for i in range(9):
            print(f"Row {i+1}: ", end='')
            inputString = input()

            if(inputString.lower() == 'blank'):
                inputString = '---------'
                print(f"Row {i+1}: ---------")
            else:
                # input validation is now here
                while(len(inputString) != 9 or self.duplicateCheck(inputString) or self.nonNumericCheck(inputString)):
                    print(f"You can only input numbers from 1 to 9 without duplicating each number or '-' to represent an empty square and make sure that the length is EXACTLY 9.")
                    print(f"Row {i+1}: ", end='')
                    inputString = input()

            for j in range(9):
                ch = inputString[j]
                if (ch >= '1' and ch <= '9'): # surprising that this also works in Python, similar to int(ch) < 1 and int(ch) > 9 but make sure ch is not '-'
                    self.initEntry(i, j, int(ch))
        
        self.printArray()

    # method for printing statistics on the number of placements/guesses made in a mini-square
    def printStats(self):
        S = 0

        print()
        print(f"Level Counts: ")
        print()

        # this while loop will cause a runtime error if you input a fully solved Sudoku puzzle
        while(levelCount[S] == 0): # levelCount[S] represents how many placements/guesses were done, and there are only 81 squares in a Sudoku Puzzle
            if(S < 80): # array-indexing in Python is 0-based, thus going over 80 will lead to an error
                S += 1
            else: # break the loop when S reaches 80 already
                break
        
        i = 0
        
        while(S < 81):
            seq = sequence[S]
            print(f"{(seq // 9) + 1}, {(seq % 9) + 1}):  {levelCount[S]} ",   end=' ') # formula here is row #, col #, # of placements/guesses
            i += 1
            if(i > 5):
                print()
                i = 0
            S += 1
        
        print()
        print()
        print(f"Count = {count}")

    # method to invoke if program has successfully solved the Sudoku puzzle
    def succeed(self):
        self.printArray()
        self.printStats()

    # method for getting the next pointer for swapping in current sequence
    def nextSeq(self, S):
        S2 = 0
        MinBitCount = 100
        T = S

        for a in range(T, 81):
            Square = sequence[a]
            Possibles = block[inBlock[Square]] & row[inRow[Square]] & col[inCol[Square]]
            BitCount = 0
            while (Possibles):
                Possibles &= ~(Possibles & -Possibles) # the one in parenthesis gets the least significant '1' bit, and then proceeds to flip the bits, and does logical AND to the original value
                BitCount += 1
            if (BitCount < MinBitCount):
                MinBitCount = BitCount
                S2 = a

        return S2

    # method for placing the right number to put in the empty mini-squares
    def place(self, S):
        if(S >= 81):
            self.succeed()
            return

        global count
        levelCount[S] += 1
        count += 1
        
        S2 = self.nextSeq(S)
        self.swapSeqEntries(S, S2)

        Square = sequence[S]

        #these indexes should have a value greater than or equal to zero and less than 9
        BlockIndex = inBlock[Square]
        RowIndex = inRow[Square]
        ColIndex = inCol[Square]

        Possibles = block[BlockIndex] & row[RowIndex] & col[ColIndex]
        while(Possibles):
            valbit = Possibles & (-Possibles) # gets the least significant '1' bit, basically where the first 1 bits of both numbers are going to intersect; this is where calculation of what to put in an empty mini-square happens
            Possibles &= ~valbit # Possibles = Possibles & ~valbit, sort of reducing the number of possibilities left
            entry[Square] = valbit # this is where placing the value actually happens
            block[BlockIndex] &= ~valbit 
            row[RowIndex] &= ~valbit 
            col[ColIndex] &= ~valbit 

            self.place(S + 1) # recursive call

            block[BlockIndex] |= valbit
            row[RowIndex] |= valbit 
            col[ColIndex] |= valbit 

        entry[Square] = CONST_BLANK # can be put inside while loop

        self.swapSeqEntries(S, S2)
    
    # method for resetting everything when choosing to solve again
    def reset_everything(self):
        global inBlock, inRow, inCol, entry, block, row, col, seqPtr, sequence, count, levelCount

        inBlock = [0] * 81
        inRow = [0] * 81
        inCol = [0] * 81

        entry = [0] * 81
        block = [0] * 9
        row = [0] * 9
        col = [0] * 9

        seqPtr = 0
        sequence = [0] * 81

        count = 0
        levelCount = [0] * 81
    
    # method for initializing when starting to solve
    def initialize(self):
        for i in range(9):
            for j in range(9):
                square = 9 * i + j
                inRow[square] = i
                inCol[square] = j
                inBlock[square] = (i // 3) * 3 + (j // 3) # both (i // 3) and (j // 3) will have values ranged from 0 to 2; a block is a 2D array with 3 rows and 3 columns, thus this formula for represntation

        for square in range(81):
            sequence[square] = square
            entry[square] = CONST_BLANK
            levelCount[square] = 0

        for i in range(9):
            block[i] = row[i] = col[i] = CONST_ONES # initialize the 9-bit integers
   
    # main method
    def main(self):
        try:
            with open(f"./custom-files/welcome-message.txt", "r") as f:
                next_line = f.readline()
                while(next_line):
                    if(f.readline() != ''):
                        print(f'{next_line}')
                        next_line = f.readline()
                    else:
                        print(f'{next_line}', end=' ')
                        break
            
            choice = input()
            iteration = 0

            while(choice):
                if(choice == '1'):
                    iteration += 1
                    if (iteration > 1):
                        self.reset_everything()
                    self.initialize()
                    self.consoleInput()
                    self.place(seqPtr)
                    print(f"\nTotal Count = {count}\n")
                    print(f"Great! Would you like to solve again? If so, input 1. Else, input 0/exit.\n")
                    print(f"Please input your choice:", end=' ')
                    choice = input()
                elif(choice == '0' or choice.lower() == 'exit'):
                    print(f"\nThanks for using the program!")
                    break
                else:
                    print(f"\nInvalid input given. Please input either 1 to see action or 0/exit to exit the program.\n")
                    print(f"Please input your choice:", end=' ')
                    choice = input()
        except:
            print(f"\nAn error occured.")

import cProfile
import pstats
import io
import os
from datetime import datetime

# call the class' main method
if __name__ == "__main__":
    #profiling code
    with cProfile.Profile() as pr:
        pr.enable()
        SudokuSolver().main()
        pr.disable()

    # making results readable to a human
    s = io.StringIO()
    ps = pstats.Stats(pr, stream=s).sort_stats('tottime')
    ps.print_stats()

    #getting file name for logging
    now = datetime.now()
    dt_string = now.strftime("%d%m%Y%H%M%S")

    if (not os.path.isdir(f'./program-logs/')):
        os.mkdir(f'./program-logs/')

    with open(f"./program-logs/{dt_string}.txt", 'w+') as f:
        f.write(s.getvalue())