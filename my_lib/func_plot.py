##
# @file func_plot.py
# @brief 描画処理

import matplotlib.pyplot as plt
import numpy as np
import itertools

##
# @brief 描画オブジェクトの生成
# @param size オブジェクトサイズ
# @param row 行数
# @param col 列数
# @retval fig 描画オブジェクトハンドル
# @retval ax 軸ハンドル ax[row][col]で返す
def Fig(size=(10,5), row=1, col=1):
    row = max(1, int(row))
    col = max(1, int(col))
    fig, ax = plt.subplots(row, col, figsize=size,
                           facecolor="whitesmoke",
                           tight_layout=True)
    ax = [ax] if (row==1 and col==1) else ax

    tmp = [ax] if (row==1 and col==1) else ax.reshape([ax.size,1])
    for a in tmp:
        a[0].grid(linestyle='--')
        a[0].tick_params(axis='x', labelsize=16)
        a[0].tick_params(axis='y', labelsize=16)
        for i in ['top','bottom','left','right']:
            a[0].spines[i].set_linewidth(1)
    return fig, ax

##
# @brief 全軸にタイトルを設定
# @param args タイトル文字列
# @return None
def title(ax, *args):
    flat_ax = np.reshape(ax,-1)
    n_ax = len(flat_ax)
    n_in = len(args)
    for i in range(min(n_ax,n_in)):
        flat_ax[i].set_title(args[i])

##
# @brief 全軸のX軸範囲を一括設定
# @param lim (min, max)で設定
# @return None
def xlim(ax, lim):
    flat_ax = np.reshape(ax,-1)
    for a in flat_ax:
        a.set_xlim(lim)

##
# @brief 全軸のY軸範囲を一括設定
# @param lim (min, max)で設定
# @return None
def ylim(ax, lim):
    flat_ax = np.reshape(ax,-1)
    for a in flat_ax:
        a.set_ylim(lim)

