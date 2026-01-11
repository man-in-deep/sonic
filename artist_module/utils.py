"""
Utility functions for artist module
"""

import os
import uuid
from datetime import datetime
from PIL import Image
import pymysql
from dotenv import load_dotenv

load_dotenv()

class ImageProcessor:
    """Process images for artist module"""
    
    @staticmethod
    def save_uploaded_file(file, upload_folder):
        """Save uploaded file and return path"""
        if not os.path.exists(upload_folder):
            os.makedirs(upload_folder)
        
        # Generate unique filename
        filename = f"{uuid.uuid4().hex}_{file.filename}"
        filepath = os.path.join(upload_folder, filename)
        
        # Save file
        file.save(filepath)
        
        return filepath
    
    @staticmethod
    def validate_image(file):
        """Validate uploaded image"""
        allowed_extensions = {'jpg', 'jpeg', 'png', 'gif', 'webp'}
        
        if '.' not in file.filename:
            return False
        
        ext = file.filename.rsplit('.', 1)[1].lower()
        return ext in allowed_extensions
    
    @staticmethod
    def resize_image(image_path, max_size=1024):
        """Resize image if too large"""
        with Image.open(image_path) as img:
            width, height = img.size
            
            if max(width, height) > max_size:
                ratio = max_size / max(width, height)
                new_width = int(width * ratio)
                new_height = int(height * ratio)
                
                img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
                img.save(image_path)
        
        return image_path
    
    @staticmethod
    def image_to_base64(image_path):
        """Convert image to base64 string"""
        import base64
        with open(image_path, 'rb') as img_file:
            return base64.b64encode(img_file.read()).decode()

class DatabaseManager:
    """Manage database operations for artworks"""
    
    def __init__(self):
        self.connection = None
        self.connect()
    
    def connect(self):
        """Connect to MySQL database"""
        try:
            self.connection = pymysql.connect(
                host=os.getenv('DB_HOST', 'localhost'),
                port=int(os.getenv('DB_PORT', 3306)),
                user=os.getenv('DB_USER', 'sonic_ai_user'),
                password=os.getenv('DB_PASSWORD', 'sonic_ai_password_2024'),
                database=os.getenv('DB_NAME', 'sonic_ai'),
                charset='utf8mb4',
                cursorclass=pymysql.cursors.DictCursor
            )
            print("Database connected successfully")
        except Exception as e:
            print(f"Database connection failed: {e}")
            self.connection = None
    
    def save_artwork(self, artwork_data):
        """Save artwork to database"""
        if not self.connection:
            self.connect()
            if not self.connection:
                return False
        
        try:
            with self.connection.cursor() as cursor:
                sql = """
                INSERT INTO artworks (
                    user_id, user_prompt, reference_image_path, art_type, 
                    medium_style, model_used, stroke_sequence, 
                    generation_parameters, image_path, creation_duration
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
                
                cursor.execute(sql, (
                    artwork_data.get('user_id', 'anonymous'),
                    artwork_data['user_prompt'],
                    artwork_data.get('reference_image_path'),
                    artwork_data['art_type'],
                    artwork_data['medium_style'],
                    artwork_data['model_used'],
                    artwork_data.get('stroke_sequence'),
                    artwork_data.get('generation_parameters'),
                    artwork_data['image_path'],
                    artwork_data.get('creation_duration', 0)
                ))
            
            self.connection.commit()
            return True
            
        except Exception as e:
            print(f"Error saving artwork: {e}")
            return False
    
    def get_artwork_history(self, user_id=None, limit=10):
        """Get artwork history"""
        if not self.connection:
            self.connect()
            if not self.connection:
                return []
        
        try:
            with self.connection.cursor() as cursor:
                if user_id:
                    sql = "SELECT * FROM artworks WHERE user_id = %s ORDER BY created_at DESC LIMIT %s"
                    cursor.execute(sql, (user_id, limit))
                else:
                    sql = "SELECT * FROM artworks ORDER BY created_at DESC LIMIT %s"
                    cursor.execute(sql, (limit,))
                
                return cursor.fetchall()
                
        except Exception as e:
            print(f"Error fetching artwork history: {e}")
            return []
    
    def close(self):
        """Close database connection"""
        if self.connection:
            self.connection.close()

class StyleTranslator:
    """Translate user inputs to AI generation parameters"""
    
    @staticmethod
    def get_generation_parameters(art_type, medium_style):
        """Get generation parameters based on art type and medium"""
        params = {
            'steps': 30,
            'guidance_scale': 7.5,
            'width': 1024,
            'height': 1024,
            'seed': -1
        }
        
        # Adjust based on art type
        if art_type in ['Realism', 'Impressionism']:
            params['steps'] = 40
            params['guidance_scale'] = 8.0
        elif art_type in ['Abstract Expressionism', 'Surrealism']:
            params['steps'] = 25
            params['guidance_scale'] = 9.0
        
        # Adjust based on medium
        if medium_style == 'Watercolor':
            params['guidance_scale'] = 6.5
        elif medium_style == 'Oil Paint':
            params['steps'] = 35
        
        return params