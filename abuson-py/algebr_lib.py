#! /usr/bin/python3.5 -i
# -*- coding: utf-8 -*-

"""
def despised_IntDivision(D,d,q = 0):
    if (D < d and D != 0):
		r = D
		return q,r
	elif (D == 0):
		return q,0
	elif ( D < 0 and d > 0):
		[x,y] = intDivision(-1*D , d)
		return -1*x , y
	elif ( d < 0 and D > 0):
		[x,y] = intDivision(D , -1*d)
		return -1*x , y
	elif ( d < 0 and D < 0):
		[x,y] = intDivision(-1*D , -1*d)
		return x , y
	else:
		D = D-d
		q = q +1
		q1,r = intDivision(D,d,q)
		return q1,r
"""
from numpy.testing.tests.test_utils import my_cacw

"""
def modularExp(a,k,n,verbose = False):
	t = len(bin(k))
	k_b = bin(k)[2:t]
	t = len(k_b) - 1

	if verbose:
		print ("\nKb=\t",k_b)

	b = 1
	if( k == 0):
		return b

	A = a
	if(k_b[t] == 1):
		b = a

	for i in range(t-1,-1,-1):
		A = (A**2)%n
		if verbose:
			print "\nKb=\t",k_b[i],"\ti =",i
		if (int(k_b[i]) == 1):
			b = (A*b) % n
		if verbose:
			print "\tA :\t" , A , "\tB:\t" , b

	return b
"""

from Crypto.Util import number
import re


def toInt(text):
    output = int(text.encode("hex"), 16)
    return output


def toText(intValue):
    message = re.sub('L', '', hex(intValue)[2:]).decode("hex")
    return message


def intDivision(D, d):
    q = int(D / d)
    r = D - d * q
    return [q, r]


def stdEuclid(m, n, verbose=False):
    if (m > n):
        t = 1
        if (n == 0):
            return m
        else:
            while (n > 0):
                [x, r] = intDivision(m, n)
                m = n
                n = r
                if verbose:
                    print("\n ", t, "ª Iteracion: \tm= ", m, "\tn=", n)
                t = t + 1
            return m
    else:
        return stdEuclid(n, m)


def extEuclid(m, n, verbose=False):
    t = 0
    if (n == 0):
        d = m
        x = 1
        y = 0
        if verbose:
            print("\n", t, "ª Iteracion:\tm=", m, "\tn=", n, "\tx=", x, "\ty=", y)
        t = t + 1
    else:
        x1 = 0
        x2 = 1
        y1 = 1
        y2 = 0

        if verbose:
            print("\n", t, "ª Iteracion:\tm=", m, "\tn=", n, "\tx=", x2, "\ty=", y2)

        while (n > 0):
            t = t + 1
            [q, r] = intDivision(m, n)
            x = x2 - q * x1
            y = y2 - q * y1
            m = n
            n = r
            x2 = x1
            x1 = x
            y2 = y1
            y1 = y

            if verbose:
                print("\n", t, "ª Iteracion:\tm=", m, "\tn=", n, "\tx=", x2, "\ty=", y2)

        d = m
        x = x2
        y = y2

    return [d, x, y, t]


def euclidExp(a, b):
    m = 2 ** a - 1
    n = 2 ** b - 1

    print("\nForma Exponencial:\tm=", m, "\tn=", n)

    [i, x] = stdEuclid(a, b)
    mcdProp = 2 ** i - 1

    print("\nMCD(propiedad):\t", mcdProp)

    [i, x] = stdEuclid(m, n)
    mcdStd = i
    print("\nMCD (forma estandar):\t", mcdStd)

    if (mcdStd == mcdProp):
        print("\nCumple")
    else:
        print("\n:c")


def modularInverse(a, n):
    [D, x, y, t] = extEuclid(a, n)

    d = a * x + n * y

    if (d > 1):
        return [-1, False]
    else:
        if (x < 0):
            i = n - abs(x) % n
        else:
            i = x % n
        return [i, True]


def modularExp(x, e, m):
    X = x
    E = e
    Y = 1
    while E > 0:
        if E % 2 == 0:
            X = (X * X) % m
            E = E//2
        else:
            Y = (X * Y) % m
            E = E - 1
    return Y


