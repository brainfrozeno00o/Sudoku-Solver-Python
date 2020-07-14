inBlock = [0] * 81
inRow = [0] * 81
inCol = [0] * 81

CONST_BLANK = 0
CONST_ONES = int(hex(0b1111111110), 16)

entry = [0] * 81
block = [0] * 9
row = [0] * 9
col = [0] * 9

seqPtr = 0
sequence = [0] * 81

count = 0
levelCount = [0] * 81
class SudokuSolver:
    def SwapSeqEntries(self, S1, S2):
        temp = sequence[S2]
        sequence[S2] = sequence[S1]
        sequence[S1] = temp


    def InitEntry(self, i, j, val):
        square = 9 * i + j
        valbit = 1 << val
        seqPtr2 = 0

        entry[square] = valbit
        block[inBlock[square]] &= ~valbit
        # col[inCol[square]] = col[inCol[square]] & ~valbit
        # row[inRow[square]] = row[inRow[square]] & ~valbit
        col[j] &= ~valbit
        row[i] &= ~valbit

        global seqPtr
        seqPtr2 = seqPtr

        while (seqPtr2 < 81 and sequence[seqPtr2] != square):
            seqPtr2 += 1

        self.SwapSeqEntries(seqPtr, seqPtr2)
        seqPtr += 1


    def printArray(self):
        i = 0
        j = 0
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
                            ch = str(val)
                            break
                print(ch, end=' ')
            print()

    def consoleInput(self):
        i = 0
        j = 0
        inputString = [''] * 80

        for i in range(9):
            print("Row %d: " % (i+1), end='')
            inputString = input()

            for j in range(9):
                ch = inputString[j]
                if (ch >= '1' and ch <= '9'):
                    self.InitEntry(i, j, int(ch))
        
        self.printArray()

    def printStats(self):
        S = 0

        print()
        print("Level Counts: ")
        print()

        while(levelCount[S] == 0):
            if(S < 80):
                S += 1
            else:
                break
        
        i = 0
        
        while(S < 81):
            seq = sequence[S]
            print("(%d, %d): %3d " % ((seq // 9) + 1, (seq % 9) + 1, levelCount[S]), end=' ')
            i += 1
            if(i > 5):
                print()
                i = 0
            S += 1
        
        print()
        print()
        print("Count = %d" % count)

    def succeed(self):
        self.printArray()
        self.printStats()

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
   
        
    def main(self):
        i = 0
        j = 0
        Square = 0

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

if __name__ == "__main__":
    SudokuSolver().main()