def check_fit(book_height, shelf_height):
    return book_height <= shelf_height

def assign_car(volume):
    if volume < 0.01:
        return "small"
    elif volume < 0.05:
        return "medium"
    else:
        return "large"