def rsaKeyGenerator(nLen, pPrime=0, qPrime=0, eKey=0, verbose=False):
    if pPrime == 0 and qPrime == 0:

        flag = True
        while flag:
            pPrime = number.getPrime(int(nLen / 2))
            qPrime = number.getPrime(int(nLen / 2))
            if pPrime != qPrime:
                flag = False

    nKey = pPrime * qPrime
    phi = (pPrime - 1) * (qPrime - 1)

    phiLen = len(str(bin(phi)[2:])) - 1

    if eKey == 0:
        flag = True
        while flag:

            eKey = number.getRandomRange(0, phi)

            if stdEuclid(eKey, phi) != 1:
                flag = True
            else:
                flag = False

    dKey = modularInverse(eKey, phi)

    if verbose:
        return [[pPrime, qPrime, phi], [nKey, eKey], dKey]

    else:
        return [[nKey, eKey], dKey[0]]


def encryptor(noCypherMessage, nKey, eKey):
    cypherMessage = 0

    cypherMessage = modularExp(noCypherMessage, eKey, nKey)
    return cypherMessage


def decryptor(cypherMessage, nKey, dKey):
    carryValue = modularExp(cypherMessage, dKey, nKey)
    return carryValue


def rsa(debugMessage=False, pPrime=0, qPrime=0, eKey=0, hexOn=True):
    if debugMessage:
        ##
        [[nKey, eKey], dKey] = rsaKeyGenerator(0, pPrime, qPrime, eKey)
        messageOriginal = debugMessage
    ##
    else:
        flag = True
        while flag:
            maxBitSize = input("\nNumero de bits de las Claves:\t")
            try:
                maxBitSize = int(maxBitSize)
                flag = False
            except:
                "\nSolo valores enteros"

        fooString = 2 ** maxBitSize

        maxMessageLength = len(re.sub('L', '', hex(fooString)[2:]).encode("hex"))
        ##
        messageOriginal = input("\nMensaje - max[" + str(maxMessageLength) + "]:\t")

        [[nKey, eKey], dKey] = rsaKeyGenerator(maxBitSize)
    ##
    if hexOn:
        print("Publica - nKey:\n\t\t", str(hex(nKey)).upper(), "\n\n\n")
        print("Publica - eKey:\n\t\t", str(hex(eKey)).upper(), "\n\n\n")
        print("Privada - dKey:\n\t\t", str(hex(dKey)).upper(), "\n\n\n")
    else:
        print("Publica - nKey:\n\t\t", nKey, "\n\n\n")
        print("Publica - eKey:\n\t\t", eKey, "\n\n\n")
        print("Privada - dKey:\n\t\t", dKey, "\n\n\n")

    doString = False
    try:
        integerMessage = int(messageOriginal)
    except:
        integerMessage = toInt(messageOriginal)
        doString = True

    cypher = encryptor(integerMessage, nKey, eKey)
    message = decryptor(cypher, nKey, dKey)

    print("Mensaje Original:\n\t\t", messageOriginal, "\n\n\n")
    if hexOn:
        print("Mensaje Cifrado:\n\t\t", str(hex(cypher)).upper(), "\n\n\n")
    else:
        print("Mensaje Cifrado:\n\t\t", cypher, "\n\n\n")

    if doString:
        message = toText(message)
    else:
        pass

    print("Mensaje Decifrado:\n\t\t", message, "\n\n\n")


import sys,threading
from PyQt5 import QtWidgets


