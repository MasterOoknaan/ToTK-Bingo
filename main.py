from square import Grid

slots = []
f = open('squares.txt')
for line in f.readlines():
    d, t = line.split(',')
    slots.append((int(d), t.strip()))

grid = Grid(slots)
grid.fill()
print(grid)
