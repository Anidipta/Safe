import streamlit as st
from web3 import Web3
import json
from eth_account.messages import encode_defunct
import time

class StreamlitWalletConnect:
    def __init__(self):
        # Initialize Web3 with your Infura endpoint
        INFURA_KEY = "3ea8bdfcd5b747bf81ec845624685679"
        self.w3 = Web3(Web3.HTTPProvider(f'https://mainnet.infura.io/v3/{INFURA_KEY}'))
        
        # Verify connection
        self.is_connected = self.w3.is_connected()
        if not self.is_connected:
            st.error("⚠️ Could not connect to Ethereum network")
        
        # Store connection state in session state
        if 'wallet_connected' not in st.session_state:
            st.session_state.wallet_connected = False
        if 'wallet_address' not in st.session_state:
            st.session_state.wallet_address = None
        if 'wallet_chain_id' not in st.session_state:
            st.session_state.wallet_chain_id = 1  # Mainnet

    def get_eth_balance(self, address):
        """Get ETH balance for an address"""
        try:
            balance_wei = self.w3.eth.get_balance(address)
            balance_eth = self.w3.from_wei(balance_wei, 'ether')
            return round(balance_eth, 4)
        except Exception as e:
            st.error(f"Error fetching balance: {str(e)}")
            return 0

    def generate_message(self):
        """Generate a unique message for signing"""
        timestamp = int(time.time())
        return f"Login to Crypton App\nTimestamp: {timestamp}\nChain: Ethereum Mainnet"

    def verify_signature(self, message, signature, address):
        """Verify that the signature is valid"""
        try:
            message_hash = encode_defunct(text=message)
            recovered_address = self.w3.eth.account.recover_message(message_hash, signature=signature)
            return recovered_address.lower() == address.lower()
        except Exception as e:
            st.error(f"Error verifying signature: {str(e)}")
            return False

    def connect_button(self):
        """Display the wallet connect button and handle connection"""
        if not st.session_state.wallet_connected:
            st.markdown("#### Connect Your Ethereum Wallet")
            
            # Network status indicator
            if self.is_connected:
                st.success("✅ Connected to Ethereum Mainnet")
            else:
                st.error("❌ Not connected to Ethereum network")
                return False
            
            connect_col1, connect_col2 = st.columns([3, 1])
            
            with connect_col1:
                wallet_address = st.text_input(
                    "Enter your Ethereum wallet address",
                    key="wallet_input",
                    placeholder="0x..."
                )
            
            with connect_col2:
                connect_clicked = st.button("Connect", key="connect_button")
                
            if connect_clicked and wallet_address:
                if self.w3.is_address(wallet_address):
                    # Show wallet info
                    balance = self.get_eth_balance(wallet_address)
                    st.info(f"Wallet Balance: {balance} ETH")
                    
                    # Generate message for signing
                    message = self.generate_message()
                    
                    # Display signing instructions
                    st.info(f"""
                    Please sign this message with MetaMask to verify wallet ownership:
                    
                    {message}
                    
                    Steps:
                    1. Open MetaMask
                    2. Click Sign when prompted
                    3. Copy the signature
                    4. Paste it below
                    """)
                    
                    # Get signature from user
                    signature = st.text_input("Signature:", key="signature_input")
                    
                    if signature:
                        if self.verify_signature(message, signature, wallet_address):
                            st.session_state.wallet_connected = True
                            st.session_state.wallet_address = wallet_address
                            st.success(f"✅ Successfully connected: {wallet_address[:6]}...{wallet_address[-4:]}")
                            return True
                        else:
                            st.error("❌ Invalid signature. Please try again.")
                else:
                    st.error("❌ Invalid Ethereum address format")
        else:
            # Show connected wallet info
            address = st.session_state.wallet_address
            balance = self.get_eth_balance(address)
            
            st.success(f"Connected: {address[:6]}...{address[-4:]}")
            st.info(f"Balance: {balance} ETH")
            
            if st.button("Disconnect", key="disconnect_button"):
                st.session_state.wallet_connected = False
                st.session_state.wallet_address = None
                st.rerun()
        
        return False

    def get_connected_address(self):
        """Return the connected wallet address"""
        return st.session_state.wallet_address if st.session_state.wallet_connected else None

    def is_wallet_connected(self):
        """Check if wallet is connected"""
        return st.session_state.wallet_connected