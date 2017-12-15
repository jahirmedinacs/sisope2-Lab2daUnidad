import sys,threading
from PyQt5 import QtWidgets

import auxiliar as aux
import hub as hb


class Node(QtWidgets.QWidget):

    _blocked = False
    _processId = 0
    _nodeId = 0
    _adminId = 0
    _iAdmin = False

    def __init__(self, nodeid, refHub):
        super().__init__()

        self._nodeId = nodeid
        self._hub = refHub

        self._adminId = 0
        self._iAdmin = False

        self._highProcessIdNodesRef = []

        self.init_ui()

    def init_ui(self):

        self.nodeIDText = QtWidgets.QLabel("Nodo\t" + str(self._nodeId))
        self.processIdText = QtWidgets.QLabel("Id de Proceso\t" + str(self._processId))

        self.blockedText = QtWidgets.QLabel("Estado:\t" + "Desbloqueado")
        self.blockButton = QtWidgets.QPushButton("Bloquear")

        self.adminStateTest = QtWidgets.QLabel("Activo")
        self.pledgeAdminButton = QtWidgets.QPushButton("Solicitar Administrador")
        self.eventRepoterTextEdit = QtWidgets.QTextEdit("Ningun Evento")

        v_box = QtWidgets.QVBoxLayout()


        ###

        h_box_nodeIDText = QtWidgets.QHBoxLayout()
        h_box_nodeIDText.addStretch()
        h_box_nodeIDText.addWidget(self.nodeIDText)
        h_box_nodeIDText.addStretch()
        v_box.addLayout(h_box_nodeIDText)

        h_box_processIdText = QtWidgets.QHBoxLayout()
        h_box_processIdText.addStretch()
        h_box_processIdText.addWidget(self.processIdText)
        h_box_processIdText.addStretch()
        v_box.addLayout(h_box_processIdText)

        ###

        h_box_blockedText = QtWidgets.QHBoxLayout()
        h_box_blockedText.addStretch()
        h_box_blockedText.addWidget(self.blockedText)
        h_box_blockedText.addStretch()
        v_box.addLayout(h_box_blockedText)

        h_box_blockButton = QtWidgets.QHBoxLayout()
        h_box_blockButton.addStretch()
        h_box_blockButton.addWidget(self.blockButton)
        h_box_blockButton.addStretch()
        v_box.addLayout(h_box_blockButton)

        #

        h_box_adminStateTest = QtWidgets.QHBoxLayout()
        h_box_adminStateTest.addStretch()
        h_box_adminStateTest.addWidget(self.adminStateTest)
        h_box_adminStateTest.addStretch()
        v_box.addLayout(h_box_adminStateTest)

        h_box_pledgeAdminButton = QtWidgets.QHBoxLayout()
        h_box_pledgeAdminButton.addStretch()
        h_box_pledgeAdminButton.addWidget(self.pledgeAdminButton)
        h_box_pledgeAdminButton.addStretch()
        v_box.addLayout(h_box_pledgeAdminButton)

        ###

        h_box_eventRepoterTextEdit = QtWidgets.QHBoxLayout()
        h_box_eventRepoterTextEdit.addStretch()
        h_box_eventRepoterTextEdit.addWidget(self.eventRepoterTextEdit)
        h_box_eventRepoterTextEdit.addStretch()
        v_box.addLayout(h_box_eventRepoterTextEdit)

        ###

        self.setLayout(v_box)
        self.setWindowTitle("NODO\t" + str(self._nodeId))

        self.blockButton.clicked.connect(self.blockEvent)
        self.pledgeAdminButton.clicked.connect(self.pledgeAdmin)

        self.show()

    def setProcessId(self, id):
        self._processId = id
        self.updateProcessId()

    def getProcessId(self):
        return self._processId

    def updateProcessId(self):
        self.processIdText.setText("Id de Proceso\t" + str(self._processId))

    def blockEvent(self):
        if self._blocked == False:
            self.blockButton.setText("Desbloquear")
            self.blockedText.setText("Estado:\t" + "Bloqueado")
            self._blocked = True
            self.pushMessage("Nodo Bloqueado")
        else:
            self.blockButton.setText("Bloquear")
            self.blockedText.setText("Estado:\t" + "Desbloqueado")
            self._blocked = False
            self.pushMessage("Nodo Desbloqueado")

            if self._iAdmin:
                self.pushMessage("Ex-Administrador Recuperado")
                self.startVotation()
            else:
                pass

    def notAdmin(self):
        self._iAdmin = False

    def getState(self):
        return not self._blocked

    def setAdmin(self, id):
        self._adminId = id

    def startVotation(self):

        self._highProcessIdNodesRef = []

        self.pushMessage("Iniciando Votacion")

        self.pushMessage("Recopilando Nodos con indices mayores")

        index = 0
        for ref in self._hub.getNodeList():
            if ref.getProcessId() > self._processId:
                self._highProcessIdNodesRef.append(index)
                print(index)
            index += 1


        mostHigh = self._processId
        mostHighId = 0

        atleastone = 0

        for i in self._highProcessIdNodesRef:
            if self._hub.getNodeList()[i].getState():
                if self._hub.getNodeList()[i].getProcessId() > mostHigh:
                    mostHigh = self._hub.getNodeList()[i].getProcessId()
                    print(mostHigh)
                    mostHighId = i
                atleastone += 1
            else:
                pass

        self.pushMessage("Verificando Disponibilidad")

        if atleastone > 0:
            self.pushMessage("Se encontro un posible administrador, pasando votacion")
            self._iAdmin = False
            self._hub.getNodeList()[mostHighId].startVotation()
        else:
            self.pushMessage("No se encontro un posible adminsitrador, asumiendo administracion")
            self._iAdmin = True
            self._adminId = self._nodeId
            self.populateAdmin()

    def populateAdmin(self):
        for ref in self._hub.getNodeList():
            ref.setAdmin(self._adminId)
            if ref.getState():
                ref.notAdmin()
            else:
                pass
            ref.pushMessage("Aceptando nuevo administrador:\t\t NODO " + str(self._adminId))

    def pushMessage(self, newMessage):
        if self._blocked:
            pass
        else:
            self.eventRepoterTextEdit.setText(self.eventRepoterTextEdit.toPlainText() +
                                              "\n*** " + aux.getTime() + " ***\n" + newMessage + "\n")
            aux.autoSlide(self.eventRepoterTextEdit)

    def doAdminStuff(self):

        if self._hub.getNodeList()[self._adminId].getState():
            return True
        else:
            return False

    def pledgeAdmin(self):
        if self._blocked:
            pass
        else:
            if self._iAdmin:
                self.pushMessage("Administrador - No se puede solicitar procedimientos a si mismo")
            else:
                if self.doAdminStuff():
                    self.pushMessage("Administrador - Se realizo el procedimiento Solicitado")
                else:
                    self.pushMessage("Detectado: Administrador No Disponible")
                    self.startVotation()