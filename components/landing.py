import streamlit as st
from PIL import Image

# Inject custom CSS for enhanced visuals
def add_custom_css():
    st.markdown(
        """
        <style>
        /* General page styling */
        body {
            font-family: 'Arial', sans-serif;
            background: linear-gradient(to right, #1e3c72, #2a5298); /* Nebula blue */
            color: white;
        }
        .section-header {
            font-size: 24px;
            font-weight: bold;
            margin-top: 30px;
            color: #ff6ec4; /* Vibrant pink */
            text-align: center;
            text-shadow: 2px 2px 4px #000;
        }
        .text-section {
            font-size: 16px;
            margin: 20px 10px;
            text-align: justify;
        }
        .text-section a {
            color: #ff6ec4;
            text-decoration: none;
        }
        .text-section a:hover {
            text-decoration: underline;
        }
        .hover-card {
            border-radius: 10px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
            transition: transform 0.2s;
            padding: 20px;
            background: rgba(255, 255, 255, 0.1);
        }
        .hover-card:hover {
            transform: scale(1.01);
        }
        /* Infinite running text effect */
        .running-text {
            font-size: 18px;
            white-space: nowrap;
            overflow: hidden;
            width: 100%;
            text-align: center;
            background: rgba(255, 255, 255, 0.1);
            padding: 10px 0;
        }
        @keyframes marquee {
            0% { transform: translateX(100%); }
            100% { transform: translateX(-100%); }
        }
        /* Gradient text */
        .gradient-text {
            background: linear-gradient(to right, #ff6ec4, #ffca6e);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-weight: bold;
        }
        /* Centered button */
        .center-button {
            display: flex;
            justify-content: center;
            margin-top: 20px;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

# Function for the landing page
def landing():
    add_custom_css()

    # Running text at the top
    st.markdown(
        """
        <div class="running-text">
            🌟 Welcome to Crypton - Your Gateway to Blockchain Mastery 🌟
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.title("Welcome to Crypton")
    st.markdown(
        """
        <div class="text-section"><h4>
        <span class="gradient-text">Crypton</span> is your gateway to mastering cryptocurrency, learning about the blockchain, 
        and exploring Web3 technologies. Connect your wallet to get started!
        </h4>
        </div>
        """,
        unsafe_allow_html=True,
    )
    
    # Load and display logo
    logo = Image.open("assets/icons/logo.png")
    original_width, original_height = logo.size
    scaled_width = int(original_width * 0.45)
    scaled_height = int(original_height * 0.45)
    image_resized = logo.resize((scaled_width, scaled_height))
    st.image(image_resized, use_container_width=False)

    # Purpose Section with motion cards
    st.markdown('<div class="section-header">Purpose</div>', unsafe_allow_html=True)
    st.markdown(
        """
        <div class="hover-card">
        Crypton is a blockchain-based educational game designed to help beginners explore and understand blockchain concepts, 
        including NFTs, DeFi, and more, through interactive and fun games.
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Pipeline Section
    st.markdown('<div class="section-header">Pipeline</div>', unsafe_allow_html=True)
    st.markdown(
        """
        <div class="hover-card">
        <ul>
            <li>User selects a game or lesson.</li>
            <li>Interactive content explains blockchain concepts.</li>
            <li>Simulations demonstrate blockchain mechanics.</li>
            <li>Rewards like NFTs and tokens are awarded for progress.</li>
            <li>Users track their progress on an intuitive dashboard.</li>
        </ul>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # How to Play Section
    st.markdown('<div class="section-header">How to Play</div>', unsafe_allow_html=True)
    st.markdown(
        """
        <div class="hover-card">
        <ul>
            <li>Navigate to the "Games" section from the menu.</li>
            <li>Complete the challenges to earn rewards.</li>
            <li>Unlock badges and NFTs as you progress.</li>
            <li>Have fun while learning blockchain concepts!</li>
        </ul>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # How to Connect Section
    st.markdown('<div class="section-header">How to Connect</div>', unsafe_allow_html=True)
    st.markdown(
        """
        <div class="hover-card">
        <ul>
            <li>Sign up using your email or a Web3 wallet.</li>
            <li>Start exploring lessons and games right away!</li>
            <li>Follow your progress via the dashboard.</li>
        </ul>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Call-to-action button
    st.markdown('<div class="center-button">', unsafe_allow_html=True)
    if st.button("Get Started"):
        from components.login import signup
        signup()
    st.markdown('</div>', unsafe_allow_html=True)
