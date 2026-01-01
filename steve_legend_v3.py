"""
Steve Harrington "THE LEGEND" - Ultimate Edit v3
Maximum effects, beat-synced, cinematic style

Features:
- Precise beat-synced cuts
- Dynamic speed ramps (slow-mo to normal)
- Flash transitions with varying intensity
- Zoom keyframes (Ken Burns effect)
- Heavy cinematic color grading
- Shake/vibration effects on drops
- Vignette overlay
"""

from moviepy import *
import numpy as np
from PIL import Image, ImageFilter, ImageDraw
import os

# === PATHS ===
ASSETS = "/Users/satyendra/Desktop/Atharv/Assets"
SOURCE = os.path.join(ASSETS, "ST5_Premiere.mp4")
AUDIO = os.path.join(ASSETS, "SteveHH.mp3")
OUTPUT = os.path.join(ASSETS, "steve_legend_v3.mp4")

# === BEAT MAP for Montagem Noche (Slowed) ===
# Precise beat timestamps for cuts
BEATS = [
    0.0,    # Intro start
    2.6,    # First bass hit
    5.2,    # Build
    5.8,    # Quick hit
    6.4,    # Quick hit
    7.0,    # Quick hit
    7.6,    # Drop
    8.4,    # Hit
    9.0,    # Quick
    9.6,    # Quick
    10.2,   # Quick
    10.8,   # Build
    11.6,   # Drop
    12.4,   # Hit
    13.0,   # Quick
    13.6,   # Quick
    14.4,   # Slow section start
    15.6,   # Hold
    16.8,   # Final
    18.0,   # End
]

# === CLIP DEFINITIONS ===
# (source_start, clip_duration, speed, effect_type)
# effect_type: "normal", "slowmo", "impact", "ending"
CLIPS = [
    # Opening - establish the vibe
    (12, 2.4, 1.0, "normal"),      # 0-2.6s
    
    # First section - building energy
    (38, 2.4, 1.0, "normal"),      # 2.6-5.2s
    
    # Quick cuts section - beat drops
    (62, 0.5, 1.0, "impact"),      # 5.2-5.8s
    (88, 0.5, 1.0, "impact"),      # 5.8-6.4s
    (115, 0.5, 1.0, "impact"),     # 6.4-7.0s
    (142, 0.5, 1.0, "impact"),     # 7.0-7.6s
    
    # Drop - slow-mo moment
    (168, 1.6, 0.5, "slowmo"),     # 7.6-8.4s (0.8s * 2 = 1.6s output)
    
    # Quick hits
    (195, 0.5, 1.0, "impact"),     # 8.4-9.0s
    (218, 0.5, 1.0, "impact"),     # 9.0-9.6s
    (242, 0.5, 1.0, "impact"),     # 9.6-10.2s
    (268, 0.5, 1.0, "impact"),     # 10.2-10.8s
    
    # Build section
    (295, 0.7, 0.9, "normal"),     # 10.8-11.6s
    
    # Second drop - slow-mo
    (320, 1.6, 0.5, "slowmo"),     # 11.6-12.4s
    
    # More quick cuts
    (348, 0.5, 1.0, "impact"),     # 12.4-13.0s
    (372, 0.5, 1.0, "impact"),     # 13.0-13.6s
    
    # Slow ending section
    (398, 1.6, 0.5, "slowmo"),     # 13.6-14.4s
    (420, 2.4, 0.5, "ending"),     # 14.4-15.6s
    (445, 2.4, 0.5, "ending"),     # 15.6-16.8s
    (460, 2.4, 0.6, "ending"),     # 16.8-18.0s
]


def create_vignette(size, intensity=0.4):
    """Create a vignette mask"""
    w, h = size
    # Create radial gradient
    center_x, center_y = w // 2, h // 2
    max_dist = np.sqrt(center_x**2 + center_y**2)
    
    y, x = np.ogrid[:h, :w]
    dist = np.sqrt((x - center_x)**2 + (y - center_y)**2)
    
    # Normalize and create vignette
    vignette = 1 - (dist / max_dist) * intensity
    vignette = np.clip(vignette, 0, 1)
    
    return vignette


def apply_cinematic_grade(frame, vignette=None):
    """Heavy cinematic color grading"""
    f = frame.astype(np.float32)
    
    # Darken overall
    f = f * 0.82
    
    # Increase contrast significantly
    f = (f - 128) * 1.25 + 128
    
    # Cool blue/teal shadows, warm highlights
    # Shadows (dark areas) - push blue/teal
    shadow_mask = (f.mean(axis=2, keepdims=True) < 100).astype(np.float32)
    f[:, :, 0] = f[:, :, 0] - shadow_mask[:, :, 0] * 8   # Less red in shadows
    f[:, :, 1] = f[:, :, 1] + shadow_mask[:, :, 0] * 3   # Slight green/teal
    f[:, :, 2] = f[:, :, 2] + shadow_mask[:, :, 0] * 12  # More blue in shadows
    
    # Highlights - slight warmth
    highlight_mask = (f.mean(axis=2, keepdims=True) > 180).astype(np.float32)
    f[:, :, 0] = f[:, :, 0] + highlight_mask[:, :, 0] * 5  # Warm highlights
    
    # Apply vignette if provided
    if vignette is not None:
        for c in range(3):
            f[:, :, c] = f[:, :, c] * vignette
    
    return np.clip(f, 0, 255).astype(np.uint8)


