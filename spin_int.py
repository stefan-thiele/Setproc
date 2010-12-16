"""
@uthor : Romain Vincent
This file defines a JsonData class to handle easily the json files

@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
This program part is dedicated to the simulation of magnetic systems. 
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
"""


"""
    Created on Fri Nov 13 10:50:30 2009

@author: Romain VINCENT
Couplage de spins
"""
.5e-7
g=5/4.
muBeV = 5.7883817555e-5 #eV
kB = 8.617343e-5 #eV
muB = muBeV/kB
"""
Some function for energy converstion
"""
def K_to_muB(x) : 
	return  (x*kb/muB *1e6)

def K_to_eV(x) :
	"""
	The value is in micro eV
	"""
	return (x*kb/1e-6)

def muB_to_eV(x) :
	return x*muB

def eV_to_muB(x) :
	return x/muB

def eV_to_K(x) :
	return (x/kb *1e-6)

def muB_to_K(x) :
	return eV_to_K(muB_to_eV(x))

"""
////////////////////////////////////////////////
Definition of the Pauli matrices
///////////////////////////////////////////////
"""
def MPauli(J) :
    """Compute the Pauli matrices for a given system. It returns them in the following order : Sx,Sy,Sz,S+,S-"""
    
    """This part creates the different matrices filled with zeros"""
    sigmaX = matrix( zeros((2*J+1,2*J+1)) )
    sigmaY = matrix( zeros((2*J+1,2*J+1)) )
    sigmaZ = matrix( zeros((2*J+1,2*J+1)) )
    sigmaPlus = matrix( zeros((2*J+1,2*J+1)) )
    sigmaMoins = matrix( zeros((2*J+1,2*J+1)) )
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
                sigmaPlus[i,j] = sqrt(J * (J+1) - (sigmaZ[j,j] * (sigmaZ[j,j] + 1)))          

    """SigmaMoins"""
    for i in range(n) :
        for j in range(n) :
            if j == i - 1 :
                sigmaMoins[i,j] = sqrt(J * (J + 1) - (sigmaZ[j,j] * (sigmaZ[j,j] - 1)))          
                
    
    """SigmaX"""
    sigmaX = (sigmaPlus+sigmaMoins) / 2.
    
    """SigmaY"""
    sigmaY=1j * (sigmaMoins-sigmaPlus) / 2.
    
    
    return [sigmaX*muB,  sigmaY*muB, sigmaZ *muB , sigmaPlus * muB, sigmaMoins * muB] 



"""
////////////////////////////////////////////////
Definition of the Pauli matrices for several particles
///////////////////////////////////////////////
"""

def sysPau(J) :
    """This function compute the different Sx,Sy,Sz,S+,S- for all the particles of the system and return them in a single array in the same order than given in argument."""
    n = len(J)
    sysPau = []
    for i in range(n) :
        sysPau.append(MPauli(J[i]))
    
    return sysPau   
    """It returns and array of matrices"""
    

"""
////////////////////////////////////////////////
Definition of the Pauli matrices of several product into the final space using the kronecker product
///////////////////////////////////////////////
"""

def tensorProduct(J):
    """For a given matrix J=[J1,J2,...,Jn] this function return the same operateur but in the new space obtained using the kroenecker product"""
    n = len(J)
    result = []
    for i in range(n) :
        Temp1 = 1
        Temp2 = 1
        for j in range(i) :
            Temp1 = kron(Temp1, eye(len(J[j])))
        for j in range((i+1), n):
            Temp2 = kron(Temp2, eye(len(J[j])))
        result.append(kron(Temp1, kron(J[i], Temp2)))
    return result


"""
////////////////////////////////////////////////
Extraction of the different data (such as Sx or Sy) for a given system
///////////////////////////////////////////////
"""
def extractData(J, N):
    """This function is helpful extracting data from the matrix returned sysPau and using tensorProduct, construct the quantum operators in the new space"""
    n = len(J)
    temp = []
    for i in range(n):
        temp.append(J[i][N])
    result = tensorProduct(temp)
    return result
    

def sumOver(S):
    n = len(S)
    result = []
    for i in range(n):
        result = result + S[i]
    return result


def TwoSpinCoupling(J1, J2, Jint):
    n = len(J1)
    m = len(J1[0])
    result = matrix( zeros((m ,  m)) )
    
    for i in range(n):
        for j in range(n):
            result = result + Jint[i , j] * J1[i] * J2[j]
    return result
    
