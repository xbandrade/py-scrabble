def get_end_pos(start, length, down=True) -> tuple:
    x = start[0] + (length - 1) * down
    y = start[1] + (length - 1) * (not down)
    return (x, y)


def get_word_path(start, length, down) -> tuple:
    end = get_end_pos(start, length, down)
    if down:
        return ([(i, start[1]) for i in range(
            start[0], end[0] + 1)], end)
    return ([(start[0], i) for i in range(
        start[1], end[1] + 1)], end)
