"""
Steve Harrington "THE LEGEND" - EXACT REPLICA
Matches the reference edit's cut timing precisely

Reference edit structure (30 cuts):
- 0.00-0.55s: Opening clip
- 0.55-1.10s: Quick cut
- 1.10-1.65s: Quick cut  
- 1.65-2.20s: Quick cut
- 2.20-3.25s: Longer clip
- 3.25-3.80s: Quick cut
- 3.80-5.50s: Longer slow section
- 5.50-6.05s: Quick cut (high diff = flash)
- 6.05-6.55s: Quick cut
- 6.55-8.65s: Slow-mo section
- 8.65-9.25s: Quick cut
- 9.25-9.80s: Quick cut
- 9.80-10.95s: Rapid fire cuts (4 cuts in ~1s)
- 10.95-11.40s: Flash + cut
- 11.40-12.70s: Rapid fire section
- 12.70-13.60s: Longer clip
- 13.60-14.10s: Quick cut
- 14.10-15.25s: Longer clip
- 15.25-16.20s: Build up
- 16.20-18.20s: Final flash sequence
"""

from moviepy import *
import numpy as np
from PIL import Image
import os

# === PATHS ===
ASSETS = "/Users/satyendra/Desktop/Atharv/Assets"
SOURCE = os.path.join(ASSETS, "ST5_Premiere.mp4")
AUDIO = os.path.join(ASSETS, "SteveHH.mp3")
OUTPUT = os.path.join(ASSETS, "steve_legend_EXACT.mp4")

# === EXACT CUT TIMINGS from reference ===
# (output_start, output_end) - these are the timestamps in the final edit
CUTS = [
    (0.00, 0.55),   # 1
    (0.55, 1.10),   # 2
    (1.10, 1.65),   # 3
    (1.65, 2.20),   # 4
    (2.20, 3.25),   # 5
    (3.25, 3.80),   # 6
    (3.80, 5.50),   # 7 - longer
    (5.50, 6.05),   # 8
    (6.05, 6.55),   # 9
    (6.55, 8.65),   # 10 - slow-mo
    (8.65, 9.25),   # 11
    (9.25, 9.80),   # 12
    (9.80, 9.95),   # 13 - rapid
    (9.95, 10.10),  # 14 - rapid
    (10.10, 10.25), # 15 - rapid
    (10.25, 10.95), # 16
    (10.95, 11.40), # 17 - flash
    (11.40, 11.90), # 18
    (11.90, 12.05), # 19 - rapid
    (12.05, 12.20), # 20 - rapid
    (12.20, 12.35), # 21 - rapid
    (12.35, 12.55), # 22 - rapid
    (12.55, 12.70), # 23 - rapid
    (12.70, 13.60), # 24
    (13.60, 14.10), # 25
    (14.10, 15.25), # 26
    (15.25, 16.20), # 27
    (16.20, 16.35), # 28 - flash
    (16.35, 16.55), # 29
    (16.55, 18.20), # 30 - ending
]

# === SOURCE TIMESTAMPS - Best Steve moments from ST5 Premiere ===
# These are manually selected iconic Steve moments
# (source_start, speed_multiplier)
# Speed < 1 means slow-mo (0.5 = half speed = 2x longer output)
SOURCE_CLIPS = [
    (15, 1.0),      # 1 - Opening (0.55s)
    (42, 1.0),      # 2 (0.55s)
    (68, 1.0),      # 3 (0.55s)
    (95, 1.0),      # 4 (0.55s)
    (120, 1.0),     # 5 (1.05s)
    (148, 1.0),     # 6 (0.55s)
    (175, 0.5),     # 7 - Slow section (1.70s output, needs 0.85s source)
    (205, 1.0),     # 8 (0.55s)
    (228, 1.0),     # 9 (0.50s)
    (255, 0.5),     # 10 - Slow-mo (2.10s output, needs 1.05s source)
    (285, 1.0),     # 11 (0.60s)
    (308, 1.0),     # 12 (0.55s)
    (332, 1.0),     # 13 - Rapid (0.15s)
    (345, 1.0),     # 14 - Rapid (0.15s)
    (358, 1.0),     # 15 - Rapid (0.15s)
    (372, 1.0),     # 16 (0.70s)
    (388, 1.0),     # 17 (0.45s)
    (402, 1.0),     # 18 (0.50s)
    (415, 1.0),     # 19 - Rapid (0.15s)
    (425, 1.0),     # 20 - Rapid (0.15s)
    (435, 1.0),     # 21 - Rapid (0.15s)
    (442, 1.0),     # 22 - Rapid (0.20s)
    (448, 1.0),     # 23 - Rapid (0.15s)
    (30, 1.0),      # 24 (0.90s)
    (58, 1.0),      # 25 (0.50s)
    (85, 0.5),      # 26 - Slow (1.15s output)
    (112, 0.5),     # 27 - Build (0.95s output)
    (138, 1.0),     # 28 (0.15s)
    (165, 1.0),     # 29 (0.20s)
    (192, 0.5),     # 30 - Ending slow (1.65s output)
]


