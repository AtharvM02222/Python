"""
Steve Harrington "The Legend" Style Edit
Using MoviePy for programmatic video editing

This script creates a stylized edit with:
- Beat-synced cuts
- Speed ramps (slow-mo effects)
- Zoom/scale keyframes
- Flash effects
- Color grading
"""

from moviepy import *
import numpy as np
import os

# === FILE PATHS ===
ASSETS_DIR = "/Users/satyendra/Desktop/Atharv/Assets"
SOURCE_VIDEO = os.path.join(ASSETS_DIR, "ST5_Premiere.mp4")
AUDIO_FILE = os.path.join(ASSETS_DIR, "SteveHH.mp3")
OUTPUT_FILE = os.path.join(ASSETS_DIR, "steve_legend_output.mp4")

# === BEAT TIMESTAMPS (in seconds) - adjust these to match your audio ===
# These are the moments where cuts/effects should hit
BEATS = [
    0.0, 2.5, 5.6, 6.2, 6.6, 7.0, 7.6, 8.8, 9.4, 10.0,
    10.4, 11.0, 11.4, 12.2, 12.8, 13.6, 14.2, 14.8, 15.2, 16.2, 17.4, 18.2
]

# === CLIP DEFINITIONS ===
# Each tuple: (start_time_in_source, end_time_in_source, speed_multiplier)
# Source video is 467s long
# CUSTOMIZE THESE TIMESTAMPS after first render

CLIPS = [
    # (start, end, speed) - speed < 1 = slow-mo, speed > 1 = fast
    # Opening - longer establishing shot
    (5, 8, 1.0),         # Scene 1: Opening ~3s
    
    # Quick cuts section (beat drops)
    (25, 26, 1.0),       # Scene 2: Quick 
    (45, 46, 1.0),       # Scene 3: Quick
    (65, 66, 1.0),       # Scene 4: Quick
    
    # Slow-mo moment
    (85, 88, 0.5),       # Scene 5: Slow-mo (~6s output)
    
    # More quick cuts
    (105, 106, 1.0),     # Scene 6: Quick
    (125, 126, 1.0),     # Scene 7: Quick
    (145, 146, 1.0),     # Scene 8: Quick
    
    # Another slow-mo
    (165, 167, 0.5),     # Scene 9: Slow-mo
    
    # Final quick cuts
    (185, 186, 1.0),     # Scene 10: Quick
    (205, 206, 1.0),     # Scene 11: Quick
    
    # Ending slow-mo + freeze
    (225, 228, 0.6),     # Scene 12: Slow ending
]


def create_flash(duration=0.08, size=(1920, 1080)):
    """Create a white flash frame"""
    return ColorClip(size=size, color=(255, 255, 255), duration=duration)


def apply_zoom_effect(clip, zoom_start=1.0, zoom_end=1.15):
    """Apply a gradual zoom effect to a clip"""
    def zoom_func(get_frame, t):
        frame = get_frame(t)
        progress = t / clip.duration
        current_zoom = zoom_start + (zoom_end - zoom_start) * progress
        
        h, w = frame.shape[:2]
        new_h, new_w = int(h / current_zoom), int(w / current_zoom)
        
        # Calculate crop coordinates (center crop)
        y1 = (h - new_h) // 2
        x1 = (w - new_w) // 2
        
        cropped = frame[y1:y1+new_h, x1:x1+new_w]
        
        # Resize back to original dimensions
        from PIL import Image
        img = Image.fromarray(cropped)
        img = img.resize((w, h), Image.LANCZOS)
        return np.array(img)
    
    return clip.transform(zoom_func)


def apply_color_grade(clip):
    """Apply cinematic color grading - dark, cool tones"""
    def color_filter(frame):
        # Convert to float for processing
        f = frame.astype(np.float32)
        
        # Reduce brightness slightly
        f = f * 0.9
        
        # Increase contrast
        f = (f - 128) * 1.15 + 128
        
        # Cool blue tint (reduce red, boost blue slightly)
        f[:, :, 0] = f[:, :, 0] * 0.95  # Red
        f[:, :, 2] = f[:, :, 2] * 1.05  # Blue
        
        # Clip values
        f = np.clip(f, 0, 255)
        return f.astype(np.uint8)
    
    return clip.image_transform(color_filter)


def create_edit():
    """Main function to create the edit"""
    print("Loading source video...")
    source = VideoFileClip(SOURCE_VIDEO)
    
    print(f"Source video duration: {source.duration}s")
    print(f"Source video size: {source.size}")
    
    # Get video dimensions
    video_size = source.size
    
    processed_clips = []
    
    print("\nProcessing clips...")
    for i, (start, end, speed) in enumerate(CLIPS):
        print(f"  Processing clip {i+1}/{len(CLIPS)}: {start}s - {end}s")
        
        # Make sure we don't exceed source duration
        if start >= source.duration:
            print(f"    Skipping - start time exceeds source duration")
            continue
        end = min(end, source.duration)
        
        # Extract subclip
        clip = source.subclipped(start, end)
        
        # Apply speed change
        if speed != 1.0:
            clip = clip.with_speed_scaled(1/speed)  # MoviePy 2.x syntax
        
        # Apply color grading
        clip = apply_color_grade(clip)
        
        # Add flash at the beginning of each clip (except first)
        if i > 0:
            flash = create_flash(duration=0.06, size=video_size)
            clip = concatenate_videoclips([flash, clip])
        
        processed_clips.append(clip)
    
    print("\nConcatenating clips...")
    final_video = concatenate_videoclips(processed_clips, method="compose")
    
    # Load and add audio
    print("Adding audio...")
    if os.path.exists(AUDIO_FILE):
        audio = AudioFileClip(AUDIO_FILE)
        # Trim audio to match video length
        if audio.duration > final_video.duration:
            audio = audio.subclipped(0, final_video.duration)
        final_video = final_video.with_audio(audio)
    else:
        print(f"  Warning: Audio file not found at {AUDIO_FILE}")
    
    # Export
    print(f"\nExporting to {OUTPUT_FILE}...")
    print("This may take a few minutes...")
    
    final_video.write_videofile(
        OUTPUT_FILE,
        fps=60,
        codec='libx264',
        audio_codec='aac',
        bitrate='8000k',
        preset='medium'
    )
    
    # Cleanup
    source.close()
    final_video.close()
    
    print(f"\n✓ Edit complete! Output saved to: {OUTPUT_FILE}")


if __name__ == "__main__":
    create_edit()
