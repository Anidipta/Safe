import streamlit as st
import base64
from io import BytesIO
import matplotlib.pyplot as plt
from data.database import update_activity_progress, get_user_progress
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import plotly.graph_objects as go

LESSONS = {
    1: {
        "title": "Introduction to Blockchain",
        "emoji": "🔗",
        "sections": [
            {
                "title": "What is Blockchain?",
                "content": """
                A blockchain is a distributed digital ledger that stores data in blocks that are linked together chronologically.
                
                Key characteristics:
                - Decentralized
                - Immutable
                - Transparent
                - Secure
                
                Think of it as a chain of digital 'blocks' containing information, where each block is connected to the ones before and after it.
                """,
                "quiz": [
                    {
                        "question": "What is the main characteristic of blockchain technology?",
                        "options": [
                            "Centralized control",
                            "Decentralized structure",
                            "Single point of failure",
                            "Editable records"
                        ],
                        "correct": 1
                    }
                ]
            },
            {
                "title": "How Blockchain Works",
                "content": """
                Blockchain operates through a network of computers (nodes) that all maintain the same record of transactions.
                
                Process:
                1. Transaction is initiated
                2. Transaction is broadcast to network
                3. Nodes validate the transaction
                4. Transaction is added to a block
                5. Block is added to the chain
                """,
                "quiz": [
                    {
                        "question": "What must happen before a transaction is added to the blockchain?",
                        "options": [
                            "It must be validated by nodes",
                            "It must be printed on paper",
                            "It must be encrypted only",
                            "It must be deleted first"
                        ],
                        "correct": 0
                    }
                ]
            },
            {
                "title": "Blockchain Applications",
                "content": """
                Blockchain technology has numerous real-world applications across various industries.
                
                Common applications:
                - Cryptocurrency
                - Supply Chain Management
                - Healthcare Records
                - Voting Systems
                - Smart Contracts
                """,
                "quiz": [
                    {
                        "question": "Which is a real-world application of blockchain?",
                        "options": [
                            "Word Processing",
                            "Video Gaming only",
                            "Cryptocurrency",
                            "Email Service"
                        ],
                        "correct": 2
                    }
                ]
            }
        ]
    },
    2: {
        "title": "Cryptography Basics",
        "emoji": "🔐",
        "sections": [
            {
                "title": "Public Key Cryptography",
                "content": """
                Public key cryptography is a fundamental concept in blockchain technology.
                
                Key Components:
                - Public Key: Shared with everyone
                - Private Key: Kept secret
                - Digital Signatures
                - Encryption/Decryption
                """,
                "quiz": [
                    {
                        "question": "Which key must be kept secret in public key cryptography?",
                        "options": [
                            "Public Key",
                            "Private Key",
                            "Master Key",
                            "Shared Key"
                        ],
                        "correct": 1
                    }
                ]
            },
            {
                "title": "Hash Functions",
                "content": """
                Hash functions are crucial for blockchain security and data integrity.
                
                Properties:
                - One-way function
                - Deterministic
                - Fast computation
                - Avalanche effect
                """,
                "quiz": [
                    {
                        "question": "What is a key property of hash functions?",
                        "options": [
                            "Reversible",
                            "Random output",
                            "Deterministic",
                            "Slow computation"
                        ],
                        "correct": 2
                    }
                ]
            },
            {
                "title": "Digital Signatures",
                "content": """
                Digital signatures provide authentication and non-repudiation in blockchain.
                
                Uses:
                - Transaction verification
                - Identity proof
                - Message authentication
                - Smart contract execution
                """,
                "quiz": [
                    {
                        "question": "What is the main purpose of digital signatures?",
                        "options": [
                            "Data encryption",
                            "Authentication",
                            "Data storage",
                            "Network speed"
                        ],
                        "correct": 1
                    }
                ]
            }
        ]
    }
}

