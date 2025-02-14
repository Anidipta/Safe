import streamlit as st
from data.database import update_activity_progress, get_user_progress
import random
from datetime import datetime
import time


MINE_SVG = """<svg viewBox="0 0 100 100">
    <circle cx="50" cy="50" r="40" fill="#FF4444"/>
    <path d="M30,50 L70,50 M50,30 L50,70" stroke="white" stroke-width="8"/>
</svg>"""

FLAG_SVG = """<svg viewBox="0 0 100 100">
    <rect x="45" y="20" width="5" height="60" fill="#333"/>
    <path d="M50,20 L80,35 L50,50" fill="#FF4444"/>
</svg>"""

# Theme colors
THEME_COLORS = {
    "Classic": {"primary": "#4ECDC4", "secondary": "#FF6B6B", "accent": "#FFD93D"},
    "Space": {"primary": "#2C3E50", "secondary": "#8E44AD", "accent": "#F1C40F"},
    "Fantasy": {"primary": "#2ECC71", "secondary": "#E74C3C", "accent": "#F39C12"},
    "Cyberpunk": {"primary": "#FF006E", "secondary": "#3A86FF", "accent": "#FFBE0B"}
}

# Achievements
ACHIEVEMENTS = {
    'puzzle': {
        'collector': {'name': '🎨 Master Collector', 'desc': 'Collect all rare pieces', 'threshold': 3},
        'speedster': {'name': '⚡ Speed Solver', 'desc': 'Complete puzzle under 2 minutes', 'threshold': 120},
        'perfectionist': {'name': '✨ Perfectionist', 'desc': 'Complete 3 puzzles', 'threshold': 3}
    },
    'minesweeper': {
        'expert': {'name': '💫 Mine Expert', 'desc': 'Win without any flags', 'threshold': 1},
        'speed_demon': {'name': '🏃 Speed Demon', 'desc': 'Win under 1 minute', 'threshold': 60},
        'survivor': {'name': '🛡️ Survivor', 'desc': 'Win 5 games', 'threshold': 5}
    }
}

# Utility functions
def create_rarity_animation(rarity):
    """Create animated sparkle effect based on rarity"""
    colors = ["#FFD700" if rarity > 90 else "#C0C0C0" if rarity > 70 else "#CD7F32"]
    return f"""
    <style>
    @keyframes sparkle {{
        0% {{ transform: scale(1); opacity: 1; }}
        50% {{ transform: scale(1.2); opacity: 0.8; }}
        100% {{ transform: scale(1); opacity: 1; }}
    }}
    .rarity-{rarity} {{
        background: linear-gradient(45deg, {colors[0]}, #FFFFFF);
    }}
    </style>
    """

def create_achievement_badge(title, description):
    """Create an achievement badge with animation"""
    return f"""
    <div style="
        background: linear-gradient(45deg, #4ECDC4, #556270);
        padding: 15px;
        border-radius: 10px;
        margin: 10px 0;
        animation: badge-glow 2s infinite alternate;
    ">
        <h3 style="color: white; margin: 0;">🏆 {title}</h3>
        <p style="color: #DDD; margin: 5px 0 0 0;">{description}</p>
    </div>
    <style>
    @keyframes badge-glow {{
        from {{ box-shadow: 0 0 10px #4ECDC4; }}
        to {{ box-shadow: 0 0 20px #4ECDC4; }}
    }}
    </style>
    """

def create_piece_card(piece, theme_colors):
    """Create a themed piece card with SVG and animations"""
    rarity_color = "#FFD700" if piece['rarity'] > 90 else "#C0C0C0" if piece['rarity'] > 70 else "#CD7F32"
    return f"""
    <div class="piece-card rarity-{piece['rarity']}" style="
        padding: 15px;
        border: 2px solid {rarity_color};
        border-radius: 10px;
        margin: 5px;
        background: linear-gradient(45deg, {theme_colors['primary']}22, {theme_colors['secondary']}22);
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    ">
        <h4 style="color: {theme_colors['accent']}; text-align: center; margin: 10px 0;">
            Piece #{piece['type']}
        </h4>
        <p style="color: {rarity_color}; margin: 5px 0;">✨ {piece['effect']}</p>
        <p style="color: {theme_colors['secondary']}">📈 Rarity: {piece['rarity']}%</p>
    </div>
    """


