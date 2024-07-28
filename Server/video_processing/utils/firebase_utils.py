from uuid import uuid4
import os
import time
import random
import string
from ..config.firebase_config import db, storage, bucket, firestore

def upload_image_to_storage(file_path, board_id):
    """
    Upload an image to Firebase Storage.

    Args:
        file_path (str): Local path of the image file.
        board_id (str): ID of the board associated with the image.

    Returns:
        str: Public URL of the uploaded image.
    """
    original_filename = os.path.basename(file_path)
    extension = os.path.splitext(original_filename)[1]
    filename = f"{uuid4()}{extension}"
    blob = bucket.blob(f"boards/{board_id}/{filename}")
    blob.upload_from_filename(file_path, content_type="image/jpeg")
    blob.make_public()
    return blob.public_url

def board_exists(board_id):
    """
    Check if a board exists in Firestore.

    Args:
        board_id (str): ID of the board to check.

    Returns:
        bool: True if the board exists, False otherwise.
    """
    board_ref = db.collection("boards").document(board_id)
    board_doc = board_ref.get()
    return board_doc.exists

def create_board(board_id):
    """
    Create a new board in Firestore.

    Args:
        board_id (str): ID of the board to create.
    """
    board_data = {
        "created_at": firestore.SERVER_TIMESTAMP,
    }
    board_ref = db.collection("boards").document(board_id)
    board_ref.set(board_data)

def add_query_to_board(board_id, query_data):
    """
    Add a query to a board in Firestore.

    If the board doesn't exist, it will be created first.

    Args:
        board_id (str): ID of the board to add the query to.
        query_data (dict): Data of the query to add.
    """
    if not board_exists(board_id):
        create_board(board_id)
    
    query_id = generate_query_id()
    query_ref = (
        db.collection("boards")
        .document(board_id)
        .collection("queries")
        .document(query_id)
    )
    query_ref.set(query_data)

def generate_query_id():
    """
    Generate a unique query ID.

    The ID is a combination of a timestamp and a random string.

    Returns:
        str: A unique query ID.
    """
    timestamp = int(time.time())
    random_str = "".join(random.choices(string.ascii_lowercase + string.digits, k=6))
    return f"{timestamp}_{random_str}"