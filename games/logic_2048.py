def merge_left(row):
    """Slides and merges a single row to the left."""
    # remove all 0
    new_row = [i for i in row if i != 0]

    #merge adjacent tiles
    for i in range(len(new_row) - 1):
        if new_row[i] == new_row[i+1] and new_row[i] != 0:
            new_row[i] *= 2
            new_row[i+1] = 0

        #compress after merge
    new_row = [i for i in new_row if i != 0]

    #fill wit 0 til orig length
    return new_row + [0] * (len(row) - len(new_row))