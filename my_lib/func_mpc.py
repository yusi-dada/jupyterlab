import pickle as pic
import numpy as np
from func_plot import *
from func_polytope import *


class system():
    A  = None
    Bu = None
    Bw = None
    X  = None # 制御状態集合
    U  = None # 入力集合
    W  = None # 外乱集合
    E  = None # 入力誤差集合
    Xf = None # 終端制御状態集合
       
def dump_system(sys, filepath="system.pickle"):
    with open(filepath, 'wb') as f:
        pic.dump(sys, f)

def load_system(filepath="system.pickle"):
    with open(filepath, 'rb') as f:
        sys = pic.load(f)
        return sys

def augment_system(sys):
    nx = sys.A.shape[1]
    nu = sys.Bu.shape[1]
    A1 = np.hstack([sys.A, sys.Bu])
    A2 = np.hstack([np.zeros([nu,nx]), np.eye(nu)])
    A = np.vstack([A1,A2])   
    Bu = np.vstack([sys.Bu, np.eye(nu)])
    
    
def Pre(sys, X):
    H, h  = X.A, X.b
    Hu,hu = sys.U.A, sys.U.b
    Hp    = np.hstack([H@sys.A, H@sys.Bu])
    Hp    = np.vstack([Hp, np.hstack([np.zeros([Hu.shape[0], sys.A.shape[1]]),Hu])])
    h_    = np.array(h).reshape(len(h),1)
    hu_   = np.array(hu).reshape(len(hu),1)
    if (sys.Bw is not None) and (sys.W is not None):
        h_ = h_ - np.max(H@sys.Bw@extreme(sys.W).T,axis=1)        
    if (sys.Bu is not None) and (sys.E is not None):
        h_ = h_ - np.max(H@sys.Bu@extreme(sys.E).T,axis=1)
    hp = np.vstack([h_, hu_])
    G = polytope_h(np.array(Hp),np.array(hp))
    return project(G, list(range(0,H.shape[1])))


def InvariantSet(sys, fig=None):
    tol = 1e-3
    X   = sys.X
    for i in range(100):
        X0 = X
        P  = Pre(sys, X)
        X  = intersect(P, X)
        
        if fig is not None:
            Xp = project(X,[0,1])
            Xp.plot(fig, alpha=1, color='None', edgecolor='black', linestyle='-', linewidth=1)

        if X0<=mul(X, 1+tol):
            print("\nInvariant set found on {0}-th iteration".format(i))
            return X

        if not (np.zeros(sys.A.shape[0]) in X):
            print("\nNo invariant set exist!")
            return X

        disp="*" if i%10==0 and i>1 else "|"        
        print(disp, end="")

    print("\nInvariant set is still being computed!")
    return X