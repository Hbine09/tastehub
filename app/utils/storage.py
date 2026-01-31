from google.cloud import storage
import os
from werkzeug.utils import secure_filename
import uuid

# Initialize Cloud Storage client
storage_client = storage.Client()
BUCKET_NAME = 'cloudbite-menu-images'

def upload_image(file, folder='menu'):
    """
    Upload an image file to Google Cloud Storage
    
    Args:
        file: File object from request.files
        folder: Folder name in the bucket (default: 'menu')
    
    Returns:
        Public URL of the uploaded file or None if upload fails
    """
    try:
        if not file:
            return None
        
        # Get the bucket
        bucket = storage_client.bucket(BUCKET_NAME)
        
        # Generate unique filename
        filename = secure_filename(file.filename)
        unique_filename = f"{folder}/{uuid.uuid4()}_{filename}"
        
        # Create blob and upload
        blob = bucket.blob(unique_filename)
        blob.upload_from_file(file, content_type=file.content_type)
        
        # Make the blob publicly accessible
        blob.make_public()
        
        # Return public URL
        return blob.public_url
        
    except Exception as e:
        print(f"Error uploading image: {e}")
        return None


def delete_image(image_url):
    """
    Delete an image from Google Cloud Storage
    
    Args:
        image_url: Public URL of the image to delete
    
    Returns:
        True if deleted successfully, False otherwise
    """
    try:
        # Extract blob name from URL
        # URL format: https://storage.googleapis.com/bucket-name/blob-name
        if BUCKET_NAME not in image_url:
            return False
        
        blob_name = image_url.split(f'{BUCKET_NAME}/')[1]
        
        bucket = storage_client.bucket(BUCKET_NAME)
        blob = bucket.blob(blob_name)
        blob.delete()
        
        return True
        
    except Exception as e:
        print(f"Error deleting image: {e}")
        return False


def list_images(folder='menu'):
    """
    List all images in a folder
    
    Args:
        folder: Folder name in the bucket
    
    Returns:
        List of public URLs
    """
    try:
        bucket = storage_client.bucket(BUCKET_NAME)
        blobs = bucket.list_blobs(prefix=folder)
        
        urls = [blob.public_url for blob in blobs if not blob.name.endswith('/')]
        return urls
        
    except Exception as e:
        print(f"Error listing images: {e}")
        return []