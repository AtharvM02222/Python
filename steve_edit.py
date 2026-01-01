"""
Steve Harrington "The Legend" Edit - FROM SCRATCH
Phonk style edit with finez watermark
Based on the detailed scene breakdown
"""

from moviepy import *
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import os
import random

# ============ CONFIGURATION ============
PREMIERE_VIDEO = "/Users/satyendra/Desktop/Atharv/Assets/ST5_Premiere.mp4"
AUDIO_FILE = "/Users/satyendra/Desktop/Atharv/Assets/SteveHH.mp3"
OUTPUT_VIDEO = "/Users/satyendra/Desktop/Atharv/Assets/finez_steve_edit.mp4"

WATERMARK_TEXT = "finez"
WATERMARK_POSITION = "bottom-right"
WATERMARK_OPACITY = 0.8
WATERMARK_FONT_SIZE = 45

# Output settings
OUTPUT_WIDTH = 720
OUTPUT_HEIGHT = 1280  # 9:16 vertical for shorts
OUTPUT_FPS = 60


def create_watermark(size, text="finez", font_size=45, opacity=0.8):
    """Create stylish watermark with glow"""
    width, height = size
    img = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    try:
        font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", font_size)
    except:
        font = ImageFont.load_default()
    
    bbox = draw.textbbox((0, 0), text, font=font)
    text_w, text_h = bbox[2] - bbox[0], bbox[3] - bbox[1]
    
    # Bottom right position
    x = width - text_w - 25
    y = height - text_h - 25
    
    # Glow effect
    for offset in range(6, 0, -1):
        glow_alpha = int(20 * (7 - offset) / 6)
        glow_color = (255, 255, 255, glow_alpha)
        for dx, dy in [(-offset, 0), (offset, 0), (0, -offset), (0, offset)]:
            draw.text((x + dx, y + dy), text, font=font, fill=glow_color)
    
    # Main text
    alpha = int(255 * opacity)
    draw.text((x, y), text, font=font, fill=(255, 255, 255, alpha))
    
    return np.array(img)


def apply_vignette(frame, intensity=0.4):
    """Dark vignette effect"""
    h, w = frame.shape[:2]
    Y, X = np.ogrid[:h, :w]
    center_y, center_x = h / 2, w / 2
    dist = np.sqrt((X - center_x)**2 + (Y - center_y)**2)
    max_dist = np.sqrt(center_x**2 + center_y**2)
    vignette = 1 - (dist / max_dist) ** 2 * intensity
    vignette = np.clip(vignette, 0.4, 1)
    
    result = frame.astype(np.float32)
    for i in range(3):
        result[:, :, i] *= vignette
    return np.clip(result, 0, 255).astype(np.uint8)


def apply_color_grade(frame, tint="cool"):
    """Phonk color grading"""
    result = frame.astype(np.float32)
    
    # Boost contrast
    result = (result - 128) * 1.15 + 128
    
    if tint == "cool":
        result[:, :, 0] *= 0.92  # Less red
        result[:, :, 2] *= 1.12  # More blue
    elif tint == "warm":
        result[:, :, 0] *= 1.1   # More red
        result[:, :, 2] *= 0.95  # Less blue
    
    return np.clip(result, 0, 255).astype(np.uint8)


def create_flash_frame(size, intensity=1.0):
    """Create white flash frame"""
    w, h = size
    flash = np.ones((h, w, 3), dtype=np.uint8) * int(255 * intensity)
    return flash


def process_frame_cool(get_frame, t):
    """Process with cool tint + vignette"""
    frame = get_frame(t)
    frame = apply_color_grade(frame, "cool")
    frame = apply_vignette(frame, 0.45)
    return frame


def process_frame_warm(get_frame, t):
    """Process with warm tint + vignette"""
    frame = get_frame(t)
    frame = apply_color_grade(frame, "warm")
    frame = apply_vignette(frame, 0.4)
    return frame