def get_user_stats(wallet_address):
    """Get user's gaming statistics from database"""
    puzzle_progress = get_user_progress(wallet_address, 'Puzzle NFT Game')
    minesweeper_progress = get_user_progress(wallet_address, 'Minesweeper')
    return {
        'puzzle_nfts': puzzle_progress.get('completed', 0),
        'minesweeper_wins': minesweeper_progress.get('completed', 0),
        'total_revealed': minesweeper_progress.get('current_progress', 0),
        'achievements': puzzle_progress.get('achievements', []) + minesweeper_progress.get('achievements', [])
    }

def get_player_rank(stats):
    """Calculate player rank based on total score"""
    total_score = (stats['puzzle_nfts'] * 100 + 
                  stats['minesweeper_wins'] * 200 + 
                  len(stats['achievements']) * 300)
    
    if total_score < 500:
        return "🥉 Bronze"
    elif total_score < 1500:
        return "🥈 Silver"
    elif total_score < 3000:
        return "🥇 Gold"
    else:
        return "👑 Diamond"

def display_stats(wallet_address):
    """Display user stats in sidebar"""
    stats = get_user_stats(wallet_address)
    
    st.sidebar.markdown("### 🏆 Gaming Profile")
    
    # Profile Card
    st.sidebar.markdown(f"""
    <div style='padding: 10px; 
                background: linear-gradient(45deg, #1e3799, #0c2461); 
                border-radius: 10px; 
                color: white;'>
        <h3>👤 Player Stats</h3>
        <p>Wallet: {wallet_address[:6]}...{wallet_address[-4:]}</p>
        <p>Rank: {get_player_rank(stats)}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Stats Grid
    col1, col2 = st.sidebar.columns(2)
    with col1:
        st.metric("🧩 NFTs", stats['puzzle_nfts'], f"+{len(stats['achievements'])}")
        st.metric("💣 Wins", stats['minesweeper_wins'])
    with col2:
        st.metric("🎯 Revealed", stats['total_revealed'])
        completion_rate = (stats['total_revealed'] / 64 * 100) if stats['total_revealed'] > 0 else 0
        st.metric("📊 Success", f"{completion_rate:.1f}%")
    
    # Achievements
    if stats['achievements']:
        st.sidebar.markdown("### 🌟 Achievements")
        for achievement in stats['achievements']:
            st.sidebar.markdown(create_achievement_badge(
                ACHIEVEMENTS['puzzle' if 'puzzle' in achievement else 'minesweeper'][achievement]['name'],
                ACHIEVEMENTS['puzzle' if 'puzzle' in achievement else 'minesweeper'][achievement]['desc']
            ), unsafe_allow_html=True)

def game1_puzzle_nft(wallet_address):
    """Puzzle NFT Game Implementation with save/reset functionality"""
    st.title("🧩 Puzzle NFT Game")
    
    # Theme selection
    theme = st.selectbox("🎨 Select Theme", 
                        ["Classic", "Space", "Fantasy", "Cyberpunk"],
                        help="Different themes affect piece rarity and special effects!")
    
    # Initialize session state
    if 'puzzle_board' not in st.session_state:
        st.session_state.puzzle_board = [0] * 9
        st.session_state.piece_collection = []
        st.session_state.game_started = False
        st.session_state.start_time = None
        st.session_state.saved_games = []
    
    # Game Controls
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        if st.button("🎲 New Game", use_container_width=True):
            # Save current game if it exists
            if st.session_state.game_started and len(st.session_state.piece_collection) > 0:
                saved_game = {
                    'board': st.session_state.puzzle_board.copy(),
                    'collection': st.session_state.piece_collection.copy(),
                    'theme': theme,
                    'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
                update_activity_progress(
                    wallet_address, 
                    'Puzzle NFT Game', 
                    2,  # Save game activity type
                    len(st.session_state.piece_collection), 
                    9
                )
                st.success("Current game saved! Starting new game...")
            
            # Reset game state
            st.session_state.puzzle_board = [0] * 9
            st.session_state.piece_collection = []
            st.session_state.game_started = False
            st.session_state.start_time = None
            st.rerun()
    
    with col2:
        if st.button("🔄 Reset Board", use_container_width=True):
            st.session_state.puzzle_board = [0] * 9
            st.rerun()

    with col3:
        if st.button("💾 Save Game", use_container_width=True):
            if st.session_state.game_started and len(st.session_state.piece_collection) > 0:
                saved_game = {
                    'board': st.session_state.puzzle_board.copy(),
                    'collection': st.session_state.piece_collection.copy(),
                    'theme': theme,
                    'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
                update_activity_progress(
                    wallet_address, 
                    'Puzzle NFT Game', 
                    2,  # Save game activity type
                    len(st.session_state.piece_collection), 
                    9,
                    additional_data=saved_game
                )
                st.success("Game saved successfully!")
            else:
                st.warning("No active game to save!")
    
    def get_special_effect(rarity, theme):
        effects = {
            'Classic': ['Sparkle', 'Glow', 'Rainbow'],
            'Space': ['Nebula', 'Stardust', 'Black Hole'],
            'Fantasy': ['Magic Aura', 'Dragon\'s Breath', 'Fairy Dust'],
            'Cyberpunk': ['Neon Pulse', 'Digital Glitch', 'Matrix Code']
        }
        return random.choice(effects[theme])
    
    def mint_puzzle_piece():
        if len(st.session_state.piece_collection) < 9:
            piece_type = random.randint(1, 9)
            rarity = random.randint(1, 100)
            special_effect = get_special_effect(rarity, theme)
            
            while piece_type in [p['type'] for p in st.session_state.piece_collection]:
                piece_type = random.randint(1, 9)
            
            piece = {
                'type': piece_type,
                'rarity': rarity,
                'effect': special_effect,
                'theme': theme,
                'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            st.session_state.piece_collection.append(piece)
            
            if rarity > 90:
                st.balloons()
                st.markdown(f"""
                <div class='legendary-piece' style='text-align: center; animation: pulse 2s infinite;'>
                    🌟 LEGENDARY {theme.upper()} PIECE MINTED! 🌟
                    <br>Special Effect: {special_effect}
                </div>
                """, unsafe_allow_html=True)
            elif rarity > 70:
                st.snow()
                st.info(f"✨ Rare {theme} piece minted! Effect: {special_effect}")
            else:
                st.success(f"New {theme} piece minted! Effect: {special_effect}")
            
            update_activity_progress(wallet_address, 'Puzzle NFT Game', 1, 
                                  len(st.session_state.piece_collection), 9)
        else:
            st.warning("Maximum pieces collected! Place them to complete the puzzle.")
    
    # Game Interface
    col1, col2 = st.columns([2, 3])
    
    with col1:
        st.markdown("### 🎲 Mint New Pieces")
        if st.button("Mint Piece", use_container_width=True):
            mint_puzzle_piece()
            if not st.session_state.game_started:
                st.session_state.game_started = True
                st.session_state.start_time = time.time()
    
    with col2:
        st.markdown("### 🎯 Progress")
        progress = len([x for x in st.session_state.puzzle_board if x != 0]) / 9
        st.progress(progress)
        if st.session_state.start_time:
            elapsed_time = int(time.time() - st.session_state.start_time)
            st.markdown(f"⏱️ Time: {elapsed_time//60}m {elapsed_time%60}s")
    
    # Collection Display
    st.markdown("### 🗃️ Collection")
    piece_cols = st.columns(3)
    for idx, piece in enumerate(st.session_state.piece_collection):
        with piece_cols[idx % 3]:
            st.markdown(
                create_piece_card(piece, THEME_COLORS[theme]) + 
                create_rarity_animation(piece['rarity']),
                unsafe_allow_html=True
            )
    
    # Game Board
    st.markdown("### 🎮 Puzzle Board")
    board_cols = st.columns(3)
    for i in range(9):
        with board_cols[i % 3]:
            piece_value = st.session_state.puzzle_board[i]
            if piece_value != 0:
                piece = next((p for p in st.session_state.piece_collection if p['type'] == piece_value), None)
                if piece:
                    st.markdown(f"""
                    <div style="padding: 20px; border-radius: 10px; border: 2px solid #ccc; text-align: center;">
                        <p margin: 5px 0;">
                            {piece['effect']}
                        </p>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.markdown("""
                <div style="padding: 20px; 
                            border-radius: 10px; 
                            text-align: center;
                            border: 2px dashed #ccc;">
                    -
                </div>
                """, unsafe_allow_html=True)

    # Place pieces
    st.markdown("### 🎯 Place Pieces")
    place_cols = st.columns(3)
    for idx, piece in enumerate(st.session_state.piece_collection):
        with place_cols[idx % 3]:
            if st.button(f"Place #{piece['type']}", 
                        key=f"place_{piece['type']}", 
                        use_container_width=True):
                if 0 in st.session_state.puzzle_board:
                    empty_index = st.session_state.puzzle_board.index(0)
                    st.session_state.puzzle_board[empty_index] = piece['type']
                    
                    # Check completion
                    if 0 not in st.session_state.puzzle_board:
                        completion_time = int(time.time() - st.session_state.start_time)
                        st.balloons()
                        st.markdown(f"""
                        <div style="text-align: center; animation: victory 1s infinite;">
                            🎊 PUZZLE COMPLETED! 🎊<br>
                            Time: {completion_time//60}m {completion_time%60}s
                        </div>
                        <style>
                        @keyframes victory {{
                            0% {{ transform: scale(1); }}
                            50% {{ transform: scale(1.1); }}
                            100% {{ transform: scale(1); }}
                        }}
                        </style>
                        """, unsafe_allow_html=True)
                        
                        # Achievement checks
                        if completion_time < 120:
                            update_achievement(wallet_address, 'speedster')
                        if all(p['rarity'] > 70 for p in st.session_state.piece_collection):
                            update_achievement(wallet_address, 'collector')
                        
                        update_activity_progress(wallet_address, 'Puzzle NFT Game', 1, 9, 9)
                else:
                    st.warning("No empty spaces left!")

def game2_minesweeper(wallet_address):
    """Minesweeper Game Implementation"""
    st.title("💣 Minesweeper")
    
    # Difficulty selection with visual indicators
    st.markdown("""
    <style>
    .difficulty-selector {
        display: flex;
        justify-content: space-around;
        margin: 20px 0;
    }
    .difficulty-option {
        padding: 10px 20px;
        border-radius: 5px;
        cursor: pointer;
    }
    .difficulty-option:hover {
        transform: translateY(-2px);
    }
    </style>
    """, unsafe_allow_html=True)
    
    difficulty = st.select_slider(
        "Select Difficulty",
        options=["Easy", "Medium", "Hard"],
        value="Medium",
        help="Adjusts board size and number of mines"
    )
    
    difficulty_settings = {
        "Easy": {"size": 6, "mines": 6, "color": "#4CAF50"},
        "Medium": {"size": 8, "mines": 10, "color": "#FFC107"},
        "Hard": {"size": 10, "mines": 20, "color": "#F44336"}
    }
    
    # Initialize session state
    if 'board' not in st.session_state:
        st.session_state.board = None
        st.session_state.mines = None
        st.session_state.game_over = False
        st.session_state.game_won = False
        st.session_state.revealed = None
        st.session_state.flags = None
        st.session_state.moves = 0
        st.session_state.start_time = None
        st.session_state.powerups = 3

    def create_board(settings):
        """Create minesweeper board with given settings"""
        size = settings["size"]
        num_mines = settings["mines"]
        board = [[0 for _ in range(size)] for _ in range(size)]
        mines = set()
        
        while len(mines) < num_mines:
            x, y = random.randint(0, size-1), random.randint(0, size-1)
            if (x, y) not in mines:
                board[x][y] = -1
                mines.add((x, y))
        
        for x in range(size):
            for y in range(size):
                if board[x][y] != -1:
                    board[x][y] = count_adjacent_mines(board, x, y)
        
        return board, mines

    def count_adjacent_mines(board, x, y):
        """Count mines in adjacent cells"""
        mines = 0
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                nx, ny = x + dx, y + dy
                if 0 <= nx < len(board) and 0 <= ny < len(board):
                    if board[nx][ny] == -1:
                        mines += 1
        return mines

    def reveal_cell(x, y, board, revealed):
        """Recursively reveal cells"""
        if not (0 <= x < len(board) and 0 <= y < len(board)) or revealed[x][y]:
            return
        
        revealed[x][y] = True
        if board[x][y] == 0:
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    reveal_cell(x + dx, y + dy, board, revealed)

    # Game controls
    col1, col2, col3 = st.columns([2, 2, 1])
    
    with col1:
        if st.button("🎮 New Game", use_container_width=True):
            settings = difficulty_settings[difficulty]
            st.session_state.board, st.session_state.mines = create_board(settings)
            st.session_state.revealed = [[False for _ in range(settings["size"])] 
                                       for _ in range(settings["size"])]
            st.session_state.flags = [[False for _ in range(settings["size"])] 
                                    for _ in range(settings["size"])]
            st.session_state.game_over = False
            st.session_state.game_won = False
            st.session_state.moves = 0
            st.session_state.start_time = time.time()
            st.session_state.powerups = 3

    # Display game stats
    with col2:
        if st.session_state.board:
            elapsed_time = int(time.time() - st.session_state.start_time) if st.session_state.start_time else 0
            st.markdown(f"""
            <div style="text-align: center;">
                <p>⏱️ Time: {elapsed_time//60}m {elapsed_time%60}s</p>
                <p>🎯 Moves: {st.session_state.moves}</p>
                <p>💪 Powerups: {st.session_state.powerups}</p>
            </div>
            """, unsafe_allow_html=True)

    # Game board
    if st.session_state.board:
        st.markdown("""
        <style>
        .minesweeper-cell {
            width: 40px;
            height: 40px;
            margin: 2px;
            border-radius: 5px;
            font-weight: bold;
            transition: all 0.3s ease;
        }
        .mine { background-color: #ff4444 !important; }
        .revealed { background-color: #e6f3ff; }
        .hidden { background-color: #f0f0f0; }
        .minesweeper-cell:hover {
            transform: scale(1.05);
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        </style>
        """, unsafe_allow_html=True)
        
        settings = difficulty_settings[difficulty]
        for x in range(settings["size"]):
            cols = st.columns(settings["size"])
            for y in range(settings["size"]):
                with cols[y]:
                    cell_value = st.session_state.board[x][y]
                    is_revealed = st.session_state.revealed[x][y]
                    is_flagged = st.session_state.flags[x][y]
                    
                    if st.session_state.game_over and cell_value == -1:
                        st.markdown(f"""
                        <div class="minesweeper-cell mine">
                            {MINE_SVG}
                        </div>
                        """, unsafe_allow_html=True)
                    elif is_revealed:
                        color = "#1e88e5" if cell_value > 0 else "#4caf50"
                        st.markdown(f"""
                        <div class="minesweeper-cell revealed" 
                             style="color: {color};">
                            {cell_value if cell_value > 0 else ''}
                        </div>
                        """, unsafe_allow_html=True)
                    elif is_flagged:
                        if st.button('🚩', key=f'flag_{x}_{y}'):
                            st.session_state.flags[x][y] = False
                    else:
                        if st.button('?', key=f'{x}_{y}'):
                            if not st.session_state.game_over and not st.session_state.game_won:
                                st.session_state.moves += 1
                                if cell_value == -1:
                                    st.session_state.game_over = True
                                    st.error("💥 BOOM! Game Over!")
                                else:
                                    reveal_cell(x, y, st.session_state.board, st.session_state.revealed)
                                    revealed_cells = sum(row.count(True) for row in st.session_state.revealed)
                                    update_activity_progress(wallet_address, 'Minesweeper', 2, 
                                                          revealed_cells, settings["size"]**2)
                                    
                                    # Check win condition
                                    safe_cells = settings["size"]**2 - len(st.session_state.mines)
                                    if revealed_cells == safe_cells:
                                        st.session_state.game_won = True
                                        game_time = int(time.time() - st.session_state.start_time)
                                        st.markdown(f"""
                                        <div style="text-align: center; animation: victory 1s infinite;">
                                            🎊 Congratulations! You've won! 🎊<br>
                                            Time: {game_time//60}m {game_time%60}s
                                        </div>
                                        """, unsafe_allow_html=True)
                                        st.balloons()
                                        
                                        # Achievement checks
                                        if game_time < 60:
                                            update_achievement(wallet_address, 'speed_demon')
                                        if not any(any(row) for row in st.session_state.flags):
                                            update_achievement(wallet_address, 'expert')
                                        update_activity_progress(wallet_address, 'Minesweeper', 1, 1, 1)

def games(wallet_address):
    """Main game selection and display"""
    # Display stats in sidebar
    display_stats(wallet_address)
    
    # Main game selection
    st.markdown("""
    <h1 style='text-align: center;'>🎮 Blockchain Games</h1>
    <style>
    .game-selector {
        animation: fadeIn 0.5s ease-in-out;
    }
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(-10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    </style>
    """, unsafe_allow_html=True)
    
    game_choice = st.selectbox(
        "Choose your game", 
        ["Puzzle NFT Game", "Minesweeper"],
        format_func=lambda x: f"🧩 {x}" if x == "Puzzle NFT Game" else f"💣 {x}"
    )
    
    if game_choice == "Puzzle NFT Game":
        game1_puzzle_nft(wallet_address)
    else:
        game2_minesweeper(wallet_address)

def update_achievement(wallet_address, achievement_type):
    """Update player achievements and display badge"""
    achievement = ACHIEVEMENTS['puzzle' if 'puzzle' in achievement_type else 'minesweeper'][achievement_type]
    st.markdown(create_achievement_badge(achievement['name'], achievement['desc']), unsafe_allow_html=True)
    update_activity_progress(wallet_address, 'achievements', achievement_type, 1, 1)