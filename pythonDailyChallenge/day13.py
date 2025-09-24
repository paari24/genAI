import streamlit as st
import random
import time

def initialize_game():
    """Initialize or reset the game state"""
    return {
        'user_score': 0,
        'computer_score': 0,
        'rounds_played': 0,
        'last_user_choice': None,
        'last_computer_choice': None,
        'last_result': None,
        'game_history': []
    }

def get_computer_choice():
    """Generate computer's choice"""
    return random.choice(['rock', 'paper', 'scissors'])

def determine_winner(user_choice, computer_choice):
    """Determine the winner of a round"""
    if user_choice == computer_choice:
        return 'tie'
    
    winning_combinations = {
        'rock': 'scissors',
        'paper': 'rock', 
        'scissors': 'paper'
    }
    
    if winning_combinations[user_choice] == computer_choice:
        return 'user'
    else:
        return 'computer'

def get_emoji(choice):
    """Get emoji representation for choices"""
    emoji_map = {
        'rock': '🪨',
        'paper': '📄',
        'scissors': '✂️'
    }
    return emoji_map.get(choice, choice)

def get_result_color(result):
    """Get color for result display"""
    color_map = {
        'user': 'green',
        'computer': 'red', 
        'tie': 'orange'
    }
    return color_map.get(result, 'gray')

def get_result_message(user_choice, computer_choice, result):
    """Get descriptive result message"""
    if result == 'tie':
        return "It's a tie! 🤝"
    
    winning_moves = {
        ('rock', 'scissors'): "Rock crushes Scissors! 💥",
        ('scissors', 'paper'): "Scissors cut Paper! ✂️",
        ('paper', 'rock'): "Paper covers Rock! 📄"
    }
    
    if result == 'user':
        return winning_moves.get((user_choice, computer_choice), "You win! 🎉")
    else:
        return winning_moves.get((computer_choice, user_choice), "Computer wins! 🤖")

