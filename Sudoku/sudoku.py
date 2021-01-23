def cross(a,b):
    return [s+t for s in a for t in b]


rows= 'ABCDEFGHI'
cols= '123456789'

boxes = cross(rows,cols)
row_units = [cross(r,cols) for r in rows]
column_units = [cross(rows,c) for c in cols]
square_units = [cross(rs,cs) for rs in ('ABC','DEF','GHI') for cs in('123','456','789')]
unitlist = row_units + column_units + square_units
units = dict((s,[u for u in unitlist if s in u]) for s in boxes)
peers = dict((s,set(sum(units[s],[]))-set([s])) for s in boxes)

values=[]
digits='123456789'
def grid_values(grid):
    values = []
    assert len(grid) == 81, "Input grid must be a string of length 81 (9x9)"
    for i in grid:
        if i == '.':
            values.append(digits)
        else:
            values.append(i)
    return dict(zip(boxes,values))

def display(values):
    """
    Display the values as a 2-D grid.
    Input: The sudoku in dictionary form
    Output: None
    """
    width = 1 + max(len(values[s]) for s in boxes)
    line = '+'.join(['-'*(width*3)]*3)
    for r in rows:
        print(''.join(values[r+c].center(width)+('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF': print(line)
    return

def eliminate(values):
    solved_values = [box for box in values.keys() if len(values[box])==1]
    for box in solved_values:
        digit = values[box]
        for peer in peers[box]:
            values[peer] = values[peer].replace(digit,'')
    return values

def only_choice(values):
    for unit in unitlist:
        for digit in '123456789':
            dplaces = [box for box in unit if digit in values[box]]
            if len(dplaces)==1:
                values[dplaces[0]]= digit
    return values

def reduce_puzzle(values):
    stalled=False
    while not stalled:

        # No of boxes with determined value before reducing
        solved_values_before = len([box for box in values.keys() if len(values[box])==1])

        # Elimination
        values = eliminate(values)
        # Only-Choice
        values = only_choice(values)
        # No of boxes with determined value after reducing
        solved_values_after = len([box for box in values.keys() if len(values[box])==1])
        stalled = solved_values_before==solved_values_after

        if(len([box for box in values.keys() if len(values[box])==0])):
            return False

    return values


grid= '..3.2.6..9..3.5..1..18.64....81.29..7.......8..67.82....26.95..8..2.3..9..5.1.3..'
values= grid_values(grid)
values=reduce_puzzle(values)
display(values)



grid2 = '4.....8.5.3..........7......2.....6.....8.4......1.......6.3.7.5..2.....1.4......'
values2 = grid_values(grid2)
values2 = reduce_puzzle(values2)
display(values2)
