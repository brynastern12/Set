def is_valid_set(cards):
    colors = set()
    shapes = set()
    fillings = set()
    numbers = set()

    for card in cards:
        colors.add(card['color'])
        shapes.add(card['shape'])
        fillings.add(card['filling'])
        numbers.add(card['number'])

    if len(colors) in {1, 3} and len(shapes) in {1, 3} and len(fillings) in {1, 3} and len(numbers) in {1, 3}:
        return True
    else:
        return False

