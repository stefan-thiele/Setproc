from numpy import linspace, size, linalg, real

class SysMag():
    """
    This class allows to define easily a magnetic system with
    """
    def __init__(self, J, D, E, g):
        temp = MPauli(J)
        self.Sx = temp[0]
        self.Sy = temp[1]
        self.Sz = temp[2]
        self.Sp = temp[3]
        self.Sm = temp[4]
        self.D = D
        self.E = E
        self.g = g

    def Hs(self, B, muB = 1):
        H = - self.D * self.Sz**2
        H = H + self.E * (self.Sp**2 + self.Sm**2)
        H = H + self.g * muB * (self.Sx * B[0] +self.Sy * B[1] + self.Sz * B[2])
        return H

    def zeeman(self, Bmin, Bmax, nbr, Bx = 0, By =0):
        self.zeem = dict()
        self.zeem["Bmin"] = Bmin
        self.zeem["Bmax"] = Bmax
        self.result = []
        B = linspace(Bmin, Bmax, nbr)
        for i in range(size(B)) :
            H =  self.Hs( [Bx , By, B[i]], 1)
            E = linalg.eigvals(H)
            self.result.append(real(E))
        return self.result

    def plot_zeeman(self, marker = 'b.'):
        R = dict()
        si = size(self.result[0])
        nbr = len(self.result)
        B = linspace(self.zeem["Bmin"], self.zeem["Bmax"], nbr)
        for j in range(si) :
            R[j] =[]

        for x in self.result :
            for j in range(si) :
                R[j].append(x[j])

        for j in range(si):
            plot(B, R[j], marker)

        return True
