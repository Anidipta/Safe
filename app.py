import streamlit as st
from components import dashboard, games, lessons, landing
from data import database
from wallet_connect import wallet_connect

# Set Page Configuration (this must be the first Streamlit command)
st.set_page_config(page_title="Crypton", layout="wide")

# Initialize Database
database.init_db()

# Initialize session state attributes if they don't exist
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "wallet_address" not in st.session_state:
    st.session_state.wallet_address = None
if "user_name" not in st.session_state:
    st.session_state.user_name = None
if "page" not in st.session_state:
    st.session_state.page = "Dashboard"
if "show_login_form" not in st.session_state:
    st.session_state.show_login_form = False
if "show_signup_form" not in st.session_state:
    st.session_state.show_signup_form = False


# Initialize Wallet Connect
with st.sidebar:
    wc = wallet_connect(label="wallet", key="wallet")
    
# Initialize wallet_address
wallet_address = None

# Default Landing Page
if not st.session_state.logged_in:
    landing.landing()  # Display the landing page before login/signup

    st.sidebar.title("🔗 Navigation")
    st.sidebar.markdown("### Connect Wallet:")

    # Connect Wallet
    if wc:
        if wc == True:
            wallet_address = wc.get_address()  # Retrieve the wallet address
            st.sidebar.success(f"Connected: {wallet_address}")

            # Auto-register or login if user is new or logged in
            if not database.check_user_exists(wallet_address):
                # Auto-register on wallet connect
                password = [wallet_address[-6], wallet_address[-5], wallet_address[-2], wallet_address[-1]].astype(int)
                database.add_user(wallet_address, password, "Auto Signup")
                st.sidebar.success(f"🆕 Auto registered with password: {password}")

            # Save user data in session state
            st.session_state.wallet_address = wallet_address
            st.session_state.logged_in = True
            st.session_state.user_name = wallet_address  # Optional: Replace with actual name if available

        else:
            st.sidebar.warning("Connect your wallet.")
    else:
        st.sidebar.warning("Connect your wallet.")

    # Sidebar - Login and Signup buttons side-by-side with unique keys
    login_signup_col1, login_signup_col2 = st.sidebar.columns(2)

    with login_signup_col1:
        show_login = st.button("Login", key="login_button")

    with login_signup_col2:
        show_signup = st.button("Sign Up", key="signup_button")

    # Conditional rendering for Login and Sign Up forms
    if show_login:
        st.session_state.show_login_form = True
        st.session_state.show_signup_form = False
    elif show_signup:
        st.session_state.show_login_form = False
        st.session_state.show_signup_form = True

    # Display Login form if the Login button is clicked
    if st.session_state.show_login_form:
        st.sidebar.markdown("### Login")
        login_address = st.sidebar.text_input("Metamask Address", key="login_address")  # Unique key for login address
        login_password = st.sidebar.text_input("Password", type="password", key="login_password")  # Unique key for login password

        if st.sidebar.button("Login", key="login_submit"):
            if database.validate_user(login_address, login_password):
                st.sidebar.success("Logged in successfully!")
                st.session_state.wallet_address = login_address
                st.session_state.logged_in = True
                st.session_state.user_name = login_address  # You can replace this with actual name if saved
            else:
                st.sidebar.error("Invalid credentials. Please check your address and password.")

    # Display Signup form if the Sign Up button is clicked
    if st.session_state.show_signup_form:
        st.sidebar.markdown("### Sign Up")
        signup_name = st.sidebar.text_input("Name", key="signup_name")  # Unique key for name input
        signup_address = st.sidebar.text_input("Metamask Address", key="signup_address")  # Unique key for signup address input
        signup_password = st.sidebar.text_input("Password (4 digits)", type="password", key="signup_password")  # Unique key for signup password input

        if st.sidebar.button("Sign Up", key="signup_submit"):
            if database.check_user_exists(signup_address):
                st.sidebar.error("Account exists. Please login.")
            elif len(signup_password) != 4 or not signup_password.isdigit():
                st.sidebar.error("Password must be exactly 4 digits.")
            else:
                database.add_user(signup_address, signup_password, "Manual Signup", signup_name)
                st.sidebar.success("Account created successfully! Please login.")
else:
    st.sidebar.success(f"Connected: {st.session_state.user_name}")
    st.sidebar.markdown("### Logout")
    if st.sidebar.button("Logout", key="logout_button"):
        # Clear session state and reset to initial state
        st.session_state.clear()
        st.sidebar.success("Logged out successfully!")
        st.rerun()

    st.markdown("### Select an Activity:")

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("📊 Dashboard", key="dashboard_button"):
            st.session_state.page = "Dashboard"
    with col2:
        if st.button("📚 Lessons", key="lessons_button"):
            st.session_state.page = "Lessons"
    with col3:
        if st.button("🎮 Games", key="games_button"):
            st.session_state.page = "Games"

    # Page Rendering
    if "page" not in st.session_state:
        st.session_state.page = "Dashboard"

    if st.session_state.page == "Dashboard":
        dashboard.dashboard(st.session_state.wallet_address)
    elif st.session_state.page == "Lessons":
        lessons.lessons(st.session_state.wallet_address)
    elif st.session_state.page == "Games":
        games.games(st.session_state.wallet_address)