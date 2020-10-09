# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'DEMATMM.ui'
#
# Created by: PyQt5 UI code generator 5.15.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.
from PyQt5 import QtCore, QtGui, QtWidgets

from PyQt5.QtWidgets import QTableWidget, QApplication, QMainWindow, QTableWidgetItem, QFileDialog,qApp, QAction,QStyledItemDelegate,QLineEdit,QWidget,qApp, QAction,QMessageBox

from pandas import DataFrame
from tabulate import tabulate
from numpy.linalg import inv
from PyQt5.QtCore import QRegExp
from PyQt5.QtGui import QRegExpValidator
from PyQt5.QtCore import pyqtSlot
import sqlite3 
import os
import csv
import re
import numpy as np 
import pandas as pd

class NumericDelegate(QStyledItemDelegate):
    def createEditor(self, parent, option, index):
        editor = super(NumericDelegate, self).createEditor(parent, option, index)
        if isinstance(editor, QLineEdit):
            reg_ex = QRegExp("[0-9]+.?[0-9]{,2}")
            validator = QRegExpValidator(reg_ex, editor)
            editor.setValidator(validator)
        return editor
    
class Ui_MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.check_change = True
       
    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Window Close', 'Are you sure you want to close the window?',
                QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            event.accept()
            print('Window closed')
        else:
            event.ignore()
    def addRow(self):
        self.tableWidgetInput.insertRow(self.tableWidgetInput.rowCount()+0)                   
        self.tableWidgetOutput.insertRow(self.tableWidgetOutput.rowCount()+0)
    def addCol(self):    
        print("Row size of the Matrix is Increased")
        columnCount = self.tableWidgetInput.columnCount()
        self.tableWidgetInput.insertColumn(columnCount )
        columnCount = self.tableWidgetOutput.columnCount()
        self.tableWidgetOutput.insertColumn(columnCount )
        print("Column size of the Matrix is Increased")


    def removeRow(self):
        if self.tableWidgetInput.rowCount() > 0:                             ##########input table#######
            self.tableWidgetInput.removeRow(self.tableWidgetInput.rowCount()-1)
        if self.tableWidgetOutput.rowCount() > 0:                                       #####output table##########
            self.tableWidgetOutput.removeRow(self.tableWidgetOutput.rowCount()-1)
        print("Row size of the Matrix is Decreased")


    def removeCol(self):
        if self.tableWidgetInput.columnCount() > 0:
            self.tableWidgetInput.removeColumn(self.tableWidgetInput.columnCount()-1)
        if self.tableWidgetOutput.columnCount() > 0:
            self.tableWidgetOutput.removeColumn(self.tableWidgetOutput.columnCount()-1)
        print("Column size of the Matrix is Decreased")

    def click_me(self):
        rows  =  self.tableWidgetInput.rowCount()
        listi = []
        for i in range(rows):
            it = self.tableWidgetInput.item(i, 0)
            if it:
                if it.text():
                    listi.append(it.text())

            else:
                print("Enter")     
      
        print(len(listi))

    def close_sheet(self):
        qApp.quit()

    def open_sheet(self):
        print("opening the sheet")
        
        
        rc = self.tableWidgetInput.rowCount()
        cc = self.tableWidgetInput.columnCount()

        global rowData
        self.check_change = False
        path = QFileDialog.getOpenFileName(self, 'Open CSV', os.getenv('HOME'), 'CSV(*.csv)')
        if path[0] != '':
            with open(path[0], newline='') as csv_file:
                self.tableWidgetInput.setRowCount(0)
                self.tableWidgetInput.setColumnCount(10)
                my_file = csv.reader(csv_file, dialect='excel')

                for rowData in my_file:
                    row = self.tableWidgetInput.rowCount()
                    self.tableWidgetInput.insertRow(row)
                    if len(rowData) > 10:
                        
                        self.tableWidgetInput.setColumnCount(len(rowData))
                    for column, stuff in enumerate(rowData):
                        item = QTableWidgetItem(stuff)
                        self.tableWidgetInput.setItem(row, column, item)

                
        self.check_change = True

    def cellcheck(self,row,column):
        global EnteredData,listi ,isize,iTabrow,iTabcol,oTabrow,oTabCol
        iTabrow = self.tableWidgetInput.rowCount()
        iTabcol = self.tableWidgetInput.columnCount()
        
        
        isize=iTabrow*iTabcol    
        listi = []
        for i in range(iTabrow):
            for j in range(iTabcol):
                it = self.tableWidgetInput.item(i, j)
                if it:
                    if it.text():
                        listi.append(it.text())
            
                     
        EnteredData= len(listi)
        if (EnteredData==isize):
            self.pushButton_submit.setEnabled(True)
        

    def view(self):
    
        self.pushButton_submit.setEnabled(True)
        self.frame2.setVisible(True) 
        oTabrow = self.tableWidgetOutput.setRowCount(iTabrow)
        oTabCol =self.tableWidgetOutput.setColumnCount(iTabcol)
        

        print("View the result")
        for i in range(iTabrow):
            for j in range(iTabcol):
                it = self.tableWidgetInput.item(i, j)
                if it and it.text():
                    self.textEdit1.clear()
                    self.textEdit2.clear()
                    self.textEdit3.clear()
                    self.textEdit4.clear()
                    self.textEdit5.clear() 
                    for row_number,rdata in enumerate(TMatrix):   
                        for Columnn_number, data in enumerate(rdata):
                            self.tableWidgetOutput.setItem(row_number,Columnn_number,QtWidgets.QTableWidgetItem(str(round(data,4))))

                    RiPCiprint= np.around(RiplusCi,decimals=4)
                    RiMCiprint= np.around(RiMinusCi,decimals=4)
                    Riprint=np.around(Ri,decimals=4)
                    Ciprint= np.around(Ci,decimals=4) 
                    #PTMatrix = tabulate(TMatrix , tablefmt="github", floatfmt = ".4f")
                    self.textEdit1.insertPlainText(str(tabulate(TMatrix , tablefmt="simple", floatfmt = ".4f")))

                    np.set_printoptions(formatter={'all':lambda x: '{}\n'.format(x)})
                    self.textEdit2.insertPlainText(str(Riprint))
                    self.textEdit3.insertPlainText(str(Ciprint))
                    self.textEdit4.insertPlainText(str(RiPCiprint))
                    self.textEdit5.insertPlainText(str(RiMCiprint))

    @pyqtSlot()
    def clear(self):
        
        self.tableWidgetInput.clear()
        self.tableWidgetOutput.clear()
        self.textEdit1.clear()
        self.textEdit2.clear()
        self.textEdit3.clear()
        self.textEdit4.clear()
        self.textEdit5.clear() 
        print("cleared the data")

    def save_sheet(self):
        path = QFileDialog.getSaveFileName(self, 'Save CSV', os.getenv('HOME'), 'CSV(*.csv)')
        if path[0] != '':
            with open(path[0], 'w',newline='\n') as csv_file:
                writer = csv.writer(csv_file, dialect='excel')
                
                istr =['The Input Matrix is  :']
                writer.writerow(istr)
                writer.writerow("\n")
                for row in range(self.tableWidgetInput.rowCount()): ###########################Write the Input###############################
                    SaveInputData = []
                    for column in range(self.tableWidgetInput.columnCount()):
                        item = self.tableWidgetInput.item(row, column)
                        if item is not None:
                            SaveInputData.append(item.text())
                        else:
                            SaveInputData.append('')
                    writer.writerow(SaveInputData)


                ostr =['The Output Matrix is  :']
                writer.writerow(ostr)
                writer.writerow("\n")
                for row in range(self.tableWidgetOutput.rowCount()): ###########################Write the Input###############################
                    SaveOutputData = []
                    for column in range(self.tableWidgetOutput.columnCount()):
                        item = self.tableWidgetOutput.item(row, column)
                        if item is not None:
                            SaveOutputData.append(item.text())
                        else:
                            SaveOutputData.append('')
                    writer.writerow(SaveOutputData)
                
                ostr =['The Ri   values are   :']
                writer.writerow(ostr)
                writer.writerow(Ri)
                writer.writerow("\n")
                ostr =['The Ci   values are   :']
                writer.writerow(ostr)
                writer.writerow(Ci)
                writer.writerow("\n")

                ostr =['The Ri+Ci   values are   :']
                writer.writerow(ostr)
                writer.writerow(RiplusCi)
                writer.writerow("\n")

                ostr =['The Ri-Ci   values are   :']
                writer.writerow(ostr)
                writer.writerow(RiMinusCi)
                writer.writerow("\n")          
   
    
    def submit(self):
        global EnteredData,listi ,isize,iTabrow,iTabcol,rowData,TMatrix
        iTabrow = self.tableWidgetInput.rowCount()
        iTabcol = self.tableWidgetInput.columnCount()

        

        #tTabrow= self.tempTable.rowCount()
        #tTabcol= self.tempTable.columnCount()
        
        isize=iTabrow*iTabcol    
        listi = []
        for i in range(iTabrow):
            for j in range(iTabcol):
                it = self.tableWidgetInput.item(i, j)
                if it:
                    if it.text():
                        listi.append(it.text())
                           
        EnteredData= len(listi)
        if (EnteredData==isize):
            self.pushButton_submit.setEnabled(True)
        
    
            rowCount = self.tableWidgetInput.rowCount()
            columnCount = self.tableWidgetInput.columnCount()
            
            max_sum = 0
            global TMatrix,Ri,Ci,RiplusCi,RiMinusCi,inputArray_2D
            if (rowCount==columnCount):
                size=rowCount

                print("The size of the matrxi is %d * %d "%(size,size))
                print("The Given  matrxi is",  "SUM of Row" )
            
                rowData =[]
                
                for row in range(size):
                    for column in range (size):
                            widegetItem = self.tableWidgetInput.item(row,column)
                            if widegetItem and widegetItem.text():
                                rowData.append(float(widegetItem.text()) )
                            else:
                                rowData.append('NULL')
                np.set_printoptions(formatter={'all':lambda x: '{}\n'.format(x)})
                #print(rowData)
                inputArray = np.array(rowData,dtype=np.float64)  ###convert the list into numpy array.
                #print(inputArray)
                size_rowdata = len(rowData)
                print("The total number of elemets are ",size_rowdata)
                inputArray_2D = np.reshape(inputArray, (rowCount, columnCount))   ### Reshape the numpy array into 2D
                
                print(tabulate(inputArray_2D , tablefmt="simple", floatfmt = ".4f"))

                sumofCol = np.sum(inputArray_2D,axis = 0,dtype='float')  ###find the sum of Column
                sumofRow = np.sum(inputArray_2D,axis = 1,dtype='float') ### find the sum of Row     
                maxInCol = np.amax(sumofCol)
                maxInRows = np.amax(sumofRow)

                print( "The Sum of Column is : ",sumofCol)
                print( "The Sum of Row is :",sumofRow)
                print( "The Maximum value in the  Column is :",maxInCol)
                print( "The Maximum value in the  Row is  : ",maxInRows)
               


             ##########################################################################################################################################################################################################
                print("\n\n")
                print("The D matrix  :")
                
                Dmatrix = inputArray_2D/ maxInRows 
                #Dmatrix = np.around(p1,decimals=4)
                print(tabulate(Dmatrix , tablefmt="simple", floatfmt = ".4f"))
                print("\n\n")


                print("The I matrix :")
               
                IMatrix= np.identity(size)
                #IMatrix = np.around(p2,decimals=4)
                print(tabulate(IMatrix , tablefmt="simple", floatfmt = ".4f"))
                print("\n\n")


                print("The I-D matrix  :")
                IminDmatrix = IMatrix  - Dmatrix
                IminDmatrix = IMatrix  - Dmatrix
                #IminDmatrix = np.around(p3,decimals=4)
                print(tabulate(IminDmatrix , tablefmt="simple", floatfmt = ".4f"))
                print("\n\n")


                print("The (I-D)^1 matrix :")
               
                InversofIminDmatrix= np.linalg.inv(IminDmatrix)
                #InversofIminDmatrix = np.around(p4,decimals=4)
                print(tabulate(InversofIminDmatrix , tablefmt="simple", floatfmt = ".4f"))
                print("\n\n")


                print("The D*(I-D)^1 matrix  :")
                
                TMatrix= np.matmul(Dmatrix  , InversofIminDmatrix)
                #TMatrix=np.around(p5,decimals=4)
                print(tabulate(TMatrix , tablefmt="simple", floatfmt = ".4f"))
                print("\n\n")


                print("The Ri   values are   :")
                print("----------------------")
                Ri= np.sum(TMatrix  ,axis= 1)
                np.savetxt(sys.stdout, Ri, fmt="%.4f")
                #np.savetxt(sys.stdout, p6, fmt="%.3f")
                
                print("\n\n")


                print("The Ci   values are   :")
                print("----------------------")
                Ci = np.sum(TMatrix  ,axis= 0)
                np.savetxt(sys.stdout, Ci, fmt="%.4f")
               # print(Ci)
                print("\n\n")


                print("************************************************************************************************************************************")

                print("The Ri+Ci   values are   :")
                print("----------------------")

                RiplusCi = Ri + Ci 
                np.savetxt(sys.stdout, RiplusCi, fmt="%.4f")
                #RiplusCi=np.around(p8,decimals=4)

                #print(RiplusCi)
                print("\n\n")


                print("The Ri-Ci   values are   :")
                print("----------------------")
                RiMinusCi = Ri - Ci 
                np.savetxt(sys.stdout, RiMinusCi, fmt="%.4f")
                #print(RiMinusCi)

                print("************************************************************************************************************************************")
                print("\n\n")


            else:
                print("Data is not Submitted Sucessfully")
                print("Please give the square matrix as a input. ")
                
        else:
            print("Please fill the input matrix ")
  
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(2300, 1800)
        MainWindow.setStyleSheet("QMainWindow {\n"
" background-color: beige;\n"
"}\n"
"QPushButton {\n"
"    background-color: palegoldenrod;\n"
"    border-width: 2px;\n"
"    border-color: darkkhaki;\n"
"    border-style: solid;\n"
"    border-radius: 2;\n"
"    padding: 3px;\n"
"    min-width: 9ex;\n"
"    min-height: 2.5ex;\n"
"}\n"
"QTabWidget::pane { /* The tab widget frame */\n"
"    border-top: 2px solid #C2C7CB;\n"
"background-color: palegoldenrod\n"
"}\n"
"\n"
"QTabWidget::tab-bar {\n"
"    left: 5px; /* move to the right by 5px */\n"
"}\n"
"\n"
"/* Style the tab using the tab sub-control. Note that\n"
"    it reads QTabBar _not_ QTabWidget */\n"
"QTabBar::tab {\n"
"    background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,\n"
"                                stop: 0 #E1E1E1, stop: 0.4 #DDDDDD,\n"
"                                stop: 0.5 #D8D8D8, stop: 1.0 #D3D3D3);\n"
"    border: 2px solid #C4C4C3;\n"
"    border-bottom-color: #C2C7CB; /* same as the pane color */\n"
"    border-top-left-radius: 4px;\n"
"    border-top-right-radius: 4px;\n"
"    min-width: 12ex;\n"
"    padding: 2px;\n"
"}\n"
"\n"
"QTabBar::tab:selected, QTabBar::tab:hover {\n"
"    background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,\n"
"                                stop: 0 #fafafa, stop: 0.4 #f4f4f4,\n"
"                                stop: 0.5 #e7e7e7, stop: 1.0 #fafafa);\n"
"}\n"
"\n"
"QTabBar::tab:selected {\n"
"    border-color: blue;\n"
"    border-bottom-color: blue; /* same as pane color */\n"
"}\n"
"\n"
"QTabBar::tab:!selected {\n"
"    margin-top: 2px; /* make non-selected tabs look smaller */\n"
"}\n"
"\n"
"/* make use of negative margins for overlapping tabs */\n"
"QTabBar::tab:selected {\n"
"    /* expand/overlap to the left and right by 4px */\n"
"    margin-left: -4px;\n"
"    margin-right: -4px;\n"
"}\n"
"\n"
"QTabBar::tab:first:selected {\n"
"    margin-left: 0; /* the first selected tab has nothing to overlap with on the left */\n"
"}\n"
"\n"
"QTabBar::tab:last:selected {\n"
"    margin-right: 0; /* the last selected tab has nothing to overlap with on the right */\n"
"}\n"
"\n"
"QTabBar::tab:only-one {\n"
"    margin: 0; /* if there is only one tab, we don\'t want overlapping margins */\n"
"}"


"\n"
"QTableView{\n"
"    background-color: palegoldenrod;\n"
"    border-width: 2px;\n"
"    border-color: darkkhaki;\n"
"    border-style: solid;\n"
"    border-radius: 5;\n"
"    padding: 3px;\n"
"    min-width: 9ex;\n"
"    min-height: 2.5ex;\n"
"}\n"
"\n"
"/* Increase the padding, so the text is shifted when the button is\n"
"   pressed. */\n"
"QPushButton:pressed {\n"
"    padding-left: 5px;\n"
"    padding-top: 5px;\n"
"    background-color: #d0d67c;\n"
"}\n"
"\n"
"QLabel, QAbstractButton {\n"
"    font: bold;\n"
"}\n"
"\n"
"/* Mark mandatory fields with a brownish color. */\n"
".mandatory {\n"
"    color: brown;\n"
"}\n"
"\n"
"/* Bold text on status bar looks awful. */\n"
"QStatusBar QLabel {\n"
"   font: normal;\n"
"}\n"
"\n"
"QStatusBar::item {\n"
"    border-width: 1;\n"
"    border-color: darkkhaki;\n"
"    border-style: solid;\n"
"    border-radius: 2;\n"
"}")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
################################INPUT  FRAME  ###################################################################################################################################################################################################
        self.frame1 = QtWidgets.QFrame(self.centralwidget)
        self.frame1.setGeometry(QtCore.QRect(30, 50, 2500, 2000))
        self.frame1.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame1.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame1.setObjectName("frame1")
        self.label = QtWidgets.QLabel(self.frame1)
        self.label.setGeometry(QtCore.QRect(30, 20, 691, 41))
        font = QtGui.QFont()
        font.setFamily("Adobe Devanagari")
        font.setPointSize(20)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setAutoFillBackground(False)
        self.label.setObjectName("label")
        self.tableWidgetInput = QtWidgets.QTableWidget(self.frame1)
        self.tableWidgetInput.setGeometry(QtCore.QRect(30, 90, 1549, 520))
        self.tableWidgetInput.setObjectName("tableWidgetInput")
        self.tableWidgetInput.setColumnCount(2)
        self.tableWidgetInput.setRowCount(2)
        delegate = NumericDelegate(self.tableWidgetInput)
        self.tableWidgetInput.setItemDelegate(delegate)
        self.tableWidgetInput.cellChanged.connect(self.cellcheck)
        
        self.verticalLayoutWidget = QtWidgets.QWidget(self.frame1)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(1600, 90, 121, 331))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        ###############################################
        self.pushButton_addRow = QtWidgets.QPushButton(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Arial Black")
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_addRow.setFont(font)
        self.pushButton_addRow.setObjectName("pushButton_addRowCol")
        self.verticalLayout.addWidget(self.pushButton_addRow)
        self.pushButton_addRow.clicked.connect(self.addRow)  
##########################################################################

        self.pushButton_addCol = QtWidgets.QPushButton(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Arial Black")
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_addCol.setFont(font)
        self.pushButton_addCol.setObjectName("pushButton_addRowCol")
        self.verticalLayout.addWidget(self.pushButton_addCol)
        self.pushButton_addCol.clicked.connect(self.addCol)                                            #####Increse the size#####
        ##################################################################
        self.pushButton_removeRow = QtWidgets.QPushButton(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Arial Black")
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_removeRow.setFont(font)
        self.pushButton_removeRow.setObjectName("pushButton_removeRowCol")
        self.pushButton_removeRow.clicked.connect(self.removeRow)  

                                          #####Increse the size#####
        ##################################################################
        self.pushButton_removeCol = QtWidgets.QPushButton(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Arial Black")
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_removeCol.setFont(font)
        self.pushButton_removeCol.setObjectName("pushButton_removeRowCol")
        self.pushButton_removeCol.clicked.connect(self.removeCol)      
                                                 ####Decrease the sie####
        self.verticalLayout.addWidget(self.pushButton_addRow)
        self.verticalLayout.addWidget(self.pushButton_addCol)
        self.verticalLayout.addWidget(self.pushButton_removeRow)
        self.verticalLayout.addWidget(self.pushButton_removeCol)
        ################################################################

        self.pushButton_submit = QtWidgets.QPushButton(self.frame1)
        self.pushButton_submit.setGeometry(QtCore.QRect(350, 625, 131, 51))
        font = QtGui.QFont()
        font.setFamily("Arial Black")
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_submit.setFont(font)
        self.pushButton_submit.setObjectName("pushButton_submit")                                        
        self.pushButton_submit.clicked.connect(self.submit)                                                      ####SUBMIT THE INPUT MATRIX### 
       
        self.pushButton_submit.setEnabled(False)
        #self.pushButton_submit.clicked.connect(lambda:self.click_me())

        #####################################################################
        self.pushButton_view = QtWidgets.QPushButton(self.frame1)
        self.pushButton_view.setGeometry(QtCore.QRect(520, 625, 131, 51))
        font = QtGui.QFont()
        font.setFamily("Arial Black")
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_view.setFont(font)
        self.pushButton_view.setObjectName("pushButton_view")
        self.pushButton_view.clicked.connect(self.view)                                                      #### view the output MATRIX###
        ################################################################
        self.pushButton_clear = QtWidgets.QPushButton(self.frame1)
        self.pushButton_clear.setGeometry(QtCore.QRect(690, 625, 131, 51))
        font = QtGui.QFont()
        font.setFamily("Arial Black")
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_clear.setFont(font)
        self.pushButton_clear.setObjectName("pushButton_view")
        self.pushButton_clear.clicked.connect(self.clear)                                                      #### clear the output MATRIX### 
        

################################OUTPUT FRAME  ##################################################################################################################################################################################################
       

        self.frame2 = QtWidgets.QFrame(self.centralwidget)
        self.frame2.setGeometry(QtCore.QRect(30, 800, 2500, 2000))
        self.frame2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame2.setObjectName("frame2")
        self.frame2.setVisible(False)

        self.label_3 = QtWidgets.QLabel(self.frame2)
        self.label_3.setGeometry(QtCore.QRect(30, 20, 691, 41))
        font = QtGui.QFont()
        font.setFamily("Adobe Devanagari")
        font.setPointSize(20)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.label_3.setFont(font)
        self.label_3.setAutoFillBackground(False)
        self.label_3.setObjectName("label_3")
     

        self.label_33 = QtWidgets.QLabel(self.frame2)
        self.label_33.setGeometry(QtCore.QRect(1600, 20, 691, 41))
        font = QtGui.QFont()
        font.setFamily("Adobe Devanagari")
        font.setPointSize(20)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.label_33.setFont(font)
        self.label_33.setAutoFillBackground(False)
        self.label_33.setObjectName("label_3")
        self.tableWidgetOutput = QtWidgets.QTableWidget(self.frame2)
        self.tableWidgetOutput.setGeometry(QtCore.QRect(30,90, 1549, 520))
        self.tableWidgetOutput.setObjectName("tableWidgetOutput")
        #self.tableWidgetOutput.setColumnCount(2)
        #self.tableWidgetOutput.setRowCount(2)
        self.tableWidgetOutput.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)


        self.tabWidget = QtWidgets.QTabWidget(self.frame2)
        self.tabWidget.setGeometry(QtCore.QRect(1670, 90, 550, 520))
        self.tabWidget.setObjectName("tabWidget")
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setWeight(30)
        self.tabWidget.setFont(font)

        self.tab1 = QtWidgets.QWidget()
        self.tab1.setObjectName("tab1")
        self.textEdit1 = QtWidgets.QTextEdit(self.tab1)
        self.textEdit1.setGeometry(QtCore.QRect(10, 10, 480, 470))
        self.textEdit1.setObjectName("textEdit1")
        self.textEdit1.setFont(font)
        self.textEdit1.setReadOnly(True)
        self.tabWidget.addTab(self.tab1, "")
        
        self.tab2 = QtWidgets.QWidget()
        self.tab2.setObjectName("tab2")
        self.textEdit2 = QtWidgets.QTextEdit(self.tab2)
        self.textEdit2.setGeometry(QtCore.QRect(10, 10, 480, 470))
        self.textEdit2.setObjectName("textEdit2")
        self.textEdit2.setFont(font)
        self.textEdit2.setReadOnly(True)
        self.tabWidget.addTab(self.tab2, "")
        
        self.tab3 = QtWidgets.QWidget()
        self.tab3.setObjectName("tab3")
        self.textEdit3 = QtWidgets.QTextEdit(self.tab3)
        self.textEdit3.setGeometry(QtCore.QRect(10, 10, 480, 470))
        self.textEdit3.setObjectName("textEdit1")
        self.textEdit3.setFont(font)
        self.textEdit3.setReadOnly(True)
        self.tabWidget.addTab(self.tab3, "")

        self.tab4 = QtWidgets.QWidget()
        self.tab4.setObjectName("tab4")
        self.textEdit4 = QtWidgets.QTextEdit(self.tab4)
        self.textEdit4.setGeometry(QtCore.QRect(10, 10, 480, 470))
        self.textEdit4.setObjectName("textEdit1")
        self.textEdit4.setFont(font)
        self.textEdit4.setReadOnly(True)
        self.tabWidget.addTab(self.tab4, "")


        self.tab5 = QtWidgets.QWidget()
        self.tab5.setObjectName("tab5")
        self.textEdit5 = QtWidgets.QTextEdit(self.tab5)
        self.textEdit5.setGeometry(QtCore.QRect(10, 10, 480, 470))
        self.textEdit5.setObjectName("textEdit1")
        self.textEdit5.setFont(font)
        self.textEdit5.setReadOnly(True)
        self.tabWidget.addTab(self.tab5, "")




        self.pushButton_save = QtWidgets.QPushButton(self.frame2)
        self.pushButton_save.setGeometry(QtCore.QRect(350, 625, 131, 51))
        font = QtGui.QFont()
        font.setFamily("Arial Black")
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_save.setFont(font)
        self.pushButton_save.setObjectName("pushButton_save")
        self.pushButton_save.clicked.connect(self.save_sheet)
        self.pushButton_cancel = QtWidgets.QPushButton(self.frame2)
        self.pushButton_cancel.setGeometry(QtCore.QRect(520, 625, 131, 51))
        font = QtGui.QFont()
        font.setFamily("Arial Black")
        font.setBold(True)
        font.setWeight(75)
        ######################################################################################
        self.pushButton_cancel.setFont(font)
        self.pushButton_cancel.setObjectName("pushButton_cancel")

        MainWindow.setCentralWidget(self.centralwidget)
        #############################################################################################
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1151, 18))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuEdit = QtWidgets.QMenu(self.menubar)
        self.menuEdit.setObjectName("menuEdit")
        self.menuHelp = QtWidgets.QMenu(self.menubar)
        self.menuHelp.setObjectName("menuHelp")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionSave = QtWidgets.QAction(MainWindow)
        self.actionSave.setObjectName("actionSave")
        self.actionOpen = QtWidgets.QAction(MainWindow)
        self.actionOpen.setObjectName("actionOpen")
        #self.actionCopy = QtWidgets.QAction(MainWindow)
        #self.actionCopy.setObjectName("actionCopy")
        #self.actionPaste = QtWidgets.QAction(MainWindow)
        #self.actionPaste.setObjectName("actionPaste")
        self.actionClose = QtWidgets.QAction(MainWindow)
        self.actionClose.setObjectName("actionClose")
        self.menuFile.addAction(self.actionSave)
        self.menuFile.addAction(self.actionOpen)
        self.menuFile.addAction(self.actionClose)
        #self.menuEdit.addAction(self.actionCopy)
        #self.menuEdit.addAction(self.actionPaste)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuEdit.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())
        
        self.actionOpen.triggered.connect(self.open_sheet)
        self.actionClose.triggered.connect(self.close_sheet)
        #self.actionSave.triggered.connect(self.save_sheet)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
   
    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "Fill the Values in the matrix"))
        self.pushButton_addRow.setText(_translate("MainWindow", "+ Row"))
        self.pushButton_addCol.setText(_translate("MainWindow", "+ Col"))
        self.pushButton_removeRow.setText(_translate("MainWindow", "- Row"))
        self.pushButton_removeCol.setText(_translate("MainWindow", "- Col"))

        self.pushButton_submit.setText(_translate("MainWindow", "Submit"))
        self.pushButton_view.setText(_translate("MainWindow", "View "))
        self.pushButton_clear.setText(_translate("MainWindow", "Clear"))
        self.label_3.setText(_translate("MainWindow", "The Output matrix"))
        self.label_33.setText(_translate("MainWindow", "The Ri Ci  Data's"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab1), _translate("MainWindow", "T Matrix "))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab2), _translate("MainWindow", "Ri"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab3), _translate("MainWindow", "Ci"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab4), _translate("MainWindow", "Ri+Ci"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab5), _translate("MainWindow", "Ri-Ci"))

        self.pushButton_save.setText(_translate("MainWindow", "Save"))
        self.pushButton_cancel.setText(_translate("MainWindow", "Cancel"))
        self.menuFile.setStatusTip(_translate("MainWindow", "File Menu"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.menuEdit.setTitle(_translate("MainWindow", "Edit"))
        self.menuHelp.setTitle(_translate("MainWindow", "Help"))

        self.actionSave.setText(_translate("MainWindow", "Save"))
        self.actionSave.setStatusTip(_translate("MainWindow", "Save the file"))
        self.actionSave.setShortcut(_translate("MainWindow", "Ctrl+S"))
        
        self.actionOpen.setText(_translate("MainWindow", "Open"))
        self.actionOpen.setStatusTip(_translate("MainWindow", "Open New "))
        self.actionOpen.setShortcut(_translate("MainWindow", "Ctrl+O"))

        '''self.actionCopy.setText(_translate("MainWindow", "Copy"))
        self.actionCopy.setStatusTip(_translate("MainWindow", "Copy the data"))
        self.actionCopy.setShortcut(_translate("MainWindow", "Ctrl+C"))

        self.actionPaste.setText(_translate("MainWindow", "Paste"))
        self.actionPaste.setStatusTip(_translate("MainWindow", "Paste the data"))
        self.actionPaste.setShortcut(_translate("MainWindow", "Ctrl+V"))
        self.actionClose.setText(_translate("MainWindow", "Close"))'''

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