def create_certificate(lesson_number, wallet_address):
    """Create a certificate as a PIL Image"""
    # Create a new image with a white background
    width = 800
    height = 600
    image = Image.new('RGB', (width, height), 'white')
    draw = ImageDraw.Draw(image)
    
    # Add decorative border
    draw.rectangle([(20, 20), (width-20, height-20)], outline='#4ecdc4', width=2)
    
    # Add certificate content
    title_text = "Certificate of Completion"
    lesson_text = f"Lesson {lesson_number}: {LESSONS[lesson_number]['title']}"
    completion_text = "has successfully completed"
    date_text = "Date: " + st.session_state.get('current_date', '')
    wallet_text = f"Wallet: {wallet_address[:6]}...{wallet_address[-4:]}"
    
    # Add text to image
    # Note: In production, you'd need to specify proper font paths
    draw.text((width//2, 100), title_text, fill='#333333', anchor="mm")
    draw.text((width//2, 200), lesson_text, fill='#4ecdc4', anchor="mm")
    draw.text((width//2, 300), completion_text, fill='#333333', anchor="mm")
    draw.text((width//2, 400), wallet_text, fill='#666666', anchor="mm")
    draw.text((width//2, 500), date_text, fill='#666666', anchor="mm")
    
    return image

def get_certificate_download_link(image):
    """Generate a download link for the certificate"""
    buffered = BytesIO()
    image.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    href = f'<a href="data:image/png;base64,{img_str}" download="certificate.png">Download Certificate</a>'
    return href

def create_blockchain_visualization():
    """Create an interactive blockchain visualization using Plotly"""
    fig = go.Figure()
    
    # Create blocks
    for i in range(4):
        fig.add_trace(go.Scatter(
            x=[i, i+0.8, i+0.8, i, i],
            y=[0, 0, 1, 1, 0],
            fill="toself",
            fillcolor='rgba(78, 205, 196, 0.2)',
            line=dict(color='#4ecdc4'),
            name=f'Block {i}',
            hoverinfo='text',
            text=f'Block {i}'
        ))
        
        # Add arrows between blocks
        if i < 3:
            fig.add_annotation(
                x=i+0.9,
                y=0.5,
                ax=i+1.1,
                ay=0.5,
                xref='x',
                yref='y',
                axref='x',
                ayref='y',
                text='',
                showarrow=True,
                arrowhead=2,
                arrowsize=1.5,
                arrowwidth=2,
                arrowcolor='#4ecdc4'
            )
    
    fig.update_layout(
        showlegend=False,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        margin=dict(l=20, r=20, t=20, b=20)
    )
    
    return fig

def display_interactive_content(section):
    """Display interactive content based on section"""
    st.markdown(f"### {section['title']}")
    
    # Add interactive visualizations based on content
    if "blockchain" in section['title'].lower():
        st.plotly_chart(create_blockchain_visualization(), use_container_width=True)
    
    # Display content with enhanced formatting
    st.markdown(f"""
        <div style='background-color: rgba(40, 40, 40, 0.9); 
                    padding: 20px; 
                    border-radius: 8px; 
                    border: 1px solid #4ecdc4;'>
            {section['content']}
        </div>
    """, unsafe_allow_html=True)
    
    # Add interactive elements
    if "characteristics" in section['content'].lower():
        for char in ["Decentralized", "Immutable", "Transparent", "Secure"]:
            if st.button(f"Learn more about {char}", key=f"learn_{char}"):
                st.info(f"Detailed explanation about {char} characteristic would appear here.")

def display_progress_chart(progress_data):
    """Display an interactive progress chart"""
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=list(progress_data.keys()),
        y=list(progress_data.values()),
        marker_color='#4ecdc4'
    ))
    
    fig.update_layout(
        title="Your Learning Progress",
        xaxis_title="Sections",
        yaxis_title="Completion %",
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )
    
    st.plotly_chart(fig, use_container_width=True)

def display_progress_bar(lesson_number, current_section, total_sections):
    """
    Display a stylized progress bar for lesson progression
    
    Args:
        lesson_number (int): Current lesson number
        current_section (int): Current section number
        total_sections (int): Total number of sections in the lesson
    """
    # Calculate progress percentage
    progress = (current_section / total_sections) * 100
    
    # Create progress bar container with custom styling
    st.markdown("""
        <style>
            .progress-container {
                background-color: rgba(30, 30, 30, 0.9);
                padding: 20px;
                border-radius: 8px;
                margin: 20px 0;
                border: 1px solid #4ecdc4;
            }
            .progress-stats {
                color: #ffffff;
                margin-bottom: 10px;
                display: flex;
                justify-content: space-between;
            }
            .progress-bar {
                width: 100%;
                height: 10px;
                background-color: rgba(78, 205, 196, 0.2);
                border-radius: 5px;
                overflow: hidden;
            }
            .progress-fill {
                height: 100%;
                background: linear-gradient(90deg, #4ecdc4, #556270);
                transition: width 0.3s ease;
            }
        </style>
        
        <div class="progress-container">
            <div class="progress-stats">
                <span>Lesson {lesson_number} Progress</span>
                <span>{current_section}/{total_sections} Sections</span>
            </div>
            <div class="progress-bar">
                <div class="progress-fill" style="width: {progress}%;"></div>
            </div>
        </div>
    """, unsafe_allow_html=True)

def lessons(wallet_address):
    # Apply custom styling
    st.markdown("""
        <style>
            .stApp {
                color: #ffffff;
            }
            
            .stButton button {
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 5px;
                transition: all 0.3s ease;
            }
            .stButton button:hover {
                transform: translateY(-2px);
                box-shadow: 0 4px 12px rgba(78, 205, 196, 0.2);
            }
        </style>
    """, unsafe_allow_html=True)

    if 'logged_in' in st.session_state and st.session_state.logged_in:
        st.title("🎓 Interactive Blockchain Learning Path")
        
        # Get user progress
        progress = get_user_progress(wallet_address, "lesson")
        
        # Initialize session states
        if 'current_lesson' not in st.session_state:
            st.session_state.current_lesson = 1
            st.session_state.current_section = 0
            st.session_state.current_date = st.date_input("", value=None)

        # Display progress overview
        col1, col2 = st.columns([3, 1])
        with col1:
            lesson_choice = st.selectbox(
                "Select a Lesson",
                range(1, len(LESSONS) + 1),
                format_func=lambda x: f"{LESSONS[x]['emoji']} Lesson {x}: {LESSONS[x]['title']}"
            )
            st.session_state.current_lesson = lesson_choice
        
        with col2:
            current_progress = progress.get('current_progress', 0)
            st.markdown(f"""
                <div style='padding: 20px; text-align: center; 
                     background-color: rgba(30, 30, 30, 0.9); 
                     border-radius: 10px; 
                     border: 2px solid #4ecdc4;'>
                    <h4 style='color: #4ecdc4;'>Progress</h4>
                    <h2 style='color: #ffffff;'>{current_progress}%</h2>
                </div>
            """, unsafe_allow_html=True)

        # Display interactive lesson content
        current_lesson = LESSONS[lesson_choice]
        
        st.markdown(f"""
            <div class='lesson-card'>
                <h2 style='color: #4ecdc4;'>{current_lesson['emoji']} {current_lesson['title']}</h2>
                <p style='color: #ffffff;'>Sections: {len(current_lesson['sections'])}</p>
                <p style='color: #ffffff;'>Points: {len(current_lesson['sections']) * 10}</p>
            </div>
        """, unsafe_allow_html=True)

        # Reset section when changing lessons
        if 'prev_lesson' not in st.session_state or st.session_state.prev_lesson != lesson_choice:
            st.session_state.current_section = 0
            st.session_state.prev_lesson = lesson_choice

        current_section = current_lesson['sections'][st.session_state.current_section]
        
        # Display progress bar
        display_progress_bar(
            lesson_choice,
            st.session_state.current_section + 1,
            len(current_lesson['sections'])
        )

        # Display interactive content
        display_interactive_content(current_section)

        # Display quiz with enhanced UI
        if 'quiz' in current_section:
            st.markdown("### 📝 Knowledge Check")
            for idx, question in enumerate(current_section['quiz']):
                st.markdown(f"""
                    <div style='background-color: rgba(40, 40, 40, 0.9); 
                         padding: 15px; 
                         border-radius: 5px; 
                         margin: 10px 0;
                         border: 1px solid #4ecdc4;'>
                        <p style='color: #fff; font-weight: bold;'>{question['question']}</p>
                    </div>
                """, unsafe_allow_html=True)
                
                answer = st.radio(
                    "Select your answer:",
                    question['options'],
                    key=f"quiz_{lesson_choice}_{st.session_state.current_section}_{idx}"
                )
                
                if st.button("Submit Answer", key=f"check_{lesson_choice}_{st.session_state.current_section}_{idx}"):
                    if answer == question['options'][question['correct']]:
                        st.success("✅ Excellent! You got it right!")
                        progress_percentage = ((st.session_state.current_section + 1) * 100) // len(current_lesson['sections'])
                        update_activity_progress(
                            wallet_address=wallet_address,
                            activity_type="lesson",
                            sl_no=lesson_choice,
                            completion=progress_percentage,
                            points=10
                        )
                    else:
                        st.error("❌ Not quite right. Try again!")

        # Navigation and completion
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col1:
            if st.session_state.current_section > 0:
                if st.button("← Previous", use_container_width=True):
                    st.session_state.current_section -= 1
                    st.rerun()
        
        with col3:
            if st.session_state.current_section < len(current_lesson['sections']) - 1:
                if st.button("Next →", use_container_width=True):
                    st.session_state.current_section += 1
                    st.rerun()
            elif current_progress == 100:
                if st.button("🎉 Complete & Get Certificate", use_container_width=True):
                    certificate = create_certificate(lesson_choice, wallet_address)
                    st.image(certificate, caption="Your Certificate of Completion")
                    st.markdown(get_certificate_download_link(certificate), unsafe_allow_html=True)

        # Display completion certificate if lesson is finished
        if current_progress == 100:
            st.markdown("""
                <div style='background-color: rgba(30, 30, 30, 0.9); 
                     padding: 20px; 
                     border-radius: 10px; 
                     text-align: center;
                     border: 2px solid; 
                     border-image: linear-gradient(45deg, #ff6b6b, #4ecdc4) 1;'>
                    <h2 style='color: #4ecdc4;'>🎉 Congratulations!</h2>
                    <p style='color: #fff;'>You've mastered this lesson. Keep up the great work!</p>
                </div>
            """, unsafe_allow_html=True)
