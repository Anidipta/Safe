import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px

DB_NAME = "data/data.db"

# Function to fetch data from database
def fetch_user_data(wallet_address):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # Fetch user information
    user_info = cursor.execute(
        "SELECT name, password FROM log_book WHERE metamask_account = ?", (wallet_address,)
    ).fetchone()

    # Fetch activity stats
    activity_data = pd.read_sql_query(
        "SELECT * FROM activity WHERE wallet_address = ?", conn, params=(wallet_address,)
    )

    conn.close()
    return user_info, activity_data

# Function to update user information
def update_user_info(wallet_address, new_name=None, new_password=None):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    if new_name:
        cursor.execute(
            "UPDATE log_book SET name = ? WHERE metamask_account = ?", (new_name, wallet_address)
        )

    if new_password:
        cursor.execute(
            "UPDATE log_book SET password = ? WHERE metamask_account = ?", (new_password, wallet_address)
        )

    conn.commit()
    conn.close()

# Main Dashboard function
def dashboard(wallet_address):
    st.markdown(
        """
        <style>
            body {
                background-color: black;
                color: white;
            }
            .profile-card, .hover-card {
                background: #1E1E1E;
                padding: 20px;
                box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.4);
                color: white;
                margin-bottom: 20px;
                border-radius: 10px;
                border: 2px solid;
                border-image: linear-gradient(45deg, #ff6b6b, #4ecdc4) 1;
                margin: 10px 0;
                transition: transform 0.2s;
            }
            .hover-card:hover {
                transform: scale(1.01);
                transition: 0.3s ease-in-out;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # Fetch user data
    user_info, activity_data = fetch_user_data(wallet_address)

    if not user_info:
        st.error("User not found. Please log in again.")
        return

    user_name, password = user_info
    st.title("📊 Crypton Dashboard")
    st.subheader(f"Welcome, {user_name}!")

    # Profile Card
    st.markdown(
        f"""
        <div class="profile-card">
            <h3>{user_name}</h3>
            <p><strong>Wallet:</strong> {wallet_address}</p>
            <p><strong>Password:</strong> {'*' * len(password)}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Activity Summary
    if not activity_data.empty:
        st.subheader("Activity Summary")
        col1, col2, col3, col4 = st.columns(4)

        # Pie Chart for Completion
        with col1:
            activity_summary = activity_data.groupby("activity_type")["completion"].sum().reset_index()
            fig = px.pie(
                activity_summary,
                values="completion",
                names="activity_type",
                title="Completion by Activity Type",
                color_discrete_sequence=px.colors.sequential.RdBu,
            )
            st.plotly_chart(fig, use_container_width=True)

        # Bar Chart for Points
        with col2:
            points_summary = activity_data.groupby("activity_type")["points"].sum().reset_index()
            fig = px.bar(
                points_summary,
                x="activity_type",
                y="points",
                title="Points by Activity Type",
                text_auto=True,
                color="points",
                color_continuous_scale=px.colors.sequential.Plasma,
            )
            st.plotly_chart(fig, use_container_width=True)
            
        # Line Chart for Progression Over Activities
        with col3:
            fig = px.line(
                activity_data,
                x="sl_no",
                y="completion",
                title="Completion Progression Over Activities",
                markers=True,
                color="activity_type",
                line_shape="spline",
            )
            st.plotly_chart(fig, use_container_width=True)

        # Scatter Plot for Points vs. Completion
        with col4:
            fig = px.scatter(
                activity_data,
                x="completion",
                y="points",
                color="activity_type",
                size="points",
                title="Points vs. Completion",
                hover_data=["sl_no"],
            )
            st.plotly_chart(fig, use_container_width=True)
        
        user_info, activity_data = fetch_user_data(wallet_address)

    # Update Profile
    st.write("### Update Profile")
    with st.form("update_profile_form"):
        new_name = st.text_input("Update Name", value=user_name)
        new_password = st.text_input("Update Password", type="password")
        submit = st.form_submit_button("Update")

        if submit:
            update_user_info(wallet_address, new_name, new_password)
            st.success("Profile updated successfully!")
            st.rerun()

    # Footer
    st.markdown(
        """
        <footer style="text-align: center; margin-top: 20px; color: white;">
            <p>Powered by Crypton Blockchain Learning Platform</p>
        </footer>
        """,
        unsafe_allow_html=True,
    )