def create_flash(duration, size, intensity=0.5, color="white"):
    """Create flash transition"""
    if color == "white":
        c = tuple([int(255 * intensity)] * 3)
    elif color == "blue":
        c = (int(100 * intensity), int(150 * intensity), int(255 * intensity))
    else:
        c = (255, 255, 255)
    return ColorClip(size=size, color=c, duration=duration)


def apply_zoom(clip, start_zoom=1.0, end_zoom=1.12):
    """Apply smooth zoom effect"""
    def zoom_frame(get_frame, t):
        frame = get_frame(t)
        progress = t / max(clip.duration, 0.01)
        zoom = start_zoom + (end_zoom - start_zoom) * progress
        
        h, w = frame.shape[:2]
        new_h, new_w = int(h / zoom), int(w / zoom)
        
        y1 = (h - new_h) // 2
        x1 = (w - new_w) // 2
        
        cropped = frame[y1:y1+new_h, x1:x1+new_w]
        
        img = Image.fromarray(cropped)
        img = img.resize((w, h), Image.LANCZOS)
        return np.array(img)
    
    return clip.transform(zoom_frame)


def apply_shake(clip, intensity=3):
    """Apply camera shake effect"""
    def shake_frame(get_frame, t):
        frame = get_frame(t)
        h, w = frame.shape[:2]
        
        # Random offset based on time
        np.random.seed(int(t * 1000) % 10000)
        dx = int(np.random.uniform(-intensity, intensity))
        dy = int(np.random.uniform(-intensity, intensity))
        
        # Shift frame
        shifted = np.zeros_like(frame)
        
        src_x1 = max(0, dx)
        src_x2 = min(w, w + dx)
        src_y1 = max(0, dy)
        src_y2 = min(h, h + dy)
        
        dst_x1 = max(0, -dx)
        dst_x2 = min(w, w - dx)
        dst_y1 = max(0, -dy)
        dst_y2 = min(h, h - dy)
        
        shifted[dst_y1:dst_y2, dst_x1:dst_x2] = frame[src_y1:src_y2, src_x1:src_x2]
        
        return shifted
    
    return clip.transform(shake_frame)


def create_edit():
    print("=" * 60)
    print("  STEVE HARRINGTON - THE LEGEND - ULTIMATE EDIT v3")
    print("=" * 60)
    
    # Load source
    print("\n[1/6] Loading source video...")
    source = VideoFileClip(SOURCE)
    video_size = source.size
    print(f"      Source: {source.duration:.1f}s @ {video_size}")
    
    # Load audio
    print("\n[2/6] Loading audio...")
    audio = AudioFileClip(AUDIO)
    target_duration = min(audio.duration, 18.2)
    print(f"      Audio: {audio.duration:.1f}s")
    
    # Pre-compute vignette
    print("\n[3/6] Creating vignette overlay...")
    vignette = create_vignette(video_size, intensity=0.35)
    
    # Process clips
    print("\n[4/6] Processing clips...")
    processed_clips = []
    
    for i, (start, dur, speed, effect) in enumerate(CLIPS):
        if start >= source.duration:
            print(f"      Clip {i+1}: SKIPPED (beyond source)")
            continue
        
        end = min(start + dur, source.duration)
        print(f"      Clip {i+1}/{len(CLIPS)}: {start}s-{end:.1f}s | {effect} | {speed}x")
        
        # Extract clip
        clip = source.subclipped(start, end)
        
        # Apply speed
        if speed != 1.0:
            clip = clip.with_speed_scaled(1/speed)
        
        # Apply color grading with vignette
        def grade_with_vignette(frame, vig=vignette):
            return apply_cinematic_grade(frame, vig)
        clip = clip.image_transform(grade_with_vignette)
        
        # Apply effect-specific processing
        if effect == "impact":
            # Quick zoom + slight shake for impact
            clip = apply_zoom(clip, 1.0, 1.08)
            clip = apply_shake(clip, intensity=2)
        elif effect == "slowmo":
            # Smooth zoom for slow-mo
            clip = apply_zoom(clip, 1.0, 1.15)
        elif effect == "ending":
            # Slow zoom out feel
            clip = apply_zoom(clip, 1.05, 1.0)
        else:
            # Normal - subtle zoom
            clip = apply_zoom(clip, 1.0, 1.06)
        
        # Add flash transition
        if i > 0:
            if effect == "impact":
                flash = create_flash(0.04, video_size, 0.6)
            elif effect == "slowmo":
                flash = create_flash(0.08, video_size, 0.4, "blue")
            else:
                flash = create_flash(0.05, video_size, 0.35)
            clip = concatenate_videoclips([flash, clip])
        
        processed_clips.append(clip)
    
    # Concatenate
    print("\n[5/6] Concatenating clips...")
    final = concatenate_videoclips(processed_clips, method="compose")
    
    # Trim to audio length
    if final.duration > target_duration:
        final = final.subclipped(0, target_duration)
    
    # Add audio
    print("      Adding audio track...")
    audio_trimmed = audio.subclipped(0, min(final.duration, audio.duration))
    final = final.with_audio(audio_trimmed)
    
    # Export
    print(f"\n[6/6] Exporting to {OUTPUT}...")
    print("      This will take several minutes...")
    
    final.write_videofile(
        OUTPUT,
        fps=60,
        codec='libx264',
        audio_codec='aac',
        bitrate='12000k',
        preset='medium',
        threads=4
    )
    
    # Cleanup
    source.close()
    audio.close()
    final.close()
    
    print("\n" + "=" * 60)
    print(f"  ✓ COMPLETE! Output: {OUTPUT}")
    print("=" * 60)


if __name__ == "__main__":
    create_edit()
