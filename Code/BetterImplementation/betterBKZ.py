from sameUtilsasinfirstimplementation import *
from Knutsfix import *
from schnorr_enumeration import *
import time

def update_block(Bm, b_, j, k, delta):
    """
    Updates the block Bm with the new shortest vector b_
    """
    #Now we have a new shorter vector
    #Insert into block 
    block = Bm[:k]
    block = np.insert(block, j, b_, 0)     #IS it really position j?????
    # print("This schould be the block yo")
    # print(np.array2string(block,separator=','))
    block = main_LLL(block, delta)
    # print()
    # print("This is block after LLL")
    # print(block)
    Bm[:k] = block
    # print()
    # print("Then this schould be the correct one")
    # print(Bm)
    # B_gs, Mym = gram_schmidt(Bm)
    return Bm


def shortest_vector_and_prints(tempblock):
    tempB_gs, tempMym = gram_schmidt(tempblock)
    tempB_norms = calc_norm(tempB_gs)
    a, b_, c_bar = ENUM(tempblock, tempMym, tempB_norms)
    return b_, c_bar, tempB_norms[0]


def BKZ(Bm, delta, beta):
    """
    Description
    """
    r,k = Bm.shape

    z = 0
    j = 0         #So we start at 0
    Bm = main_LLL(Bm, delta)
    # B_gs, Mym = gram_schmidt(Bm)
    # print(B_gs)
    # print()
    # print(PI(B_gs[1], 0, 1, B_gs))
    while z < r - 1:
        # print(z)
        # if z > 10:
            # print()
            # print(Bm)
        j = (j % (r - 1))              #So we start at 0
        k = min(j + beta, r)
        tempblock = Bm[j:k,:]
        # bound = np.inner(tempblock[0],tempblock[0])
        b_, c_bar, B_gs_norm_first_in_block = shortest_vector_and_prints(tempblock)


        """
        Then the actual code starts
        """
        if (b_ == Bm[j]).all() or (b_ == -Bm[j]).all():
            z += 1
        elif delta * B_gs_norm_first_in_block >  c_bar:
            # print()
            # print("Block")
            # print(tempblock)
            # print("delta * B_gs_norm_first_in_block", delta * B_gs_norm_first_in_block)
            # print(c_bar)
            # print()
            # print("b_:", b_)
            Bm_updated = update_block(Bm, b_, j, k, delta)
            if Bm_updated.all() == Bm.all():
                z += 1
            else:
                Bm = Bm_updated
                z = 0
            # print("New Bm")
            # print(Bm)
        else:
            z += 1
            Bm = main_LLL(Bm, 0.99)
        j += 1


    return Bm




if __name__ == "__main__":
    Bm = np.random.randint(500, size=(30, 30)) 
#     Bm = np.array([[ 28,391,231,116,260,433,  0, 55, 74,200,440,258,225, 12],
#  [158,357,192, 66,227,  4, 44,452,218,  4,484, 18,409,181],
#  [487,207,303,221,144,  5,178,228,290,216,124,461, 66, 57],
#  [ 72, 74,261,205,222,113,386,323,376,222, 86, 89,454,359],
#  [161,481, 48,173,166,300,370, 98,399,244,360,318,490,376],
#  [ 36,405,405,433,496,264,362, 20,240,216,450,359,120,420],
#  [305,460,107, 79,281,223,113,401,415,140,471,150,373, 97],
#  [171,164,376,216,218,147, 51,187,308,432,444,313,156,367],
#  [303,470,169, 70,238,252,127,444,468,320,127,191,335,241],
#  [485,382,330, 97,105,118,340,286,204,386, 48,200,284, 73],
#  [ 84,379,151,292,433,483,218,471,330,330,246,140,426,321],
#  [459,285,129,228,223,301, 74, 26,272,366,367,210, 36,458],
#  [420,440, 57,330,263, 29, 71,441, 95,312,476,382,392,274],
#  [  9,271,497, 56, 88,216,223,493,307, 13,235,332,272,244]])'
#     Bm = np.array([[78,29,43,25,39,67,13,79,23,33],
#  [33, 7,51,67,32,78,21,48,69,32],
#  [40,49,61, 7,60,46,36,92,33,29],
#  [56,52,82,28, 0,93,56,54,54,73],
#  [71, 0,48,14,15,67,82,47,12,49],
#  [66,12,16, 3,81, 4,68,71,37, 9],
#  [10,15,90,78,40,19,82,90,48, 4],
#  [58,21,76,61,72,25,41,33,92,34],
#  [34,23,98,48,54,48,36, 0,22,38],
#  [57,19,27,47,49, 8,13, 4,57,47]])
    print("Bm")
    print(np.array2string(Bm,separator=','))
    start = time.time()
    BKZBm = BKZ(Bm, 0.80, beta = 5)
    print("Time taken: ", time.time() - start)
    print()
    print("BKZBm")
    print(np.array2string(BKZBm,separator=','))

    # print()
    # print()
    # print("Norms:")
    # B_gs, Mym = gram_schmidt(BKZBm)
    # for i in range(len(B_gs)):
    #     print(np.linalg.norm(B_gs[i]))



# print(np.linalg.norm(np.array([ 14 ,-38, -26,  15,  48])))
# print(np.linalg.norm(np.array([ 52 ,-6, -16,  44,  -9])))









"""Gives same as CoCalc"""
# [[78,29,43,25,39,67,13,79,23,33],
#  [33, 7,51,67,32,78,21,48,69,32],
#  [40,49,61, 7,60,46,36,92,33,29],
#  [56,52,82,28, 0,93,56,54,54,73],
#  [71, 0,48,14,15,67,82,47,12,49],
#  [66,12,16, 3,81, 4,68,71,37, 9],
#  [10,15,90,78,40,19,82,90,48, 4],
#  [58,21,76,61,72,25,41,33,92,34],
#  [34,23,98,48,54,48,36, 0,22,38],
#  [57,19,27,47,49, 8,13, 4,57,47]]