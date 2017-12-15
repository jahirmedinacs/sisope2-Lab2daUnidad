import sys,threading
from PyQt5 import QtWidgets

import auxiliar as aux
import random

import node as nd
import time

def getRandomList(amount):
    return random.sample(range(2 ** 12), amount)

class Hub(QtWidgets.QWidget):

    def __init__(self):
        super().__init__()

        self._nodeAmount = 0
        self._nodeList = []
        self._nodeId = 0

        self._randomProcessId = getRandomList(100)

        self.init_ui()

    def init_ui(self):

        self.nodeAmountText = QtWidgets.QLabel("Nodos Enrutados\t" + str(self._nodeAmount))

        self.addNodeButton = QtWidgets.QPushButton("Añadir Nodo")

        self.eventRepoterTextEdit = QtWidgets.QTextEdit("Ningun Evento")
        self.eventRepoterTextEdit.setReadOnly(True)

        v_box = QtWidgets.QVBoxLayout()


        ###

        h_box_nodeAmountText = QtWidgets.QHBoxLayout()
        h_box_nodeAmountText.addStretch()
        h_box_nodeAmountText.addWidget(self.nodeAmountText)
        h_box_nodeAmountText.addStretch()
        v_box.addLayout(h_box_nodeAmountText)

        h_box_addNodeButton = QtWidgets.QHBoxLayout()
        h_box_addNodeButton.addStretch()
        h_box_addNodeButton.addWidget(self.addNodeButton)
        h_box_addNodeButton.addStretch()
        v_box.addLayout(h_box_addNodeButton)

        ###

        h_box_eventRepoterTextEdit = QtWidgets.QHBoxLayout()
        h_box_eventRepoterTextEdit.addStretch()
        h_box_eventRepoterTextEdit.addWidget(self.eventRepoterTextEdit)
        h_box_eventRepoterTextEdit.addStretch()
        v_box.addLayout(h_box_eventRepoterTextEdit)

        ###

        self.setLayout(v_box)
        self.setWindowTitle("HUB DE RED")

        self.addNodeButton.clicked.connect(self.createNode)

        self.show()

    def createNode(self):
        print("Create")

        if self._nodeId == 0:
            self.eventRepoterTextEdit.setText("\n*** " + aux.getTime() + " ***\n" +
                                              "Añadido Nodo al sistema, identificador: 0\t\t<NODO 0>")
        else:
            self.eventRepoterTextEdit.setText(self.eventRepoterTextEdit.toPlainText() + "\n*** " +
                                              aux.getTime() + " ***\n" + "Añadido Nodo al sistema, identificador: " +
                                              str(self._nodeId) +"\t\t<NODO " +  str(self._nodeId) + ">")

        aux.autoSlide(self.eventRepoterTextEdit)

        carry = nd.Node(self._nodeId, self)
        carry.setProcessId(self._randomProcessId[self._nodeId])

        self._nodeList.append(carry)

        carry.startVotation()

        self._nodeId += 1

        self.updateNodeAmount()

    def updateNodeAmount(self):
        self._nodeAmount = len(self._nodeList)
        self.nodeAmountText.setText("Nodos Enrutados\t" + str(self._nodeAmount))

    def getNodeList(self):
        return self._nodeList