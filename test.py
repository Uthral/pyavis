from PySide2 import QtWidgets

app = QtWidgets.QApplication([])
window = QtWidgets.QWidget()
layout = QtWidgets.QVBoxLayout()
layout.addWidget(QtWidgets.QPushButton('Top'))
layout.addWidget(QtWidgets.QPushButton('Bottom'))
window.setLayout(layout)
window.show()
app.exec_()