def main():
    st.set_page_config(
        page_title="Rock Paper Scissors",
        page_icon="🎮",
        layout="centered"
    )
    
    # Custom CSS for styling
    st.markdown("""
    <style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        margin-bottom: 2rem;
        background: linear-gradient(45deg, #FF6B6B, #4ECDC4);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .score-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 15px;
        padding: 1.5rem;
        color: white;
        text-align: center;
        margin: 1rem 0;
    }
    .choice-card {
        background: #f8f9fa;
        border-radius: 10px;
        padding: 1rem;
        text-align: center;
        border: 2px solid #e9ecef;
        transition: all 0.3s ease;
    }
    .choice-card:hover {
        border-color: #667eea;
        transform: translateY(-2px);
    }
    .result-banner {
        border-radius: 10px;
        padding: 1rem;
        text-align: center;
        font-weight: bold;
        margin: 1rem 0;
    }
    .history-item {
        padding: 0.5rem;
        border-radius: 5px;
        margin: 0.2rem 0;
        background: #f8f9fa;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Initialize session state
    if 'game' not in st.session_state:
        st.session_state.game = initialize_game()
    
    # Header
    st.markdown('<div class="main-header">Rock 🪨 Paper 📄 Scissors ✂️</div>', unsafe_allow_html=True)
    
    # Sidebar for controls and history
    with st.sidebar:
        st.header("Game Controls")
        
        # Reset game button
        if st.button("🔄 Reset Game", use_container_width=True):
            st.session_state.game = initialize_game()
            st.rerun()
        
        # Game statistics
        st.header("📊 Statistics")
        st.metric("Rounds Played", st.session_state.game['rounds_played'])
        st.metric("Win Rate", 
                 f"{(st.session_state.game['user_score'] / st.session_state.game['rounds_played'] * 100):.1f}%" 
                 if st.session_state.game['rounds_played'] > 0 else "0%")
        
        # Game history
        st.header("📜 Recent Games")
        if st.session_state.game['game_history']:
            for i, history in enumerate(st.session_state.game['game_history'][-5:]):
                with st.container():
                    user_emoji = get_emoji(history['user_choice'])
                    comp_emoji = get_emoji(history['computer_choice'])
                    result_icon = "✅" if history['result'] == 'user' else "❌" if history['result'] == 'computer' else "⚖️"
                    st.write(f"{result_icon} {user_emoji} vs {comp_emoji}")
        else:
            st.info("No games played yet")
    
    # Main game area
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        # Score display
        st.markdown(f"""
        <div class="score-card">
            <div style="font-size: 1.5rem; margin-bottom: 1rem;">Current Score</div>
            <div style="display: flex; justify-content: space-around;">
                <div>
                    <div style="font-size: 2rem;">👤</div>
                    <div style="font-size: 2rem; font-weight: bold;">{st.session_state.game['user_score']}</div>
                </div>
                <div>
                    <div style="font-size: 2rem;">VS</div>
                </div>
                <div>
                    <div style="font-size: 2rem;">🤖</div>
                    <div style="font-size: 2rem; font-weight: bold;">{st.session_state.game['computer_score']}</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Choice buttons
        st.subheader("Make your choice:")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("🪨 Rock", use_container_width=True, key="rock"):
                play_round('rock')
        
        with col2:
            if st.button("📄 Paper", use_container_width=True, key="paper"):
                play_round('paper')
        
        with col3:
            if st.button("✂️ Scissors", use_container_width=True, key="scissors"):
                play_round('scissors')
        
        # Display last round results
        if st.session_state.game['last_user_choice']:
            display_round_results()
        
        # Game instructions
        with st.expander("ℹ️ How to Play"):
            st.markdown("""
            **Rules:**
            - **Rock** 🪨 beats **Scissors** ✂️
            - **Scissors** ✂️ beat **Paper** 📄  
            - **Paper** 📄 beats **Rock** 🪨
            - Same choice results in a tie
            
            **Scoring:**
            - Win: +1 point
            - Tie: +0 points
            - Loss: +0 points
            
            Make your choice by clicking one of the buttons above!
            """)

def play_round(user_choice):
    """Play a round of Rock, Paper, Scissors"""
    game = st.session_state.game
    
    # Computer makes choice
    computer_choice = get_computer_choice()
    
    # Determine winner
    result = determine_winner(user_choice, computer_choice)
    
    # Update scores
    if result == 'user':
        game['user_score'] += 1
    elif result == 'computer':
        game['computer_score'] += 1
    
    game['rounds_played'] += 1
    
    # Store round data
    game['last_user_choice'] = user_choice
    game['last_computer_choice'] = computer_choice
    game['last_result'] = result
    
    # Add to history (keep last 10 rounds)
    game['game_history'].append({
        'user_choice': user_choice,
        'computer_choice': computer_choice,
        'result': result
    })
    if len(game['game_history']) > 10:
        game['game_history'] = game['game_history'][-10:]

def display_round_results():
    """Display the results of the last round"""
    game = st.session_state.game
    
    # Create columns for choices display
    col1, col2, col3 = st.columns([2, 1, 2])
    
    with col1:
        st.markdown(f"""
        <div class="choice-card">
            <div style="font-size: 3rem;">{get_emoji(game['last_user_choice'])}</div>
            <div style="font-weight: bold;">Your Choice</div>
            <div>{game['last_user_choice'].title()}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="display: flex; justify-content: center; align-items: center; height: 100%;">
            <div style="font-size: 2rem;">VS</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="choice-card">
            <div style="font-size: 3rem;">{get_emoji(game['last_computer_choice'])}</div>
            <div style="font-weight: bold;">Computer's Choice</div>
            <div>{game['last_computer_choice'].title()}</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Result banner
    result_color = get_result_color(game['last_result'])
    result_message = get_result_message(
        game['last_user_choice'], 
        game['last_computer_choice'], 
        game['last_result']
    )
    
    st.markdown(f"""
    <div class="result-banner" style="background-color: {result_color}; color: white;">
        <div style="font-size: 1.2rem;">{result_message}</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Add some celebration for wins
    if game['last_result'] == 'user':
        st.balloons()
    elif game['last_result'] == 'computer':
        st.snow()

if __name__ == "__main__":
    main()