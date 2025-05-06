from PyQt6.QtWidgets import *
from voteApp import *
import csv
import datetime
import re

class Logic(QMainWindow, Ui_Dialog):
    def __init__(self):
        '''
        This function:
        1. Connects the buttons to their functions
        2.Moves the buttons to the correct layers
        3.Makes it so pyqt won't focus on any of the buttons
        4.Brings up the Vote/Exit Menu
        '''
        super().__init__()
        self.setupUi(self)
        self.voteButton.clicked.connect(lambda: self.summonCandidiateMenu())
        self.exitButton.clicked.connect(lambda: self.summonStats())
        self.voteJaneButton.clicked.connect(lambda: self.vote("Jane"))
        self.voteJohnButton.clicked.connect(lambda: self.vote("John"))
        self.voteJaneButton.raise_()
        self.voteJohnButton.raise_()
        self.voteButton.raise_()
        self.exitButton.raise_()
        self.voteButton.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)
        self.exitButton.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)
        self.voteJaneButton.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)
        self.voteJohnButton.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)
        self.bottomLabel.raise_()
        self.idInput.raise_()
        self.summonVoteMenu()

    def summonCandidiateMenu(self):
        '''
        This function
        1. brings up the vote and exit buttons
        2. Brings up voter id input field
        3. hides everything else
        4. sets the labels to the correct text
        '''
        self.voteJaneButton.show()
        self.voteJohnButton.show()
        self.idInput.show()
        self.idLabel.show()
        self.voteButton.hide()
        self.exitButton.hide()
        self.janeLabel.hide()
        self.johnLabel.hide()
        self.totalLabel.hide()
        self.topLabel.setText("Vote Menu")
        self.bottomLabel.setText("Choose a Candidate")

    def summonVoteMenu(self):
        '''
        This function:
        1.Brings up the Vote and exit button and id input
        2.Hides everything else
        3.Moves the votebutton to its proper position
        4.Sets the top label to "Candidate Menu
        '''
        self.voteJaneButton.hide()
        self.voteJohnButton.hide()
        self.idInput.hide()
        self.idLabel.hide()
        self.janeLabel.hide()
        self.johnLabel.hide()
        self.totalLabel.hide()
        self.voteButton.show()
        self.voteButton.move(90, 80)
        self.exitButton.show()
        self.topLabel.setText("Candidate Menu")

    def summonStats(self):
        '''
        This function:
        1.Brings up the labels that will show the vote counts
        2.Hides everything else
        3. Sets the top label to the right text
        4. Opens the file with all the votes, counts the votes
        for each candidate
        5.Displays the votes for Jane, John, and total
        6.Shows and moves the vote button to the bottom of the screen
        '''
        self.voteJaneButton.hide()
        self.voteJohnButton.hide()
        self.idInput.hide()
        self.idLabel.hide()
        self.voteButton.hide()
        self.bottomLabel.hide()
        self.exitButton.hide()
        self.bottomLabel.move(100, 230)
        self.janeLabel.show()
        self.johnLabel.show()
        self.totalLabel.show()
        self.topLabel.setText("Results:")
        __johnCount: int = 0
        __janeCount: int = 0
        try:
            with open('votesData.csv', 'r', newline='') as votesFile:
                dataReader = csv.reader(votesFile)
                for row in dataReader:
                    if row[0] == "Jane":
                        __janeCount += 1
                    else:
                        __johnCount += 1
                self.janeLabel.setText(f'Jane: {__janeCount}')
                self.johnLabel.setText(f'John: {__johnCount}')
                self.totalLabel.setText(f'Total: {__johnCount + __janeCount}')
        except:
            self.bottomLabel.setText('Unable to access votes')
        self.voteButton.show()
        self.voteButton.move(90,200)

    def vote(self, candidiate: str) -> str:
        '''
        1.Stips input of everything but digits, checks for length, prompts user if input is incorrect
        2.Checks if the ID has already voted, tells user
        1.Writes what candiate was voted for, time of the vote, and voter id into a csv file
        2.Tells the user their vote went through
        3. Bring up the vote/exit menu
        :param candidiate:
        '''
        __userInput = self.idInput.text()
        __userInput = re.sub(r'\D', '', __userInput)
        while len(__userInput) != 9:
            self.bottomLabel.show()
            self.bottomLabel.move(50,230)
            self.bottomLabel.setText(f'Please Use the correct Format.')
            self.bottomLabel.setStyleSheet('color: red')
            self.idInput.setFocus()
            return
        with open('votesData.csv', 'a+', newline='') as votesFile:
            dataReader = csv.reader(votesFile)
            votesFile.seek(0)
            for row in dataReader:
                if row[2] and row[2] == __userInput:
                    self.bottomLabel.show()
                    self.bottomLabel.setText(f'You already voted.')
                    self.bottomLabel.setStyleSheet('color: red')
                    self.idInput.setFocus()
                    return

            votesFile.seek(0,2)
            dataWriter = csv.writer(votesFile)
            dataWriter.writerow([candidiate, datetime.datetime.now(), __userInput])
            self.bottomLabel.setText(f'You voted for {candidiate}')
            self.bottomLabel.move(100,230)
            self.idInput.setText('')
            self.bottomLabel.setStyleSheet('color: green')
            self.bottomLabel.show()
            self.summonVoteMenu()
