"""
Quantum stroke simulation for artistic rendering
FIXED: JSON serialization issues with numpy types
"""

import random
import math
import json
from PIL import Image, ImageDraw
import numpy as np

class QuantumStrokeSimulator:
    """Simulates quantum-enhanced stroke generation"""
    
    def __init__(self):
        self.stroke_sequences = []
        self.quantum_states = []
        
    def plan_strokes(self, image, art_type, medium_style):
        """Plan stroke sequence for drawing simulation"""
        strokes = []
        
        # Different stroke strategies based on art type
        if art_type == 'Impressionism':
            strokes = self._plan_impressionist_strokes(image)
        elif art_type == 'Cubism':
            strokes = self._plan_cubist_strokes(image)
        elif art_type == 'Realism':
            strokes = self._plan_realistic_strokes(image)
        else:
            strokes = self._plan_general_strokes(image)
        
        # Apply medium-specific properties
        strokes = self._apply_medium_properties(strokes, medium_style)
        
        # Add quantum randomness
        strokes = self._add_quantum_effects(strokes)
        
        # Convert all numpy types to Python native types for JSON serialization
        serializable_strokes = []
        for stroke in strokes:
            serializable_stroke = self._convert_to_serializable(stroke)
            serializable_strokes.append(serializable_stroke)
        
        return serializable_strokes
    
    def _convert_to_serializable(self, stroke_dict):
        """Convert numpy types to Python native types for JSON serialization"""
        serializable = {}
        for key, value in stroke_dict.items():
            if isinstance(value, np.integer):
                serializable[key] = int(value)
            elif isinstance(value, np.floating):
                serializable[key] = float(value)
            elif isinstance(value, np.ndarray):
                serializable[key] = value.tolist()
            elif isinstance(value, (list, tuple)):
                # Handle nested numpy arrays in lists/tuples
                if len(value) > 0 and isinstance(value[0], (np.integer, np.floating)):
                    serializable[key] = [float(v) if isinstance(v, np.floating) else int(v) for v in value]
                else:
                    serializable[key] = value
            elif key == 'color' and isinstance(value, tuple):
                # Convert color tuple to list
                serializable[key] = [int(v) if isinstance(v, (int, np.integer)) else v for v in value]
            elif isinstance(value, dict):
                serializable[key] = self._convert_to_serializable(value)
            else:
                serializable[key] = value
        return serializable
    
    def _plan_impressionist_strokes(self, image):
        """Plan impressionist-style short, visible strokes"""
        strokes = []
        width, height = image.size
        
        # Convert to numpy for analysis
        img_array = np.array(image)
        
        # Detect edges and high-contrast areas
        for y in range(0, height, 10):
            for x in range(0, width, 10):
                if random.random() > 0.7:  # 30% chance of stroke
                    length = random.randint(5, 15)
                    angle = random.uniform(0, 2 * math.pi)
                    
                    stroke = {
                        'type': 'brush',
                        'x': int(x),
                        'y': int(y),
                        'length': int(length),
                        'angle': float(angle),
                        'pressure': float(random.uniform(0.3, 0.8)),
                        'color': self._get_color_at(img_array, x, y),
                        'quantum_state': float(random.uniform(0, 1))
                    }
                    strokes.append(stroke)
        
        return strokes
    
    def _plan_cubist_strokes(self, image):
        """Plan cubist-style geometric strokes"""
        strokes = []
        width, height = image.size
        
        # Divide image into geometric regions
        regions = self._divide_geometric(width, height)
        
        for region in regions:
            # Each region gets strokes at different angles
            for angle in [0, 45, 90, 135]:
                stroke = {
                    'type': 'geometric',
                    'region': region,
                    'angle': float(angle),
                    'length': int(random.randint(20, 50)),
                    'pressure': 0.5,
                    'quantum_state': float(random.uniform(0, 1))
                }
                strokes.append(stroke)
        
        return strokes
    
    def _plan_realistic_strokes(self, image):
        """Plan realistic-style smooth strokes"""
        strokes = []
        width, height = image.size
        img_array = np.array(image)
        
        # Follow contours and gradients
        for y in range(0, height, 5):
            for x in range(0, width, 5):
                if random.random() > 0.9:  # 10% chance - detailed
                    # Longer, smoother strokes
                    stroke = {
                        'type': 'smooth',
                        'x': int(x),
                        'y': int(y),
                        'length': int(random.randint(10, 30)),
                        'angle': float(self._get_gradient_angle(img_array, x, y)),
                        'pressure': float(random.uniform(0.2, 0.6)),
                        'color': self._get_color_at(img_array, x, y),
                        'quantum_state': float(random.uniform(0, 1))
                    }
                    strokes.append(stroke)
        
        return strokes
    
    def _plan_general_strokes(self, image):
        """Plan general strokes for other art types"""
        strokes = []
        width, height = image.size
        img_array = np.array(image)
        
        for y in range(0, height, 8):
            for x in range(0, width, 8):
                if random.random() > 0.8:
                    stroke = {
                        'type': 'general',
                        'x': int(x),
                        'y': int(y),
                        'length': int(random.randint(8, 25)),
                        'angle': float(random.uniform(0, 2 * math.pi)),
                        'pressure': float(random.uniform(0.4, 0.7)),
                        'color': self._get_color_at(img_array, x, y),
                        'quantum_state': float(random.uniform(0, 1))
                    }
                    strokes.append(stroke)
        
        return strokes
    
    def _divide_geometric(self, width, height):
        """Divide image into geometric regions for cubism"""
        regions = []
        cell_size = 100
        
        for y in range(0, height, cell_size):
            for x in range(0, width, cell_size):
                regions.append({
                    'x': int(x),
                    'y': int(y),
                    'width': int(min(cell_size, width - x)),
                    'height': int(min(cell_size, height - y))
                })
        
        return regions
    
    def _get_color_at(self, img_array, x, y):
        """Get color at specific coordinates"""
        if 0 <= y < img_array.shape[0] and 0 <= x < img_array.shape[1]:
            color = img_array[y, x]
            # Convert numpy types to Python native types
            if isinstance(color, np.ndarray):
                return tuple(int(c) for c in color[:3])
            elif isinstance(color, (list, tuple)):
                return tuple(int(c) for c in color[:3])
            else:
                return (int(color), int(color), int(color))
        return (128, 128, 128)  # Default gray
    
    def _get_gradient_angle(self, img_array, x, y):
        """Calculate gradient angle for stroke direction"""
        # Simplified gradient calculation
        if y > 0 and x > 0 and y < img_array.shape[0]-1 and x < img_array.shape[1]-1:
            # Calculate simple gradient
            dy = float(img_array[y+1, x, 0] - img_array[y-1, x, 0])
            dx = float(img_array[y, x+1, 0] - img_array[y, x-1, 0])
            
            if dx != 0:
                angle = math.atan2(dy, dx)
            else:
                angle = math.pi / 2
        else:
            angle = random.uniform(0, 2 * math.pi)
        
        return float(angle)
    
    def _apply_medium_properties(self, strokes, medium_style):
        """Apply medium-specific properties to strokes"""
        medium_properties = {
            'Oil Paint': {'viscosity': 0.8, 'blending': 0.9, 'drying': 0.1},
            'Watercolor': {'viscosity': 0.3, 'blending': 0.7, 'drying': 0.8},
            'Pencil Art': {'viscosity': 0.1, 'blending': 0.4, 'drying': 0.9},
            'Digital Painting': {'viscosity': 0.5, 'blending': 1.0, 'drying': 0.0}
        }
        
        props = medium_properties.get(medium_style, {'viscosity': 0.5, 'blending': 0.7, 'drying': 0.5})
        
        for stroke in strokes:
            stroke['medium_properties'] = props
            # Adjust stroke properties based on medium
            stroke['pressure'] *= props['viscosity']
            stroke['length'] *= (1 + props['blending'] * 0.5)
            
            # Ensure types are Python native
            stroke['pressure'] = float(stroke['pressure'])
            stroke['length'] = int(stroke['length'])
        
        return strokes
    
    def _add_quantum_effects(self, strokes):
        """Add quantum randomness and entanglement effects"""
        # Quantum tunneling - some strokes appear in random locations
        for _ in range(int(len(strokes) * 0.1)):  # 10% quantum tunneling
            if strokes:
                base_stroke = random.choice(strokes)
                quantum_stroke = base_stroke.copy()
                quantum_stroke['x'] += random.randint(-50, 50)
                quantum_stroke['y'] += random.randint(-50, 50)
                quantum_stroke['quantum_state'] = float(random.uniform(0.8, 1.0))
                quantum_stroke['quantum_tunnel'] = True
                strokes.append(quantum_stroke)
        
        # Quantum entanglement - link related strokes
        for i in range(0, len(strokes), 5):
            if i + 1 < len(strokes):
                strokes[i]['entangled_with'] = i + 1
                strokes[i + 1]['entangled_with'] = i
        
        return strokes
    
    def simulate_stroke_rendering(self, image, strokes):
        """Simulate stroke-by-stroke rendering on canvas"""
        # Create a new image for stroke simulation
        stroke_image = Image.new('RGB', image.size, color='white')
        draw = ImageDraw.Draw(stroke_image)
        
        # Sort strokes for rendering order
        sorted_strokes = sorted(strokes, key=lambda s: s.get('pressure', 0.5))
        
        # Render each stroke
        for i, stroke in enumerate(sorted_strokes):
            try:
                # Calculate stroke coordinates
                x1 = stroke.get('x', 0)
                y1 = stroke.get('y', 0)
                length = stroke.get('length', 10)
                angle = stroke.get('angle', 0)
                
                # Ensure values are Python native types
                x1 = float(x1)
                y1 = float(y1)
                length = float(length)
                angle = float(angle)
                
                x2 = x1 + length * math.cos(angle)
                y2 = y1 + length * math.sin(angle)
                
                # Get stroke color
                color = stroke.get('color', (255, 215, 0))  # Default gold
                
                # Ensure color is tuple of ints
                if isinstance(color, (list, tuple)):
                    color = tuple(int(c) for c in color[:3])
                else:
                    color = (255, 215, 0)
                
                # Apply quantum effects
                if stroke.get('quantum_tunnel', False):
                    # Quantum tunneled strokes are semi-transparent
                    alpha = 128
                else:
                    alpha = int(255 * stroke.get('pressure', 0.5))
                
                # Draw stroke
                draw.line([(x1, y1), (x2, y2)], fill=color, width=2)
                
            except Exception as e:
                # Skip strokes that cause errors
                continue
        
        return stroke_image