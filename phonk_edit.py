"""
Phonk Style Video Editor with Watermark
Creates a stylized edit with "finez" watermark
"""

from moviepy import *
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import os

# ============ CONFIGURATION ============
INPUT_VIDEO = "/Users/satyendra/Desktop/Atharv/Assets/＂The Legend🗿＂ - Steve Harrington 'Stranger Things 5 World premiere' Edit ｜ MONTAGEM NOCHE (Slowed) [1aJ2hJ48HU8].mp4"
OUTPUT_VIDEO = "/Users/satyendra/Desktop/Atharv/Assets/finez_edit.mp4"
WATERMARK_TEXT = "finez"

# Watermark settings
WATERMARK_POSITION = "bottom-right"  # Options: bottom-right, bottom-left, top-right, top-left, center
WATERMARK_OPACITY = 0.7
WATERMARK_FONT_SIZE = 50
WATERMARK_COLOR = (255, 255, 255)  # White

# Effect settings
ADD_VIGNETTE = True
ADD_COLOR_GRADE = True
CONTRAST_BOOST = 1.1


def create_text_watermark(text, size, font_size=50, color=(255, 255, 255)):
    """Create a text watermark image with glow effect"""
    width, height = size
    
    # Create transparent image
    img = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Try to use a cool font, fallback to default
    try:
        font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", font_size)
    except:
        try:
            font = ImageFont.truetype("/System/Library/Fonts/SFNSMono.ttf", font_size)
        except:
            font = ImageFont.load_default()
    
    # Get text bounding box
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    
    # Position based on setting
    padding = 30
    if WATERMARK_POSITION == "bottom-right":
        x = width - text_width - padding
        y = height - text_height - padding
    elif WATERMARK_POSITION == "bottom-left":
        x = padding
        y = height - text_height - padding
    elif WATERMARK_POSITION == "top-right":
        x = width - text_width - padding
        y = padding
    elif WATERMARK_POSITION == "top-left":
        x = padding
        y = padding
    else:  # center
        x = (width - text_width) // 2
        y = (height - text_height) // 2
    
    # Draw glow effect (multiple layers)
    glow_color = (color[0], color[1], color[2], 30)
    for offset in range(8, 0, -2):
        draw.text((x - offset, y), text, font=font, fill=glow_color)
        draw.text((x + offset, y), text, font=font, fill=glow_color)
        draw.text((x, y - offset), text, font=font, fill=glow_color)
        draw.text((x, y + offset), text, font=font, fill=glow_color)
    
    # Draw main text
    alpha = int(255 * WATERMARK_OPACITY)
    draw.text((x, y), text, font=font, fill=(color[0], color[1], color[2], alpha))
    
    return np.array(img)


def apply_vignette(frame):
    """Apply vignette effect to frame"""
    h, w = frame.shape[:2]
    
    # Create vignette mask
    Y, X = np.ogrid[:h, :w]
    center_y, center_x = h / 2, w / 2
    
    # Calculate distance from center (normalized)
    dist = np.sqrt((X - center_x)**2 + (Y - center_y)**2)
    max_dist = np.sqrt(center_x**2 + center_y**2)
    dist = dist / max_dist
    
    # Create vignette (darker at edges)
    vignette = 1 - (dist ** 2) * 0.5
    vignette = np.clip(vignette, 0.3, 1)
    
    # Apply to frame
    result = frame.astype(np.float32)
    for i in range(3):
        result[:, :, i] = result[:, :, i] * vignette
    
    return np.clip(result, 0, 255).astype(np.uint8)


def apply_color_grade(frame):
    """Apply phonk-style color grading (cool blue/teal tint with contrast)"""
    result = frame.astype(np.float32)
    
    # Boost contrast
    result = (result - 128) * CONTRAST_BOOST + 128
    
    # Add slight blue/teal tint
    result[:, :, 0] = result[:, :, 0] * 0.95  # Reduce red slightly
    result[:, :, 1] = result[:, :, 1] * 1.0   # Keep green
    result[:, :, 2] = result[:, :, 2] * 1.1   # Boost blue
    
    return np.clip(result, 0, 255).astype(np.uint8)


def process_frame(get_frame, t):
    """Apply all effects to a single frame"""
    frame = get_frame(t)
    result = frame
    
    if ADD_COLOR_GRADE:
        result = apply_color_grade(result)
    
    if ADD_VIGNETTE:
        result = apply_vignette(result)
    
    return result


def main():
    print("=" * 50)
    print("PHONK STYLE VIDEO EDITOR")
    print(f"Watermark: {WATERMARK_TEXT}")
    print("=" * 50)
    
    # Check if input exists
    if not os.path.exists(INPUT_VIDEO):
        print(f"ERROR: Input video not found at:\n{INPUT_VIDEO}")
        print("\nPlease update the INPUT_VIDEO path in the script.")
        return
    
    print(f"\nLoading video: {INPUT_VIDEO}")
    
    # Load the video
    video = VideoFileClip(INPUT_VIDEO)
    print(f"Video loaded: {video.duration:.2f}s, {video.size[0]}x{video.size[1]}")
    
    # Apply effects to video
    print("\nApplying effects (color grade + vignette)...")
    processed_video = video.transform(process_frame)
    
    # Create watermark
    print(f"Adding '{WATERMARK_TEXT}' watermark...")
    watermark_img = create_text_watermark(
        WATERMARK_TEXT, 
        video.size, 
        font_size=WATERMARK_FONT_SIZE,
        color=WATERMARK_COLOR
    )
    
    # Create watermark clip
    watermark_clip = ImageClip(watermark_img).with_duration(video.duration)
    
    # Composite video with watermark
    final_video = CompositeVideoClip([processed_video, watermark_clip])
    
    # Copy audio from original
    final_video = final_video.with_audio(video.audio)
    
    # Write output
    print(f"\nRendering to: {OUTPUT_VIDEO}")
    print("This may take a few minutes...")
    
    final_video.write_videofile(
        OUTPUT_VIDEO,
        codec='libx264',
        audio_codec='aac',
        fps=video.fps,
        preset='medium',
        threads=4
    )
    
    # Cleanup
    video.close()
    final_video.close()
    
    print("\n" + "=" * 50)
    print("DONE!")
    print(f"Output saved to: {OUTPUT_VIDEO}")
    print("=" * 50)


if __name__ == "__main__":
    main()
