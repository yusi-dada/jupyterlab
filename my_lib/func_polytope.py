##
# @file func_polytope.py
# @brief polytope演算処理

##
# @namespace func_polytope
# @brief polytope演算処理
# @details 内部でpolytopeライブラリ(https://tulip-control.github.io/polytope/)を使用\n
#          polytopeライブラリで対応できない処理はpypomanライブラリ(https://pypi.org/project/pypoman/)で対応
#
#          <version>\n
#           numpy 1.17.4\n
#           cvxpy 1.1.15\n
#           polytope 0.2.3\n
#           pypoman 0.5.4

import copy
import cvxpy as cp
import numpy as np
import polytope as pt
import pypoman as pm

##
# @brief 半空間表現による生成
# @details Ax≦bで表現されたpolytopeを生成
# @param A 例）A = np.array([[1.0, 1.0],[0.0, 1.0],[-1.0, -0.0],[-0.0, -1.0]]);
# @param b 例）b = np.array([2.0, 1.0, 0.0, 0.0]);
# @return polytopeオブジェクト
def polytope_h(A,b):
    return pt.Polytope(A,b)

##
# @brief 頂点座標による生成
# @details 例）polytope_v(np.array([[0,0],[4,0],[3,2],[1,4]]))
# @return polytopeオブジェクト
def polytope_v(v):
    return pt.qhull(v)

##
# @brief 一次元の範囲[lower, upper]による生成
# @return polytopeオブジェクト
def polytope_range(lower, upper):
    A = np.array([[1],[-1]])
    b = np.array([[upper],[-lower]])
    return pt.Polytope(A,b)

##
# @brief ボックスによる生成
# @return polytopeオブジェクト
def polytope_box(lower, upper):
    n_lower = len(lower)
    n_upper = len(upper)
    if n_lower == n_upper:
        tmp = np.vstack([lower,upper])
        return pt.box2poly(tmp.T)
    else:
        raise ValueError("error!")

## 
# @brief 射影
# @details axisで指定した次元への射影オブジェクトを生成
# @param p polytopeオブジェクト
# @param axis 射影軸（リストで入力。インデックスは0から）
# @return 射影後のpolytopeオブジェクト
# @note polytopeライブラリでは計算できなかったのでpypomanを利用
def project(p, axis):
    if isinstance(p, pt.Polytope):
        A = p.A
        b = p.b
        E = np.zeros((len(axis), A.shape[1]))
        for idx, ax in enumerate(axis):
            E[idx, ax] = 1.
        f = np.zeros(p)
        v = pm.projection.project_polytope((E,f),(A,b))
        return polytope_v(np.array(v))
    else:
        raise ValueError("error!")

##
# @brief 頂点
# @details オブジェクトの頂点データを取得
# @param p polytopeオブジェクト
# @return 頂点リスト
def extreme(p):
    if isinstance(p, pt.Polytope):
        return pt.extreme(p)
    else:
        raise ValueError("error!")
        
##
# @brief 差集合（NOT）
# @param p1 polytopeオブジェクト
# @param p2 polytopeオブジェクト
# @return p1 ∧ (Not p2)
def diff(p1, p2):
    if isinstance(p1, pt.Polytope):
        return p1.diff(p2)
    else:
        raise ValueError("error!")

##
# @brief 和集合（OR）
# @param p1 polytopeオブジェクト
# @param p2 polytopeオブジェクト
# @return p1 ∨ p2
def union(p1, p2):
    if isinstance(p1, pt.Polytope):
        return p1.union(p2)
    else:
        raise ValueError("error!")

##
# @brief 積集合（AND）
# @param p1 polytopeオブジェクト
# @param p2 polytopeオブジェクト
# @return p1 ∧ p2
def intersect(p1, p2):
    if isinstance(p1, pt.Polytope):
        return p1.intersect(p2)
    else:
        raise ValueError("error!")

##
# @brief 凸包
# @details p1とp2の頂点集合からpolytopeを生成
# @param p1 polytopeオブジェクト
# @param p2 polytopeオブジェクト
# @return polytopeオブジェクト
def hull(p1, p2):
    if isinstance(p1, pt.Polytope) and isinstance(p2, pt.Polytope):
        v1 = pt.extreme(p1)
        v2 = pt.extreme(p2)
        v3 = np.vstack((v1,v2))
        return pt.qhull(v3)
    else:
        raise ValueError("error!")

##
# @brief 有効制約
# @details p1とp2の各制約和
# @param p1 polytopeオブジェクト
# @param p2 polytopeオブジェクト
# @return polytopeオブジェクト
def envelope(p1,p2):
    return pt.envelope(pt.Region([p1,p2]))

##
# @brief Minkowski sum
# @param p1 polytopeオブジェクト
# @param p2 polytopeオブジェクト
# @return polytopeオブジェクト
# @note polytopeライブラリが対応していないため独自処理
def plus(p1, p2):
    if isinstance(p1, pt.Polytope) and isinstance(p2, pt.Polytope):
        H1 = p1.A
        K1 = p1.b
        H2 = p2.A
        K2 = p2.b
        tmp1 = np.hstack((np.zeros(H1.shape), H1))
        tmp2 = np.hstack([H2, -H2])
        H3 = np.vstack([tmp1, tmp2])
        K3 = np.hstack([K1,K2])
        p3 = pt.Polytope(H3, K3)
        return project(p3, list(range(0,H1.shape[1])))
    else:
        raise ValueError("error!")

##
# @brief Pontryagin diff
# @param p1 polytopeオブジェクト
# @param p2 polytopeオブジェクト
# @return polytopeオブジェクト
# @note polytopeライブラリが対応していないためcvxpyで処理
def minus(p1, p2):
    if isinstance(p1, pt.Polytope) and isinstance(p2, pt.Polytope):
        H1 = p1.A
        K1 = p1.b
        H2 = p2.A
        K2 = p2.b
        (row,col) = H1.shape
        H = np.zeros([row,1])
        x   = cp.Variable(col)

        for i in range(row):
            obj = cp.Maximize(H1[i,:] @ x)
            constraint = [H2 @ x <= K2]        
            prob = cp.Problem(obj, constraint)
            H[i,:] = prob.solve(verbose=False)

        return pt.Polytope(H1, K1 - H)
    else:
        raise ValueError("error!")
        
##
# @brief スケーリング
# @brief polytope頂点を係数倍し生成
# @param p1 polytopeオブジェクト/スケーリング定数
# @param p2 スケーリング定数/polytopeオブジェクト
# @return polytopeオブジェクト
# @note polytopeのscaleメソッドでは規模が大きいと計算されなかった
def mul(p1, p2):
    if isinstance(p1, pt.Polytope):
        v = extreme(p1)
        return polytope_v(v*p2)
    elif isinstance(p2, pt.Polytope):
        return mul(p2,p1)
    else:
        raise ValueError("error!")