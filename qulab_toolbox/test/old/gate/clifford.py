import numpy as np
from functools import reduce

__all__=['clifford_group','clifford_index','find_index','matrix_compare',
        'rbm_seq','check_seq']

clifford_group_singlequbit=np.array([
    [ [  1,  0] , [  0, 1] ],
    [ [  0,-1j] , [-1j, 0] ],
    [ [  0, -1] , [  1, 0] ],
    [ [-1j,  0] , [  0,1j] ],

    [ [1/np.sqrt(2), -1j/np.sqrt(2)] , [-1j/np.sqrt(2), 1/np.sqrt(2)] ],
    [ [1/np.sqrt(2),  1j/np.sqrt(2)] , [ 1j/np.sqrt(2), 1/np.sqrt(2)] ],
    [ [1/np.sqrt(2),  -1/np.sqrt(2)] , [  1/np.sqrt(2), 1/np.sqrt(2)] ],
    [ [1/np.sqrt(2),   1/np.sqrt(2)] , [ -1/np.sqrt(2), 1/np.sqrt(2)] ],
    [ [1/np.sqrt(2)-1j/np.sqrt(2),0] , [0,1/np.sqrt(2)+1j/np.sqrt(2)] ],
    [ [1/np.sqrt(2)+1j/np.sqrt(2),0] , [0,1/np.sqrt(2)-1j/np.sqrt(2)] ],

    [ [-1j/np.sqrt(2),-1j/np.sqrt(2)] , [-1j/np.sqrt(2), 1j/np.sqrt(2)] ],
    [ [ 1j/np.sqrt(2),-1j/np.sqrt(2)] , [-1j/np.sqrt(2),-1j/np.sqrt(2)] ],
    [ [-1j/np.sqrt(2), -1/np.sqrt(2)] , [  1/np.sqrt(2), 1j/np.sqrt(2)] ],
    [ [ 1j/np.sqrt(2), -1/np.sqrt(2)] , [  1/np.sqrt(2),-1j/np.sqrt(2)] ],
    [ [0,-1/np.sqrt(2)-1j/np.sqrt(2)] , [1/np.sqrt(2)-1j/np.sqrt(2), 0] ],
    [ [0,-1/np.sqrt(2)+1j/np.sqrt(2)] , [1/np.sqrt(2)+1j/np.sqrt(2), 0] ],

    [ [ 0.5-0.5j, -0.5-0.5j ],  [  0.5-0.5j,  0.5+0.5j ] ],
    [ [ 0.5+0.5j, -0.5+0.5j ],  [  0.5+0.5j,  0.5-0.5j ] ],
    [ [ 0.5+0.5j,  0.5-0.5j ],  [ -0.5-0.5j,  0.5-0.5j ] ],
    [ [ 0.5-0.5j,  0.5+0.5j ],  [ -0.5+0.5j,  0.5+0.5j ] ],
    [ [ 0.5-0.5j,  0.5-0.5j ],  [ -0.5-0.5j,  0.5+0.5j ] ],
    [ [ 0.5+0.5j,  0.5+0.5j ],  [ -0.5+0.5j,  0.5-0.5j ] ],
    [ [ 0.5+0.5j, -0.5-0.5j ],  [  0.5-0.5j,  0.5-0.5j ] ],
    [ [ 0.5-0.5j, -0.5+0.5j ],  [  0.5+0.5j,  0.5+0.5j ] ],
])

clifford_group_singlequbit_index=[    ['I'],
                                      ['X'],
                                      ['Y'],
                                      ['Y','X'],

                                      ['X2p'],
                                      ['X2n'],
                                      ['Y2p'],
                                      ['Y2n'],
                                      ['X2n','Y2p','X2p'],
                                      ['X2n','Y2n','X2p'],

                                      ['X','Y2n'],
                                      ['X','Y2p'],
                                      ['Y','X2p'],
                                      ['Y','X2n'],
                                      ['X2p','Y2p','X2p'],
                                      ['X2n','Y2p','X2n'],

                                      ['Y2p','X2p'],
                                      ['Y2p','X2n'],
                                      ['Y2n','X2p'],
                                      ['Y2n','X2n'],
                                      ['X2p','Y2n'],
                                      ['X2n','Y2n'],
                                      ['X2p','Y2p'],
                                      ['X2n','Y2p'],
                                 ]

clifford_group = clifford_group_singlequbit
clifford_index = clifford_group_singlequbit_index

def find_index(a,b):
    for i,v in enumerate(b):
        if any([matrix_compare(f*a, v) for f in [1,-1,1j,-1j]]):
            return i

def matrix_compare(a,b):
    return np.where(abs(a-b)<1e-5, True, False).all()


# 需要随机的门在 clifford_group 中的索引 的列表，默认包含所有24个门
default_random_group=[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23]

def rbm_seq(size,group=None):
    '''随机RBM的波形序列'''
    if group is None:
        group = default_random_group
    i_r = [group[idx] for idx in np.random.randint(len(group), size=int(size))]
    mat=reduce(np.dot, [clifford_group[i] for i in reversed(i_r)])
    mat_inv=np.array(np.matrix(mat).H)
    inv_index=find_index(mat_inv,clifford_group)
    i_r.append(inv_index)
    index_seq=reduce(np.append,[clifford_index[i] for i in i_r])
    return index_seq

def check_seq(seq):
    '''check the sequence generated by rbm_seq, ensure the sequence product identity matrix !'''
    index={'I':0, 'X':1, 'Y':2, 'X2p':4, 'X2n':5, 'Y2p':6, 'Y2n':7}
    idxs=[index[i] for i in seq]
    check_mat=reduce(np.dot,[clifford_group[i] for i in reversed(idxs)])
    _res = [matrix_compare(f*check_mat,clifford_group[0]) for f in [1,-1,1j,-1j]]
    res = any(_res)
    return res
