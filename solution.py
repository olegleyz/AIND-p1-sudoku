assignments = []

def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """

    # Don't waste memory appending actions that don't actually change any values
    if values[box] == value:
        return values

    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values

def naked_twins(values):
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """
    for unit in unitlist:
        twos = [values[box] for box in unit if len(values[box]) == 2]
        if len(twos) > len(set(twos)):
            twins = set([twos[i] for i in range(len(twos)) if twos[i] in twos[:i] + twos[i + 1:]])
            for box in unit:
                if values[box] not in twins:
                    for t in ''.join(twins):
                        if (t in values[box]):
                            value = values[box].replace(t, "")
                            assign_value(values, box, value)

    return values

def cross(A, B):
    "Cross product of elements in A and elements in B."
    return [s + t for s in A for t in B]

def grid_values(grid):
    """
    Convert grid into a dict of {square: char} with '123456789' for empties.
    Args:
        grid(string) - A grid in string form.
    Returns:
        A grid in dictionary form
            Keys: The boxes, e.g., 'A1'
            Values: The value in each box, e.g., '8'. If the box has no value, then the value will be '123456789'.
    """
    return {boxes[i]: (grid[i] if grid[i] != '.' else cols) for i in range(len(grid))}

def display(values):
    """
    Display the values as a 2-D grid.
    Args:
        values(dict): The sudoku in dictionary form
    """
    width = 1 + max(len(values[s]) for s in boxes)
    line = '+'.join(['-' * (width * 3)] * 3)
    for r in rows:
        print(''.join(values[r + c].center(width) + ('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF': print(line)
    return


def eliminate(values):
    """
    Go through all the boxes, and whenever there is a box with a value, eliminate this value from the values of all its peers.
    Input: A sudoku in dictionary form.
    Output: The resulting sudoku in dictionary form.
    """
    known = [box for box in values.keys() if len(values[box])==1]
    for box in known:
        for peer in peers[box]:
            value = values[peer].replace(values[box], '')
            values = assign_value(values, peer, value)
    return values

def only_choice(values):
    """
    Go through all the units, and whenever there is a unit with a value that only fits in one box, assign the value to this box.
    Input: A sudoku in dictionary form.
    Output: The resulting sudoku in dictionary form.
    """
    for unit in unitlist:
        for num in cols:
            temp = [box for box in unit if (num in values[box])]
            if len(temp) == 1:
                values = assign_value(values, temp[0], num)
    return values

def reduce_puzzle(values):
    """
    Apply eliminate, only_choice and naked_twins in a loop to solve the puzzle until the amount of solved boxes decreases
    Input: A sudoku in dictionary form.
    Output: The resulting sudoku in dictionary form.
    """
    stalled = False
    while not stalled:
        # Check how many boxes have a determined value
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])
        # Your code here: Use the Eliminate Strategy
        values = eliminate(values)
        # Your code here: Use the Only Choice Strategy
        values = only_choice(values)
        # Naked twins
        values = naked_twins(values)
        # Check how many boxes have a determined value, to compare
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        # If no new values were added, stop the loop.
        stalled = solved_values_before == solved_values_after
        # Sanity check, return False if there is a box with zero available values:
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values

def search(values):
    """
    Applying Depth First Search in combination with reduce_puzzle to solve the pazzle.
    Input: A sudoku in dictionary form.
    Output: The resulting sudoku in dictionary form.
    """
    values = reduce_puzzle(values)
    if values == False:
        return False
    if all(len(values[s]) == 1 for s in boxes):
        return values  ## Solved!

    # Choose one of the unfilled squares with the fewest possibilities
    min = 2
    root = -1
    while (root == -1 or min == 10):
        for elem in values:
            if len(values[elem]) == min:
                root = elem
                pass
        min += 1

    # Now use recursion to solve each one of the resulting sudokus, and if one returns a value (not False), return that answer!
    # n,root = min((len(values[s]), s) for s in boxes if len(values[s]) > 1)
    vals = values[root]

    for val in vals:
        values_ = values.copy()
        values_[root] = val
        attemp = search(values_)
        if attemp:
            return attemp

def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """
    values = grid_values(grid)
    #values = reduce_puzzle(values)
    values = search(values)
    return values


rows = 'ABCDEFGHI'
cols = '123456789'
boxes = cross(rows, cols)
row_units = [cross(r, cols) for r in rows]
col_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC', 'DEF', 'GHI') for cs in ('123', '456', '789')]
diag1 = [rows[i]+cols[i] for i in range(len(rows))]
diag2 = [rows[i]+cols[-i-1] for i in range(len(rows))]
unitlist = row_units + col_units + square_units + [diag1] + [diag2]
units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes)


if __name__ == '__main__':


    #diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    diag_sudoku_grid = '9.1....8.8.5.7..4.2.4....6...7......5..............83.3..6......9................'
    display(solve(diag_sudoku_grid))
    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
