"""
Tic-Tac-Toe Game using Python

This project implements a simple console-based Tic-Tac-Toe game using Python. 
The game allows two players to take turns marking spaces on a 3x3 grid as either 'X' or 'O'. 
The game ends when one player successfully marks three consecutive spaces in a row, column, or diagonal, or when the grid is completely filled without a winner (resulting in a tie).

The project demonstrates:
- Basic usage of Python for game logic.
- Using dictionaries to represent the game board.
- Organizing code into functions for improved readability and maintainability.
- Handling user input and controlling game flow in a loop until the game is over.
- Simple win detection logic based on preset win conditions.

To run this project, ensure you have Python installed. The game runs entirely in the console and does not require any additional libraries. 
When executed, the game prompts players to take turns entering their moves, and the result is displayed after every turn.

This project is suitable for beginners who want to practice writing simple game logic in Python and improve their skills in structuring code.

Version: 0.1
Author: Sun Yufei
Date: 2024-08-17
"""

import os

def clear_screen():
    """Clears the console screen for both Windows and Unix-based systems."""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_board(board):
    """Prints the current state of the Tic-Tac-Toe board."""
    print(board['TL'] + '|' + board['TM'] + '|' + board['TR'])
    print('-+-+-')
    print(board['ML'] + '|' + board['MM'] + '|' + board['MR'])
    print('-+-+-')
    print(board['BL'] + '|' + board['BM'] + '|' + board['BR'])

def check_winner(board, turn):
    """Checks if the current player has won the game."""
    win_conditions = [
        ['TL', 'TM', 'TR'], ['ML', 'MM', 'MR'], ['BL', 'BM', 'BR'],  # rows
        ['TL', 'ML', 'BL'], ['TM', 'MM', 'BM'], ['TR', 'MR', 'BR'],  # columns
        ['TL', 'MM', 'BR'], ['TR', 'MM', 'BL']  # diagonals
    ]
    
    for condition in win_conditions:
        if board[condition[0]] == board[condition[1]] == board[condition[2]] == turn:
            return True
    return False

def main():
    """Main function to handle the game logic."""
    play_again = True
    while play_again:
        # Initialize the board with empty spaces
        board = {
            'TL': ' ', 'TM': ' ', 'TR': ' ',
            'ML': ' ', 'MM': ' ', 'MR': ' ',
            'BL': ' ', 'BM': ' ', 'BR': ' '
        }
        turn = 'x'  # 'x' always starts the game
        move_count = 0  # Keep track of the number of moves made
        game_over = False
        
        clear_screen()
        print_board(board)
        
        while move_count < 9 and not game_over:
            # Prompt the current player for their move
            move = input(f"Player {turn}'s turn. Enter position: ").upper()

            # Ensure the selected position is valid and not already occupied
            if move in board and board[move] == ' ':
                board[move] = turn
                move_count += 1

                clear_screen()
                print_board(board)

                # Check if the current player has won the game
                if check_winner(board, turn):
                    print(f"Player {turn} wins!")
                    game_over = True
                else:
                    # Switch turns between 'x' and 'o'
                    turn = 'o' if turn == 'x' else 'x'
            else:
                print("Invalid move, try again.")
        
        if not game_over:
            print("It's a tie!")
        
        # Ask if the players want to play again
        play_again = input('Do you want to play again? (yes|no): ').lower() == 'yes'

if __name__ == '__main__':
    main()