class Window(QtWidgets.QWidget):

    idWindow = ""

    refSocket = None
    isConected = False

    gNumber = 0
    pNumber = 0

    myNumber = []
    myNumberPublic = []
    foreignNumber = []

    preSharedKey = -1
    myMessage = -1
    plainMyMessage = ""
    foreignMessage = -1

    nRSA = -1
    eRSA = -1

    dRSA = -1

    nRSA_foreign = -1
    eRSA_foreign = -1

    rsaKeyLen = -1
    def __init__(self,name_of_window,g,p,n_bit_size):
        super().__init__()

        self.idWindow = name_of_window

        self.gNumber = g
        self.pNumber = p

        self.rsaKeyLen = n_bit_size
        self.rsaStart()

        self.init_ui()

    def rsaStart(self):
        x = rsaKeyGenerator(self.rsaKeyLen)
        self.nRSA = x[0][0]
        self.eRSA = x[0][1]
        self.dRSA = x[1]

    def init_ui(self):

        self.gText = QtWidgets.QLabel("Primo\n" + str(self.gNumber))
        self.pText = QtWidgets.QLabel("Base\n" + str(self.pNumber))

        self.self_valueLineEdit = QtWidgets.QLineEdit("Solo Enteros")
        self.send_self_valueButton = QtWidgets.QPushButton("Publicar")

        self.midText0 = QtWidgets.QLabel("Numero Enviado:")
        self.self_value_publicLabel = QtWidgets.QLabel("No Calculado")

        self.get_other_valueButton = QtWidgets.QPushButton("Recibir Numero Foraneo")
        self.other_valueLabel = QtWidgets.QLabel("Valor Recibido")

        self.verifyButton = QtWidgets.QPushButton("Verificar y Comunicar")
        self.verfiedText = QtWidgets.QLabel("Aun no verificado")

        self.self_messageLineEdit = QtWidgets.QLineEdit("")
        self.send_self_sendMessageButton = QtWidgets.QPushButton("Enviar")
        self.foreignMessageLabel = QtWidgets.QLabel("")

        v_box = QtWidgets.QVBoxLayout()


        ###

        h_box_gText = QtWidgets.QHBoxLayout()
        h_box_gText.addStretch()
        h_box_gText.addWidget(self.gText)
        h_box_gText.addStretch()
        v_box.addLayout(h_box_gText)

        h_box_pText = QtWidgets.QHBoxLayout()
        h_box_pText.addStretch()
        h_box_pText.addWidget(self.pText)
        h_box_pText.addStretch()
        v_box.addLayout(h_box_pText)

        ###

        h_box_self_valueLineEdit = QtWidgets.QHBoxLayout()
        h_box_self_valueLineEdit.addStretch()
        h_box_self_valueLineEdit.addWidget(self.self_valueLineEdit)
        h_box_self_valueLineEdit.addStretch()
        v_box.addLayout(h_box_self_valueLineEdit)

        h_box_send_self_valueButton = QtWidgets.QHBoxLayout()
        h_box_send_self_valueButton.addStretch()
        h_box_send_self_valueButton.addWidget(self.send_self_valueButton)
        h_box_send_self_valueButton.addStretch()
        v_box.addLayout(h_box_send_self_valueButton)

        #

        h_box_midText0 = QtWidgets.QHBoxLayout()
        h_box_midText0.addStretch()
        h_box_midText0.addWidget(self.midText0)
        h_box_midText0.addStretch()
        v_box.addLayout(h_box_midText0)

        h_box_self_value_publicLabel = QtWidgets.QHBoxLayout()
        h_box_self_value_publicLabel.addStretch()
        h_box_self_value_publicLabel.addWidget(self.self_value_publicLabel)
        h_box_self_value_publicLabel.addStretch()
        v_box.addLayout(h_box_self_value_publicLabel)

        #
        """
        h_box_get_other_valueButton = QtWidgets.QHBoxLayout()
        h_box_get_other_valueButton.addStretch()
        h_box_get_other_valueButton.addWidget(self.get_other_valueButton)
        h_box_get_other_valueButton.addStretch()
        v_box.addLayout(h_box_get_other_valueButton)

        h_box_other_valueLabel = QtWidgets.QHBoxLayout()
        h_box_other_valueLabel.addStretch()
        h_box_other_valueLabel.addWidget(self.other_valueLabel)
        h_box_other_valueLabel.addStretch()
        v_box.addLayout(h_box_other_valueLabel)
        """
        ###

        h_box_verifyButton = QtWidgets.QHBoxLayout()
        h_box_verifyButton.addStretch()
        h_box_verifyButton.addWidget(self.verifyButton)
        h_box_verifyButton.addStretch()
        v_box.addLayout(h_box_verifyButton)

        h_box_verfiedText = QtWidgets.QHBoxLayout()
        h_box_verfiedText.addStretch()
        h_box_verfiedText.addWidget(self.verfiedText)
        h_box_verfiedText.addStretch()
        v_box.addLayout(h_box_verfiedText)

        ###

        h_box_self_messageLineEdit = QtWidgets.QHBoxLayout()
        h_box_self_messageLineEdit.addStretch()
        h_box_self_messageLineEdit.addWidget(self.self_messageLineEdit)
        h_box_self_messageLineEdit.addStretch()
        v_box.addLayout(h_box_self_messageLineEdit)

        h_box_send_self_sendMessageButton = QtWidgets.QHBoxLayout()
        h_box_send_self_sendMessageButton.addStretch()
        h_box_send_self_sendMessageButton.addWidget(self.send_self_sendMessageButton)
        h_box_send_self_sendMessageButton.addStretch()
        v_box.addLayout(h_box_send_self_sendMessageButton)

        h_box_foreignMessageLabel = QtWidgets.QHBoxLayout()
        h_box_foreignMessageLabel.addStretch()
        h_box_foreignMessageLabel.addWidget(self.foreignMessageLabel)
        h_box_foreignMessageLabel.addStretch()
        v_box.addLayout(h_box_foreignMessageLabel)

        ###

        self.setLayout(v_box)
        self.setWindowTitle(self.idWindow)

        self.send_self_valueButton.clicked.connect(self.button_click_send)
        #self.get_other_valueButton.clicked.connect(self.button_click_recept)
        self.verifyButton.clicked.connect(self.button_click_verify)
        self.send_self_sendMessageButton.clicked.connect(self.connectAndSend)

        self.show()

    def setMyNumber(self,externalValue):
        self.myNumber = externalValue

    def setMyNumberPublic(self,externalValue):
        self.myNumberPublic = externalValue

    def setForeignNumber(self,externalValue):
        self.foreignNumber = externalValue

    def button_click_send(self):
        try:
            self.myNumber[0] = int(self.self_valueLineEdit.text())
            works = True
        except:
            works = False

        if works and self.myNumber[0]>0:
            self.myNumberPublic[0] = modularExp(self.gNumber,self.myNumber[0],self.pNumber)
            self.self_value_publicLabel.setText(str(self.myNumberPublic[0]))
        else:
            self.self_valueLineEdit.clear()
            self.self_valueLineEdit.insert("Solo Naturales")
    """
    def button_click_recept(self):
        try:
            textToDisplay = str(self.foreignNumber[0])
            works = True
        except:
            works = False

        if works and self.foreignNumber[0] != -1:
            self.other_valueLabel.setText(textToDisplay)
        else:
            self.other_valueLabel.setText("No Disponible")
    """
    def button_click_verify(self):
        if self.foreignNumber[0] < 0 or self.myNumber[0] < 0:
            self.verfiedText.setText("Ningun Valor a Revisar")
        else:
            self.preSharedKey = modularExp(self.foreignNumber[0], self.myNumber[0], self.pNumber)
            self.verfiedText.setText(str(self.preSharedKey))

    def encryptor(self,numberData):
        self.myMessage = encryptor(numberData, self.nRSA_foreign, self.eRSA_foreign)


    def decryptor(self):
        print (self.idWindow + ">>\t\tmensaje foraneo cifrado>>>\t" + str(self.foreignMessage))
        self.foreignMessage = decryptor(self.foreignMessage,self.nRSA,self.dRSA)

    def setForeignMessage(self):
            if self.foreignMessage == -1:
                self.foreignMessageLabel.setText("Ningun Mensaje")
            else:
                self.foreignMessageLabel.setText(str(self.foreignMessage))

    def connectAndSend(self):
        if self.refSocket.comunnicate():
            self.refSocket.crossKeys()
            if self.self_messageLineEdit.text() == "" and not(self.isConected):

                print ("\n\n____________***************____________\n\n" +
                    "ME\n" + self.idWindow + "\nN\t" + str(self.nRSA) + "\ne\t" + str(self.eRSA) + "\nd\t" + str(self.dRSA) + "\n"
                   "HE\n" + "\nN\t" + str(self.nRSA_foreign) + "\ne\t" + str(self.eRSA_foreign) +
                       "\n\n____________***************____________\n\n")

                self.foreignMessageLabel.setText("<<Comunicacion Establecida>>")
                self.isConected = True
            else:
                try:
                    inputText = int(self.self_messageLineEdit.text())
                    if inputText > 0:
                        self.plainMyMessage = self.self_messageLineEdit.text()
                        self.encryptor(inputText)
                        self.refSocket.crossMessage()

                        print(self.idWindow + ">>\t\tmi mensaje\t" + self.plainMyMessage + "\n\t\tmi mensaje cifrado>>\t"
                              + str(self.myMessage) + "\n\t\tmensaje foraneo descifrado>>\t" + str(self.foreignMessage))
                    else:
                        self.self_messageLineEdit.setText("Solo Naturales")
                except:
                    self.plainMyMessage = ""
                    self.myMessage = -1




        else:
            self.foreignMessageLabel.setText("<<Imposible Comunicar>>")



