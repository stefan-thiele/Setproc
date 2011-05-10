import sage 

def SageMPauli(J) :
    """Compute the Pauli matrices for a given system. It returns them in the following order : Sx,Sy,Sz,S+,S-"""
    
    """This part creates the different matrices filled with zeros"""
    sigmaX = zero_matrix(CC,2*J+1)
    sigmaY = zero_matrix(CC,2*J+1)
    sigmaZ = zero_matrix(CC,2*J+1)
    sigmaPlus = zero_matrix(CC,2*J+1)
    sigmaMoins = zero_matrix(CC,2*J+1)
    n = int(2*J+1)
    """Sigma Z """
    for i in range(n) :
        for j in range(n) :
            if i == j :
                sigmaZ[i,j] = J - i          

        """SigmaPlus"""
    for i in range(n) :
        for j in range(n) :
            if j == i + 1 :
                sigmaPlus[i,j] = sqrt(J*(J+1) - (sigmaZ[j,j] * (sigmaZ[j,j] + 1)))          

    """SigmaMoins"""
    for i in range(n) :
        for j in range(n) :
            if j == i - 1 :
                sigmaMoins[i,j] = sqrt(J * (J + 1) - (sigmaZ[j,j] * (sigmaZ[j,j] - 1)))          
                
    
    """SigmaX"""
    sigmaX = (sigmaPlus+sigmaMoins) / 2.
    
    """SigmaY"""
    sigmaY= j * (sigmaMoins-sigmaPlus) / 2.
    
    
    return sigmaX*muB,  sigmaY*muB, sigmaZ *muB , sigmaPlus * muB, sigmaMoins * muB 
