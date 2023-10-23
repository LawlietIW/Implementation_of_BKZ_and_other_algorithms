from utils.utilFunctions import *
from myBKZ import *
from galbraithLLL import *

def test_gs():
    Bm = np.random.randint(20, size=(4, 3))
    print("B:")
    print(Bm)
    Bstar,Mym = gram_schmidt(Bm)
    print()
    print("B*:")
    print(Bstar)
    print()
    print("Mym:")
    print(Mym)


def test_pi():
    Bm =  np.array([[1, 2, 3], [2, 4, -1]])
    print("B:")
    print(Bm)
    pi = PI([5,2,5],Bm)
    print("PI")
    print(pi)
    

def test_trivialLLL():
    Bm = np.array([[64,45,20],[24,19,17],[0,0,80]])
    #[[0, -17, 4],
    #[ 16, -10, -10],
    #[ 24,   2,  21]]
    print("B:")
    print(Bm)
    BLLL = trivial_LLL_removing_linear_dependence(Bm,3/4)
    print()
    print("BLLL:")
    print(BLLL)
    print()
    print()
    Bm = np.array([[64,45,20],[24,19,17],[0,0,80],[4,5,7]])
    #[[0, -17, 4],
    #[ 16, -10, -10],
    #[ 24,   2,  21]]
    print("B:")
    print(Bm)
    BLLL = trivial_LLL_removing_linear_dependence(Bm,3/4)
    print()
    print("BLLL:")
    print(BLLL)
    print()
    print()

# test_trivialLLL()
# # print()
# # print()
test_pi()


# def testPI():
#     B = np.array([[64,45,20],[24,19,17],[0,0,80]])
#     B = PI()