# Importing all necessary modules
import matplotlib
matplotlib.use('Qt5Agg')
from PyQt5 import QtWidgets, Qt, QtCore, QtGui
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QMainWindow, QApplication, QInputDialog, QLineEdit, QVBoxLayout, QHBoxLayout, QFormLayout, QTableWidget, QTableWidgetItem, QFileDialog, QHeaderView
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import pandas
import random
import csv
import os
import sys

# A class that creates the GUI for the initial window to take in user data
class inputWindow(QMainWindow):
    
    submitted = QtCore.pyqtSignal(str)

    def __init__(self):
        super(inputWindow, self).__init__()
        self.states = ['Alabama', 'Alaska', 'Arizona', 'Arkansas', 'California', 'Colorado', 'Connecticut', 'Delaware', 'Florida', 'Georgia', 'Hawaii', 'Idaho', 'Illinois', 'Indiana', 'Iowa', 'Kansas', 'Kentucky', 'Louisiana', 'Maine', 'Maryland', 'Massachusetts', 'Michigan', 'Minnesota', 'Mississippi', 'Missouri', 'Montana', 'Nebraska', 'Nevada', 'New Hampshire', 'New Jersey', 'New Mexico', 'New York', 'North Carolina', 'North Dakota', 'Ohio', 'Oklahoma', 'Oregon', 'Pennsylvania', 'Rhode Island', 'South Carolina', 'South Dakota', 'Tennessee', 'Texas', 'Utah', 'Vermont', 'Virginia', 'Washington', 'West Virginia', 'Wisconsin', 'Wyoming']
        self.initUI()

    def initUI(self):
        self.setGeometry(1025, 475, 600, 1100)
        self.setWindowTitle('College Comparison Tool')
        self.setStyleSheet('background-color: #ffffff')
        self.imagePath = 'Graduation Cap.png'

        self.image = QImage(self.imagePath)
        self.imageLabel = QtWidgets.QLabel(self)
        self.imageLabel.setPixmap(QPixmap.fromImage(self.image))
        self.imageLabel.setAlignment(QtCore.Qt.AlignCenter)

        self.titleFont = QFont('Arial', 20, QFont.Bold)
        self.title = QtWidgets.QLabel("College Comparison Tool")
        self.title.setAlignment(QtCore.Qt.AlignCenter)
        self.title.setStyleSheet('color: #00204a')
        self.title.setFont(self.titleFont)

        self.descriptionFont = QFont('Arial', 10)
        self.description = QtWidgets.QLabel("Click 'SUBMIT' to see how you compare against schools in the selected state")
        self.description.setAlignment(QtCore.Qt.AlignCenter)
        self.description.setStyleSheet('color: #00204a')
        self.description.setFont(self.descriptionFont)

        self.combo = QtWidgets.QComboBox(self)
        self.combo.addItems(self.states)
        self.combo.setMinimumHeight(75)
        self.combo.setStyleSheet('selection-background-color: #005792')
        self.comboFont = QFont('Arial', 10)
        self.combo.setFont(self.comboFont)

        self.GPA = QLineEdit()
        self.GPA.setValidator(QDoubleValidator(0.0, 2.0, 1))
        self.GPA.setMaxLength(3)
        self.GPA.setStyleSheet('border: 3px solid #00204a')
        self.GPA.setPlaceholderText('GPA')
        self.GPA.setMinimumHeight(75)
        self.SAT = QLineEdit()
        self.SAT.setValidator(QIntValidator())
        self.SAT.setMaxLength(4)
        self.SAT.setStyleSheet('border: 3px solid #005792')
        self.SAT.setPlaceholderText('SAT')
        self.SAT.setMinimumHeight(75)
        self.ACT = QLineEdit()
        self.ACT.setValidator(QIntValidator())
        self.ACT.setMaxLength(4)
        self.ACT.setStyleSheet('border: 3px solid #00bbf0')
        self.ACT.setPlaceholderText('ACT')
        self.ACT.setMinimumHeight(75)

        self.submit = QtWidgets.QPushButton('SUBMIT', self)
        self.submit.clicked.connect(self.submitClicked)
        self.submit.setMinimumHeight(75)
        self.submit.setStyleSheet('background-color: #005792; color: white')
        self.submitFont = QFont('Arial', 10, QFont.Bold)
        self.submit.setFont(self.submitFont)
        
        self.verticalLayout = QVBoxLayout(self)
        self.verticalLayout.addWidget(self.imageLabel)
        self.verticalLayout.addStretch()
        self.verticalLayout.addWidget(self.title)
        self.verticalLayout.addStretch()
        self.verticalLayout.addWidget(self.description)
        self.verticalLayout.addStretch()
        self.verticalLayout.addWidget(self.combo)
        self.verticalLayout.addStretch()
        self.verticalLayout.addWidget(self.GPA)
        self.verticalLayout.addStretch()
        self.verticalLayout.addWidget(self.SAT)
        self.verticalLayout.addStretch()
        self.verticalLayout.addWidget(self.ACT)
        self.verticalLayout.addStretch()
        self.verticalLayout.addWidget(self.submit)

        self.widget = QtWidgets.QWidget()
        self.widget.setLayout(self.verticalLayout)
        self.setCentralWidget(self.widget)

    def submitClicked(self):
        self.submittedState = str(self.combo.currentText())
        self.submittedGPA = self.GPA.text()
        self.submittedSAT = self.SAT.text()
        self.submittedACT = self.ACT.text()
        self.GPA.setText('')
        self.SAT.setText('')
        self.ACT.setText('')
        self.userInput = {'State' : self.submittedState}
        if (self.submittedGPA != ''):
            if (float(self.submittedGPA) <= 4.0 and float(self.submittedGPA) >= 0.0):
                self.userInput.update({'GPA' : float(self.submittedGPA)})
            else:
                print('Not a valid GPA!')
        else:
            print('No GPA submitted!')
        if (self.submittedSAT != ''):
            if (int(self.submittedSAT) <= 1600 and int(self.submittedSAT) >= 0):
                self.userInput.update({'SAT' : int(self.submittedSAT)})
            else:
                print('Not a valid SAT score!')
        else:
            print('No SAT submitted!')

        if (self.submittedACT != ''):
            if (int(self.submittedACT) <= 36 and int(self.submittedACT) >= 0):
                self.userInput.update({'ACT' : int(self.submittedACT)})
            else:
                print('Not a valid ACT score!')
        else:
            print('No ACT submitted!')
        self.dataWin = dataWindow(self.userInput)
        self.dataWin.show()

