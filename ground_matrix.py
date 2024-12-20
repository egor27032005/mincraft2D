class Ground_Matrix:
    def __init__(self, width, height):
        self.height = height
        self.width = width
        self.matrix = self.create_matrix()

    def create_matrix(self):
        return [[0 for _ in range(self.width)] for _ in range(self.height)]

    def __getitem__(self, coords):
        x, y = coords
        if -self.width // 2 <= x < self.width // 2 and 0 <= y < self.height:
            return self.matrix[y][x + self.width // 2]
        else:
            raise IndexError("Coordinates out of bounds")

    def __setitem__(self, coords, value):
        x, y = coords
        if -self.width // 2 <= x < self.width // 2 and 0 <= y < self.height:
            self.matrix[y][x + self.width // 2] = value
        else:
            raise IndexError("Coordinates out of bounds")

    def __str__(self):
        return '\n'.join([' '.join(map(str, row)) for row in self.matrix])



# Пример использования
if __name__ == "__main__":
    height = 7
    width = 7
    matrix = Ground_Matrix(width, height)
    # matrix[0, -1] = 1
    matrix[-3, 0] = 1
    print(matrix)