def create_flash(duration, size, intensity=0.9):
    """Create white flash"""
    c = tuple([int(255 * intensity)] * 3)
    return ColorClip(size=size, color=c, duration=duration)


def apply_color_grade(frame):
    """Cinematic color grading matching reference style"""
    f = frame.astype(np.float32)
    
    # Darken
    f = f * 0.80
    
    # High contrast
    f = (f - 128) * 1.3 + 128
    
    # Cool blue shadows
    shadow_mask = (np.mean(f, axis=2, keepdims=True) < 80)
    f[:, :, 0] = np.where(shadow_mask[:, :, 0], f[:, :, 0] * 0.85, f[:, :, 0])
    f[:, :, 2] = np.where(shadow_mask[:, :, 0], f[:, :, 2] * 1.15, f[:, :, 2])
    
    # Slight overall blue tint
    f[:, :, 0] = f[:, :, 0] * 0.95
    f[:, :, 2] = f[:, :, 2] * 1.05
    
    return np.clip(f, 0, 255).astype(np.uint8)


def create_edit():
    print("=" * 60)
    print("  STEVE HARRINGTON - THE LEGEND - EXACT REPLICA")
    print("=" * 60)
    
    # Load source
    print("\n[1/5] Loading source video...")
    source = VideoFileClip(SOURCE)
    video_size = source.size
    print(f"      Source: {source.duration:.1f}s @ {video_size}")
    
    # Load audio
    print("\n[2/5] Loading audio...")
    audio = AudioFileClip(AUDIO)
    print(f"      Audio: {audio.duration:.1f}s")
    
    # Process each clip
    print(f"\n[3/5] Processing {len(CUTS)} clips...")
    processed_clips = []
    
    # Flash timestamps from reference
    flash_indices = [7, 16, 27]  # Clips that should have flash before them
    
    for i, ((out_start, out_end), (src_start, speed)) in enumerate(zip(CUTS, SOURCE_CLIPS)):
        target_duration = out_end - out_start
        
        # Calculate source duration needed (for slow-mo, we need less source)
        # If speed=0.5, output is 2x longer, so we need target_duration * speed of source
        src_duration = target_duration * speed
        
        # Make sure we don't exceed source
        if src_start + src_duration > source.duration:
            src_start = max(0, source.duration - src_duration - 1)
        
        print(f"      Clip {i+1}/{len(CUTS)}: {out_start:.2f}-{out_end:.2f}s "
              f"(src: {src_start}s for {src_duration:.2f}s, speed: {speed}x -> {target_duration:.2f}s output)")
        
        # Extract clip with enough source material
        clip = source.subclipped(src_start, src_start + src_duration)
        
        # Apply speed change (1/speed because MoviePy's speed_scaled is inverse)
        if speed != 1.0:
            clip = clip.with_speed_scaled(1/speed)
        
        # Trim to exact target duration
        if clip.duration > target_duration:
            clip = clip.subclipped(0, target_duration)
        elif clip.duration < target_duration - 0.01:
            # If clip is too short, extend by looping or freezing last frame
            print(f"        Warning: Clip {i+1} is {clip.duration:.2f}s, need {target_duration:.2f}s")
        
        # Apply color grading
        clip = clip.image_transform(apply_color_grade)
        
        # Add flash for specific cuts
        if i in flash_indices:
            flash = create_flash(0.05, video_size, 0.85)
            # Reduce clip duration to make room for flash
            if clip.duration > 0.05:
                clip = clip.subclipped(0.05, clip.duration)
            clip = concatenate_videoclips([flash, clip])
        
        processed_clips.append(clip)
    
    # Concatenate
    print("\n[4/5] Concatenating clips...")
    final = concatenate_videoclips(processed_clips, method="compose")
    
    # Trim to exact audio length
    target_duration = min(audio.duration, 18.2)
    if final.duration > target_duration:
        final = final.subclipped(0, target_duration)
    elif final.duration < target_duration:
        # Extend last clip if needed
        print(f"      Note: Final is {final.duration:.2f}s, target is {target_duration:.2f}s")
    
    # Add audio
    print("      Adding audio track...")
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