def SpinsCoupling(S, Jint,B):
    """This function compute and return on a matrix form the coupling between several spin given the coupling matrices Jint """
    n = len(S)
    m = len(S[0][0])
    result = matrix( zeros((m ,  m)) )
    for i in range(n - 1):
        for j in range (i+ 1, n):
            result = result + TwoSpinCoupling(S[i], S [j], Jint[i + j - 1]) 

    return result


"""
The stevensons coeficient
"""

#k=2

def O_02(S) :
	""""
	S is given such that
	S[0] = Sx
	S[1] = Sy
	S[2] = Sz
	S[3] = S+
	S[4] = S-
	which is the case if you use the MPauli function
	"""
	J = ( sqrt(size(S[0])) -1 )/2.  #j(j+1) 
	alpha = J*(J+1)
	m = size(S[0])
	result = matrix( zeros((m,m))) 
	result = 3 * S[2]**2 - alpha
	return result

def O_22(S) :
	""""
	S is given such that
	S[0] = Sx
	S[1] = Sy
	S[2] = Sz
	S[3] = S+
	S[4] = S-
	which is the case if you use the MPauli function
	""" 
	m = size(S[0])
	result = matrix( zeros((m,m))) 
	result = 0.5 * (S[3]**2 + S[4]**2)
	return result 

#k=4

def O_04(S) :
	""""
	S is given such that
	S[0] = Sx
	S[1] = Sy
	S[2] = Sz
	S[3] = S+
	S[4] = S-
	which is the case if you use the MPauli function
	"""
	J =  ( sqrt(size(S[0])) -1 )/2. #j(j+1) 
	alpha = J*(J+1)
	m = size(S[0])
	result = matrix( zeros((m,m))) 
	result = 35 * S[2]**4 - 30 * alpha *S[2]**2 + 25 * S[2]**2 - 6*alpha + 3*alpha**2 
	return result

def O_24(S) :
	""""
	S is given such that
	S[0] = Sx
	S[1] = Sy
	S[2] = Sz
	S[3] = S+
	S[4] = S-
	which is the case if you use the MPauli function
	"""
	J = ( sqrt(size(S[0])) -1 )/2. #j(j+1) 
	alpha = J*(J+1)
	m = size(S[0])
	result = matrix( zeros((m,m))) 
	result = 0.25 * ((7*S[2]**2 - alpha - 5)*(S[3]**2 + S[4]**2) + (S[3]**2 + S[4]**2)*(7*S[2]**2 - alpha - 5))
	return result 

def O_34(S) :
	""""
	S is given such that
	S[0] = Sx
	S[1] = Sy
	S[2] = Sz
	S[3] = S+
	S[4] = S-
	which is the case if you use the MPauli function
	"""
	J = ( sqrt(size(S[0])) -1 )/2. #j(j+1) 
	alpha = J*(J+1)
	m = size(S[0])
	result = matrix( zeros((m,m))) 
	result = 0.25 * ( S[2]*(S[3]**3 + S[4]**3) + (S[3]**3 + S[4]**3)*S[2])
	return result 

def O_44(S) :
	""""
	S is given such that
	S[0] = Sx
	S[1] = Sy
	S[2] = Sz
	S[3] = S+
	S[4] = S-
	which is the case if you use the MPauli function
	"""
	m = size(S[0])
	result = matrix( zeros((m,m))) 
	result = 0.5 * (S[3]**4 + S[4]**4)
	return result

#k=6

def O_06(S) :
	""""
	S is given such that
	S[0] = Sx
	S[1] = Sy
	S[2] = Sz
	S[3] = S+
	S[4] = S-
	which is the case if you use the MPauli function
	"""
	J = ( sqrt(size(S[0])) -1 )/2. #j(j+1) 
	alpha = J*(J+1)
	m = size(S[0])
	result = matrix( zeros((m,m))) 
	result = 231*S[2]**6 - 315*alpha* S[2]**4 + 735*S[2]**4 + 105*(alpha**2)*S[2]**2 - 525*alpha*S[2]**2 + 294*S[2]**2 -5*alpha**3 + 40*(alpha**2) - 60*alpha
	return result

