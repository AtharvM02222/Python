from PIL import Image, ImageDraw, ImageFont
from moviepy import VideoClip
import numpy as np
import os

# Settings
WIDTH, HEIGHT = 648, 584
FPS = 30
DURATION = 5.0
TEXT = "z_editz"
BAR_WIDTH = 6

# Create output directory
os.makedirs('editz/output', exist_ok=True)

# Load font - Avenir Next Condensed Italic for that futuristic look
try:
    font = ImageFont.truetype("/System/Library/Fonts/Avenir Next Condensed.ttc", 80)
except:
    font = ImageFont.load_default()
    print("Warning: Using default font")

def make_frame(t):
    img = Image.new('RGB', (WIDTH, HEIGHT), (0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    bbox = draw.textbbox((0, 0), TEXT, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    
    center_x = WIDTH // 2
    center_y = HEIGHT // 2
    
    # Animation phases
    text_alpha = 255
    bar_alpha = 255
    text_offset_x = 0
    
    if t < 1.0:
        text_alpha = int(255 * (t / 1.0))
        bar_alpha = text_alpha
    elif t < 3.0:
        text_alpha = 255
        bar_alpha = 255
    elif t < 4.0:
        progress = (t - 3.0) / 1.0
        text_offset_x = -int(progress * 150)
        text_alpha = int(255 * (1 - progress))
        bar_alpha = 255
    else:
        text_alpha = 0
        progress = (t - 4.0) / 1.0
        bar_alpha = int(255 * (1 - progress))
    
    text_x = center_x - text_width // 2 - 20 + text_offset_x
    text_y = center_y - text_height // 2
    
    if text_alpha > 0:
        txt_img = Image.new('RGBA', (WIDTH, HEIGHT), (0, 0, 0, 0))
        txt_draw = ImageDraw.Draw(txt_img)
        txt_draw.text((text_x, text_y), TEXT, font=font, fill=(255, 255, 255, text_alpha))
        img = Image.alpha_composite(img.convert('RGBA'), txt_img).convert('RGB')
        draw = ImageDraw.Draw(img)
    
    bar_x = center_x + text_width // 2 + 15
    bar_top = center_y - text_height // 2 - 10
    bar_bottom = center_y + text_height // 2 + 10
    
    if bar_alpha > 0:
        bar_color = (bar_alpha, bar_alpha, bar_alpha)
        draw.rectangle([bar_x, bar_top, bar_x + BAR_WIDTH, bar_bottom], fill=bar_color)
    
    return np.array(img)

print("Creating watermark video...")
clip = VideoClip(make_frame, duration=DURATION)
clip = clip.with_fps(FPS)
clip.write_videofile('editz/output/z_editz_watermark.mp4', codec='libx264', fps=FPS)
print("Done! Saved to editz/output/z_editz_watermark.mp4")
