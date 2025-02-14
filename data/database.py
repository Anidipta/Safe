import sqlite3
from datetime import datetime
from typing import Optional, Dict, Any
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Database constants
DB_NAME = "data/data.db"
ACTIVITY_TYPES = ('lesson', 'game')  # Changed to match the original schema

class DatabaseError(Exception):
    """Custom exception for database operations"""
    pass

def ensure_db_directory():
    """Ensure the database directory exists"""
    Path(DB_NAME).parent.mkdir(parents=True, exist_ok=True)

def get_db_connection() -> sqlite3.Connection:
    """Create and return a database connection with proper settings"""
    try:
        ensure_db_directory()
        conn = sqlite3.connect(DB_NAME)
        conn.row_factory = sqlite3.Row
        return conn
    except sqlite3.Error as e:
        logger.error(f"Database connection error: {e}")
        raise DatabaseError(f"Failed to connect to database: {e}")

def init_db():
    """Initialize the database with required tables"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Create the log_book table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS log_book (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                datetime TEXT NOT NULL,
                activity TEXT NOT NULL,
                metamask_account TEXT UNIQUE NOT NULL,
                name TEXT NOT NULL DEFAULT 'Guest',
                password TEXT NOT NULL
            )
        """)
        
        # Create the activity table - Note the CHECK constraint matches the ACTIVITY_TYPES
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS activity (
                wallet_address TEXT NOT NULL,
                activity_type TEXT NOT NULL CHECK(activity_type IN ('lesson', 'game')),
                sl_no INTEGER NOT NULL,
                completion INTEGER DEFAULT 0,
                points INTEGER DEFAULT 0,
                PRIMARY KEY (wallet_address, activity_type, sl_no)
            )
        """)

        conn.commit()
        logger.info("Database initialized successfully")
    except sqlite3.Error as e:
        logger.error(f"Database initialization error: {e}")
        raise DatabaseError(f"Failed to initialize database: {e}")
    finally:
        conn.close()

def add_user(metamask_account: str, password: str, activity: str, name: str = 'Guest') -> bool:
    """Add a new user to the database"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        cursor.execute("""
            INSERT INTO log_book (datetime, activity, metamask_account, name, password) 
            VALUES (?, ?, ?, ?, ?)
        """, (current_time, activity, metamask_account, name, password))
        
        conn.commit()
        logger.info(f"New user added: {metamask_account}")
        return True
    except sqlite3.IntegrityError:
        logger.warning(f"Attempted to add duplicate user: {metamask_account}")
        return False
    except sqlite3.Error as e:
        logger.error(f"Error adding user: {e}")
        raise DatabaseError(f"Failed to add user: {e}")
    finally:
        conn.close()

def check_user_exists(metamask_account: str) -> bool:
    """Check if a user exists in the database"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT 1 FROM log_book WHERE metamask_account = ?", 
            (metamask_account,)
        )
        exists = cursor.fetchone() is not None
        return exists
    except sqlite3.Error as e:
        logger.error(f"Error checking user existence: {e}")
        raise DatabaseError(f"Failed to check user existence: {e}")
    finally:
        conn.close()

def validate_user(metamask_account: str, password: str) -> bool:
    """Validate user credentials"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT 1 FROM log_book 
            WHERE metamask_account = ? AND password = ?
        """, (metamask_account, password))
        
        valid = cursor.fetchone() is not None
        
        if valid:
            logger.info(f"User logged in: {metamask_account}")
        
        return valid
    except sqlite3.Error as e:
        logger.error(f"Error validating user: {e}")
        raise DatabaseError(f"Failed to validate user: {e}")
    finally:
        conn.close()

def update_activity_progress(
    wallet_address: str, 
    activity_type: str, 
    sl_no: int, 
    completion: int, 
    points: int
) -> bool:
    """Update user's activity progress"""
    # Map activity types to database values
    activity_mapping = {
        'Puzzle NFT Game': 'game',
        'Minesweeper': 'game'
    }
    
    # Convert activity type to database value
    db_activity_type = activity_mapping.get(activity_type, activity_type)
    
    if db_activity_type not in ACTIVITY_TYPES:
        raise ValueError(f"Invalid activity type. Must map to one of: {ACTIVITY_TYPES}")
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Insert or update the record
        cursor.execute("""
            INSERT INTO activity (wallet_address, activity_type, sl_no, completion, points)
            VALUES (?, ?, ?, ?, ?)
            ON CONFLICT(wallet_address, activity_type, sl_no)
            DO UPDATE SET
                completion = excluded.completion,
                points = excluded.points
        """, (wallet_address, db_activity_type, sl_no, completion, points))
        
        conn.commit()
        logger.info(f"Activity progress updated: {wallet_address} - {activity_type} - {sl_no}")
        return True
    except sqlite3.Error as e:
        logger.error(f"Error updating activity progress: {e}")
        raise DatabaseError(f"Failed to update activity progress: {e}")
    finally:
        conn.close()

def get_user_progress(wallet_address: str, activity_type: str) -> Dict[str, Any]:
    """Get user's progress for a specific activity type"""
    # Map activity types to database values
    activity_mapping = {
        'Puzzle NFT Game': 'game',
        'Minesweeper': 'game'
    }
    
    # Convert activity type to database value
    db_activity_type = activity_mapping.get(activity_type, activity_type)
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT 
                COUNT(CASE WHEN completion = 100 THEN 1 END) as completed,
                SUM(points) as total_points,
                AVG(completion) as current_progress
            FROM activity
            WHERE wallet_address = ? AND activity_type = ?
        """, (wallet_address, db_activity_type))
        
        result = dict(cursor.fetchone())
        result['total_points'] = result['total_points'] or 0
        result['current_progress'] = round(result['current_progress'] or 0, 2)
        
        return result
    except sqlite3.Error as e:
        logger.error(f"Error fetching user progress: {e}")
        raise DatabaseError(f"Failed to fetch user progress: {e}")
    finally:
        conn.close()

