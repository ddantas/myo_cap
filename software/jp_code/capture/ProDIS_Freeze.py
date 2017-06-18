# -*- coding: utf-8 -*-
import sys
import serial
#import matplotlib.pyplot as plt
import time
import threading
import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui
import numpy as np

from PyQt4 import QtGui, QtCore

from GUI_ProDIS_Freeze import Ui_MainWindow

ser = serial.Serial('COM3', 115200, timeout=3)  # abre porta serial COM3 com o baud rate de 115200


# Lembrar que o Python tem que ser o do disco C:\ p/ o uso de JP
class Main(QtGui.QMainWindow):
    @property
    def t(self):
        return self.__t

    @property
    def cancela(self):  # flag para sair do loop
        return self.__cancela

    @property
    def contImagem(self):  # contador para as imagens
        return self.__contImagem

    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.initBlock()
        self.__contImagem = 0

        ser.close()  # eh necessario fechar a conexao porque o Serial ja abriu e na funcao enviaSerial abro novamente
        # libera sinais
        QtCore.QObject.connect(self.ui.rbt_f_bs, QtCore.SIGNAL('toggled(bool)'), self.libera_f_bs)
        QtCore.QObject.connect(self.ui.rbt_f_bp, QtCore.SIGNAL('toggled(bool)'), self.libera_f_bp)
        QtCore.QObject.connect(self.ui.rbt_f_lp, QtCore.SIGNAL('toggled(bool)'), self.libera_f_lp)
        QtCore.QObject.connect(self.ui.rbt_f_hp, QtCore.SIGNAL('toggled(bool)'), self.libera_f_hp)

        QtCore.QObject.connect(self.ui.rbt_f_be, QtCore.SIGNAL('toggled(bool)'), self.libera_be)
        QtCore.QObject.connect(self.ui.rbt_f_bu, QtCore.SIGNAL('toggled(bool)'), self.libera_bu)
        QtCore.QObject.connect(self.ui.rbt_f_ch, QtCore.SIGNAL('toggled(bool)'), self.libera_cheb)

        QtCore.QObject.connect(self.ui.rbt_gerador_sim,QtCore.SIGNAL('toggled(bool)'), self.libera_frequencia_sinal)
        QtCore.QObject.connect(self.ui.rbt_gerador_nao, QtCore.SIGNAL('toggled(bool)'), self.bloqueia_frequencia_sinal)

        # Controle de entrada de texto
        QtCore.QObject.connect(self.ui.lineEdit_fc, QtCore.SIGNAL('editingFinished()'), self.validacao)
        QtCore.QObject.connect(self.ui.lineEdit_fc_2, QtCore.SIGNAL('editingFinished()'), self.validacao)
        QtCore.QObject.connect(self.ui.lineEdit_fa, QtCore.SIGNAL('editingFinished()'), self.validacao)
        QtCore.QObject.connect(self.ui.lineEdit_chebrip, QtCore.SIGNAL('editingFinished()'), self.validacao)
        QtCore.QObject.connect(self.ui.lineEdit_ordem, QtCore.SIGNAL('editingFinished()'), self.validacao)
        QtCore.QObject.connect(self.ui.lineEdit_freq_ger, QtCore.SIGNAL('editingFinished()'), self.validacao)

        # Envio pela serial
        QtCore.QObject.connect(self.ui.bt_init_conv, QtCore.SIGNAL('clicked()'), self.enviaSerial)

        # Cancelamento da serial
        self.__t = threading.Thread(target=self.testeCancela)
        self.__t.daemon = True
        self.__cancela = True
        QtCore.QObject.connect(self.ui.bt_stop_conv, QtCore.SIGNAL('clicked()'), self.chamaCancela)


    def initBlock(self):  # Inicia a GUI bloqueando a entrada da frequencia de corte 2, o chebrip, conversao, cancelamneto e a frequencia
        #do gerador de sinal
        self.ui.lineEdit_fc_2.setEnabled(False)
        self.ui.lineEdit_chebrip.setEnabled(False)
        self.ui.bt_init_conv.setEnabled(False)
        self.ui.bt_stop_conv.setEnabled(False)
        self.ui.lineEdit_freq_ger.setEnabled(False)

    def libera_f_bs(
            self):  # Quando o radio button do rejeita faixa eh marcado ou desmarcado, verifica e, ativa ou desativa o mesmo
        if (self.ui.rbt_f_bs.isChecked()):
            self.ui.lineEdit_fc_2.setEnabled(True)
            self.ui.lineEdit_fc_2.setToolTip("Somente Numeros")
            self.ui.bt_init_conv.setEnabled(False)
        else:
            self.ui.lineEdit_fc_2.setEnabled(False)

    def libera_f_bp(
            self):  # Quando o radio button do passa faixa eh marcado ou desmarcado, verifica e, ativa ou desativa o mesmo
        if (self.ui.rbt_f_bp.isChecked()):
            self.ui.lineEdit_fc_2.setEnabled(True)
            self.ui.lineEdit_fc_2.setToolTip("Somente Numeros")
            self.ui.bt_init_conv.setEnabled(False)
        else:
            self.ui.lineEdit_fc_2.setEnabled(False)

    def libera_f_lp(
            self):  # Quando o radio button do passa baixa eh marcado ou desmarcado, verifica e desativa o botao enviar
        if (self.ui.rbt_f_lp.isChecked()):
            self.ui.bt_init_conv.setEnabled(False)

    def libera_f_hp(
            self):  # Quando o radio button do passa alta eh marcado ou desmarcado, verifica e desativa o botao enviar
        if (self.ui.rbt_f_hp.isChecked()):
            self.ui.bt_init_conv.setEnabled(False)

    def libera_cheb(
            self):  # Quando o radio button do chebshev eh marcado ou desmarcado, verifica e, ativa ou desativa o mesmo
        if (self.ui.rbt_f_ch.isChecked()):
            self.ui.lineEdit_chebrip.setEnabled(True)
            self.ui.bt_init_conv.setEnabled(False)
        else:
            self.ui.lineEdit_chebrip.setEnabled(False)

    def libera_be(self):  # Quando o radio button do Bessel eh marcado ou desmarcado, verifica e desativa o botao enviar
        if (self.ui.rbt_f_be.isChecked()):
            self.ui.bt_init_conv.setEnabled(False)

    def libera_bu(self):  # Quando o radio button do Buterworth eh marcado ou desmarcado, verifica e desativa o botao enviar
        if (self.ui.rbt_f_bu.isChecked()):
            self.ui.bt_init_conv.setEnabled(False)

    def libera_frequencia_sinal(self): #Quando o radio button do gerador de sinal eh marcado com sim, ativa o line edit
        if self.ui.rbt_gerador_sim.isChecked():
            self.ui.lineEdit_freq_ger.setEnabled(True)

    def bloqueia_frequencia_sinal(self):  # Quando o radio button do gerador de sinal eh marcado com não, bloqueia o line edit
        if self.ui.rbt_gerador_nao.isChecked():
            self.ui.lineEdit_freq_ger.setEnabled(False)

    #-------------------------------------------------------------------------------------------------------------------
    def validacao(self):
        # declarando o validator de double para o lineEdit
        validator = QtGui.QDoubleValidator()
        # fc
        self.ui.lineEdit_fc.setValidator(validator)
        state = validator.validate(self.ui.lineEdit_fc.text(), 0)[0]  # verificando o estado da entrada do texto
        if state == QtGui.QValidator.Acceptable:
            print("aceitavel")
            self.ui.lineEdit_fc.setStyleSheet("QLineEdit { background-color:}")
            # F2
            if (self.ui.rbt_f_bs.isChecked()) or (self.ui.rbt_f_bp.isChecked()):  # verificando se tem outra frequencia
                self.ui.lineEdit_fc_2.setValidator(validator)
                state_fc2 = validator.validate(self.ui.lineEdit_fc_2.text(), 0)[0]  # verificando o estado da entrada do texto em fc2
                if state_fc2 == QtGui.QValidator.Acceptable:
                    print("aceitavel fc2")
                    self.ui.lineEdit_fc_2.setStyleSheet("QLineEdit { background-color:}")  # cor normal, passou
                    # fa passo 2
                    self.ui.lineEdit_fa.setValidator(validator)
                    state = validator.validate(self.ui.lineEdit_fa.text(), 0)[0]
                    if state == QtGui.QValidator.Acceptable:
                        print("aceital Fa")
                        self.ui.lineEdit_fa.setStyleSheet("QLineEdit { background-color:}")
                        # verificar se o chebrip esta selecionado
                        if (self.ui.rbt_f_ch.isChecked()):
                            self.ui.lineEdit_chebrip.setValidator(validator)
                            state = validator.validate(self.ui.lineEdit_chebrip.text(), 0)[0]
                            if (state == QtGui.QValidator.Acceptable):
                                print("aceitavel valor chebrip")
                                self.ui.lineEdit_chebrip.setStyleSheet("QLineEdit { background-color:}")  # cor normal, passou
                                # ordem
                                self.ui.lineEdit_ordem.setValidator(validator)
                                state = validator.validate(self.ui.lineEdit_ordem.text(), 0)[0]
                                if (state == QtGui.QValidator.Acceptable):
                                    print("aceitavel ordem")
                                    self.ui.lineEdit_ordem.setStyleSheet("QLineEdit { background-color:}")
                                    #Gerador de Sinal
                                    #Verificar se o gerador de sinal esta "SIM"
                                    if self.ui.rbt_gerador_sim.isChecked():
                                        self.ui.lineEdit_freq_ger.setValidator(validator)
                                        state = validator.validate(self.ui.lineEdit_freq_ger.text(),0)[0]
                                        if state == QtGui.QValidator.Acceptable:
                                            self.ui.lineEdit_chebrip.setStyleSheet("QLineEdit { background-color:}")  # cor normal, passou
                                            self.ui.bt_init_conv.setEnabled(True)  # ATIVOU O BOTAO INICIAR
                                    elif self.ui.rbt_gerador_nao.isChecked():
                                        self.ui.bt_init_conv.setEnabled(True)  # ATIVOU O BOTAO INICIAR

                                else:
                                    print(state)
                                    self.ui.lineEdit_ordem.setStyleSheet("QLineEdit { background-color: red }")
                            else:
                                print(state)
                                self.ui.lineEdit_chebrip.setStyleSheet(
                                    "QLineEdit { background-color: red }")  # cor vermelha, errado
                        else:
                            # ordem
                            self.ui.lineEdit_ordem.setValidator(validator)
                            state = validator.validate(self.ui.lineEdit_ordem.text(), 0)[0]
                            if (state == QtGui.QValidator.Acceptable):
                                print("aceitavel ordem")
                                self.ui.lineEdit_ordem.setStyleSheet("QLineEdit { background-color:}")
                                # verificando se algum filtro foi selecionado
                                if (self.ui.rbt_f_be.isChecked()) or (self.ui.rbt_f_bu.isChecked()):
                                    # Gerador de Sinal
                                    # Verificar se o gerador de sinal esta "SIM"
                                    if self.ui.rbt_gerador_sim.isChecked():
                                        self.ui.lineEdit_freq_ger.setValidator(validator)
                                        state = validator.validate(self.ui.lineEdit_freq_ger.text(), 0)[0]
                                        if state == QtGui.QValidator.Acceptable:
                                            self.ui.lineEdit_chebrip.setStyleSheet("QLineEdit { background-color:}")# cor normal, passou
                                            self.ui.bt_init_conv.setEnabled(True)  # ATIVOU O BOTAO INICIAR
                                    elif self.ui.rbt_gerador_nao.isChecked():
                                        self.ui.bt_init_conv.setEnabled(True)  # ATIVOU O BOTAO INICIAR

                            else:
                                print(state)
                                self.ui.lineEdit_ordem.setStyleSheet("QLineEdit { background-color: red }")
                    else:
                        print(state)
                        self.ui.lineEdit_fa.setStyleSheet("QLineEdit { background-color: red }")
                else:
                    print(state_fc2)
                    self.ui.lineEdit_fc_2.setStyleSheet("QLineEdit { background-color: red }")  # cor vermelha, errado
            # fa
            self.ui.lineEdit_fa.setValidator(validator)
            state = validator.validate(self.ui.lineEdit_fa.text(), 0)[0]
            if (state == QtGui.QValidator.Acceptable):
                print("aceitavel Fa")
                self.ui.lineEdit_fa.setStyleSheet("QLineEdit { background-color:}")
                # verificar se o chebrip esta selecionado
                if (self.ui.rbt_f_ch.isChecked()):
                    self.ui.lineEdit_chebrip.setValidator(validator)
                    state = validator.validate(self.ui.lineEdit_chebrip.text(), 0)[0]
                    if (state == QtGui.QValidator.Acceptable):
                        print("aceitavel valor chebrip")
                        self.ui.lineEdit_chebrip.setStyleSheet("QLineEdit { background-color:}")  # cor normal, passou
                        # ordem
                        self.ui.lineEdit_ordem.setValidator(validator)
                        state = validator.validate(self.ui.lineEdit_ordem.text(), 0)[0]
                        if (state == QtGui.QValidator.Acceptable):
                            print("aceitavel ordem")
                            self.ui.lineEdit_ordem.setStyleSheet("QLineEdit { background-color:}")
                            if (self.ui.rbt_f_lp.isChecked() or self.ui.rbt_f_hp.isChecked()):
                                # Gerador de Sinal
                                # Verificar se o gerador de sinal esta "SIM"
                                if self.ui.rbt_gerador_sim.isChecked():
                                    self.ui.lineEdit_freq_ger.setValidator(validator)
                                    state = validator.validate(self.ui.lineEdit_freq_ger.text(), 0)[0]
                                    if state == QtGui.QValidator.Acceptable:
                                        self.ui.lineEdit_chebrip.setStyleSheet("QLineEdit { background-color:}")  # cor normal, passou
                                        self.ui.bt_init_conv.setEnabled(True)  # ATIVOU O BOTAO INICIAR
                                elif self.ui.rbt_gerador_nao.isChecked():
                                    self.ui.bt_init_conv.setEnabled(True)  # ATIVOU O BOTAO INICIAR
                        else:
                            print(state)
                            self.ui.lineEdit_ordem.setStyleSheet("QLineEdit { background-color: red }")
                    else:
                        print(state)
                        self.ui.lineEdit_chebrip.setStyleSheet("QLineEdit { background-color: red }")  # cor vermelha, errado
                else:
                    # ordem
                    self.ui.lineEdit_ordem.setValidator(validator)
                    state = validator.validate(self.ui.lineEdit_ordem.text(), 0)[0]
                    if (state == QtGui.QValidator.Acceptable):
                        print("aceitavel ordem")
                        self.ui.lineEdit_ordem.setStyleSheet("QLineEdit { background-color:}")
                        if (self.ui.rbt_f_be.isChecked()) or (self.ui.rbt_f_bu.isChecked()):
                            if (self.ui.rbt_f_lp.isChecked() or self.ui.rbt_f_hp.isChecked()):
                                # Gerador de Sinal
                                # Verificar se o gerador de sinal esta "SIM"
                                if self.ui.rbt_gerador_sim.isChecked():
                                    self.ui.lineEdit_freq_ger.setValidator(validator)
                                    state = validator.validate(self.ui.lineEdit_freq_ger.text(), 0)[0]
                                    if state == QtGui.QValidator.Acceptable:
                                        self.ui.lineEdit_chebrip.setStyleSheet("QLineEdit { background-color:}")  # cor normal, passou
                                        self.ui.bt_init_conv.setEnabled(True)  # ATIVOU O BOTAO INICIAR
                                elif self.ui.rbt_gerador_nao.isChecked():
                                    self.ui.bt_init_conv.setEnabled(True)  # ATIVOU O BOTAO INICIAR
                    else:
                        print(state)
                        self.ui.lineEdit_ordem.setStyleSheet("QLineEdit { background-color: red }")
            else:
                print(state)
                self.ui.lineEdit_fa.setStyleSheet("QLineEdit { background-color: red }")
        else:
            print(state)
            self.ui.lineEdit_fc.setStyleSheet("QLineEdit { background-color: yellow }")

    #------------------------------------------------------------------------------------------------------------------
    def enviaSerial(self):  # Realizando o condicionamento para enviar os dados via serial
        self.amostragem = float(self.ui.lineEdit_fa.text())
        print(self.amostragem)
        # adicionando o filtro
        if (self.ui.rbt_f_be.isChecked()):
            filtro = "be-"
        elif (self.ui.rbt_f_bu.isChecked()):
            filtro = "bu-"
        elif (self.ui.rbt_f_ch.isChecked()):
            filtro = "ch-"
            valorCheb = self.ui.lineEdit_chebrip.text()
            # filtro = filtro + valorCheb + "-"
        # adicionando a resposta em frequencia
        if (self.ui.rbt_f_lp.isChecked()):
            filtro = filtro + "lp-"
        elif (self.ui.rbt_f_hp.isChecked()):
            filtro = filtro + "hp-"
        elif (self.ui.rbt_f_bs.isChecked()):
            filtro = filtro + "bs-"
        elif (self.ui.rbt_f_bp.isChecked()):
            filtro = filtro + "bp-"
        # adicionando a ordem desejada
        ordemFiltro = self.ui.lineEdit_ordem.text()
        filtro = filtro + ordemFiltro
        if (self.ui.rbt_f_ch.isChecked()):
            filtro = filtro + "r" + valorCheb
        fcorte = float(self.ui.lineEdit_fc.text())
        alpha = fcorte / self.amostragem
        print("O valor de alpha eh ")
        filtro = filtro + "a" + (str(alpha))  # simboliza o inicio de alpha1
        print(filtro)
        if ((self.ui.rbt_f_bs.isChecked()) or (self.ui.rbt_f_bp.isChecked())):  # verificando se tem outra frequencia
            fcorte2 = float(self.ui.lineEdit_fc_2.text())
            alpha2 = str(fcorte2 / self.amostragem)
            filtro = filtro + "t" + alpha2
            print(filtro)
        #Pegando o valor da frequencia desejada
        if self.ui.rbt_gerador_sim.isChecked():
            self.frequencia_gerador = self.ui.lineEdit_freq_ger.text()
        self.comunicaSerial(filtro)

    #-------------------------------------------------------------------------------------------------------------------
    # abrindo a porta serial e enviando o filtro desejado
    def comunicaSerial(self, valorfiltro):
        print("Enviando o filtro a placa")
        valorfiltro = valorfiltro + "z" + "\n"
        ser.open()

        #Enviando a frequencia
        if self.ui.rbt_gerador_sim.isChecked():
            frequencia_desejada = "G" + self.frequencia_gerador
            envia_frequencia = bytes(frequencia_desejada)
            ser.write(envia_frequencia)
            while ser.inWaiting() == 0:
                pass
            uart = ser.readline()
            while uart != 'G\r\n':
                print("uart eh:")
                print(uart)
                uart = ser.readline()
            time.sleep(1)
        ser.flushOutput()
        time.sleep(2)

        #enviando a amostragem
        self.amostragem_envio = "K" + str(self.amostragem)
        self.amostragem_envio = bytes(self.amostragem_envio)
        ser.write(self.amostragem_envio)
        print("enviei a amostragem")
        while ser.inWaiting() == 0:
            pass
        uart = ser.readline()
        while uart != 'K\r\n':
            print("uart eh:")
            print(uart)
            uart = ser.readline()
        time.sleep(1)
        ser.flushOutput()
        print("recebi k")
        ser.flushInput()

        #----------------------------------------
        parte1, parte2 = valorfiltro.split('a')
        parte1 = parte1 + "a"
        if ((self.ui.rbt_f_hp.isChecked()) or (self.ui.rbt_f_lp.isChecked())):
            b = bytes(parte1)
            c = bytes(parte2)
            ser.write(b)
            while ser.inWaiting() == 0:
                pass
            uart = ser.readline()
            while uart != 'a\r\n':
                print("uart eh:")
                print(uart)
                uart = ser.readline()
            ser.flushOutput()
            ser.write(c)
        elif ((self.ui.rbt_f_bs.isChecked()) or (self.ui.rbt_f_bp.isChecked())):
            parte2, parte3 = parte2.split('t')
            parte2 = parte2 + "t"
            b = bytes(parte1)
            c = bytes(parte2)
            d = bytes(parte3)
            ser.write(b)
            print("Enviei b:")
            print(b)
            while ser.inWaiting() == 0:
                pass
            uart = ser.readline()
            print("uart fora eh:")
            print(uart)
            while uart != 'a\r\n':
                print("uart eh:")
                print(uart)
                uart = ser.readline()
            ser.flushOutput()
            ser.write(c)
            print(" Enviei c:")
            print(c)
            while ser.inWaiting() == 0:
                pass
            uart = ser.readline()
            print("uart fora eh:")
            print(uart)
            while uart != 'b\r\n':
                print("uart eh:")
                print(uart)
                uart = ser.readline()
            ser.flushOutput()
            ser.write(d)
        self.ui.bt_init_conv.setEnabled(False)
        self.ui.bt_stop_conv.setEnabled(True)

        ser.flushOutput()
        print("antes tinha na serial: %d\n", ser.inWaiting())
        ser.flushInput()
        time.sleep(2)
        print("depis do flush tinha na serial: %d\n", ser.inWaiting())

        self.armazenamento = []  # armazenar os valores recebidos
        ser.flushInput()

        ##--------------------------------------------------
        pg.setConfigOption('background', 'w')
        pg.setConfigOption('foreground', 'k')

        self.win = pg.GraphicsWindow()
        self.win.setWindowTitle('ProDIS')

        self.stringaxisx = pg.AxisItem(orientation='bottom')
        self.stringaxisy = pg.AxisItem(orientation='left')
        self.stringaxisx.setLabel('Número de Pontos')
        self.stringaxisy.setLabel('Tensão', 'V')
        self.p1 = self.win.addPlot(axisItems={'left': self.stringaxisy, 'bottom': self.stringaxisx})
        #Se tirar esse setXRange e esse setYRange, fica automatica a escala
        self.p1.setXRange(0,1000)
        self.p1.setYRange(0,3)

        # global data1, curve1
        self.tamanho_vetor = 1000
        self.data1 = np.empty(self.tamanho_vetor)
        self.data1[:] = None #Prenchendo o vetor com NULL
        self.curve1 = self.p1.plot(self.data1)

        self.ptr1 = 0

        ##--------------------------------------------------
        self.timer = pg.QtCore.QTimer()
        self.timer.timeout.connect(self.update)
        self.timer.start(0)

    def update(self):

        self.ptr1 += 1
        #self.data1[:-1] = self.data1[1:]  # shift data in the array one sample left

        while (ser.inWaiting() == 0):
            pass
        data = float(ser.readline())
        ##atenção multiplicaç~]ao duplicada com o firmware tirar
        #data = data * 0.0008
        print(data)
        self.armazenamento.append(str(data) + ",")
        if self.ptr1%self.tamanho_vetor ==0:
            self.p1.clear()
            self.curve1 = self.p1.plot(self.data1, pen='k')
            self.data1[:] = None
        self.data1[self.ptr1%self.tamanho_vetor] = data
        if self.ptr1%10 == 0:
            self.curve1.setData(self.data1, pen=pg.mkPen('k', width=3))
        #self.curve1.setPos(self.ptr1, 0)

    #-------------------------------------------------------------------------------------------------------------------
    # Cancelamento da comunicacao serial
    def cancelaSerial(self):
        self.__contImagem = self.__contImagem + 1
        self.caminhoArmazenamento= 'D:\Mestrado\Experimento\GUI\Imagens GUI\Valores'  # local onde imagem vai ser armazenada
        self.caminhoArmazenamento = self.caminhoArmazenamento + str(self.__contImagem) + '.txt'
        arq = open(self.caminhoArmazenamento, 'w')
        arq.writelines(self.armazenamento)  # escrevendo os valores recebidos
        arq.close()
        # Desabilitando os botões init e stop
        self.ui.bt_init_conv.setEnabled(False)
        self.ui.bt_stop_conv.setEnabled(False)
        # limpando os campos de entrada de texto
        self.ui.lineEdit_fc.selectAll()
        self.ui.lineEdit_fc.del_()
        if (self.ui.rbt_f_bs.isChecked()) or (self.ui.rbt_f_bp.isChecked()):
            self.ui.lineEdit_fc_2.selectAll()
            self.ui.lineEdit_fc_2.del_()
        self.ui.lineEdit_fa.selectAll()
        self.ui.lineEdit_fa.del_()
        if self.ui.rbt_f_ch.isChecked():
            self.ui.lineEdit_chebrip.selectAll()
            self.ui.lineEdit_chebrip.del_()
        self.ui.lineEdit_ordem.selectAll()
        self.ui.lineEdit_ordem.del_()
        # Finalizando a comunicacao
        b = bytes("FIM\n")  # Convertendo para bytes para ser enviado serialmente
        ser.write(b)
        print("FIM")
        time.sleep(1)  # delay
        ser.close()


    def chamaCancela(self):
        self.__t.run()
        self.__t = threading.Thread(target=self.testeCancela)
        self.__t.daemon = True
        self.timer.stop()

    def testeCancela(self):
        self.__cancela = False
        self.cancelaSerial()

app = QtGui.QApplication(sys.argv)
programa = Main()
programa.show()
sys.exit(app.exec_())

