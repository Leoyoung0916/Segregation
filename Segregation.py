#  -*- coding:utf-8 -*-

import math
import random
import sys
import time
import pygame

global timepause 
timepause = 10

class cell(object):

	
	"""docstring for cell"""

	
	def __init__(self, nowstate=0, nextstate=0,x=0,y=0):
		super(cell, self).__init__()
		self.nowstate = nowstate
		self.nextstate= nowstate
		self.x = x
		self.y = y
		
	def updatecell(self):
		self.nowstate = self.nextstate
		self.nextstate = 0


class world(object):
	"""docstring for world"""
	
	def __init__(self, scale = 100):
		super(world, self).__init__()

		self.scale = scale
		self.worldmap = [[]]
		self.ifchanged = False
		
		self.emptycell = []		# nowstate = 0
		self.bluecell=[]         # nowstate = -1
		self.greencell = []		# nowstate = 1

		self.creatworld()

		pygame.init()
		self.py = 5
		self.px = 5
		self.xlen = 400/self.scale
		self.ylen = 400/self.scale

		self.screen = pygame.display.set_mode([2*self.px+self.scale*self.xlen,2*self.py+self.scale*self.ylen])

	def creatworld(self):
		worldmap = []
		for x in range(self.scale):
			raw = []
			for y in range(self.scale):
				dice = random.random()

				if dice<0.45: 
			 		onecell = cell(-1,0,x,y)
			 		self.bluecell.append([x,y])
			 	elif dice>0.55:
			 		onecell = cell(1,0,x,y)
			 		self.greencell.append([x,y])
			 	else:
			 		onecell = cell(0,0,x,y)
			 		self.emptycell.append([x,y])

				raw.append(onecell)
			worldmap.append(raw)
		self.worldmap = worldmap

	def outlook(self,x,y):
		
		# neighbourstate = 0
		# for i in range(3):
		# 	for j in range (3):
		# 		ii = i
		# 		jj = j
		# 		if (x == self.scale-1 and i == 2):
		# 			ii = -self.scale+2
		# 		if (y == self.scale-1 and j ==2):
		# 			jj = -self.scale+2
		# 		if self.worldmap[x+ii-1][y+jj-1].nowstate == self.worldmap[x][y].nowstate:
		# 			neighbourstate += 1
		# neighbourstate -= 1
		# return neighbourstate

		

		neighbourstate = 0
		#读取周边及自己的九个点中同类或空房子有多少
		for i in range(3):
			for j in range (3):
				ii = i
				jj = j
				if (x == self.scale-1 and i == 2):
					ii = -self.scale+2
				if (y == self.scale-1 and j ==2):
					jj = -self.scale+2
				if (self.worldmap[x+ii-1][y+jj-1].nowstate == self.worldmap[x][y].nowstate) or (self.worldmap[x+ii-1][y+jj-1].nowstate == 0):
					neighbourstate += 1
		#去除自己
		neighbourstate -= 1
		return neighbourstate


	def ifhappy(self,neighbourstate):

		if neighbourstate<5:
			return False
		else:
			return True


	def evolution(self):

		colorcelllist = self.bluecell+self.greencell
		random.shuffle(colorcelllist)
		self.ifchanged = False


		for colorcell in colorcelllist:
			neighbourstate=self.outlook(colorcell[0],colorcell[1])
			happy = self.ifhappy(neighbourstate)
			if(happy == True):
				self.worldmap[colorcell[0]][colorcell[1]].nextstate = self.worldmap[colorcell[0]][colorcell[1]].nowstate
			else:
				self.ifchanged = True
				random.shuffle(self.emptycell)
				nextposition = self.emptycell.pop()
				self.worldmap[nextposition[0]][nextposition[1]].nextstate = self.worldmap[colorcell[0]][colorcell[1]].nowstate
				if self.worldmap[colorcell[0]][colorcell[1]].nowstate==-1:
					self.bluecell.append([nextposition[0],nextposition[1]])
				if self.worldmap[colorcell[0]][colorcell[1]].nowstate==1:
					self.greencell.append([nextposition[0],nextposition[1]])

				self.worldmap[colorcell[0]][colorcell[1]].nextstate = 0
				self.emptycell.append([colorcell[0],colorcell[1]])
				try:
					self.bluecell.remove([colorcell[0],colorcell[1]])
				except:
					self.greencell.remove([colorcell[0],colorcell[1]])
					
		
	def updateworld(self):
		for i in range(self.scale):
			for j in range(self.scale):
				self.worldmap[i][j].updatecell()


	def drawupdateworld(self):
			blue=(102,196,255)
			green=(21,173,102)
			black = (0,0,0)

			for i in range(self.scale):
				for j in range(self.scale):
					if self.worldmap[i][j].nowstate == -1:
						pygame.draw.rect(self.screen,blue,[i*self.xlen+self.px,j*self.ylen+self.py,self.xlen,self.ylen])
					if self.worldmap[i][j].nowstate == 1:
						pygame.draw.rect(self.screen,green,[i*self.xlen+self.px,j*self.ylen+self.py,self.xlen,self.ylen])
					if self.worldmap[i][j].nowstate == 0:
						pygame.draw.rect(self.screen,black,[i*self.xlen+self.px,j*self.ylen+self.py,self.xlen,self.ylen])

			pygame.display.update()



	def display(self):

		for i in range(50):
			self.drawupdateworld()
			
			self.evolution()
			self.updateworld()
			if(self.ifchanged==False):
				time.sleep(2)
				pygame.quit()
				print "exit"
				sys.exit()
				
			time.sleep(0.5)
		
		

	def displaycell(self,x,y):
		for i in range(10):
			print self.worldmap[x][y].nowstate, self.worldmap[x][y].nextstate
			self.updateworld()
			self.evolution()
			
			time.sleep(0.3)
		

oneworld = world(30)
oneworld.display()







