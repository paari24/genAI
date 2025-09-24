import streamlit as st
import random
import time
import threading
from datetime import datetime

class SnakeGame:
    def __init__(self, grid_size=15):
        self.grid_size = grid_size
        self.reset_game()
    
    def reset_game(self):
        """Initialize or reset the game state"""
        start_pos = self.grid_size // 2
        self.snake = [(start_pos, start_pos)]
        self.direction = (1, 0)  # Start moving right
        self.food = self.generate_food()
        self.score = 0
        self.game_over = False
        self.game_started = False
        self.move_speed = 800  # milliseconds between moves
    
    def generate_food(self):
        """Generate food in a random position not occupied by snake"""
        while True:
            food = (random.randint(0, self.grid_size-1), random.randint(0, self.grid_size-1))
            if food not in self.snake:
                return food
    
    def change_direction(self, new_direction):
        """Change snake direction (prevent 180-degree turns)"""
        # Prevent reverse direction
        if (new_direction[0] * -1, new_direction[1] * -1) != self.direction:
            self.direction = new_direction
    
    def move_snake(self):
        """Move the snake one step in current direction"""
        if not self.game_started or self.game_over:
            return False
        
        # Calculate new head position
        head_x, head_y = self.snake[0]
        dir_x, dir_y = self.direction
        new_head = (head_x + dir_x, head_y + dir_y)
        
        # Check for wall collisions
        if (new_head[0] < 0 or new_head[0] >= self.grid_size or 
            new_head[1] < 0 or new_head[1] >= self.grid_size):
            self.game_over = True
            return True
        
        # Check for self collision
        if new_head in self.snake:
            self.game_over = True
            return True
        
        # Move snake
        self.snake.insert(0, new_head)
        
        # Check if food eaten
        if new_head == self.food:
            self.score += 10
            self.food = self.generate_food()
            # Increase speed every 50 points
            if self.score % 50 == 0 and self.move_speed > 200:
                self.move_speed = max(200, int(self.move_speed * 0.85))
        else:
            # Remove tail if no food eaten
            self.snake.pop()
        
        return True

