"""
RECREATE TARGET EDIT
Uses the exact timing structure from target.mp4
Applies to YOUR clips from ST5_Premiere.mp4
"""

from moviepy import *
from moviepy.video import fx
import numpy as np
from PIL import Image
import os

# === PATHS ===
ASSETS = "/Users/satyendra/Desktop/Atharv/Assets"
SOURCE = os.path.join(ASSETS, "ST5_Premiere.mp4")
TARGET = os.path.join(ASSETS, "target.mp4")  # Reference for audio
OUTPUT = os.path.join(ASSETS, "steve_RECREATED.mp4")

# === EXACT TIMING FROM TARGET ANALYSIS ===
# (start_time, end_time, clip_type)
# SLOW = slow-motion section, FAST = rapid cuts, NORMAL = regular speed
EDIT_STRUCTURE = [
    (0.00, 0.57, "NORMAL"),   # Clip 1
    (0.57, 1.10, "NORMAL"),   # Clip 2
    (1.10, 1.63, "NORMAL"),   # Clip 3
    (1.63, 2.17, "NORMAL"),   # Clip 4
    (2.17, 3.27, "SLOW"),     # Clip 5 - slow-mo
    (3.27, 3.80, "NORMAL"),   # Clip 6
    (3.80, 5.47, "SLOW"),     # Clip 7 - slow-mo
    (5.47, 6.07, "NORMAL"),   # Clip 8
    (6.07, 6.57, "NORMAL"),   # Clip 9
    (6.57, 8.67, "SLOW"),     # Clip 10 - slow-mo
    (8.67, 9.23, "NORMAL"),   # Clip 11
    (9.23, 9.77, "NORMAL"),   # Clip 12
    (9.77, 9.97, "FAST"),     # Clip 13 - rapid
    (9.97, 10.13, "FAST"),    # Clip 14 - rapid
    (10.13, 10.30, "FAST"),   # Clip 15 - rapid
    (10.30, 10.93, "NORMAL"), # Clip 16
    (10.93, 11.40, "NORMAL"), # Clip 17 - has flash before
    (11.40, 11.93, "NORMAL"), # Clip 18
    (11.93, 12.10, "FAST"),   # Clip 19 - rapid
    (12.10, 12.27, "FAST"),   # Clip 20 - rapid
    (12.27, 12.43, "FAST"),   # Clip 21 - rapid
    (12.43, 12.53, "FAST"),   # Clip 22 - rapid
    (12.53, 12.70, "FAST"),   # Clip 23 - rapid
    (12.70, 13.57, "NORMAL"), # Clip 24
    (13.57, 14.10, "NORMAL"), # Clip 25
    (14.10, 15.23, "SLOW"),   # Clip 26 - slow-mo
    (15.23, 16.17, "NORMAL"), # Clip 27
    (16.17, 18.20, "SLOW"),   # Clip 28 - slow-mo ending with flash
]

# === YOUR SOURCE CLIP TIMESTAMPS ===
# Pick the best Steve moments from ST5_Premiere.mp4
# Format: (source_start_time, speed_factor)
# speed_factor: 0.5 = half speed (slow-mo), 1.0 = normal
YOUR_CLIPS = [
    (10, 1.0),    # 1 - Opening
    (35, 1.0),    # 2
    (60, 1.0),    # 3
    (85, 1.0),    # 4
    (110, 0.5),   # 5 - SLOW
    (140, 1.0),   # 6
    (165, 0.5),   # 7 - SLOW
    (200, 1.0),   # 8
    (225, 1.0),   # 9
    (250, 0.5),   # 10 - SLOW
    (285, 1.0),   # 11
    (310, 1.0),   # 12
    (335, 1.0),   # 13 - FAST
    (350, 1.0),   # 14 - FAST
    (365, 1.0),   # 15 - FAST
    (380, 1.0),   # 16
    (395, 1.0),   # 17
    (410, 1.0),   # 18
    (420, 1.0),   # 19 - FAST
    (430, 1.0),   # 20 - FAST
    (440, 1.0),   # 21 - FAST
    (445, 1.0),   # 22 - FAST
    (450, 1.0),   # 23 - FAST
    (25, 1.0),    # 24
    (50, 1.0),    # 25
    (75, 0.5),    # 26 - SLOW
    (100, 1.0),   # 27
    (125, 0.5),   # 28 - SLOW ending
]

# Flash timestamps (from target analysis)
FLASH_TIMES = [10.93, 16.17]


def create_flash(duration, size, intensity=0.95):
    """Create white flash frame"""
    c = tuple([int(255 * intensity)] * 3)
    return ColorClip(size=size, color=c, duration=duration)


