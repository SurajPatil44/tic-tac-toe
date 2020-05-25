# ***Tic-Tac-Toe***

### Objective :
1. two player game 
2. computer vs human or computer vs computer

### Requirements or Rules :
1. Game should stop once it finishes i.e. when it reaches terminal condition.
2. terminal condition : when same sign is diagonally, horizontally or vertically present or when 9 moves are over.
3. can be checked after fifth move as to reduce computation
4. Player 1 should start 'o' and player 2 gets 'x'
5. Game AI should see for empty spaces to place the givem symbol(need to think about, primary AI is same probability,random.choice)

### Design :
	## classes:
		
		Game :
			Game_Board
			check_status : terminal or not
			check_whose_move : P1 or P2
			update_board
		Player :--> Game
			method : make_move
			AI or Human ? make_move_rand() : make_move_ask()
		Player_1 :--> Player
		Player_1 :--> Player
		
			
