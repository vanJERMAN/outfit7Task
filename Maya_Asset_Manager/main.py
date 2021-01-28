# nisem natanko razumel, kaj bi mogli določeni gumbi delat, zato sem funkcionalnost naredil
# tako kot je meni ustrezalo, kljub temu da slednja (funkcionalnost) ni bila zahtevana.
# Upam da ne bo prišlo do nobenih odstopanj v aplikaciji, kajti jaz sem svojo delal na macOs-u, medtem
# ko Vaša iz slike sodeč je na Windows-ih

import sys
from PySide2.QtWidgets import *
from PySide2.QtGui import QIcon
from pathlib import Path

# ustvarimo liste itemov, da jih spodaj vnesemo v tabele
tasks = list(map(lambda x: f"task_{x}", range(0, 20)))
files = list(map(lambda x: f"file1_00{x}.ma", range(0, 12)))

class Main(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Maya AssetManager")
        self.setGeometry(150, 60, 800, 550)
        self.UI()
        self.show()

    def UI(self):
        self.mainDesign()
        self.layouts()


    def mainDesign(self):
        # leva lista
        self.taskList = QListWidget()
        for x in range(0, len(tasks)):
            self.taskListItem = QListWidgetItem(tasks[x])
            self.taskListItem.setIcon(QIcon("icons/file_ikonca.png"))
            self.taskList.addItem(self.taskListItem)
        self.taskList.itemClicked.connect(self.taskSelectedItem)

        # desna lista
        self.fileList = QListWidget()
        for x in range(0, len(files)):
            self.fileListItem = QListWidgetItem(files[x])
            self.fileListItem.setIcon(QIcon("icons/photo_ikonca.png"))
            self.fileList.addItem(self.fileListItem)
        self.fileList.itemDoubleClicked.connect(self.publish)

        # ostali gumbi, labeli ter dropdown menuji
        self.btnNewTask = QPushButton("New task")
        self.btnNewTask.clicked.connect(self.newTask)
        self.btnPublishFile = QPushButton("Publish file")
        self.btnPublishFile.clicked.connect(self.publish)
        self.projectLabel = QLabel("Project:")
        self.categoryLabel = QLabel("Category:")
        self.projectDropdown = QComboBox()
        self.projectDropdown.addItem("Project 2")
        self.projectDropdown.activated.connect(self.projectItemClicked)
        self.categoryDropdown = QComboBox()
        self.categoryDropdown.addItem("Category 7")
        self.categoryDropdown.activated.connect(self.categoryItemClicked)
        self.btnAddProject = QPushButton("+")
        self.btnAddProject.setFixedWidth(35)
        self.btnAddProject.clicked.connect(self.addProject)
        self.btnAddCategory = QPushButton("+")
        self.btnAddCategory.setFixedWidth(35)
        self.btnAddCategory.clicked.connect(self.addCategory)

    def layouts(self):
        # da je responsive, torej ko spreminjamo velikost okna, sem ustvaril mainLayout, kateri je
        # horizontalno usmerjen, v njega sem dal leftMainLayout in rightMainLayout, oba sta vertikalno
        # usmerjena... v leftMainLayout sem vstavil leftBottomLayout in leftTopLayout, pravtako sta oba
        # vertikalno usmerjena... v leftTopLayout-u pa je topGridLayout, kateri vsebuje Project label,
        # dropdown menu, in add "+" button, ter Category label, dropdown menu ter add "+" button
        # spodaj dodam tudi spacing v grid layout, tako da je bolj vizualno podobno Vaši aplikaciji
        ############## LAYOUTS #############
        self.mainLayout = QHBoxLayout()
        self.leftMainLayout = QVBoxLayout()
        self.rightMainLayout = QVBoxLayout()
        self.leftBottomLayout = QVBoxLayout()
        self.leftTopLayout = QVBoxLayout()
        self.topGridLayout = QGridLayout()
        self.topGridLayout.setSpacing(1)
        ############# ADDING CHILD LAYOUTS TO MAIN LAYOUTS ##############
        self.leftMainLayout.addLayout(self.leftTopLayout)
        self.leftMainLayout.addLayout(self.leftBottomLayout)
        self.mainLayout.addLayout(self.leftMainLayout, 33)
        self.mainLayout.addLayout(self.rightMainLayout, 66)
        self.leftTopLayout.addLayout(self.topGridLayout)
        ############# ADDING WIDGETS TO LAYOUTS #############
        self.leftBottomLayout.addWidget(self.taskList)
        self.leftBottomLayout.addWidget(self.btnNewTask)
        self.rightMainLayout.addWidget(self.fileList)
        self.rightMainLayout.addWidget(self.btnPublishFile)
        self.topGridLayout.addWidget(self.projectLabel, 0, 0)
        self.topGridLayout.addWidget(self.projectDropdown, 0, 1, 1, 2)
        self.topGridLayout.addWidget(self.btnAddProject, 0, 3)
        self.topGridLayout.addWidget(self.categoryLabel, 1, 0)
        self.topGridLayout.addWidget(self.categoryDropdown, 1, 1, 1, 2)
        self.topGridLayout.addWidget(self.btnAddCategory, 1, 3)
        self.topGridLayout.verticalSpacing()
        self.topGridLayout.verticalSpacing()
        ############# SETTING MAIN WINDOW LAYOUT ################
        self.setLayout(self.mainLayout)

    # če klikneš na "+" gumb od "Project:", se sproži ta funkcija, katera odpre QFileDialog...
    # ta ima opcijo za .ma file extension, da išče oz. All Files..
    # izbran item doda v dropdown menu od "Project:"
    def addProject(self):
        url = QFileDialog.getOpenFileName(self, "Add project", "", "All files(*);; *ma")
        fileUrl = url[0]
        try:
            path = Path(fileUrl)
            self.projectDropdown.addItem(path.name)
        except FileNotFoundError:
            print("No file was selected")

    # isti princip, samo da je za "Category:" in ne "Project:", kot je zgoraj v addProject funkciji
    def addCategory(self):
        url = QFileDialog.getOpenFileName(self, "Add category", "", "All files(*);; *ma")
        fileUrl = url[0]
        try:
            path = Path(fileUrl)
            self.categoryDropdown.addItem(path.name)
        except FileNotFoundError:
            print("No file was selected")

    # isto kot zgornji dve, samo da tukaj lahko izbereš samo folder (directory) in ne file-a kot v
    # zgornjih dveh funkcijah...
    # čeprav po logiki sodeč v vaši aplikaciji se ne izbira folder, sodeč po ikonci...
    def newTask(self):
        url = QFileDialog.getExistingDirectory(self, "New task", "")
        try:
            path = Path(url)
            self.taskListItem = QListWidgetItem(path.name)
            self.taskListItem.setIcon(QIcon("icons/file_ikonca.png"))
            self.taskList.addItem(self.taskListItem)
        except FileNotFoundError:
            print("No file was selected")

    # ko na levi strani izbereš task, se sproži QMessageBox in napiše da si izbral specifičen task...
    def taskSelectedItem(self):
        mbox = QMessageBox.information(self, "Select task", f"You've selected '{self.taskList.currentItem().text()}' task")

    # ista zgodba je tukai, če izbereš v dropdown menuju od "Project:"
    def projectItemClicked(self):
        mbox = QMessageBox.information(self, "Project selected", f"You've selected '{self.projectDropdown.currentText()}' project")

    # pa ista stvar za "Category:"
    def categoryItemClicked(self):
        mbox = QMessageBox.information(self, "Category selected", f"You've selected '{self.categoryDropdown.currentText()}' category")

    # in isto za "Publish file" gumb, samo da kle še prej vpraša če res želiš uploadat file...
    # če izbereš Yes, ti vrže info message box, v nasprotnem primeru, če izbereš No, ne naredi nič
    # publish se lahko sproži tudi v primeru double clicka na item v listi in ne samo z klikom publish gumba
    def publish(self):
        mbox = QMessageBox.question(self, "Publish?", f"Are you sure you want to publish '{self.fileList.currentItem().text()}' file", QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
        if mbox == QMessageBox.Yes:
            QMessageBox.information(self, "Published!", f"You've successfully published '{self.fileList.currentItem().text()}' file")



def main():
    APP=QApplication(sys.argv)
    window=Main()
    sys.exit(APP.exec_())

if __name__ == "__main__":
    main()