class communicationSocket:

    a_window = None
    b_window = None

    def __init__(self,a_ref,b_ref):
        self.a_window = a_ref
        self.b_window = b_ref

    def comunnicate(self):
        # print ("alice " + str(self.a_window.preSharedKey) + "\tbob " + str(self.b_window.preSharedKey))
        if self.a_window.preSharedKey == -1 or self.b_window.preSharedKey == -1:
            return False
        else:
            return self.a_window.preSharedKey == self.b_window.preSharedKey
    def crossKeys(self):
        self.a_window.nRSA_foreign = self.b_window.nRSA
        self.a_window.eRSA_foreign = self.b_window.eRSA

        self.b_window.nRSA_foreign = self.a_window.nRSA
        self.b_window.eRSA_foreign = self.a_window.eRSA

    def crossMessage(self):
        print("\n\n__________*****______________\n\n")

        if self.b_window.plainMyMessage != "":
            self.a_window.foreignMessage = self.b_window.myMessage
            self.a_window.decryptor()
            self.a_window.setForeignMessage()
        else:
            self.a_window.setForeignMessage()

        if self.a_window.plainMyMessage != "":
            self.b_window.foreignMessage = self.a_window.myMessage
            self.b_window.decryptor()
            self.b_window.setForeignMessage()
        else:
            self.b_window.setForeignMessage()

