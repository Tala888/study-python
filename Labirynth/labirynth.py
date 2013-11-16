#!/usr/bin/env python
import curses
import time
import random
random.seed()
class Labirynth:
	def __init__(self):
		self.cells = [['#', '#', '#', '#', '#', '#', '#'], \
				  ['#', '.', '.', '.', '.', '.', '#'], \
				  ['#', '.', '#', '#', '#', '.', '#'], \
				  ['#', '.', '#', '.', '#', '.', '#'], \
				  ['#', '.', '#', '.', '.', '.', '#'], \
				  ['#', '#', '#', '#', '#', '#', '#']]
		self.width = len(self.cells[0])
		self.height = len(self.cells)
		
		
class Human:
	def __init__(self, pos, char):
		self.char = char
		self.pos = pos
		self.newpos = pos
		
	def draw(self, pad):
		pad.addch(self.pos[0], self.pos[1], self.char)
		


class LabirynthGame:
	def __init__(self):
		self.prepare()

		self.mainLoop()

	def prepare(self):
		self.lab = Labirynth()
		self.player = Human((1, 1), 'i')
		self.bandit = Human((3, 5), 'B')
	
		self.stdscr = curses.initscr()
		curses.noecho()
		curses.cbreak()
		self.stdscr.keypad(1)

		self.beginX = 20
		self.beginY = 7

		self.winHeight = self.lab.height
		self.winWidth = self.lab.width
		
		self.padHeight = 100
		self.padWidth = 100
		#win = curses.newwin(height, width, begin_y, begin_x)

		self.pad = curses.newpad(self.padHeight, self.padWidth)
		
		self.stdscr.nodelay(1)

	def refresh(self):
		for i1 in range(self.lab.height):
			for i2 in range(self.lab.width):
				try:
					self.pad.addch(i1, i2, self.lab.cells[i1][i2])
				except curses.error:
					pass
	
		self.player.draw(self.pad)
		self.bandit.draw(self.pad)
	
		endX = self.winWidth + self.beginX - 1
		endY = self.winHeight + self.beginY - 1
		self.pad.refresh(0,0, self.beginY, self.beginX, endY, endX)
		
		
	def exit(self):
		curses.nocbreak()
		self.stdscr.keypad(0)
		curses.echo()
		curses.endwin()
		print("Bye!")
		self.done = True
		
	def processKeys(self):
		code = self.stdscr.getch()
		if code == curses.ERR: # no key pressed
			return
		if code == curses.KEY_RIGHT:
			self.player.newpos = (self.player.pos[0], self.player.pos[1] + 1)
		if code == curses.KEY_LEFT:
			self.player.newpos = (self.player.pos[0], self.player.pos[1] - 1)
		if code == curses.KEY_UP:
			self.player.newpos = (self.player.pos[0] - 1, self.player.pos[1])
		if code == curses.KEY_DOWN:
			self.player.newpos = (self.player.pos[0] + 1, self.player.pos[1])
			
		#if self.lab.cells[self.player.y][self.player.x] == '.':
			#self.lab.cells[self.player.y][self.player.x] = ' '
		if code > 256:
			self.notify("Key code pressed: " + str(code))
			return
			
		char = chr(code)
		if char == 'q':
			self.exit()
			return
		self.notify("Key pressed:"+char)
	
	def processMoves(self):
		d = random.randrange(4)
		if d == 0:
			self.bandit.newpos = (self.bandit.pos[0] - 1, self.bandit.pos[1])
		if d == 1:
			self.bandit.newpos = (self.bandit.pos[0], self.bandit.pos[1] + 1)
		if d == 2:
			self.bandit.newpos = (self.bandit.pos[0], self.bandit.pos[1] - 1)
		if d == 3:
			self.bandit.newpos = (self.bandit.pos[0] + 1, self.bandit.pos[1])
		self.processHuman(self.player)
		self.processHuman(self.bandit)
		if self.player.pos == self.bandit.pos:
			self.exit()
		if self.lab.cells[self.player.pos[0]][self.player.pos[1]] == '.':
			self.lab.cells[self.player.pos[0]][self.player.pos[1]] = ' '
			
	
	def processHuman(self, human):
		newLabCell = self.lab.cells[human.newpos[0]][human.newpos[1]]
		if newLabCell != '#':
			human.pos = human.newpos
	
	def notify(self, line):
		self.stdscr.addstr(0, 0, " "*100, curses.A_BOLD)
		self.stdscr.addstr(0, 0, "Warning: "+str(line), curses.A_BOLD)
		
	def mainLoop(self):
		self.done = False
		while not self.done:
			self.refresh()
			self.processKeys()
			self.processMoves()
			time.sleep(.1)
			
		
if __name__== "__main__":
	LabirynthGame()
	
#  These loops fill the pad with letters; this is
# explained in the next section

#  Displays a section of the pad in the middle of the screen



