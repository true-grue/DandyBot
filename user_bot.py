def script(check, x, y):
    if check("gold", x, y) > 0:
        return "take"
    matrix_size = 30
    matrix = [[0 for i in range(matrix_size)] for j in range(matrix_size)]
    queue = [(x, y, 1)]
    find = False
    while queue and not find:
        elem = queue.pop(0)
        elem_x, elem_y, level = elem
        if matrix[elem_y][elem_x] > level or matrix[elem_y][elem_x] == 0:
            matrix[elem_y][elem_x] = level
        next_cells = [(elem_x, elem_y - 1, level + 1), (elem_x + 1, elem_y, level + 1),
                      (elem_x, elem_y + 1, level + 1), (elem_x - 1, elem_y, level + 1)]
        for next_cell in next_cells:
            next_x, next_y, next_level = next_cell
            if check("gold", next_x, next_y):
                matrix[next_y][next_x] = next_level + 1
                find = next_cell
                break
            if matrix[next_y][next_x] < 0:
                continue
            if check("wall", next_x, next_y):
                matrix[next_y][next_x] = -1
                continue
            if next_level >= matrix[next_y][next_x] > 0:
                continue
            queue.append(next_cell)
    find_x, find_y, find_level = find
    while find_level > 1:
        next_cells = [(find_x, find_y - 1), (find_x + 1, find_y), (find_x, find_y + 1), (find_x - 1, find_y)]
        for next_cell in next_cells:
            next_x, next_y = next_cell
            next_level = matrix[next_y][next_x]
            if next_level == 1:
                if find_x < next_x:
                    return "left"
                if find_x > next_x:
                    return "right"
                if find_y < next_y:
                    return "up"
                if find_y > next_y:
                    return "down"
            if next_level == find_level - 1:
                find_x = next_x
                find_y = next_y
                find_level = next_level
                break
    return "pass"
