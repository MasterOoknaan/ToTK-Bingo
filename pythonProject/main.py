from square import Grid
import xlsxwriter

slots = []
f = open('squares.txt')
for line in f.readlines():
    d, t = line.split('|')
    slots.append((int(d), t.strip()))

grid = Grid(slots)
grid.fill()

#print(grid)

wb = xlsxwriter.Workbook('bingo.xlsx')
ws = wb.add_worksheet()

count = 0
for row in range(0,5):
    for col in range(0,5):
        ws.write_string(row, col, str(grid.squares[count]))
        count = count + 1

ws.autofit()
wb.close()
