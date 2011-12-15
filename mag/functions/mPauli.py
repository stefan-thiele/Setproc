from numpy import matrix, zeros, sqrt


def MPauli(J, muB = 1) :
    """
    Compute the Pauli matrices for a given system. It returns them in the following order : Sx,Sy,Sz,S+,S-"""

    sigmaX = matrix( zeros((2*J+1, 2*J+1)) )
    sigmaY = matrix( zeros((2*J+1, 2*J+1)) )
    sigmaZ = matrix( zeros((2*J+1, 2*J+1)) )
    sigmaPlus = matrix( zeros((2*J+1, 2*J+1)) )
    sigmaMoins = matrix( zeros((2*J+1, 2*J+1)) )
    n = int(2*J+1)

    #Sigma Z
    for i in range(n) :
        for j in range(n) :
            if i == j :
                sigmaZ[i, j] = J - i

    #SigmaPlus
    for i in range(n) :
        for j in range(n) :
            if j == i + 1 :
                sigmaPlus[i, j] = sqrt(J * (J+1) - (sigmaZ[j, j] * (sigmaZ[j, j] + 1)))

    #SigmaMoins
    for i in range(n) :
        for j in range(n) :
            if j == i - 1 :
                sigmaMoins[i, j] = sqrt(J * (J + 1) - (sigmaZ[j, j] * (sigmaZ[j, j] - 1)))
    #SigmaX
    sigmaX = (sigmaPlus+sigmaMoins) / 2.
    #SigmaY
    sigmaY=1j * (sigmaMoins-sigmaPlus) / 2.

    return [sigmaX*muB,  sigmaY*muB, sigmaZ *muB , sigmaPlus * muB, sigmaMoins * muB]