# A class that creates the GUI for the second window to display the user data
class dataWindow(QMainWindow):
    def __init__(self, dictionary):
        super(dataWindow, self).__init__()
        self.stateData = dictionary.get('State')
        if 'GPA' in dictionary:
            self.GPAdata = dictionary.get('GPA')
        else:
            self.GPAdata = ''
        if 'SAT' in dictionary:
            self.SATdata = dictionary.get('SAT')
        else:
            self.SATdata = ''
        if 'ACT' in dictionary:
            self.ACTdata = dictionary.get('ACT')
        else:
            self.ACTdata = ''
        self.dataInitUI()

    def dataInitUI(self):
        self.setGeometry(275, 75, 2500, 1750)
        self.setWindowTitle('College Comparison Tool')
        self.setStyleSheet('background-color: #ffffff')
        self.stateLower = self.stateData.lower()
        self.csvData = pandas.read_csv(r'College Data Files\\' + self.stateLower + 'Data.csv', index_col = 0)
        self.graphCSVdata = pandas.read_csv(r'College Data Files\\' + self.stateLower + 'Data.csv', index_col = 0)

        self.graphGPA = plotCanvas(self, 5, 4, 100, self.graphCSVdata, self.GPAdata, self.SATdata, self.ACTdata, self.stateData)
        self.graphGPA.gpaPlot()

        self.graphSAT = plotCanvas(self, 5, 4, 100, self.graphCSVdata, self.GPAdata, self.SATdata, self.ACTdata, self.stateData)
        self.graphSAT.satPlot()

        self.graphACT = plotCanvas(self, 5, 4, 100, self.graphCSVdata, self.GPAdata, self.SATdata, self.ACTdata, self.stateData)
        self.graphACT.actPlot()
        
        self.tabs = QtWidgets.QTabWidget()
        self.tabs.addTab(self.graphGPA, 'GPA Graph')
        self.tabs.addTab(self.graphSAT, 'SAT Graph')
        self.tabs.addTab(self.graphACT, 'ACT Graph')
        self.tabs.setStyleSheet('color: #00204a; font-size: 25px; font-family: Arial')

        self.model = pandasTable(self.csvData)
        self.table = QtWidgets.QTableView(self)
        self.table.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.table.setModel(self.model)
        self.tableHeaderFont = QFont('monospace', 12, QFont.Bold)
        self.table.horizontalHeader().setFont(self.tableHeaderFont)
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.resizeColumnsToContents()

        self.close = QtWidgets.QPushButton('CLOSE', self)
        self.close.clicked.connect(self.closeClicked)
        self.close.setMinimumHeight(75)
        self.close.setStyleSheet('background-color: #005792; color: white')
        self.closeFont = QFont('Arial', 10, QFont.Bold)
        self.close.setFont(self.closeFont)

        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.tabs, 60)
        self.layout.addWidget(self.table, 36)
        self.layout.addWidget(self.close, 4)

        self.widget = QtWidgets.QWidget()
        self.widget.setLayout(self.layout)
        self.setCentralWidget(self.widget)

        self.show()      

    def closeClicked(self):
        self.hide()      

