class Card:
    def __init__(self, color, shape, filling, number):
        self.color = color
        self.shape = shape
        self.filling = filling
        self.number = number

    def __repr__(self):
        return f'Card(color={self.color}, shape={self.shape}, filling={self.filling}, number={self.number})'

card1 = Card(color='red', shape='diamond', filling='solid', number=1)
print(card1)