def crop_to_vertical(clip, target_w=720, target_h=1280):
    """Crop clip to vertical 9:16 format, centered on subject"""
    w, h = clip.size
    
    # Calculate crop dimensions
    target_ratio = target_w / target_h
    current_ratio = w / h
    
    if current_ratio > target_ratio:
        # Video is wider - crop sides
        new_w = int(h * target_ratio)
        x1 = (w - new_w) // 2
        cropped = clip.cropped(x1=x1, x2=x1 + new_w)
    else:
        # Video is taller - crop top/bottom
        new_h = int(w / target_ratio)
        y1 = (h - new_h) // 2
        cropped = clip.cropped(y1=y1, y2=y1 + new_h)
    
    return cropped.resized((target_w, target_h))


def create_scene(source_clip, start_time, duration, effect="cool", speed=1.0, 
                 zoom_start=1.0, zoom_end=1.0, rotation=0):
    """Create a processed scene clip"""
    
    # Extract subclip
    end_time = min(start_time + duration * speed, source_clip.duration - 0.1)
    scene = source_clip.subclipped(start_time, end_time)
    
    # Apply speed change
    if speed != 1.0:
        scene = scene.with_speed_scaled(1/speed)
    
    # Crop to vertical
    scene = crop_to_vertical(scene, OUTPUT_WIDTH, OUTPUT_HEIGHT)
    
    # Apply color grading
    if effect == "cool":
        scene = scene.transform(process_frame_cool)
    elif effect == "warm":
        scene = scene.transform(process_frame_warm)
    
    # Apply zoom if needed
    if zoom_start != 1.0 or zoom_end != 1.0:
        def zoom_effect(get_frame, t):
            frame = get_frame(t)
            progress = t / scene.duration if scene.duration > 0 else 0
            current_zoom = zoom_start + (zoom_end - zoom_start) * progress
            
            if current_zoom != 1.0:
                h, w = frame.shape[:2]
                new_h, new_w = int(h * current_zoom), int(w * current_zoom)
                
                # Resize
                from PIL import Image
                img = Image.fromarray(frame)
                img = img.resize((new_w, new_h), Image.LANCZOS)
                
                # Crop center
                left = (new_w - w) // 2
                top = (new_h - h) // 2
                img = img.crop((left, top, left + w, top + h))
                frame = np.array(img)
            
            return frame
        scene = scene.transform(zoom_effect)
    
    return scene


def create_flash_clip(duration=0.05, size=(720, 1280), intensity=1.0):
    """Create a white flash clip"""
    flash_frame = create_flash_frame(size, intensity)
    return ImageClip(flash_frame).with_duration(duration)


