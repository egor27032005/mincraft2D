import random


class Vector():
    def __init__(self, x, slant, length, height):
        self.x = x
        self.slant = slant
        self.length = length
        self.height = height
        self.tang = height / length

    def connecting_back(self, radius):
        return [(x - self.x, x * self.tang * self.slant) for x in range(radius, 0, -1)]

    def connecting_forward(self, radius):
        return [(x + self.x, x * self.tang * self.slant) for x in range(0, radius)]

def lerp(t, a, b):
    return a + t * (b - a)

def smoothstep(t):
    return t * t * (3. - 2. * t)

class PerlinNoiseFactory:
    def __init__(self, matrix, radius):
        self.matrix=matrix
        self.radius = radius
        self.matrix_length=self.matrix.width
        self.l = self.matrix_length // self.radius
        self.vec_cord = self.vectors_cords()
        self.vectors = self.get_vectors()
        self.lerps = self.connection()

    def vectors_cords(self):
        cords = [x for x in range(-self.matrix_length // 2, self.matrix_length // 2+1, self.radius)]
        return cords

    def get_vectors(self):
        vectors = []
        a = -1
        for i in range(self.matrix_length // self.radius + 1):
            length = random.randint(5, 15)
            hei = random.randint(10, 17)
            a = a * -1
            vec = Vector(self.vec_cord[i], a, length, hei)
            vectors.append(vec)
        return vectors

    def connection(self):
        lerps = []
        for i in range(len(self.vectors) - 1):
            vec1 = self.vectors[i].connecting_forward(self.radius)
            vec2 = self.vectors[i + 1].connecting_back(self.radius)
            t = [smoothstep(t / self.radius) for t in range(self.radius)]
            ler = [(vec2[i][0], round(lerp(t[i], vec1[i][1], vec2[i][1]))) for i in range(len(t))]
            lerps.append(ler)
        return sum(lerps, [])

    # def pool_matrix(self):
    #     for point in self.lerps[1:-1]:
    #         matrix[point[0], point[1] + matrix.height // 2] = 22
    #     return matrix


# matrix = Ground_Matrix(512, 150)
# x = PerlinNoiseFactory(matrix, 64)