def O_36(S) :
	""""
	S is given such that
	S[0] = Sx
	S[1] = Sy
	S[2] = Sz
	S[3] = S+
	S[4] = S-
	which is the case if you use the MPauli function
	"""
	J = ( sqrt(size(S[0])) -1 )/2. #j(j+1) 
	alpha = J*(J+1)
	m = size(S[0])
	result = matrix( zeros((m,m))) 
	result = 0.25 * ((11*S[2]**3 - 3*alpha*S[2] - 59*S[2])*(S[3]**3 + S[4]**3) + (S[3]**3 + S[4]**3)*(11*S[2]**3 - 3*alpha*S[2] - 59*S[2]))
	return result

def O_46(S) :
	""""
	S is given such that
	S[0] = Sx
	S[1] = Sy
	S[2] = Sz
	S[3] = S+
	S[4] = S-
	which is the case if you use the MPauli function
	"""
	J = ( sqrt(size(S[0])) -1 )/2.  #j(j+1) 
	alpha = J*(J+1)
	m = size(S[0])
	result = matrix( zeros((m,m))) 
	result = 0.25* ((11*S[2]**2 - alpha -38)*(S[3]**4 + S[4]**4) + (S[3]**4 + S[4]**4)*(11*S[2]**2 - alpha -38))
	return result

def O_66(S) :
	""""
	S is given such that
	S[0] = Sx
	S[1] = Sy
	S[2] = Sz
	S[3] = S+
	S[4] = S-
	which is the case if you use the MPauli function
	"""
	J = ( sqrt(size(S[0])) -1 )/2. #j(j+1) 
	alpha = J*(J+1)
	m = size(S[0])
	result = matrix( zeros((m,m))) 
	result = 0.5 * (J[3]**6 + J[4]**6)
	return result


"""
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
"""



class VectSys : 
    """"This object represents the different particle properties in the same space. Several methods allow to access to the different parameters of the system and also to implement some basic function essential in defining a basic hamiltonien."""
    def __init__(self, J):
        self.J = sysPau(J)
        self.Sx = extractData(self.J, 0)
        self.Sy = extractData(self.J, 1)
        self.Sz = extractData(self.J, 2)
        self.Splus = extractData(self.J, 3)
        self.Smoins = extractData(self.J, 4)
    

class MagSys :
    """This object represent the whole magnetic system with the partciles and the hamiltonien. It can gives access to the energie levels, the eigenvectors and some transistion probability """
    def __init__(self,J, Coupl, B):
        MagnSys = VectSys(J)
    
def zeeman_diagram(bmin,bmax,nbr,J,D,E) :
	S1 = MPauli(J)
	B = linspace(bmin,bmax,nbr)
	result = []
	alpha = -1/(30. * 15) 
	beta = -1/(11. * 2730 )
	gamma = -5/(13. * 33 * 9009 )
	for i in range(size(B)) :
		H = alpha * 273.9 * O_02(S1) + beta * (-97.7 * O_04(S1) + (-1289.1)*O_44(S1)) + gamma *( -6.5*O_06(S1) + (-631.6)*O_46(S1)) + g * S1[2] *B[i]
		En = linalg.eigvals(H)
		En.sort()
		result.append(real(En))
	return result    


def zeeman_diagramm_2(bmin,bmax,nbr) :
	B = linspace(bmin,bmax,nbr)		
	Jint=matrix([[1, 0],[0,1]])
	Jintot=[Jint]
	J=[1.5,6]
	DE=VectSys(J)
	S1=[DE.Sx[0], DE.Sy[0],DE.Sz[0]]
	S2=[DE.Sx[1], DE.Sy[1],DE.Sz[1]]
	result = []
	for i in range(size(B)) :
		H = 0.5 * S1[0]* S2[0] + 0.55 * S1[1]* S2[1] + -0.45 * S1[2]* S2[2] + B[i] * (S1[2] + S2[2]) + (S1[2] + S2[2]) **2
		E=linalg.eigvals(H)
		E.sort()
		result.append(real(E))

	return result
"""
Jint=matrix([[1, 0, 0,],[0,1,0],[0,0,1]])
Jintot=[Jint]
J=[0.5,1.5]
DE=VectSys(J)
S1=[DE.Sx[0], DE.Sy[0],DE.Sz[0]]
S2=[DE.Sx[1], DE.Sy[1],DE.Sz[1]]
S=[S1, S2]
E,V=linalg.eig(SpinsCoupling(S, Jintot))
"""
	 