def main():
    print("=" * 60)
    print("STEVE HARRINGTON 'THE LEGEND' EDIT")
    print("Creating from scratch with 'finez' watermark")
    print("=" * 60)
    
    # Check files exist
    if not os.path.exists(PREMIERE_VIDEO):
        print(f"ERROR: Premiere video not found: {PREMIERE_VIDEO}")
        return
    if not os.path.exists(AUDIO_FILE):
        print(f"ERROR: Audio not found: {AUDIO_FILE}")
        return
    
    print(f"\nLoading source video...")
    source = VideoFileClip(PREMIERE_VIDEO)
    print(f"Source: {source.duration:.1f}s, {source.size[0]}x{source.size[1]}")
    
    print(f"Loading audio...")
    audio = AudioFileClip(AUDIO_FILE)
    print(f"Audio: {audio.duration:.1f}s")
    
    # Total edit duration (match audio or ~18s)
    total_duration = min(audio.duration, 18.2)
    
    print(f"\nBuilding {total_duration:.1f}s edit...")
    
    # ============ SCENE TIMESTAMPS FROM SOURCE ============
    # These are approximate timestamps in the premiere footage
    # You may need to adjust these to find the best Steve shots
    
    # Find good Steve moments in the premiere (adjust these!)
    steve_timestamps = [
        5.0,    # Scene 1 - Steve shot
        15.0,   # Scene 2 - Another angle
        25.0,   # Scene 3 - Close up
        35.0,   # Scene 4 - Walking
        45.0,   # Scene 5 - Posing
        55.0,   # Scene 6 - Slow mo moment
        65.0,   # Scene 7 - Action
        75.0,   # Scene 8 - Close up
        85.0,   # Scene 9 - Beat hit
        95.0,   # Scene 10 - Slow mo
        105.0,  # Scene 11 - Quick cut
        115.0,  # Scene 12 - Neon moment
        125.0,  # Scene 13 - Zoom
        135.0,  # Scene 14 - Impact
        145.0,  # Scene 15 - Tilt
        155.0,  # Scene 16 - Slow end
        165.0,  # Scene 17 - Quick
        175.0,  # Scene 18 - Final slow
        185.0,  # Scene 19 - Freeze
    ]
    
    # Ensure timestamps are within source duration
    steve_timestamps = [t for t in steve_timestamps if t < source.duration - 2]
    
    # If not enough timestamps, generate more from available footage
    while len(steve_timestamps) < 19:
        steve_timestamps.append(random.uniform(10, source.duration - 5))
    steve_timestamps.sort()
    
    clips = []
    current_time = 0
    
    # ============ BUILD SCENES ============
    
    # Scene 1 (0:00-5.6s) - Opening with slow zoom
    print("  Scene 1: Opening shot with zoom...")
    scene1 = create_scene(source, steve_timestamps[0], 5.6, 
                          effect="cool", zoom_start=1.0, zoom_end=1.1)
    clips.append(scene1)
    
    # Flash at 2.5s
    flash1 = create_flash_clip(0.08).with_start(2.5)
    
    # Scene 2 (5.6-6.2s) - Quick cut
    print("  Scene 2: Quick cut...")
    scene2 = create_scene(source, steve_timestamps[1], 0.6, effect="cool")
    clips.append(scene2.with_start(5.6))
    
    # Scene 3 (6.2-6.6s) - Fast cut with shake feel
    print("  Scene 3: Fast cut...")
    scene3 = create_scene(source, steve_timestamps[2], 0.4, effect="cool")
    clips.append(scene3.with_start(6.2))
    
    # Flash
    flash2 = create_flash_clip(0.05).with_start(6.2)
    
    # Scene 4 (6.6-7.0s) - Glitch moment
    print("  Scene 4: Glitch cut...")
    scene4 = create_scene(source, steve_timestamps[3], 0.4, effect="cool")
    clips.append(scene4.with_start(6.6))
    
    flash3 = create_flash_clip(0.05).with_start(6.6)
    
    # Scene 5 (7.0-7.6s) - Zoom in
    print("  Scene 5: Zoom in...")
    scene5 = create_scene(source, steve_timestamps[4], 0.6, 
                          effect="warm", zoom_start=0.95, zoom_end=1.0)
    clips.append(scene5.with_start(7.0))
    
    # Scene 6 (7.6-8.8s) - SLOW MOTION
    print("  Scene 6: Slow motion...")
    scene6 = create_scene(source, steve_timestamps[5], 1.2, 
                          effect="cool", speed=0.5)
    clips.append(scene6.with_start(7.6))
    
    # Scene 7 (8.8-9.4s) - Action shot
    print("  Scene 7: Action...")
    scene7 = create_scene(source, steve_timestamps[6], 0.6, effect="cool")
    clips.append(scene7.with_start(8.8))
    
    flash4 = create_flash_clip(0.06).with_start(8.8)
    
    # Scene 8 (9.4-10.0s) - Close up with zoom out
    print("  Scene 8: Close up...")
    scene8 = create_scene(source, steve_timestamps[7], 0.6, 
                          effect="cool", zoom_start=1.1, zoom_end=1.0)
    clips.append(scene8.with_start(9.4))
    
    # Scene 9 (10.0-10.4s) - Beat hit
    print("  Scene 9: Beat hit...")
    scene9 = create_scene(source, steve_timestamps[8], 0.4, effect="cool")
    clips.append(scene9.with_start(10.0))
    
    flash5 = create_flash_clip(0.06).with_start(10.0)
    
    # Scene 10 (10.4-11.0s) - Slow mo warm
    print("  Scene 10: Slow mo warm...")
    scene10 = create_scene(source, steve_timestamps[9], 0.6, 
                           effect="warm", speed=0.5)
    clips.append(scene10.with_start(10.4))
    
    # Scene 11 (11.0-11.4s) - Quick spin feel
    print("  Scene 11: Quick cut...")
    scene11 = create_scene(source, steve_timestamps[10], 0.4, effect="cool")
    clips.append(scene11.with_start(11.0))
    
    # Scene 12 (11.4-12.2s) - Neon blue
    print("  Scene 12: Neon moment...")
    scene12 = create_scene(source, steve_timestamps[11], 0.8, effect="cool")
    clips.append(scene12.with_start(11.4))
    
    flash6 = create_flash_clip(0.05).with_start(11.4)
    
    # Scene 13 (12.2-12.8s) - Zoom in warm
    print("  Scene 13: Zoom warm...")
    scene13 = create_scene(source, steve_timestamps[12], 0.6, 
                           effect="warm", zoom_start=0.9, zoom_end=1.0)
    clips.append(scene13.with_start(12.2))
    
    # Scene 14 (12.8-13.6s) - Impact
    print("  Scene 14: Impact...")
    scene14 = create_scene(source, steve_timestamps[13], 0.8, effect="cool")
    clips.append(scene14.with_start(12.8))
    
    flash7 = create_flash_clip(0.05).with_start(12.8)
    
    # Scene 15 (13.6-14.2s) - Tilt
    print("  Scene 15: Tilt...")
    scene15 = create_scene(source, steve_timestamps[14], 0.6, effect="cool")
    clips.append(scene15.with_start(13.6))
    
    # Scene 16 (14.2-14.8s) - Slow end
    print("  Scene 16: Slow down...")
    scene16 = create_scene(source, steve_timestamps[15], 0.6, 
                           effect="cool", speed=0.6)
    clips.append(scene16.with_start(14.2))
    
    # Scene 17 (14.8-15.2s) - Quick black
    print("  Scene 17: Quick cut...")
    scene17 = create_scene(source, steve_timestamps[16], 0.4, effect="cool")
    clips.append(scene17.with_start(14.8))
    
    # Scene 18 (15.2-16.2s) - Final slow mo
    print("  Scene 18: Final slow mo...")
    scene18 = create_scene(source, steve_timestamps[17], 1.0, 
                           effect="cool", speed=0.5)
    clips.append(scene18.with_start(15.2))
    
    # Scene 19-20 (16.2-18.2s) - Freeze frame ending
    print("  Scene 19-20: Freeze frame ending...")
    scene19_base = create_scene(source, steve_timestamps[18], 0.5, effect="cool")
    
    # Get last frame and freeze it
    last_frame = scene19_base.get_frame(scene19_base.duration - 0.01)
    freeze_clip = ImageClip(last_frame).with_duration(2.0)
    freeze_clip = freeze_clip.with_start(16.2)
    clips.append(freeze_clip)
    
    flash8 = create_flash_clip(0.08).with_start(16.2)
    
    # Add all flashes
    flashes = [flash1, flash2, flash3, flash4, flash5, flash6, flash7, flash8]
    
    print("\nCompositing all scenes...")
    
    # Composite everything
    all_clips = clips + flashes
    video_composite = CompositeVideoClip(all_clips, size=(OUTPUT_WIDTH, OUTPUT_HEIGHT))
    video_composite = video_composite.with_duration(total_duration)
    
    # Add watermark
    print(f"Adding '{WATERMARK_TEXT}' watermark...")
    watermark_img = create_watermark((OUTPUT_WIDTH, OUTPUT_HEIGHT), WATERMARK_TEXT)
    watermark_clip = ImageClip(watermark_img).with_duration(total_duration)
    
    final_video = CompositeVideoClip([video_composite, watermark_clip])
    
    # Add audio
    print("Adding audio...")
    audio_clip = audio.subclipped(0, total_duration)
    final_video = final_video.with_audio(audio_clip)
    
    # Render
    print(f"\nRendering to: {OUTPUT_VIDEO}")
    print("This will take several minutes...")
    
    final_video.write_videofile(
        OUTPUT_VIDEO,
        codec='libx264',
        audio_codec='aac',
        fps=OUTPUT_FPS,
        preset='medium',
        threads=4,
        bitrate='8000k'
    )
    
    # Cleanup
    source.close()
    audio.close()
    final_video.close()
    
    print("\n" + "=" * 60)
    print("DONE!")
    print(f"Your edit saved to: {OUTPUT_VIDEO}")
    print("=" * 60)


if __name__ == "__main__":
    main()
