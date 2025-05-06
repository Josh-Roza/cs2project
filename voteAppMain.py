from voteAppLogic import *

if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = Logic()
    window.show()
    app.exec()