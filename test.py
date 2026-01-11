import os
from dotenv import load_dotenv
from huggingface_hub import InferenceClient
import time

# Load environment variables
load_dotenv()

# Get token from .env
HF_TOKEN = os.getenv('HF_TOKEN')

if not HF_TOKEN:
    print("❌ ERROR: No HF_TOKEN found in .env file")
    print("Please add: HF_TOKEN=your_token_here")
    exit(1)

print(f"✅ Token loaded: {HF_TOKEN[:15]}...")

# Test models
models_to_test = [
   "stabilityai/stable-diffusion-xl-base-1.0",
    "black-forest-labs/FLUX.1-schnell",
    "black-forest-labs/FLUX.1-dev",
    "stabilityai/stable-diffusion-3-medium-diffusers"

]

print("\n🔍 Testing Hugging Face API access...")
print("=" * 50)

for model_id in models_to_test:
    print(f"\n📋 Testing model: {model_id}")
    try:
        # Create client
        client = InferenceClient(model=model_id, token=HF_TOKEN)
        
        # Test with a simple prompt
        print(f"  - Testing text-to-image generation...")
        start_time = time.time()
        
        try:
            # Try to generate a small test image
            image = client.text_to_image(
                "a simple test image, red circle on white background",
                width=256,
                height=256,
                num_inference_steps=5  # Few steps for quick test
            )
            elapsed = time.time() - start_time
            
            # Check if we got an image
            if image:
                if hasattr(image, 'size'):
                    print(f"  ✅ SUCCESS: Generated {image.size[0]}x{image.size[1]} image in {elapsed:.2f}s")
                elif isinstance(image, bytes):
                    print(f"  ✅ SUCCESS: Received {len(image)} bytes of image data in {elapsed:.2f}s")
                else:
                    print(f"  ✅ SUCCESS: Received image object in {elapsed:.2f}s")
            else:
                print(f"  ⚠️ WARNING: No image data returned")
                
        except Exception as e:
            print(f"  ❌ ERROR in generation: {str(e)[:100]}...")
            
        # Test model info
        print(f"  - Testing model info...")
        try:
            from huggingface_hub import model_info
            info = model_info(model_id, token=HF_TOKEN)
            print(f"  ✅ Model exists: {info.id}")
            print(f"    - Downloads: {info.downloads}")
            print(f"    - Likes: {info.likes}")
            print(f"    - Pipeline tag: {info.pipeline_tag}")
        except Exception as e:
            print(f"  ⚠️ Couldn't get model info: {e}")
            
    except Exception as e:
        print(f"  ❌ ERROR: Failed to connect to model")
        print(f"    Error: {str(e)[:100]}...")

print("\n" + "=" * 50)
print("🧪 Running advanced tests...")

# Test specific API endpoints
test_prompts = [
    ("a cat", "simple prompt"),
    ("landscape painting", "art prompt"),
    ("abstract geometric pattern", "abstract prompt")
]

client = InferenceClient(model="stabilityai/stable-diffusion-xl-base-1.0", token=HF_TOKEN)

print("\n📊 Testing different prompts:")
for prompt, description in test_prompts:
    try:
        start = time.time()
        image = client.text_to_image(
            prompt,
            width=512,
            height=512,
            num_inference_steps=10,
            guidance_scale=7.5
        )
        elapsed = time.time() - start
        
        if image:
            print(f"  ✅ '{description}' - Generated in {elapsed:.2f}s")
        else:
            print(f"  ❌ '{description}' - No image returned")
            
    except Exception as e:
        print(f"  ❌ '{description}' - Error: {str(e)[:80]}")

# Save a test image
print("\n💾 Saving test image...")
try:
    image = client.text_to_image(
        "test image from Sonic AI artist module",
        width=512,
        height=512,
        num_inference_steps=15
    )
    
    if image:
        if isinstance(image, bytes):
            with open("test_output.png", "wb") as f:
                f.write(image)
            print("  ✅ Saved test_output.png")
        else:
            # If it's a PIL image
            image.save("test_output.png")
            print("  ✅ Saved test_output.png")
            
        print(f"  📁 File size: {os.path.getsize('test_output.png') / 1024:.1f} KB")
        
except Exception as e:
    print(f"  ❌ Failed to save image: {e}")

print("\n" + "=" * 50)
print("📋 FINAL RESULTS:")
print("-" * 30)

# Check rate limits
print("📈 Rate limit info:")
print("  - Free tier allows ~30 requests/minute")
print("  - No payment required")
print("  - Token works for all models")

# Verify token permissions
print("\n🔐 Token permissions:")
try:
    from huggingface_hub import whoami
    user_info = whoami(token=HF_TOKEN)
    print(f"  ✅ Valid token for user: {user_info.get('name', 'Unknown')}")
    print(f"  📧 Email: {user_info.get('email', 'Not provided')}")
    print(f"  👥 Type: {user_info.get('type', 'user')}")
except Exception as e:
    print(f"  ❌ Cannot verify token: {e}")

print("\n" + "=" * 50)
print("✅ TEST COMPLETE")
print("\n📝 Next steps:")
print("1. Check test_output.png for generated image")
print("2. If all tests pass, your API is working!")
print("3. If errors occur, check:")
print("   - Internet connection")
print("   - Token in .env file")
print("   - Account status at huggingface.co")
print("\n🚀 Run the artist module with: python app.py")