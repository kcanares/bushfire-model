from itertools import product

def adjacency_range(b_grid, point):
    """given a point's grid restrictions (i.e 
    whether it's in a corner, border, or neither), this function returns a list 
    of adjacent points for a point in a dimension"""
    
    if point == len(b_grid[0]) - 1:
        adjacent_range = [point - 1, point]
    elif point == 0:
        adjacent_range = [point, point + 1]
    else:
        adjacent_range = [point - 1, point, point + 1]
    
    return adjacent_range

def check_ignition(b_grid, f_grid, h_grid, i_threshold, w_direction, i, j):
    # TODO implement this function
    """returns True if cell (i, j) catches fire at time t + 1 based on 
    arguments'variables; burning state (b_grid), current fuel load (f_grid), 
    height (h_grid), ignition threshold (i_threshold), and wind direction 
    (w_direction)"""
    
    # Returns False if cell has no fuel
    if f_grid[i][j] <= 0:
        return False
    
    # Returns False if cell is currently burning
    if b_grid[i][j]:
        return False
    
    # create a list of adjacent cells
    adjacent_cells = [[i_num, j_num] for i_num in adjacency_range(b_grid, i) 
                      for j_num in adjacency_range(b_grid, j)]

    # adding extra adjacent cells if there's wind
    if w_direction:
        
        # wind_dict is a dictionary of a wind direction's characteristics.  
        # Each entry follows the form of 'w_direction': grid restriction, 
        # column or row dimension affected (i or j), co-ordinate to be appended 
        # if wind affects grid, reach of wind_direction if it's in a 2 
        # character w_direction
        wind_dict = {'N': [i - 2 >= 0, j, [i - 2, j], i - 1], 
                    'S': [i + 2 <= len(b_grid) - 1, j, [i + 2, j], i + 1], 
                    'W': [j - 2 >= 0, i, [i, j - 2], j - 1], 
                    'E': [j + 2 <= len(b_grid) - 1, i, [i, j + 2], j - 2]}
        
        if len(w_direction) == 1 and wind_dict[w_direction][0]:
            for wind_dict[w_direction][1] in adjacency_range(b_grid, 
            wind_dict[w_direction][1]):
                adjacent_cells.append(wind_dict[w_direction][2])
        
        elif len(w_direction) == 2:
            if wind_dict[w_direction[0]][0]:
                adjacent_cells.append([wind_dict[w_direction[0]][2][0], 
                wind_dict[w_direction[1]][3]])
            if wind_dict[w_direction[1]][0]:
                adjacent_cells.append([wind_dict[w_direction[0]][3], 
                wind_dict[w_direction[1]][2][1]])
            if wind_dict[w_direction[0]][0] and wind_dict[w_direction[1]][0]:
                adjacent_cells.append([wind_dict[w_direction[0]][2][0], 
                wind_dict[w_direction[1]][2][1]])
    
    # counts the ignition points contributed by burning adjacent cells 
    # factoring the cells' height differences
    ignition_points = 0
    for cell in adjacent_cells:
        if (b_grid[cell[0]][cell[1]] and f_grid[cell[0]][cell[1]] > 0 and
            h_grid[cell[0]][cell[1]] > h_grid[i][j]):
            ignition_points += 0.5
        if (b_grid[cell[0]][cell[1]] and f_grid[cell[0]][cell[1]] > 0 and
            h_grid[cell[0]][cell[1]] < h_grid[i][j]):
            ignition_points += 2
        if (b_grid[cell[0]][cell[1]] and f_grid[cell[0]][cell[1]] > 0 and
            h_grid[cell[0]][cell[1]] == h_grid[i][j]):
            ignition_points += 1
    
    if ignition_points >= i_threshold:
        return True
    else:
        return False 
