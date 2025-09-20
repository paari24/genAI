import streamlit as st
import random
import time

def initialize_game_state():
    """Initialize or reset the game board"""
    return [['' for _ in range(3)] for _ in range(3)]

def check_winner(board):
    """Check if there's a winner and return the winner and winning cells"""
    # Check rows
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] != '':
            return board[i][0], [(i, 0), (i, 1), (i, 2)]
    
    # Check columns
    for i in range(3):
        if board[0][i] == board[1][i] == board[2][i] != '':
            return board[0][i], [(0, i), (1, i), (2, i)]
    
    # Check diagonals
    if board[0][0] == board[1][1] == board[2][2] != '':
        return board[0][0], [(0, 0), (1, 1), (2, 2)]
    if board[0][2] == board[1][1] == board[2][0] != '':
        return board[0][2], [(0, 2), (1, 1), (2, 0)]
    
    # Check for draw
    if all(cell != '' for row in board for cell in row):
        return 'Draw', []
    
    return None, []

def computer_move(board, difficulty='easy'):
    """Make a computer move based on difficulty"""
    empty_cells = [(i, j) for i in range(3) for j in range(3) if board[i][j] == '']
    
    if not empty_cells:
        return None
    
    if difficulty == 'easy':
        return random.choice(empty_cells)
    else:
        # Medium difficulty: try to win or block opponent
        opponent = 'X' if st.session_state.current_player == 'O' else 'O'
        
        # Check if computer can win
        for i, j in empty_cells:
            board[i][j] = st.session_state.current_player
            winner, _ = check_winner(board)
            board[i][j] = ''
            if winner == st.session_state.current_player:
                return (i, j)
        
        # Check if need to block opponent
        for i, j in empty_cells:
            board[i][j] = opponent
            winner, _ = check_winner(board)
            board[i][j] = ''
            if winner == opponent:
                return (i, j)
        
        # Otherwise random move
        return random.choice(empty_cells)

def main():
    st.title("Tic-Tac-Toe ❌⭕")
    
    # Initialize session state
    if 'board' not in st.session_state:
        st.session_state.board = initialize_game_state()
    if 'current_player' not in st.session_state:
        st.session_state.current_player = 'X'
    if 'game_mode' not in st.session_state:
        st.session_state.game_mode = 'two_player'
    if 'difficulty' not in st.session_state:
        st.session_state.difficulty = 'easy'
    if 'winner' not in st.session_state:
        st.session_state.winner = None
    if 'winning_cells' not in st.session_state:
        st.session_state.winning_cells = []
    if 'game_over' not in st.session_state:
        st.session_state.game_over = False
    
    # Sidebar for settings
    with st.sidebar:
        st.header("Game Settings")
        
        # Game mode selection
        game_mode = st.radio(
            "Select game mode:",
            ["Two Player", "VS Computer"],
            index=0 if st.session_state.game_mode == 'two_player' else 1,
            key="game_mode_radio"
        )
        st.session_state.game_mode = 'two_player' if game_mode == "Two Player" else 'vs_computer'
        
        # Difficulty selection if playing against computer
        if st.session_state.game_mode == 'vs_computer':
            difficulty = st.radio(
                "Computer difficulty:",
                ["Easy", "Medium"],
                index=0 if st.session_state.difficulty == 'easy' else 1,
                key="difficulty_radio"
            )
            st.session_state.difficulty = 'easy' if difficulty == "Easy" else 'medium'
        
        # Reset button
        if st.button("Reset Game", use_container_width=True):
            st.session_state.board = initialize_game_state()
            st.session_state.current_player = 'X'
            st.session_state.winner = None
            st.session_state.winning_cells = []
            st.session_state.game_over = False
            st.rerun()
    
    # Display current player or winner
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.session_state.winner:
            if st.session_state.winner == 'Draw':
                st.success("It's a draw! 🎉")
            else:
                st.success(f"Player {st.session_state.winner} wins! 🎉")
        else:
            st.info(f"Current player: {st.session_state.current_player}")
    
    st.write("")  # Spacer
    
    # Create the game board
    for i in range(3):
        cols = st.columns([1, 1, 1], gap="small")
        for j in range(3):
            with cols[j]:
                # Determine button color based on state
                button_type = "secondary"
                if (i, j) in st.session_state.winning_cells:
                    button_type = "success"
                elif st.session_state.board[i][j] != '':
                    button_type = "primary"
                
                # Display cell as button if empty, or as mark if occupied
                if st.session_state.board[i][j] == '' and not st.session_state.game_over:
                    if st.button(
                        "⬜", 
                        key=f"btn_{i}_{j}", 
                        use_container_width=True,
                        disabled=st.session_state.game_over
                    ):
                        # Handle player move
                        st.session_state.board[i][j] = st.session_state.current_player
                        
                        # Check for winner
                        winner, winning_cells = check_winner(st.session_state.board)
                        if winner:
                            st.session_state.winner = winner
                            st.session_state.winning_cells = winning_cells
                            st.session_state.game_over = True
                        else:
                            # Switch player
                            st.session_state.current_player = 'O' if st.session_state.current_player == 'X' else 'X'
                            
                            # If playing against computer and it's computer's turn
                            if (st.session_state.game_mode == 'vs_computer' and 
                                st.session_state.current_player == 'O' and 
                                not st.session_state.game_over):
                                
                                # Add a small delay for better UX
                                with st.spinner("Computer thinking..."):
                                    time.sleep(0.5)
                                    
                                    # Computer makes move
                                    move = computer_move(st.session_state.board, st.session_state.difficulty)
                                    if move:
                                        i_c, j_c = move
                                        st.session_state.board[i_c][j_c] = 'O'
                                        
                                        # Check for winner after computer move
                                        winner, winning_cells = check_winner(st.session_state.board)
                                        if winner:
                                            st.session_state.winner = winner
                                            st.session_state.winning_cells = winning_cells
                                            st.session_state.game_over = True
                                        else:
                                            st.session_state.current_player = 'X'
                        
                        st.rerun()
                else:
                    # Display X or O with appropriate styling
                    display_text = st.session_state.board[i][j]
                    if display_text == 'X':
                        display_text = '❌'
                    elif display_text == 'O':
                        display_text = '⭕'
                    
                    st.button(
                        display_text,
                        key=f"disp_{i}_{j}",
                        use_container_width=True,
                        disabled=True
                    )
    
    # Game instructions
    with st.expander("How to play"):
        st.markdown("""
        **Tic-Tac-Toe Rules:**
        - Players take turns placing their mark (X or O) in a 3x3 grid
        - The first player to get 3 of their marks in a row (horizontally, vertically, or diagonally) wins
        - If all cells are filled with no winner, the game is a draw
        
        **Game Modes:**
        - **Two Player**: Play against a friend on the same device
        - **VS Computer**: Play against the computer with selectable difficulty
        
        Use the **Reset Game** button in the sidebar to start a new game.
        """)

if __name__ == "__main__":
    main()