# A class that implements methods to create the GPA, SAT, and ACT plots
class plotCanvas(FigureCanvas):
    def __init__(self, parent, width, height, dpi, df, GPA, SAT, ACT, state):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = self.fig.add_subplot(111)
        self.df = df
        self.GPAgiven = GPA
        self.SATgiven = SAT
        self.ACTgiven = ACT
        self.stateGiven = state
        super(plotCanvas, self).__init__(self.fig)
    
    def gpaPlot(self):
        counter = 0
        for data in self.df['Average GPA']:
            if data != 'Not published':
                self.df.at[counter, 'Average GPA'] = float(data)
            else:
                self.df.at[counter, 'Average GPA'] = 0.0
            counter += 1
        self.axes.scatter(self.df['Average GPA'], self.df['College Name'], s = 100, color = '#00bbf0', zorder = 6, label = 'Average GPA')
        if self.GPAgiven != '':
            self.axes.axvline(x = self.GPAgiven, color = "#005792", linewidth = 4, zorder = 3, label = 'Your GPA')
        self.axes.set_title(self.stateGiven + ' GPA Data', fontdict = {'fontsize' : 30, 'color' : '#00204a'}, pad = 15)
        self.axes.set_xlabel('Average GPA', fontsize = 20, color = '#00204a')
        self.axes.grid(linestyle = '-', linewidth = '1', zorder = 0)
        self.axes.legend(bbox_to_anchor=(1.01, 1), loc='upper left', borderaxespad=0, prop={'size' : 14}) 
        plt.setp(self.axes.get_yticklabels(), rotation = 33, ha = 'right', rotation_mode = 'anchor', color = '#00204a', fontsize = 13)   
        plt.setp(self.axes.get_xticklabels(), color = '#00204a', fontsize = 13)    
        self.axes.plot()

    def satPlot25(self):
        counter25s = 0
        for data in self.df['SAT 25th Percentile']:
            if data != 'Not published':
                self.df.at[counter25s, 'SAT 25th Percentile'] = int(data)
            else:
                self.df.at[counter25s, 'SAT 25th Percentile'] = 0
            counter25s += 1
        self.axes.scatter(self.df['SAT 25th Percentile'], self.df['College Name'], s = 100, color = '#00bbf0', zorder = 9, label = '        SAT\n25th Percentile')
        if self.SATgiven != '':
            self.axes.axvline(x = self.SATgiven, color = "#005792", linewidth = 4, zorder = 3, label = 'Your SAT')
        self.axes.set_title(self.stateGiven + ' SAT Data', fontdict = {'fontsize' : 30, 'color' : '#00204a'}, pad = 15)
        self.axes.set_xlabel('SAT Score', fontsize = 20, color = '#00204a')
        self.axes.legend(bbox_to_anchor=(1.01, 1), loc='upper left', borderaxespad=0, prop={'size' : 14})   
        plt.setp(self.axes.get_yticklabels(), rotation = 33, ha = 'right', rotation_mode = 'anchor', color = '#00204a', fontsize = 15)   
        plt.setp(self.axes.get_xticklabels(), color = '#00204a', fontsize = 13)     
        self.axes.plot()

    def satPlot75(self):
        counter75s = 0
        for data in self.df['SAT 75th Percentile']:
            if data != 'Not published':
                self.df.at[counter75s, 'SAT 75th Percentile'] = int(data)
            else:
                self.df.at[counter75s, 'SAT 75th Percentile'] = 0
            counter75s += 1
        self.axes.scatter(self.df['SAT 75th Percentile'], self.df['College Name'], s = 100, color = '#00204a', zorder = 6, label = '        SAT\n75th Percentile')
        self.axes.grid(linestyle = '-', linewidth = '1', zorder = 0)
        self.axes.legend(bbox_to_anchor=(1.01, 1), loc='upper left', borderaxespad=0, prop={'size' : 14})        
        self.axes.plot()

    def satPlot(self):
        self.satPlot25()
        self.satPlot75()
    
    def actPlot25(self):
        counter25a = 0
        for data in self.df['ACT 25th Percentile']:
            if data != 'Not published':
                self.df.at[counter25a, 'ACT 25th Percentile'] = int(data)
            else:
                self.df.at[counter25a, 'ACT 25th Percentile'] = 0
            counter25a += 1
        self.axes.scatter(self.df['ACT 25th Percentile'], self.df['College Name'], s = 100, color = '#00bbf0', zorder = 9, label = '        ACT\n25th Percentile')
        if self.ACTgiven != '':
            self.axes.axvline(x = self.ACTgiven, color = "#005792", linewidth = 4, zorder = 3, label = 'Your ACT')
        self.axes.set_title(self.stateGiven + ' ACT Data', fontdict = {'fontsize' : 30, 'color' : '#00204a'}, pad = 15)
        self.axes.set_xlabel('ACT Scores', fontsize = 20, color = '#00204a')
        self.axes.legend(bbox_to_anchor=(1.01, 1), loc='upper left', borderaxespad=0, prop={'size' : 14})     
        plt.setp(self.axes.get_yticklabels(), rotation = 33, ha = 'right', rotation_mode = 'anchor', color = '#00204a', fontsize = 13)   
        plt.setp(self.axes.get_xticklabels(), color = '#00204a', fontsize = 13)   
        self.axes.plot()

    def actPlot75(self):
        counter75a = 0
        for data in self.df['ACT 75th Percentile']:
            if data != 'Not published':
                self.df.at[counter75a, 'ACT 75th Percentile'] = int(data)
            else:
                self.df.at[counter75a, 'ACT 75th Percentile'] = 0
            counter75a += 1
        self.axes.scatter(self.df['ACT 75th Percentile'], self.df['College Name'], s = 100, color = '#00204a', zorder = 6, label = '        ACT\n75th Percentile')
        self.axes.grid(linestyle = '-', linewidth = '1', zorder = 0)
        self.axes.legend(bbox_to_anchor=(1.01, 1), loc='upper left', borderaxespad=0, prop={'size' : 14})        
        self.axes.plot()

    def actPlot(self):
        self.actPlot25()
        self.actPlot75()
    
# A class that implements methods to display the table of data.
class pandasTable(QAbstractTableModel):
    def __init__(self, data):
        QAbstractTableModel.__init__(self)
        self.data = data

    def rowCount(self, parent=None):
        return self.data.shape[0]
    
    def columnCount(self, parent=None):
        return self.data.shape[1]

    def data(self, index, role = QtCore.Qt.DisplayRole):
        if index.isValid():
            if role == QtCore.Qt.DisplayRole:
                return str(self.data.iloc[index.row(), index.column()])
        return None

    def headerData(self, column, orientation, role):
        if orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:
            return self.data.columns[column]
        return None

# A function that calls all methods needed to run the program.
def run():
    app = QApplication(sys.argv)
    win = inputWindow()
    win.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    run()