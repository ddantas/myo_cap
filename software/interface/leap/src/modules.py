from PyQt5 import QtTest
from datetime import datetime
import pygame 
from pygame import *
import threading 

import converter

gameDisplay = 0
linesEmg = []

def keyCapture():
	
	global gameDisplay

	logend = open('../routine/log.txt','a')
	now = datetime.now()
	nowS = str(now)
	date = str(nowS[0:19])
	logend.write("NOVA ROTINA -- "+str(date)+"\n\n")

	dt = 0

	#logboard = open('../../data/2018-05-04_14-39-15.log','r')
	#linesEmg = logboard.read().splitlines()

	white = (255,255,255)
	black = (0,0,0)

	old_k_delay, old_k_interval = pygame.key.get_repeat()	
	pygame.key.set_repeat (500, 30)
	i = 0
	p = 8
	gameExit = False

	try:
		while not gameExit:
			for event in pygame.event.get():	
			

				logend = open('../routine/log.txt','a')
		    		logend.write(str(dt)+";")					
			
				if event.type == pygame.QUIT:
					gameExit = True

				if pygame.key.get_pressed()[pygame.K_SPACE] != 0 :
					logend.write("100 ;")
					pygame.draw.rect(gameDisplay, black, [100,600,20,100])	
				else :
					logend.write(" 0 ;")
					pygame.draw.rect(gameDisplay, white, [100,600,20,100])
		

				if pygame.key.get_pressed()[pygame.K_7] != 0 :
					logend.write(" 100 ;")
					pygame.draw.rect(gameDisplay, black, [130,600,20,100])
			
				else :
					logend.write(" 0 ;")
					pygame.draw.rect(gameDisplay, white, [130,600,20,100])


				if pygame.key.get_pressed()[pygame.K_8] != 0 :
					logend.write(" 100 ;")
					pygame.draw.rect(gameDisplay, black, [160,600,20,100])							
				else :
					logend.write(" 0 ;")
					pygame.draw.rect(gameDisplay, white, [160,600,20,100])							

				if pygame.key.get_pressed()[pygame.K_9] != 0 :
					logend.write(" 100 ;")
					pygame.draw.rect(gameDisplay, black, [190,600,20,100])				
				else :
					logend.write(" 0 ;")
					pygame.draw.rect(gameDisplay, white, [190,600,20,100])							

 
				if pygame.key.get_pressed()[pygame.K_0] != 0 :
					logend.write(" 100;")				
					pygame.draw.rect(gameDisplay, black, [220,600,20,100])
				else :
					logend.write(" 0;")
					pygame.draw.rect(gameDisplay, white, [220,600,20,100])
				logend.write(" "+linesEmg[p]+"\n")							
				p+=1;
				pygame.draw.rect(gameDisplay, black, [100,700,20,2])
				pygame.draw.rect(gameDisplay, black, [130,700,20,2])
				pygame.draw.rect(gameDisplay, black, [160,700,20,2])
				pygame.draw.rect(gameDisplay, black, [190,700,20,2])
				pygame.draw.rect(gameDisplay, black, [220,700,20,2])
				pygame.display.update()
				
				dt+=0.1

	finally:
		pygame.key.set_repeat (old_k_delay, old_k_interval)
		

def printScreen(sequencia):		
	#global sequencia
	global gameDisplay
	tamMin = 50
	tamMax = 1200

	num_elementos_lista = len(sequencia)
	j = 0
	black = (0,0,0)

	white = (255,255,255)
	jump = (tamMax / num_elementos_lista) 
	porcent = 0
	
	try:
	
		pygame.draw.rect(gameDisplay, black, [10,430,1270,20])
		pygame.draw.rect(gameDisplay, white, [12,432,1266,16])				
		pygame.display.update()

		pygame.draw.rect(gameDisplay, black, [15,410,300,17])			
		pygame.display.update()				
		pygame.draw.rect(gameDisplay, white, [17,412,296,13])			
		pygame.display.update()				
				

		while(j < num_elementos_lista):

	
			img1 = pygame.image.load("../images/"+sequencia[j].img+".png")
			gameDisplay.blit(img1,(10,30))
	   	
			img2 = pygame.image.load("../images/"+sequencia[j+1].img+"EC.png")
			gameDisplay.blit(img2,(330,30))

			img3 = pygame.image.load("../images/"+sequencia[j+2].img+"EC.png")
			gameDisplay.blit(img3,(660,30))
	
			img4 = pygame.image.load("../images/"+sequencia[j+3].img+"EC.png")
			gameDisplay.blit(img4,(990,30))

			pygame.display.update()

			j = j + 1

			c = 0		
			por = 0
			qtdframes = 20
			aux = (300-15)/qtdframes
			while c < qtdframes:
				#print por
				pygame.draw.rect(gameDisplay, black, [19,413,por,11])			
				pygame.display.update()				
				
				por = por + aux
				QtTest.QTest.qWait(100)
				c = c + 1
			
			pygame.draw.rect(gameDisplay, white, [19,413,294,11])			
			pygame.display.update()
		
			pygame.draw.rect(gameDisplay, black, [14,433,porcent,14])
			pygame.display.update()
			
			porcent += jump
			
	finally:	
		pygame.quit()
	
	   #	sys.exit()

def main(sequencia, lineEmg):
	global gameDisplay
	global linesEmg

	linesEmg = lineEmg

	pygame.init()
	white = (255,255,255)
	black = (0,0,0)
	gameDisplay = pygame.display.set_mode((1600,740))
	gameDisplay.fill(white)
        pygame.display.update()
	
	
	t1 = threadKey()
        t1.start()

	printScreen(sequencia)


class threadKey(threading.Thread):
 
    def run(self):
	#Ui_MainWindow().keyCapture()
	keyCapture()

