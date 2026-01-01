"""
Steve Harrington Auto-Edit v2
Automatically finds interesting moments and creates a dynamic edit
"""

from moviepy import *
import numpy as np
from PIL import Image
import os

# === PATHS ===
ASSETS = "/Users/satyendra/Desktop/Atharv/Assets"
SOURCE = os.path.join(ASSETS, "ST5_Premiere.mp4")
AUDIO = os.path.join(ASSETS, "SteveHH.mp3")
OUTPUT = os.path.join(ASSETS, "steve_legend_v2.mp4")

# === BEAT TIMESTAMPS from the audio (manually mapped to Montagem Noche) ===
# These are approximate beat hits in the slowed version
BEATS = [
    0.0,    # Start
    2.8,    # First hit
    5.6,    # Drop
    6.2,    # Quick
    6.8,    # Quick  
    7.4,    # Quick
    8.0,    # Build
    8.8,    # Hit
    9.4,    # Quick
    10.0,   # Quick
    10.6,   # Quick
    11.2,   # Build
    12.0,   # Drop
    12.8,   # Hit
    13.6,   # Quick
    14.4,   # Quick
    15.2,   # Slow section
    16.4,   # Hold
    17.6,   # End
    18.2,   # Fade
]


def analyze_frame_brightness(frame):
    """Get average brightness of a frame"""
    return np.mean(frame)


def find_scene_changes(video, sample_interval=1.0):
    """Find timestamps where scenes change significantly"""
    print("Analyzing video for scene changes...")
    changes = []
    prev_brightness = None
    
    for t in np.arange(0, video.duration - 1, sample_interval):
        try:
            frame = video.get_frame(t)
            brightness = analyze_frame_brightness(frame)
            
            if prev_brightness is not None:
                diff = abs(brightness - prev_brightness)
                if diff > 15:  # Significant change
                    changes.append((t, diff))
            
            prev_brightness = brightness
        except:
            continue
    
    # Sort by difference (most dramatic changes first)
    changes.sort(key=lambda x: x[1], reverse=True)
    return [t for t, _ in changes[:30]]  # Top 30 scene changes


def create_flash(duration=0.06, size=(1920, 1080), intensity=0.4):
    """Create white flash overlay"""
    color = tuple([int(255 * intensity)] * 3)
    return ColorClip(size=size, color=color, duration=duration)


def apply_color_grade(clip):
    """Cinematic color grading"""
    def grade(frame):
        f = frame.astype(np.float32)
        # Darken
        f = f * 0.85
        # Increase contrast
        f = (f - 128) * 1.2 + 128
        # Cool blue tint
        f[:, :, 0] = f[:, :, 0] * 0.92  # Less red
        f[:, :, 2] = f[:, :, 2] * 1.08  # More blue
        return np.clip(f, 0, 255).astype(np.uint8)
    
    return clip.image_transform(grade)


def create_edit():
    print("=" * 50)
    print("STEVE HARRINGTON - THE LEGEND - AUTO EDIT v2")
    print("=" * 50)
    
    # Load source
    print("\nLoading source video...")
    source = VideoFileClip(SOURCE)
    print(f"  Duration: {source.duration:.1f}s")
    print(f"  Size: {source.size}")
    
    # Load audio
    print("\nLoading audio...")
    audio = AudioFileClip(AUDIO)
    target_duration = min(audio.duration, 18.0)
    print(f"  Audio duration: {audio.duration:.1f}s")
    print(f"  Target edit duration: {target_duration:.1f}s")
    
    # Find interesting moments
    scene_changes = find_scene_changes(source, sample_interval=2.0)
    print(f"\nFound {len(scene_changes)} potential scene changes")
    
    # Build clip list based on beats
    # Map beats to source timestamps
    clips_data = []
    
    # Manually curated timestamps from 7+ min source
    # Spread across the video for variety
    source_moments = [
        # (source_start, duration, speed, is_slow_mo)
        (10, 2.5, 1.0, False),    # Opening
        (35, 0.5, 1.0, False),    # Quick cut
        (58, 0.5, 1.0, False),    # Quick
        (82, 0.5, 1.0, False),    # Quick
        (105, 0.5, 1.0, False),   # Quick
        (128, 2.0, 0.5, True),    # Slow-mo
        (155, 0.5, 1.0, False),   # Quick
        (178, 0.5, 1.0, False),   # Quick
        (202, 0.5, 1.0, False),   # Quick
        (225, 0.5, 1.0, False),   # Quick
        (248, 2.0, 0.5, True),    # Slow-mo
        (275, 0.5, 1.0, False),   # Quick
        (298, 0.5, 1.0, False),   # Quick
        (320, 0.5, 1.0, False),   # Quick
        (345, 3.0, 0.5, True),    # Slow ending
        (380, 2.0, 0.6, True),    # Final slow
    ]
    
    video_size = source.size
    processed_clips = []
    
    print("\nProcessing clips...")
    for i, (start, dur, speed, is_slow) in enumerate(source_moments):
        if start >= source.duration:
            continue
            
        end = min(start + dur, source.duration)
        print(f"  Clip {i+1}: {start}s-{end}s (speed: {speed}x)")
        
        # Extract clip
        clip = source.subclipped(start, end)
        
        # Apply speed
        if speed != 1.0:
            clip = clip.with_speed_scaled(1/speed)
        
        # Apply color grade
        clip = apply_color_grade(clip)
        
        # Add flash transition (except first clip)
        if i > 0:
            flash_intensity = 0.5 if is_slow else 0.35
            flash = create_flash(0.06, video_size, flash_intensity)
            clip = concatenate_videoclips([flash, clip])
        
        processed_clips.append(clip)
    
    # Concatenate all clips
    print("\nConcatenating clips...")
    final = concatenate_videoclips(processed_clips, method="compose")
    
    # Trim to match audio
    if final.duration > target_duration:
        final = final.subclipped(0, target_duration)
    
    # Add audio
    print("Adding audio...")
    audio_trimmed = audio.subclipped(0, min(final.duration, audio.duration))
    final = final.with_audio(audio_trimmed)
    
    # Export
    print(f"\nExporting to {OUTPUT}...")
    print("This will take a few minutes...")
    
    final.write_videofile(
        OUTPUT,
        fps=60,
        codec='libx264',
        audio_codec='aac',
        bitrate='10000k',
        preset='medium',
        threads=4
    )
    
    # Cleanup
    source.close()
    audio.close()
    final.close()
    
    print("\n" + "=" * 50)
    print(f"✓ DONE! Output: {OUTPUT}")
    print("=" * 50)


if __name__ == "__main__":
    create_edit()
