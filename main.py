import random
import string
import sys

from PyQt6.QtWidgets import QDialog, QApplication

from layout import Ui_Dialog


class MyForm(QDialog):

    def __init__(self):
        super().__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.ui.generate.clicked.connect(self.generate)
        self.ui.easter.clicked.connect(self.easterClicked)
        self.ui.password.textChanged.connect(self.passStrength)
        # zasobnik znakow
        self.smallChars = [l for l in string.ascii_lowercase]
        self.capitalChars = [l for l in string.ascii_uppercase]
        self.numbers = [str(i) for i in range(0, 10)]
        self.specialChars = [l for l in string.punctuation]

    def generate(self):
        length = self.ui.passwordLength.text()
        type = self.ui.passwordType.currentText()
        pasword = ''
        if type == 'Pin':
            for i in range(int(length)):
                pasword += str(random.randint(0, 9))
        elif self.ui.word.isChecked():
            words = self.readDict('odm.txt')
            while len(pasword) < int(length):
                pasword += random.choice(words)
        else:
            elements = [self.smallChars]
            if self.ui.specialChar.isChecked():
                elements.append(self.specialChars)
            if self.ui.numbers.isChecked():
                elements.append(self.numbers)
            if self.ui.capitalChars.isChecked():
                elements.append(self.capitalChars)

            for i in range(int(length)):
                type = random.randint(0, len(elements) - 1)
                pasword += elements[type][random.randint(0, len(elements[type]) - 1)]

            if self.ui.easter.isChecked() and len(pasword) >= 5:
                max_index = len(pasword) - 6
                start_index = random.randint(0, max_index)
                new_pasword = ''
                easter = 'zając'
                for i in range(len(pasword)):
                    if start_index <= i < start_index + 5:
                        new_pasword += easter[i - start_index]
                    else:
                        new_pasword += pasword[i]
                pasword = new_pasword

        self.ui.genertedPassword.setText(pasword)

    def check(self, password, list):
        for i in password:
            if i in list:
                return True
        return False

    def passStrength(self):
        password = self.ui.password.text()
        if (len(password) > 3):
            stregth = [0, 20, 40, 60, 80, 100]
            howGood = 0
            if self.check(password, self.smallChars):
                howGood += 1
            if self.check(password, self.capitalChars):
                howGood += 1
            if self.check(password, self.specialChars):
                howGood += 1
            if self.check(password, self.numbers):
                howGood += 1
            if len(password) > 8:
                howGood += 10
            if howGood > 10:
                value = stregth[howGood - 9]
            elif howGood < 10 and howGood > 0:
                value = stregth[howGood - 1]
            else:
                self.ui.passwordPower.setValue(0)
                return
            self.ui.passwordPower.setValue(value)
        else:
            self.ui.passwordPower.setValue(0)

    def readDict(self, path):
        words = []
        with open(path, 'r', encoding='utf-8') as file:
            lines = file.readlines()
            for line in lines:
                line = line.split(',')[0]
                line = line.replace('\n', '')
                if len(line) > 2 and line.find(' ') == -1:
                    words.append(line)
        return words

    def easterClicked(self):
        if self.ui.easter.isChecked():
            self.ui.numbers.setChecked(False)
            self.ui.capitalChars.setChecked(False)
            self.ui.specialChar.setChecked(False)
            self.ui.word.setChecked(False)
            self.ui.numbers.setDisabled(True)
            self.ui.capitalChars.setDisabled(True)
            self.ui.specialChar.setDisabled(True)
            self.ui.word.setDisabled(True)
        else:
            self.ui.numbers.setDisabled(False)
            self.ui.capitalChars.setDisabled(False)
            self.ui.specialChar.setDisabled(False)
            self.ui.word.setDisabled(False)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    form = MyForm()
    form.show()

    sys.exit(app.exec())
