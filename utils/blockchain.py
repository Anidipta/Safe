from web3 import Web3
import streamlit as st
from eth_account import Account
from web3.exceptions import InvalidAddress
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class BlockchainConnection:
    def __init__(self):
        # Get sensitive information from environment variables
        infura_url = os.getenv("INFURA_URL")
        self.owner_address = os.getenv("OWNER_ADDRESS")
        self.private_key = os.getenv("PRIVATE_KEY")
        
        if not infura_url:
            st.error("INFURA_URL is not set in environment variables")
            raise Exception("INFURA_URL not set")
        
        if not self.owner_address or not self.private_key:
            st.error("Ethereum address or private key is not set in environment variables")
            raise Exception("Ethereum address or private key not set")

        # Connect to Ethereum network (Sepolia testnet in this case)
        self.w3 = Web3(Web3.HTTPProvider(infura_url))
        
        if not self.w3.is_connected():
            st.error("Failed to connect to Ethereum network")
            raise Exception("Failed to connect to Ethereum network")

    def validate_address(self, address):
        """Validate Ethereum address format"""
        try:
            return Web3.to_checksum_address(address)
        except (InvalidAddress, ValueError):
            return None

    def transfer_reward(self, to_address):
        """
        Transfer 0.001 test ETH to winner
        
        Args:
            to_address (str): Recipient's Ethereum address
            
        Returns:
            tuple: (success (bool), message (str))
        """
        try:
            # Validate recipient address
            valid_address = self.validate_address(to_address)
            if not valid_address:
                return False, "Invalid recipient address"

            # Validate owner address
            valid_owner = self.validate_address(self.owner_address)
            if not valid_owner:
                return False, "Invalid owner address"

            # Get the nonce
            nonce = self.w3.eth.get_transaction_count(valid_owner)
            
            # Create the transaction
            transaction = {
                'nonce': nonce,
                'to': valid_address,
                'value': self.w3.to_wei(0.001, 'ether'),
                'gas': 21000,
                'gasPrice': self.w3.eth.gas_price,
                'chainId': 11155111  # Sepolia chain ID
            }
            
            # Print transaction details for debugging (remove in production)
            print("Transaction details:", transaction)
            
            # Sign the transaction
            try:
                signed_txn = self.w3.eth.account.sign_transaction(
                    transaction, 
                    self.private_key
                )
            except Exception as e:
                return False, f"Transaction signing failed: {str(e)}"
            
            # Send the transaction
            try:
                tx_hash = self.w3.eth.send_raw_transaction(signed_txn.rawTransaction)
                receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)
                
                if receipt['status'] == 1:
                    tx_url = f"https://sepolia.etherscan.io/tx/{receipt.transactionHash.hex()}"
                    return True, tx_url
                else:
                    return False, "Transaction failed"
                    
            except Exception as e:
                return False, f"Transaction sending failed: {str(e)}"
                
        except Exception as e:
            return False, f"Error: {str(e)}"

def get_blockchain():
    """Get or create blockchain connection singleton"""
    if 'blockchain' not in st.session_state:
        st.session_state.blockchain = BlockchainConnection()
    return st.session_state.blockchain

def blockchain():
    """Main function to get blockchain functionality"""
    blockchain_connection = get_blockchain()
    return blockchain_connection.transfer_reward
