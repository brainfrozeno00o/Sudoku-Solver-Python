pyinstaller --onefile --add-data "C:/Users/john.lingad/Downloads/Random Codes/Random-Codes/SudokuSolver-LHL/Sudoku-Solver-Python/custom-files/welcome-message.txt;." SudokuSolver-Python.py
move dist\SudokuSolver-Python.exe .
rmdir dist
rmdir /s /q build
rmdir /s /q __pycache__
del *.spec
exit