def main():
    st.set_page_config(
        page_title="🐍 Snake Game",
        page_icon="🐍",
        layout="centered"
    )
    
    # Custom CSS
    st.markdown("""
    <style>
    .main-title {
        font-size: 3.5rem;
        font-weight: 900;
        text-align: center;
        background: linear-gradient(45deg, #00ff88, #0088ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 2rem;
        animation: titleGlow 2s ease-in-out infinite alternate;
    }
    
    @keyframes titleGlow {
        from { text-shadow: 0 0 20px rgba(0,255,136,0.5); }
        to { text-shadow: 0 0 30px rgba(0,136,255,0.8); }
    }
    
    .game-container {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
        border-radius: 20px;
        padding: 2rem;
        margin: 2rem 0;
        border: 3px solid #00ff88;
        box-shadow: 0 0 40px rgba(0,255,136,0.3);
    }
    
    .score-display {
        background: linear-gradient(45deg, #667eea, #764ba2);
        color: white;
        padding: 1.5rem;
        border-radius: 15px;
        text-align: center;
        margin: 1.5rem 0;
        font-size: 1.4rem;
        font-weight: bold;
        box-shadow: 0 8px 25px rgba(102,126,234,0.4);
    }
    
    .game-grid {
        display: grid;
        grid-template-columns: repeat(15, 30px);
        grid-template-rows: repeat(15, 30px);
        gap: 2px;
        background-color: #0a0a0a;
        padding: 25px;
        border-radius: 15px;
        border: 3px solid #333;
        margin: 2rem auto;
        width: fit-content;
        box-shadow: inset 0 0 50px rgba(0,0,0,0.8);
    }
    
    .cell {
        width: 30px;
        height: 30px;
        border-radius: 4px;
        transition: all 0.2s ease;
    }
    
    .snake-head {
        background: radial-gradient(circle, #00ff88, #00cc44);
        border: 2px solid #00ff88;
        border-radius: 50%;
        box-shadow: 0 0 20px rgba(0,255,136,0.8);
        animation: headPulse 1s ease-in-out infinite alternate;
    }
    
    @keyframes headPulse {
        from { transform: scale(1); }
        to { transform: scale(1.1); }
    }
    
    .snake-body {
        background: linear-gradient(45deg, #00cc44, #009933);
        border: 1px solid #00aa33;
        border-radius: 6px;
        box-shadow: 0 0 10px rgba(0,204,68,0.5);
    }
    
    .food {
        background: radial-gradient(circle, #ff4444, #cc2222);
        border: 2px solid #ff6666;
        border-radius: 50%;
        box-shadow: 0 0 25px rgba(255,68,68,0.9);
        animation: foodBounce 1.5s ease-in-out infinite;
    }
    
    @keyframes foodBounce {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.2); }
    }
    
    .empty {
        background: #1a1a1a;
        border: 1px solid #2a2a2a;
    }
    
    .controls {
        display: grid;
        grid-template-columns: 1fr 1fr 1fr;
        grid-template-rows: 1fr 1fr 1fr;
        gap: 10px;
        max-width: 200px;
        margin: 2rem auto;
    }
    
    .control-btn {
        background: linear-gradient(45deg, #00ff88, #00cc44) !important;
        color: white !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 15px !important;
        font-size: 1.5rem !important;
        font-weight: bold !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 5px 15px rgba(0,255,136,0.3) !important;
    }
    
    .control-btn:hover {
        transform: translateY(-3px) scale(1.05) !important;
        box-shadow: 0 8px 25px rgba(0,255,136,0.6) !important;
    }
    
    .game-over-screen {
        background: linear-gradient(45deg, #ff4444, #cc2222);
        color: white;
        padding: 3rem;
        border-radius: 20px;
        text-align: center;
        margin: 2rem 0;
        animation: gameOverShake 0.5s ease-in-out;
        box-shadow: 0 0 50px rgba(255,68,68,0.5);
    }
    
    @keyframes gameOverShake {
        0%, 100% { transform: translateX(0); }
        25% { transform: translateX(-5px); }
        75% { transform: translateX(5px); }
    }
    
    .start-screen {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 3rem;
        border-radius: 20px;
        text-align: center;
        margin: 2rem 0;
        box-shadow: 0 0 40px rgba(102,126,234,0.4);
    }
    
    .instructions {
        background: rgba(255,255,255,0.1);
        backdrop-filter: blur(10px);
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1.5rem 0;
        border: 1px solid rgba(255,255,255,0.2);
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Initialize game
    if 'snake_game' not in st.session_state:
        st.session_state.snake_game = SnakeGame()
        st.session_state.game_running = False
        st.session_state.last_update = time.time()
    
    game = st.session_state.snake_game
    
    # Title
    st.markdown('<h1 class="main-title">🐍 SNAKE GAME</h1>', unsafe_allow_html=True)
    
    # Main game container
    st.markdown('<div class="game-container">', unsafe_allow_html=True)
    
    # Game state
    game_state = {
        'snake': game.snake,
        'food': game.food,
        'score': game.score,
        'game_over': game.game_over,
        'game_started': game.game_started
    }
    
    # Score display
    speed = round(1000/game.move_speed, 1) if game.move_speed > 0 else 1
    st.markdown(f'''
    <div class="score-display">
        🏆 Score: {game_state["score"]} &nbsp;&nbsp;|&nbsp;&nbsp; 
        📏 Length: {len(game_state["snake"])} &nbsp;&nbsp;|&nbsp;&nbsp; 
        ⚡ Speed: {speed}x
    </div>
    ''', unsafe_allow_html=True)
    
    # Layout
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col1:
        st.markdown("### 🎮 Controls")
        
        # Direction controls
        control_cols = st.columns([1, 1, 1])
        
        # Up button
        with control_cols[1]:
            if st.button("⬆️", key="up", help="Move Up", use_container_width=True):
                game.change_direction((0, -1))
        
        # Left and Right buttons
        with control_cols[0]:
            if st.button("⬅️", key="left", help="Move Left", use_container_width=True):
                game.change_direction((-1, 0))
        with control_cols[2]:
            if st.button("➡️", key="right", help="Move Right", use_container_width=True):
                game.change_direction((1, 0))
        
        # Down button
        with control_cols[1]:
            if st.button("⬇️", key="down", help="Move Down", use_container_width=True):
                game.change_direction((0, 1))
        
        st.markdown("---")
        
        # Game control buttons
        if not game_state['game_started']:
            if st.button("🚀 START GAME", type="primary", use_container_width=True):
                game.game_started = True
                st.session_state.game_running = True
                st.session_state.last_update = time.time()
                st.rerun()
        
        if st.button("🔄 RESTART", use_container_width=True):
            st.session_state.snake_game = SnakeGame()
            st.session_state.game_running = False
            st.rerun()
    
    with col2:
        # Game screen
        if not game_state['game_started']:
            st.markdown('''
            <div class="start-screen">
                <h2>🎮 Ready to Play?</h2>
                <p>Click <strong>"START GAME"</strong> to begin!</p>
                <p>Use the arrow buttons to control your snake</p>
                <h3>🎯 Goal:</h3>
                <p>Eat the red food to grow and score points<br>
                Avoid walls and don't bite yourself!</p>
            </div>
            ''', unsafe_allow_html=True)
        elif game_state['game_over']:
            st.markdown(f'''
            <div class="game-over-screen">
                <h1>💥 GAME OVER!</h1>
                <h2>🏆 Final Score: {game_state["score"]}</h2>
                <h3>🐍 Snake Length: {len(game_state["snake"])}</h3>
                <p>Click <strong>"RESTART"</strong> to play again!</p>
            </div>
            ''', unsafe_allow_html=True)
        
        # Game grid
        grid_html = '<div class="game-grid">'
        for y in range(game.grid_size):
            for x in range(game.grid_size):
                pos = (x, y)
                
                if pos == game_state['snake'][0]:  # Snake head
                    cell_class = "cell snake-head"
                elif pos in game_state['snake']:  # Snake body
                    cell_class = "cell snake-body"
                elif pos == game_state['food']:  # Food
                    cell_class = "cell food"
                else:  # Empty
                    cell_class = "cell empty"
                
                grid_html += f'<div class="{cell_class}"></div>'
        
        grid_html += '</div>'
        st.markdown(grid_html, unsafe_allow_html=True)
    
    with col3:
        st.markdown("### 📊 Game Stats")
        st.metric("🎯 Current Score", game_state['score'])
        st.metric("🐍 Snake Length", len(game_state['snake']))
        st.metric("⚡ Game Speed", f"{speed}x")
        
        # Instructions
        st.markdown('''
        <div class="instructions">
            <h4>🎮 How to Play:</h4>
            <ul>
                <li>🔴 Eat red food to grow</li>
                <li>🎯 Each food = +10 points</li>
                <li>⚡ Speed increases with score</li>
                <li>⚠️ Don't hit walls or yourself!</li>
                <li>🎮 Use arrow buttons to steer</li>
            </ul>
        </div>
        ''', unsafe_allow_html=True)
        
        # Keyboard input
        st.markdown("### ⌨️ Keyboard Input")
        key_input = st.text_input("WASD Keys:", placeholder="Type: w,a,s,d", key="keyboard")
        
        if key_input:
            key = key_input.lower().strip()
            if key == 'w':
                game.change_direction((0, -1))
            elif key == 's':
                game.change_direction((0, 1))
            elif key == 'a':
                game.change_direction((-1, 0))
            elif key == 'd':
                game.change_direction((1, 0))
            # Clear input
            st.session_state.keyboard = ""
            st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # AUTOMATIC MOVEMENT - The key part that actually works!
    if (st.session_state.game_running and 
        game_state['game_started'] and 
        not game_state['game_over']):
        
        current_time = time.time()
        time_diff = (current_time - st.session_state.last_update) * 1000  # Convert to milliseconds
        
        if time_diff >= game.move_speed:
            # Move the snake
            moved = game.move_snake()
            st.session_state.last_update = current_time
            
            if moved:
                # Use st.empty() and automatic refresh for continuous movement
                time.sleep(0.1)
                st.rerun()
    
    # Auto-refresh mechanism using placeholder
    if (st.session_state.game_running and 
        game_state['game_started'] and 
        not game_state['game_over']):
        
        # Create an invisible placeholder that refreshes the page
        placeholder = st.empty()
        with placeholder.container():
            st.markdown("<!-- Auto refresh -->", unsafe_allow_html=True)
        
        # Force refresh after a short delay
        time.sleep(max(0.1, game.move_speed / 1000.0))
        placeholder.empty()
        st.rerun()

if __name__ == "__main__":
    main()