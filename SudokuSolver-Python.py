# The comments I am about to put are mixed with my understanding of Lee Hsien Loong's code.
# He has his own explanations via comments in his original code, which was written in C++ - C style.
# I will try my best to understand his whole logic as I put my own comments along the way.
# My comments are still flawed in terms of the logic. I will update them as soon as I understand more about how his solver works.

# Some stuff to know regarding on syntax used in the code
# & = bitwise AND (different from logical AND, which is and)
# | = bitwise OR (different from logical OR, which is or)
# << = bitwise shift left (equivalent to multiplying by 2 actually)
# ~ = bitwise NOT (flipping all the bit)
# // = integer divison (if only a single forward-slash, it is float division)

# these initializations are referred to squares that have values on input
inBlock = [0] * 81
inRow = [0] * 81
inCol = [0] * 81

# initializations of constants
CONST_BLANK = 0
CONST_ONES = int(hex(0b1111111110), 16) # can actually be just 1022, this is to show that this integer is 9 bits

entry = [0] * 81 # mini-squares in a Sudoku puzzle for console input
block = [0] * 9 # 9 blocks consisting of 3x3 mini-squares
row = [0] * 9 # 9 rows of 9 mini-squares per row
col = [0] * 9 # 9 columns of 9 mini-squares per column

# initializations for Sudoku sequence - knowing what value to put in the empty mini-squares
seqPtr = 0
sequence = [0] * 81

count = 0 # initialization for overall count of how many guesses overall
levelCount = [0] * 81 # initialization of the array of mini-squares  

class SudokuSolver:

    # basically swapping elements based on index in the sequence array
    def SwapSeqEntries(self, S1, S2):
        temp = sequence[S2]
        sequence[S2] = sequence[S1]
        sequence[S1] = temp

    # method for putting mini-squares with given values based on the input
    def InitEntry(self, i, j, val):
        square = 9 * i + j # i = row, j = column; basically the formula on which mini-square to put
        valbit = 1 << val # left-shift 1 bit to the left, equivalent to multiplying by 2

        entry[square] = valbit # putting to the mini-square twice the value of the input
        block[inBlock[square]] &= ~valbit 
        col[j] &= ~valbit # can be in this way also: col[inCol[square]] = col[inCol[square]] & ~valbit
        row[i] &= ~valbit # can be in this way also: row[inRow[square]] = row[inRow[square]] & ~valbit

        global seqPtr # this is actually frowned by Python developers: putting the global keyword :)
        seqPtr2 = seqPtr # initializing a second sequence pointer based on the current global sequence pointer

        while (seqPtr2 < 81 and sequence[seqPtr2] != square):
            seqPtr2 += 1

        self.SwapSeqEntries(seqPtr, seqPtr2)
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
                    print(' ', end='') # not printing a new line, just a space
                valbit = entry[square]
                square += 1
                if (valbit == 0):
                    ch = '-'
                else:
                    for val in range (10):
                        if (valbit == (1 << val)):
                            ch = str(val)
                            break
                print(ch, end=' ')
            print()

    # method for console input of the Sudoku puzzle
    def consoleInput(self):
        inputString = [''] * 80 # in terms of C style, a character string with 80 bits

        for i in range(9):
            print("Row %d: " % (i+1), end='')
            inputString = input() # to be honest, validation should be put here; will implement soon

            for j in range(9):
                ch = inputString[j]
                if (ch >= '1' and ch <= '9'): # surprising that this also works in Python, similar to int(ch) < 1 and int(ch) > 9 but make sure ch is not '-'
                    self.InitEntry(i, j, int(ch))
        
        self.printArray()

    # method for printing statistics on the number of placements/guesses made in a mini-square
    def printStats(self):
        S = 0

        print()
        print("Level Counts: ")
        print()

        # this while loop will cause a runtime error if you input a fully solved Sudoku puzzle
        while(levelCount[S] == 0):
            if(S < 80): 
                S += 1
            else: # this else block prevents the error from happening, but I do not have a full explanation yet as to why or how it happens
                break
        
        i = 0
        
        while(S < 81):
            seq = sequence[S]
            print("(%d, %d): %3d " % ((seq // 9) + 1, (seq % 9) + 1, levelCount[S]), end=' ') # formula here is row #, col #, # of placements/guesses
            i += 1
            if(i > 5):
                print()
                i = 0
            S += 1
        
        print()
        print()
        print("Count = %d" % count)

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
                Possibles &= ~(Possibles & -Possibles)
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
        self.SwapSeqEntries(S, S2)

        Square = sequence[S]

        BlockIndex = inBlock[Square]
        RowIndex = inRow[Square]
        ColIndex = inCol[Square]

        Possibles = block[BlockIndex] & row[RowIndex] & col[ColIndex]
        while(Possibles):
            valbit = Possibles & (-Possibles)
            Possibles &= ~valbit
            entry[Square] = valbit
            block[BlockIndex] &= ~valbit
            row[RowIndex] &= ~valbit
            col[ColIndex] &= ~valbit

            self.place(S + 1)

            block[BlockIndex] |= valbit
            row[RowIndex] |= valbit
            col[ColIndex] |= valbit
        
        entry[Square] = CONST_BLANK

        self.SwapSeqEntries(S, S2)
   
    # main method
    def main(self):
        for i in range(9):
            for j in range(9):
                square = 9 * i + j
                inRow[square] = i
                inCol[square] = j
                inBlock[square] = (i // 3) * 3 + (j // 3)

        for square in range(81):
            sequence[square] = square
            entry[square] = CONST_BLANK
            levelCount[square] = 0

        for i in range(9):
            block[i] = row[i] = col[i] = CONST_ONES

        self.consoleInput()
        self.place(seqPtr)
        print()
        print("Total Count = %d" % count)

# call the class' main method
if __name__ == "__main__":
    SudokuSolver().main()