"""
AI Service for generating art using Hugging Face models
FIXED: JSON serialization issue
"""

import os
import time
import json
import base64
import random
from io import BytesIO
from datetime import datetime
from dotenv import load_dotenv
from PIL import Image, ImageDraw, ImageFilter
import numpy as np
import logging

# Hugging Face imports
from huggingface_hub import InferenceClient

# Load environment variables
load_dotenv()

logger = logging.getLogger(__name__)

class AIService:
    """Service for AI image generation using Hugging Face models"""
    
    # Model mapping based on art type
    MODEL_MAPPING = {
        'Impressionism': 'stabilityai/stable-diffusion-xl-base-1.0',
        'Cubism': 'black-forest-labs/FLUX.1-dev',
        'Expressionism': 'stabilityai/stable-diffusion-3-medium-diffusers',
        'Surrealism': 'black-forest-labs/FLUX.1-dev',
        'Pop Art': 'stabilityai/stable-diffusion-xl-base-1.0',
        'Realism': 'black-forest-labs/FLUX.1-schnell',
        'Abstract Expressionism': 'stabilityai/stable-diffusion-3-medium-diffusers',
        'Modernism/Contemporary': 'black-forest-labs/FLUX.1-dev'
    }
    
    # Style prompts for different art types
    STYLE_PROMPTS = {
        'Impressionism': ', impressionist style, loose brushstrokes, vibrant colors, light effects',
        'Cubism': ', cubist style, geometric shapes, multiple perspectives, fragmented forms',
        'Expressionism': ', expressionist style, emotional intensity, distorted forms, bold colors',
        'Surrealism': ', surrealist style, dreamlike, bizarre, symbolic, fantastical',
        'Pop Art': ', pop art style, bold colors, commercial art, popular culture',
        'Realism': ', realistic style, detailed, accurate depiction, photographic',
        'Abstract Expressionism': ', abstract expressionist style, gestural, non-representational, emotional',
        'Modernism/Contemporary': ', contemporary art style, experimental, conceptual, modern'
    }
    
    # Medium style prompts
    MEDIUM_PROMPTS = {
        'Oil Paint': ', oil painting, rich texture, glossy finish',
        'Acrylic Paint': ', acrylic painting, vibrant colors, matte finish',
        'Watercolor': ', watercolor painting, transparent, soft edges',
        'Gouache': ', gouache painting, opaque, matte finish',
        'Pastels': ', pastel drawing, soft, chalky texture',
        'Tempera': ', tempera painting, egg tempera, historical style',
        'Encaustic': ', encaustic painting, wax medium, textured',
        'Fresco': ', fresco painting, wall mural, traditional',
        'Ink Painting': ', ink painting, brush strokes, calligraphic',
        'Pencil Art': ', pencil drawing, graphite, detailed shading',
        'Digital Painting': ', digital art, clean lines, vibrant colors'
    }
    
    def __init__(self):
        """Initialize AI service with Hugging Face client"""
        self.hf_token = os.getenv('HF_TOKEN')
        if not self.hf_token:
            raise ValueError("HF_TOKEN not found in environment variables")
        
        logger.info("AIService initialized with Hugging Face token")
    
    def _get_client(self, model_id):
        """Get InferenceClient for specific model"""
        return InferenceClient(model=model_id, token=self.hf_token)
    
    def generate_art(self, prompt, art_type, medium_style, reference_image=None, negative_prompt=None):
        """
        Generate art based on prompt, art type, and medium style
        
        Args:
            prompt: User's description
            art_type: Selected art type
            medium_style: Selected medium/style
            reference_image: PIL Image object (optional)
            negative_prompt: What to avoid in generation
            
        Returns:
            dict: Generated image and metadata
        """
        try:
            start_time = time.time()
            
            # Get model based on art type
            model_id = self.MODEL_MAPPING.get(art_type, 'stabilityai/stable-diffusion-xl-base-1.0')
            
            # Enhance prompt with style and medium
            enhanced_prompt = self._enhance_prompt(prompt, art_type, medium_style)
            
            # Get negative prompt if not provided
            if negative_prompt is None:
                negative_prompt = self._get_negative_prompt(art_type, medium_style)
            
            logger.info(f"Generating art with model: {model_id}")
            logger.info(f"Enhanced prompt: {enhanced_prompt}")
            
            # Initialize client for this model
            client = self._get_client(model_id)
            
            # Generate image
            if reference_image is not None:
                # If reference image provided, use it as guidance
                image = self._generate_with_reference(
                    client, enhanced_prompt, reference_image, negative_prompt
                )
            else:
                # Generate from scratch
                image = client.text_to_image(
                    prompt=enhanced_prompt,
                    negative_prompt=negative_prompt,
                    num_inference_steps=30,
                    guidance_scale=7.5,
                    width=1024,
                    height=1024
                )
            
            # Apply medium-specific effects
            image = self._apply_medium_effects(image, medium_style)
            
            # Simulate quantum stroke effect
            image = self._simulate_quantum_strokes(image, art_type, medium_style)
            
            generation_time = time.time() - start_time
            
            # Convert to base64 for response
            buffered = BytesIO()
            image.save(buffered, format="PNG")
            img_str = base64.b64encode(buffered.getvalue()).decode()
            
            return {
                'success': True,
                'image_data': img_str,
                'model_used': model_id,
                'prompt': enhanced_prompt,
                'generation_time': generation_time,
                'art_type': art_type,
                'medium_style': medium_style,
                'quantum_strokes': True
            }
            
        except Exception as e:
            logger.error(f"Error generating art: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'image_data': None
            }
    
    def _enhance_prompt(self, prompt, art_type, medium_style):
        """Enhance user prompt with style and medium information"""
        style_prompt = self.STYLE_PROMPTS.get(art_type, '')
        medium_prompt = self.MEDIUM_PROMPTS.get(medium_style, '')
        
        # Quantum creativity enhancement
        quantum_enhancements = [
            "quantum-enhanced creativity",
            "stroke-by-stroke simulation",
            "physical media simulation",
            "artistic coherence"
        ]
        
        quantum_enhancement = random.choice(quantum_enhancements)
        
        enhanced = f"{prompt}{style_prompt}{medium_prompt}, {quantum_enhancement}"
        return enhanced
    
    def _get_negative_prompt(self, art_type, medium_style):
        """Get appropriate negative prompt based on style"""
        base_negative = "blurry, distorted, ugly, bad anatomy, watermark, signature"
        
        # Style-specific negatives
        if 'Realism' in art_type:
            base_negative += ", abstract, cartoon, anime"
        elif 'Abstract' in art_type:
            base_negative += ", photorealistic, realistic"
        
        return base_negative
    
    def _generate_with_reference(self, client, prompt, reference_image, negative_prompt):
        """Generate image with reference image guidance"""
        # Resize reference image if needed
        max_size = 1024
        if max(reference_image.size) > max_size:
            ratio = max_size / max(reference_image.size)
            new_size = tuple(int(dim * ratio) for dim in reference_image.size)
            reference_image = reference_image.resize(new_size, Image.Resampling.LANCZOS)
        
        # Convert to RGB if needed
        if reference_image.mode != 'RGB':
            reference_image = reference_image.convert('RGB')
        
        # Use image-to-image generation
        image = client.image_to_image(
            image=reference_image,
            prompt=prompt,
            negative_prompt=negative_prompt,
            num_inference_steps=30,
            strength=0.7,
            guidance_scale=7.5
        )
        
        return image
    
    def _apply_medium_effects(self, image, medium_style):
        """Apply medium-specific visual effects"""
        try:
            if medium_style == 'Watercolor':
                # Simulate watercolor effects
                image = image.filter(ImageFilter.GaussianBlur(radius=0.5))
                # Add paper texture
                paper_texture = self._create_paper_texture(image.size)
                image = Image.blend(image, paper_texture, alpha=0.1)
                
            elif medium_style == 'Oil Paint':
                # Simulate oil paint texture
                image = image.filter(ImageFilter.EDGE_ENHANCE_MORE)
                
            elif medium_style == 'Pencil Art':
                # Convert to pencil sketch
                image = self._convert_to_pencil_sketch(image)
                
            elif medium_style == 'Pastels':
                # Soft pastel effect
                image = image.filter(ImageFilter.SMOOTH_MORE)
                
        except Exception as e:
            logger.error(f"Error applying medium effects: {str(e)}")
            # Continue without effects if they fail
        
        return image
    
    def _create_paper_texture(self, size):
        """Create paper texture overlay"""
        # Create noise pattern
        texture = Image.new('RGB', size, color='white')
        draw = ImageDraw.Draw(texture)
        
        # Add subtle noise
        for _ in range(1000):
            x = random.randint(0, size[0]-1)
            y = random.randint(0, size[1]-1)
            gray = random.randint(230, 245)
            draw.point((x, y), fill=(gray, gray, gray))
        
        return texture
    
    def _convert_to_pencil_sketch(self, image):
        """Convert image to pencil sketch effect"""
        try:
            # Convert to grayscale
            grayscale = image.convert('L')
            
            # Invert
            inverted = Image.eval(grayscale, lambda x: 255 - x)
            
            # Apply Gaussian blur
            blurred = inverted.filter(ImageFilter.GaussianBlur(radius=2))
            
            # Dodge blend
            pencil_sketch = Image.blend(grayscale, blurred, alpha=0.5)
            
            # Convert back to RGB
            return pencil_sketch.convert('RGB')
        except Exception as e:
            logger.error(f"Error converting to pencil sketch: {str(e)}")
            return image
    
    def _simulate_quantum_strokes(self, image, art_type, medium_style):
        """Simulate quantum stroke effects on the image"""
        try:
            # This simulates the stroke-by-stroke drawing process
            # For now, we'll apply a subtle effect to simulate stroke rendering
            draw = ImageDraw.Draw(image)
            
            # Add subtle stroke marks based on art type
            if 'Expressionism' in art_type or 'Abstract' in art_type:
                # Add energetic stroke marks
                self._add_expressionist_strokes(draw, image.size)
            elif 'Realism' in art_type:
                # Add subtle texture strokes
                self._add_realistic_strokes(draw, image.size)
            
        except Exception as e:
            logger.error(f"Error simulating quantum strokes: {str(e)}")
            # Continue without stroke simulation if it fails
        
        return image
    
    def _add_expressionist_strokes(self, draw, size):
        """Add expressionist-style stroke marks"""
        for _ in range(50):
            x1 = random.randint(0, size[0]-1)
            y1 = random.randint(0, size[1]-1)
            length = random.randint(10, 50)
            angle = random.uniform(0, 2 * 3.14159)
            
            x2 = x1 + int(length * np.cos(angle))
            y2 = y1 + int(length * np.sin(angle))
            
            # Random yellow-gold stroke color
            color = random.choice([
                (255, 215, 0),  # Gold
                (255, 223, 0),  # Light gold
                (255, 200, 0)   # Dark gold
            ])
            
            # Semi-transparent stroke
            draw.line([(x1, y1), (x2, y2)], fill=color, width=1)
    
    def _add_realistic_strokes(self, draw, size):
        """Add realistic-style subtle strokes"""
        for _ in range(20):
            x = random.randint(0, size[0]-1)
            y = random.randint(0, size[1]-1)
            
            # Very subtle gold dots
            color = (255, 215, 0, 30)  # Semi-transparent gold
            
            radius = random.randint(1, 3)
            draw.ellipse([x-radius, y-radius, x+radius, y+radius], fill=color)