def integerFactorizer(n,onlyPrimes = False):
    primfac = []
    d = 2
    while d*d <= n:
        while (n % d) == 0:
            primfac.append(d)
            n //= d
        d += 1
    if n > 1:
       primfac.append(n)

    if onlyPrimes:
        primfac = set(primfac)
        primfac = list(primfac)

    return primfac


def diffieHellman(nBitLen,rsa_nBitLen):

    p = number.getPrime(nBitLen)

    phi = p-1

    phiList = integerFactorizer(phi)

    firstExp = phi/phiList[0]

    secondExp = phiList[0]

    maxGvalue = 2**int(nBitLen/2)

    counter = 0
    doit = True
    while doit:
        counter +=1
        isPrimitive = True

        g = number.getRandomRange(0 , maxGvalue)

        isPrimitive *= 1 != modularExp(g,firstExp,p)
        isPrimitive *= 1 != modularExp(g,secondExp,p)

        if isPrimitive:
            doit = False
            print ("\n TRY[" + str(counter) + "] SUCCESS")
        else:
            pass
            print ("\n TRY[" + str(counter) + "] FAIL")



    app = QtWidgets.QApplication(sys.argv)

    a_window = Window("Alice",p,g,rsa_nBitLen)
    a = [-1]
    A = [-1]

    b_window = Window("Bob",p,g,rsa_nBitLen)
    b= [-1]
    B = [-1]

    a_window.setMyNumber(a)
    a_window.setMyNumberPublic(A)
    a_window.setForeignNumber(B)

    b_window.setMyNumber(b)
    b_window.setMyNumberPublic(B)
    b_window.setForeignNumber(A)

    main_socket = communicationSocket(a_window,b_window)
    a_window.refSocket = main_socket
    b_window.refSocket = main_socket

    app.exec_()

diffieHellman(64, 2048)
