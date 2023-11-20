if __name__ == "__main__":
    from utils.utilFunctions import *
    from galbraithLLL import Galbraith_LLL_removing_linear_dependence
    from enumeration import enum_short_vector
else:
    from BKZ_first_implementation.galbraithLLL import Galbraith_LLL_removing_linear_dependence
    from BKZ_first_implementation.utils.utilFunctions import *
    from BKZ_first_implementation.enumeration import enum_short_vector
import time

def pi_projection(x,b):
    """
    '''Computes the projection of x on b as a vector'''
    """
    return np.dot(x, b)/np.dot(b, b) * b

def PI(x,BGSblock):
    """
    π_i(x)

    I think it works fine
    """
    pi = 0
    for row in BGSblock:
        pi += pi_projection(x,row)
    return pi


def update_block(Bm, b_, j, k, delta):
    """
    Updates the block Bm with the new shortest vector b_
    """
    #Now we have a new shorter vector
    #Insert into block 
    block = Bm[:k,:]
    block = np.insert(block, j, b_, 0)     #IS it really position j?????
    block = Galbraith_LLL_removing_linear_dependence(block, delta)
    Bm[:k,:] = block
    B_gs, Mym = gram_schmidt(Bm)
    return Bm, B_gs, Mym


def shortest_vector_and_prints(Bm,tempblock, j, k, bound, B_gs, Mym):
    a, b_ = enum_short_vector(tempblock,bound)
    return b_


def BKZ(Bm, delta, beta):
    """
    Description
    """
    r,k = Bm.shape

    z = 0
    j = 0         #So we start at 0
    Bm = Galbraith_LLL_removing_linear_dependence(Bm, delta)
    B_gs, Mym = gram_schmidt(Bm)
    # print(B_gs)
    # print()
    # print(PI(B_gs[1], 0, 1, B_gs))
    while z < r - 1:
        j = (j % (r - 1))              #So we start at 0
        k = min(j + beta, r)
        tempblock = Bm[j:k,:]
        bound = np.inner(tempblock[0],tempblock[0])
        b_ = shortest_vector_and_prints(Bm,tempblock, j, k, bound, B_gs, Mym)


        """
        Then the actual code starts
        """
        if (b_ == Bm[j]).all() or (b_ == -Bm[j]).all():
            z += 1
        elif delta * np.linalg.norm(PI(b_, B_gs[j:k,:])) < np.linalg.norm(B_gs[j]):
            Bm, B_gs, Mym = update_block(Bm, b_, j, k, delta)
            z = 0
        else:
            z += 1
            Bm = Galbraith_LLL_removing_linear_dependence(Bm, 0.99)
        j += 1


    return Bm




if __name__ == "__main__":
    # Bm = np.random.randint(500, size=(10, 10)) 
    Bm = np.array([[447,125,441,210,223,413,187,192,121,341,315,269,468,426,492,460,180,103,
   46,467,394, 37],
 [187,360,421,443,497,176,302,320,103,346, 94,100,313, 54,215,125,470,314,
  379,223,382,389],
 [101,139,440,110,  5,145,411,344,310, 26, 40,321,270,207, 93,157,  8,320,
  252, 19,397,361],
 [493,324,437, 14,110,456,491, 66,225,170,139,135,324,171,376,237,437,132,
  195, 42,163,471],
 [366,476, 82,132,320, 56,170,222, 29, 97,234, 35,390,312,285,118,442,296,
   59,442,  9,  7],
 [194,321,498,  9,368,211,221,104,255,142,363,352,223,118,356,245,245,473,
  448,128, 86,439],
 [153,  9, 73, 75,401,270,248,423,287,406,142,320,258, 31, 34,396, 85, 20,
  324,371,155,  1],
 [270,157,100,128, 54,112, 67,460,157,157,190,369, 76,443,116,244, 82,420,
  275, 32,361,238],
 [160,453,316,363,142,264,467, 41,393,142,161,358, 12,474,185, 98,499,470,
  280,313,229,164],
 [ 73,420,142,362,210,214,337,315,225,266,111,334,267,217,  2, 48,217,110,
  358,341,249,399],
 [290,206, 22,333,179,158,324,387,212,442,246,303,341, 25,168,220, 27,476,
  268,100,206,206],
 [297,424,187,452,299,400,275,135, 53,122,234,384,397,370, 19,198, 51,252,
   92, 29,373,350],
 [321,422, 55,216,341,243,104, 36,171,301, 37,371,226,476,271, 57,415, 81,
  413,111,171,214],
 [248,358,253,223,471,143,205, 69,199,450,382,  4,346,106, 49,455,227,348,
  390, 57,166, 37],
 [214,103,123,485, 49,290,277, 88,267,419,  4,222,367,416, 45,215, 83, 28,
  111, 72,175, 31],
 [327,371,146,216,190,485,309,165,387,276,132,140,311,480, 59,117,382,107,
  194,335,479,439],
 [ 94,256,479,272,437,493,178,202,288,364,114,359,117,375, 96,  6,148,320,
  487,123,439,408],
 [178, 82,251, 67,444,311, 30, 35,165,106,396,496,424,328,236,395,358, 72,
  266,450,402, 57],
 [281,121, 63,421,310,487,320,254,100,232,103,310,495,490,412,369,269,425,
  139,450,  8,471],
 [154, 43,109, 93,319,412,228,287,464,464,349,124, 46,265,496, 30,144,354,
  100, 26,471,418],
 [ 95, 93,243, 15,171,250,421, 35, 22,267,  7,484,175,135,438,247,257,310,
  310,266,488,113],
 [154, 97,  9,338,237, 21,242, 96,399,153,292,421,263,455, 68,143, 94,431,
    5,422,464,260]])
    # Bm = np.array([[1,0,0],[0,1,0],[0,0,1]])
    # Bm = np.array([[33,89,18,17,30],
#  [ 3,42,93,48,26],
#  [17, 4,67,63,74],
#  [55,36,77,92,17],
#  [34,36,70, 9,84]])
    print("Bm")
    print(np.array2string(Bm,separator=','))
    start = time.time()
    BKZBm = BKZ(Bm, 0.8, beta = 3)
    print("Time taken: ", time.time() - start)
    print()
    print("BKZBm")
    print(np.array2string(BKZBm,separator=','))

    print()
    print()
    print("Norms:")
    B_gs, Mym = gram_schmidt(BKZBm)
    for i in range(8):
        print(np.linalg.norm(PI(BKZBm[i], B_gs[i:8,:])))



# print(np.linalg.norm(np.array([ 14 ,-38, -26,  15,  48])))
# print(np.linalg.norm(np.array([ 52 ,-6, -16,  44,  -9])))