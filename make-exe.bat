pyinstaller --onefile --add-data "./custom-files/welcome-message.txt;." SudokuSolver-Python.py
move dist\SudokuSolver-Python.exe .
rmdir dist
rmdir /s /q build
rmdir /s /q __pycache__
del *.spec
exit