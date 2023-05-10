from Board import Game

# todo: bei vollem brett schmiert das prgm ab

def humanVSrandom():
	game = Game()
	print("VIER GEWINNT")
	print(game)
	print("Enter a valid number between 0 an 7 and collect 4 symbols")
	
	turn = 1
	while not game.is_over():
		if turn == 1:
			move = int(input())
			game.place_move(move, 1)
			print(game)
			turn = 2
		else:
			#game.do_random_move(2)
			move, _ = game._do_suboptimal_search(turn, 2, 20)
			#print(game)
			game.place_move(move, 2)
			print(game)
			turn = 1
			
	if game.winner == None:
		print("Draw")
	else:
		if game.winner == 1:
			print("You win")
		else:
			print("Computer wins")

if __name__ == "__main__":
	humanVSrandom()
