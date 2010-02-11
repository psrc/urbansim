import sys

from PyQt4.QtCore import *
from PyQt4.QtGui import *

from ui_step1 import Ui_wizardStep1Dialog

class WizardDialog(QWizard):
    def __init__(self, parent=None):
        super(WizardStep1Dialog, self).__init__(parent)
        
        step1Page = QWizardPage()
        label = QLabel("Page 1")

        layout = QVBoxLayout()
        layout.addWidget(label)
        self.setLayout(layout)
        




if __name__ == '__main__':
    app = QApplication(sys.argv)
    dialog = WizardStep1Dialog()
    dialog.show()
    app.exec_()
