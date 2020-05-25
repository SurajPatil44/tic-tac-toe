import random

##TODO :: ADD AI

class Game : 
	
	def __init__(self):
		self.Game_Board = {'1': None, '2': None, '3': None,
					  '4': None, '5': None, '6': None,
					  '7': None, '8': None, '9': None}
		self.moves = 0 
		self.filled = None or []
		self.empty = ['1','2','3','4','5','6','7','8','9']
		self.players = {0: None,1: None}
		self.symbols = {'o': 0,'x': 1}
		self.symbols_num2sym = {0: 'o',1: 'x'}
		self.state = {'game_state': True, 'cur_move': None, 'cur_symbol': None}
					  
	def terminal_cond(self):
		res_hor_1 = None
		res_hor_2 = None
		res_hor_3 = None
		res_ver_1 = None
		res_ver_2 = None
		res_ver_3 = None
		res_diag_1 = None
		res_diag_2 = None
		draw = None
		winner = None
		if self.Game_Board['1'] and self.Game_Board['2'] and self.Game_Board['3']:
			res_hor_1 = (self.Game_Board['1'] == self.Game_Board['2']) and (self.Game_Board['2'] == self.Game_Board['3'])
			#print("hor_1  ",res_hor_1)
			if res_hor_1:
				winner = self.Game_Board['1']
		if self.Game_Board['4'] and self.Game_Board['5'] and self.Game_Board['6']:
			res_hor_2 = (self.Game_Board['4'] == self.Game_Board['5']) and (self.Game_Board['5'] == self.Game_Board['6'])
			#print("hor 2   ",res_hor_2)
			if res_hor_2:
				winner = self.Game_Board['4']
		if self.Game_Board['7'] and self.Game_Board['8'] and self.Game_Board['9']:
			res_hor_3 = (self.Game_Board['7'] == self.Game_Board['8']) and (self.Game_Board['8'] == self.Game_Board['9'])
			#print("hor 3   ",res_hor_3)
			if res_hor_3:
				winner = self.Game_Board['7']
		if self.Game_Board['1'] and self.Game_Board['4'] and self.Game_Board['7']:
			res_ver_1 = (self.Game_Board['1'] == self.Game_Board['4']) and (self.Game_Board['4'] == self.Game_Board['7'])
			#print("ver 1  ",res_ver_1)
			if res_ver_1:
				winner = self.Game_Board['1']
		if self.Game_Board['2'] and self.Game_Board['5'] and self.Game_Board['8']:
			res_ver_2 = (self.Game_Board['2'] == self.Game_Board['5']) and (self.Game_Board['5'] == self.Game_Board['8'])
			#print("ver 2   ",res_hor_2)
			if res_ver_2:
				winner = self.Game_Board['2']
		if self.Game_Board['3'] and self.Game_Board['6'] and self.Game_Board['9']:
			res_ver_3 = (self.Game_Board['3'] == self.Game_Board['6']) and (self.Game_Board['6'] == self.Game_Board['9'])
			#print("ver 3   ",res_ver_3)
			if res_ver_3:
				winner = self.Game_Board['3']
		if self.Game_Board['5'] and self.Game_Board['3'] and self.Game_Board['7']:
			res_diag_1 = (self.Game_Board['5'] == self.Game_Board['3']) and (self.Game_Board['3'] == self.Game_Board['7'])
			#print("diag 1  ",res_diag_1)
			if res_diag_1:
				winner = self.Game_Board['5']
		if self.Game_Board['5'] and self.Game_Board['1'] and self.Game_Board['9']:
			res_diag_2 = (self.Game_Board['5'] == self.Game_Board['1']) and (self.Game_Board['1'] == self.Game_Board['9'])
			#print("diag 2  ",res_diag_2)
			if res_diag_2:
				winner = self.Game_Board['5']
		if (res_diag_1 or res_diag_2 or res_hor_1 or res_hor_2 or res_hor_3 or res_ver_1 or res_ver_2 or res_ver_3) and self.moves <= 9:
			
			return winner,True
		else:
			if self.moves == 9:
				
				return "draw",True
		return None,False
		
	def get_human_input(self):
		
		while True:
			num = input(f"\nEnter your choice from {self.empty} --> ")
			if num.isdigit() and not num in self.filled:
				break
		return num
		
	def get_player(self):
		
		while True:
			_choice = input("\nchoose your player 1 or 2 \n")
			_symbol = input("\nchoose your symnbol 'o' or 'x' \n")
			if _choice.isdigit() and (_choice in ['1','2']):
				if _symbol.lower() in ['o','x']:
					break
		return int(_choice)-1,_symbol
			
	def make_move(self,symbol,player):
		
		if self.players[player] == 'AI':
			place = random.choice(self.empty)	###not random need to put something smart
		else :
			place = self.get_human_input()
		self.empty.remove(place)
		self.filled.append(place)
		self.Game_Board[place] = self.symbols_num2sym[symbol]
		self.moves += 1
		
	def num2word(self):
		res_dict = {}
		for k,v in self.players.items():
			res_dict[v] = k
		return res_dict
	
	def check(self,val):
		if val is None:
			return ' '
		return val
	
	def print_board(self):
		print(f"{self.check(self.Game_Board['1'])}  | {self.check(self.Game_Board['2'])}  | {self.check(self.Game_Board['3'])}")
		print("___|____|___")
		print(f"{self.check(self.Game_Board['4'])}  | {self.check(self.Game_Board['5'])}  | {self.check(self.Game_Board['6'])}")
		print("___|____|___")
		print(f"{self.check(self.Game_Board['7'])}  | {self.check(self.Game_Board['8'])}  | {self.check(self.Game_Board['9'])}")
		print("   |    |   ")
		print("\n\n")
		
	def Play(self,player1,player2):
		winner = ''
		while self.state['game_state']:
			opt,sym = self.get_player()
			self.players[opt] = player1
			self.players[opt^1] = player2
			#players_n2w = self.num2word()
			#print(players_n2w)
			self.state['cur_move'] = opt
			self.state['cur_symbol'] = self.symbols[sym]
			for num in range(10):
				winner,term = self.terminal_cond()
				print(winner,term)
				if (num >= 5) and term:
					self.state['game_state'] = False
					break
				#print(self.state)
				#print(self.empty)
				print(self.moves)
				self.make_move(self.state['cur_symbol'],self.state['cur_move'])
				self.print_board()
				self.state['cur_move'] ^= 1
				self.state['cur_symbol'] ^= 1
			else:
				break
		#print(term,winner)
		#self.print_board()
		if not "draw" in winner:
			print(f"{self.players[self.state['cur_move']^1]} wins the game")
			#print(f"{self.players},{self.state},{self.filled}")
		else:
			print("\nDRAW!!!!\n")
			#print(f"{self.players},{self.state},{self.filled}")
	

def get_yorn():
	while True:
		yorn = input("\n\npress 'y' if you play again and 'n' to quit   ")
		if yorn.lower() in ['y','n']:
			break
	return yorn
				

while True:
	g = Game()
	g.Play('Human','AI')
	yorn = get_yorn()
	if 'n' in yorn.lower():
		break
	
		
print("\nSEE YEAH AGAIN!!!!!")
		