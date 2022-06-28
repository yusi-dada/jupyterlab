# -*- coding: utf-8 -*-
##
# @file qt_dialog.py
# @brief ファイル指定ダイアログ管理（Qt）

import os
from PyQt5.QtWidgets import QFileDialog, QMessageBox, QApplication


##
# @brief テキストファイルの読込み
# @param filename [str] ファイル名
# @return 読込みテキスト
def loadInit(filename):
    file_path = os.path.dirname(__file__)+"/"+filename
    if not os.path.isfile(file_path):
        return ""
    with open(file_path, mode="r") as f:
        return f.readline()

##
# @brief テキストファイルの書込み
# @param filename [str] ファイル名
# @param txt 書込みテキスト
def saveInit(filename, txt=""):
    file_path = os.path.dirname(__file__)+"/"+filename
    with open(file_path, mode="w") as f:
        f.write(txt)

##
# @brief ファイルオープンダイアログの生成
# @param folder_path [str] 初期表示ディレクトリパス
# @param file_ext [str] 拡張子
# @return fname 選択ファイルパス
def openDialog(folder_path="", file_ext=None):
    if folder_path=="":
        folder_path = loadInit("open.init")
    options  = QFileDialog.Options()
    options |= QFileDialog.DontUseNativeDialog
    fname, _ = QFileDialog.getOpenFileName(
                parent    = None,
                caption   = 'Open file',
                directory = folder_path if os.path.isdir(folder_path) else os.getcwd(),
                filter    = file_ext if file_ext is not None else '*',
                options   = options)
    if not fname == "":
        saveInit("open.init", txt=os.path.dirname(fname))
    return fname

##
# @brief ファイル保存ダイアログの生成
# @param folder_path [str] 初期表示ディレクトリパス
# @param file_ext [str] 拡張子
# @return fname 選択ファイルパス
def saveDialog(folder_path="", file_ext=None):
    options  = QFileDialog.Options()
    options |= QFileDialog.DontUseNativeDialog
    fname, _ = QFileDialog.getSaveFileName(
                parent    = None,
                caption   = 'Save file',
                directory = folder_path if os.path.isdir(folder_path) else os.getcwd(),
                filter    = file_ext if file_ext is not None else '*',
                options   = options)
    return fname

##
# @brief フォルダオープンダイアログの生成
# @param folder_path [str] 初期表示ディレクトリパス
# @return fname 選択フォルダパス
def openFolderDialog(folder_path=""):
    if folder_path=="":
        folder_path = loadInit("open.init")
    options  = QFileDialog.Options()
    options |= QFileDialog.DontUseNativeDialog
    fname  = QFileDialog.getExistingDirectory(
                parent    = None,
                caption   = 'Open Directory',
                directory = folder_path if os.path.isdir(folder_path) else os.getcwd(),
                options   = options)
    if not fname == "":
        saveInit("open.init", txt=fname)
    return fname

import glob
##
# @brief フォルダ内のファイルリストを取得
# @param folder_path [str] フォルダパス
# @param file_ext [str] 拡張子
# @param recursive [bool] 再帰検索フラグ
# @return fname ファイルパスリスト
def getFileNames(folder_path="", file_ext="*", recursive=False):
    if not os.path.isdir(folder_path):
        folder_path = openFolderDialog()
    return glob.glob(folder_path+"/"+file_ext, recursive=recursive)


import numpy as np
import csv
##
# @brief フォルダ内のファイルリストを取得
# @param file_path [str] ファイルパス
# @param row_of_label [int] ラベル行番号（ラベルなしは0を設定）
# @retval header データヘッダーリスト
# @retval data_set データ
def csv_loader(file_path="", row_of_label=1):
    if not os.path.isfile(file_path):
        file_path = openDialog(file_ext="*.csv")
        if file_path=="":
            return None, None, None

    with open(file_path) as f:
        reader = csv.reader(f, delimiter=",")
        for i in range(row_of_label):
            header = next(reader)
    
    data_set = np.loadtxt(
        fname     = file_path,
        dtype     = "float",
        delimiter = ",",
        skiprows  = row_of_label,
        unpack    = True
    )
    return header, data_set, file_path



#os.path.expanduser('~') + '/Desktop'