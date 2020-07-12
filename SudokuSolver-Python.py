class SudokuSolver:
    def SwapSeqEntries(self, S1, S2):
        temp = sequence[S2]
        sequence[S2] = sequence[S1]
        sequence[S1] = temp

    def InitEntry(self, i, j, val):
        square = 9 * i + j
        valbit = 1 << val
        seqPtr = 0

        entry[square] = valbit
        block[inBlock[square]] &= ~valbit
        col[inCol[square]] &= ~valbit
        row[inRow[square]] &= ~valbit

        seqPtr2 = seqPtr
        while (seqPtr2 < 81 and sequence[seqPtr2] != square):
            seqPtr2 += 1

        self.SwapSeqEntries(seqPtr, seqPtr2)
        seqPtr += 1

    def printArray(self):
        i = 0
        j = 0
        valbit = 0
        val = 1
        square = 0
        ch = ''

        for i in range(9):
            if (i % 3 == 0):
                print()
            for j in range(9):
                if (j % 3 == 0):
                    print(' ', end='')
                valbit = entry[square]
                square += 1
                if (valbit == 0):
                    ch = '-'
                else:
                    for val in range (10):
                        if (valbit == (1 << val)):
                            ch = '0' + val
                            break
                print(ch, end=' ')
            print()

inBlock = [0] * 81
inRow = [0] * 81
inCol = [0] * 81

CONST_BLANK = 0
CONST_ONES = hex(0b1111111110)

entry = [0] * 81
block = [0] * 9
row = [0] * 9
col = [0] * 9

seqPtr = 0
sequence = [0] * 81

Count = 0
levelCount = [0] * 81

ss = SudokuSolver()
ss.printArray()