def apply_color_grade(frame):
    """Match the dark, cinematic look of the target"""
    f = frame.astype(np.float32)
    
    # Darken
    f = f * 0.78
    
    # High contrast
    f = (f - 128) * 1.35 + 128
    
    # Cool blue shadows, slightly warm highlights
    shadow_mask = (np.mean(f, axis=2, keepdims=True) < 80)
    f[:, :, 0] = np.where(shadow_mask[:, :, 0], f[:, :, 0] * 0.88, f[:, :, 0])
    f[:, :, 2] = np.where(shadow_mask[:, :, 0], f[:, :, 2] * 1.12, f[:, :, 2])
    
    # Overall slight blue tint
    f[:, :, 0] = f[:, :, 0] * 0.94
    f[:, :, 2] = f[:, :, 2] * 1.06
    
    return np.clip(f, 0, 255).astype(np.uint8)


def create_edit():
    print("=" * 60)
    print("  RECREATING TARGET EDIT WITH YOUR CLIPS")
    print("=" * 60)
    
    # Load source
    print("\n[1/5] Loading source video...")
    source = VideoFileClip(SOURCE)
    print(f"      Source: {source.duration:.1f}s @ {source.size}")
    
    # Load target for audio
    print("\n[2/5] Loading target audio...")
    target = VideoFileClip(TARGET)
    audio = target.audio
    print(f"      Audio: {audio.duration:.1f}s")
    
    # Target size (match target aspect ratio 720x800 = 9:10)
    target_size = (720, 800)
    
    print(f"\n[3/5] Processing {len(EDIT_STRUCTURE)} clips...")
    processed_clips = []
    
    for i, ((out_start, out_end, clip_type), (src_start, speed)) in enumerate(zip(EDIT_STRUCTURE, YOUR_CLIPS)):
        target_duration = out_end - out_start
        
        # Calculate how much source footage we need
        src_duration = target_duration * speed
        
        # Ensure we don't exceed source
        if src_start + src_duration > source.duration:
            src_start = max(0, source.duration - src_duration - 1)
        
        print(f"      Clip {i+1:2d}/{len(EDIT_STRUCTURE)}: {out_start:.2f}-{out_end:.2f}s "
              f"[{clip_type:6s}] src={src_start}s speed={speed}x")
        
        # Extract clip
        clip = source.subclipped(src_start, src_start + src_duration)
        
        # Apply speed change for slow-mo
        if speed != 1.0:
            clip = clip.with_effects([fx.MultiplySpeed(speed)])
        
        # Trim to exact duration
        if clip.duration > target_duration:
            clip = clip.subclipped(0, target_duration)
        
        # Resize to target aspect ratio (center crop to 9:10)
        w, h = clip.size
        target_ratio = 9/10
        current_ratio = w/h
        
        if current_ratio > target_ratio:
            # Too wide, crop sides
            new_w = int(h * target_ratio)
            x_offset = (w - new_w) // 2
            clip = clip.cropped(x1=x_offset, x2=x_offset + new_w)
        else:
            # Too tall, crop top/bottom
            new_h = int(w / target_ratio)
            y_offset = (h - new_h) // 2
            clip = clip.cropped(y1=y_offset, y2=y_offset + new_h)
        
        # Resize to exact target size
        clip = clip.resized(target_size)
        
        # Apply color grading
        clip = clip.image_transform(apply_color_grade)
        
        # Add flash before certain clips
        if out_start in FLASH_TIMES or (i > 0 and EDIT_STRUCTURE[i-1][1] in [10.93]):
            flash = create_flash(0.03, target_size, 0.9)
            # Trim clip to make room for flash
            if clip.duration > 0.03:
                clip = clip.subclipped(0.03, clip.duration)
            clip = concatenate_videoclips([flash, clip])
        
        processed_clips.append(clip)
    
    # Concatenate all clips
    print("\n[4/5] Concatenating clips...")
    final = concatenate_videoclips(processed_clips, method="compose")
    
    print(f"      Final duration: {final.duration:.2f}s (target: 18.20s)")
    
    # Trim to exact target duration
    if final.duration > 18.20:
        final = final.subclipped(0, 18.20)
    
    # Add audio from target
    print("      Adding audio...")
    audio_trimmed = audio.subclipped(0, min(final.duration, audio.duration))
    final = final.with_audio(audio_trimmed)
    
    # Export
    print(f"\n[5/5] Exporting to {OUTPUT}...")
    print("      This will take a few minutes...")
    
    final.write_videofile(
        OUTPUT,
        fps=60,
        codec='libx264',
        audio_codec='aac',
        bitrate='8000k',
        preset='medium',
        threads=4
    )
    
    # Cleanup
    source.close()
    target.close()
    final.close()
    
    print("\n" + "=" * 60)
    print(f"  ✓ DONE! Output: {OUTPUT}")
    print("=" * 60)
    print("\nNow you can replace the source timestamps in YOUR_CLIPS")
    print("with your preferred moments from ST5_Premiere.mp4!")


if __name__ == "__main__":
    create_edit()
