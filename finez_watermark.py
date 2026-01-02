from PIL import Image, ImageDraw, ImageFont
from moviepy import VideoClip
import numpy as np
import os
import math

# Settings
WIDTH, HEIGHT = 600, 600
FPS = 60
DURATION = 5.0
TEXT = "finez_editz"
BAR_WIDTH = 8
BAR_HEIGHT = 100

# Output directory
os.makedirs('output', exist_ok=True)

# Load font
try:
    # Try Avenir Next Condensed Italic for modern look
    font = ImageFont.truetype("/System/Library/Fonts/Avenir Next Condensed.ttc", 60, index=1)
    print("Using Avenir Next Condensed")
except:
    try:
        font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 60)
        print("Using Helvetica")
    except:
        font = ImageFont.load_default()
        print("Using default font")

# Get text dimensions
temp_img = Image.new('RGB', (WIDTH, HEIGHT))
temp_draw = ImageDraw.Draw(temp_img)
bbox = temp_draw.textbbox((0, 0), TEXT, font=font)
TEXT_WIDTH = bbox[2] - bbox[0]
TEXT_HEIGHT = bbox[3] - bbox[1]

# Positions
CENTER_X = WIDTH // 2
CENTER_Y = HEIGHT // 2
TEXT_START_X = CENTER_X - TEXT_WIDTH // 2
BAR_START_X = TEXT_START_X - 30  # Bar starts left of text
BAR_END_X = TEXT_START_X + TEXT_WIDTH + 20  # Bar ends right of text

def ease_in_out(t):
    """Smooth easing function"""
    return t * t * (3 - 2 * t)

def make_frame(t):
    img = Image.new('RGBA', (WIDTH, HEIGHT), (0, 0, 0, 255))
    draw = ImageDraw.Draw(img)
    
    # Timeline:
    # 0.0 - 0.5s: Bar draws in (grows from 0 to full height)
    # 0.5 - 2.0s: Bar moves right, revealing text
    # 2.0 - 2.5s: Bar returns to start position
    # 2.5 - 3.5s: Hold (text + bar visible)
    # 3.5 - 4.5s: Bar moves right, text disappears
    # 4.5 - 5.0s: Bar fades out
    
    bar_height = BAR_HEIGHT
    bar_x = BAR_START_X
    bar_alpha = 255
    text_reveal = 0  # 0 = hidden, 1 = fully visible
    text_hide = 0    # 0 = visible, 1 = fully hidden
    
    if t < 0.5:
        # Phase 1: Bar draws in
        progress = ease_in_out(t / 0.5)
        bar_height = int(BAR_HEIGHT * progress)
        text_reveal = 0
        
    elif t < 2.0:
        # Phase 2: Bar moves right, text reveals
        progress = ease_in_out((t - 0.5) / 1.5)
        bar_x = BAR_START_X + int((BAR_END_X - BAR_START_X) * progress)
        text_reveal = progress
        
    elif t < 2.5:
        # Phase 3: Bar returns to start
        progress = ease_in_out((t - 2.0) / 0.5)
        bar_x = BAR_END_X - int((BAR_END_X - BAR_START_X) * progress)
        text_reveal = 1
        
    elif t < 3.5:
        # Phase 4: Hold
        bar_x = BAR_START_X
        text_reveal = 1
        
    elif t < 4.5:
        # Phase 5: Bar moves right, text disappears
        progress = ease_in_out((t - 3.5) / 1.0)
        bar_x = BAR_START_X + int((BAR_END_X - BAR_START_X) * progress)
        text_reveal = 1
        text_hide = progress
        
    else:
        # Phase 6: Bar fades out
        progress = ease_in_out((t - 4.5) / 0.5)
        bar_x = BAR_END_X
        bar_alpha = int(255 * (1 - progress))
        text_reveal = 1
        text_hide = 1
    
    # Draw text with reveal/hide mask
    if text_reveal > 0 and text_hide < 1:
        text_y = CENTER_Y - TEXT_HEIGHT // 2
        
        # Create text layer
        txt_layer = Image.new('RGBA', (WIDTH, HEIGHT), (0, 0, 0, 0))
        txt_draw = ImageDraw.Draw(txt_layer)
        txt_draw.text((TEXT_START_X, text_y), TEXT, font=font, fill=(255, 255, 255, 255))
        
        # Create mask for reveal effect (text visible up to bar position)
        mask = Image.new('L', (WIDTH, HEIGHT), 0)
        mask_draw = ImageDraw.Draw(mask)
        
        # Reveal: show text from left edge to bar position
        reveal_x = int(TEXT_START_X + TEXT_WIDTH * text_reveal)
        # Hide: hide text from left edge based on hide progress
        hide_x = int(TEXT_START_X + TEXT_WIDTH * text_hide)
        
        # Draw visible region
        if hide_x < reveal_x:
            mask_draw.rectangle([hide_x, 0, reveal_x, HEIGHT], fill=255)
        
        # Apply mask
        txt_layer.putalpha(mask)
        img = Image.alpha_composite(img, txt_layer)
        draw = ImageDraw.Draw(img)
    
    # Draw vertical bar
    if bar_alpha > 0 and bar_height > 0:
        bar_top = CENTER_Y - bar_height // 2
        bar_bottom = CENTER_Y + bar_height // 2
        draw.rectangle(
            [bar_x, bar_top, bar_x + BAR_WIDTH, bar_bottom],
            fill=(255, 255, 255, bar_alpha)
        )
    
    # Convert to RGB for video
    rgb_img = Image.new('RGB', (WIDTH, HEIGHT), (0, 0, 0))
    rgb_img.paste(img, mask=img.split()[3])
    
    return np.array(rgb_img)

print("Creating finez_editz watermark...")
print(f"Text dimensions: {TEXT_WIDTH}x{TEXT_HEIGHT}")
print(f"Bar travel: {BAR_START_X} -> {BAR_END_X}")

clip = VideoClip(make_frame, duration=DURATION)
clip = clip.with_fps(FPS)
clip.write_videofile('output/finez_editz_watermark.mp4', codec='libx264', fps=FPS)
print("\nDone! Saved to output/finez_editz_watermark.mp4")
