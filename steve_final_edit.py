"""
Steve Harrington "THE LEGEND" - FINAL EDIT
Properly handles slow-motion by extracting more source footage
"""

from moviepy import *
import numpy as np
import os

# === PATHS ===
ASSETS = "/Users/satyendra/Desktop/Atharv/Assets"
SOURCE = os.path.join(ASSETS, "ST5_Premiere.mp4")
AUDIO = os.path.join(ASSETS, "SteveHH.mp3")
OUTPUT = os.path.join(ASSETS, "steve_legend_FINAL.mp4")

# === EXACT CUT TIMINGS from reference (30 cuts) ===
CUTS = [
    (0.00, 0.55),   (0.55, 1.10),   (1.10, 1.65),   (1.65, 2.20),
    (2.20, 3.25),   (3.25, 3.80),   (3.80, 5.50),   (5.50, 6.05),
    (6.05, 6.55),   (6.55, 8.65),   (8.65, 9.25),   (9.25, 9.80),
    (9.80, 9.95),   (9.95, 10.10),  (10.10, 10.25), (10.25, 10.95),
    (10.95, 11.40), (11.40, 11.90), (11.90, 12.05), (12.05, 12.20),
    (12.20, 12.35), (12.35, 12.55), (12.55, 12.70), (12.70, 13.60),
    (13.60, 14.10), (14.10, 15.25), (15.25, 16.20), (16.20, 16.35),
    (16.35, 16.55), (16.55, 18.20),
]

# === SOURCE CLIPS ===
# (source_start, speed) - speed < 1 = slow-mo
# For slow-mo: we need MORE source footage (output_duration * speed)
SOURCE_CLIPS = [
    (15, 1.0),   (42, 1.0),   (68, 1.0),   (95, 1.0),
    (120, 1.0),  (148, 1.0),  (175, 0.5),  (205, 1.0),
    (228, 1.0),  (255, 0.5),  (285, 1.0),  (308, 1.0),
    (332, 1.0),  (345, 1.0),  (358, 1.0),  (372, 1.0),
    (388, 1.0),  (402, 1.0),  (415, 1.0),  (425, 1.0),
    (435, 1.0),  (442, 1.0),  (448, 1.0),  (30, 1.0),
    (58, 1.0),   (85, 0.5),   (112, 0.5),  (138, 1.0),
    (165, 1.0),  (192, 0.5),
]


def apply_color_grade(frame):
    """Cinematic color grading"""
    f = frame.astype(np.float32)
    f = f * 0.80
    f = (f - 128) * 1.3 + 128
    f[:, :, 0] = f[:, :, 0] * 0.95
    f[:, :, 2] = f[:, :, 2] * 1.05
    return np.clip(f, 0, 255).astype(np.uint8)


def create_flash(duration, size, intensity=0.9):
    c = tuple([int(255 * intensity)] * 3)
    return ColorClip(size=size, color=c, duration=duration)


def create_edit():
    print("=" * 60)
    print("  STEVE HARRINGTON - THE LEGEND - FINAL EDIT")
    print("=" * 60)
    
    source = VideoFileClip(SOURCE)
    audio = AudioFileClip(AUDIO)
    video_size = source.size
    
    print(f"\nSource: {source.duration:.1f}s, Audio: {audio.duration:.1f}s")
    print(f"\nProcessing {len(CUTS)} clips...")
    
    processed_clips = []
    flash_indices = [7, 16, 27]
    
    for i, ((out_start, out_end), (src_start, speed)) in enumerate(zip(CUTS, SOURCE_CLIPS)):
        target_duration = out_end - out_start
        
        # For slow-mo (speed < 1), we need LESS source footage
        # because it will be stretched. E.g., 0.5x speed means
        # 1 second of source becomes 2 seconds of output
        src_duration_needed = target_duration * speed
        
        # Ensure we don't go past source end
        if src_start + src_duration_needed > source.duration:
            src_start = max(0, source.duration - src_duration_needed - 0.5)
        
        print(f"  {i+1}/{len(CUTS)}: {target_duration:.2f}s output from {src_duration_needed:.2f}s source @ {speed}x")
        
        # Extract the source clip
        clip = source.subclipped(src_start, src_start + src_duration_needed)
        
        # Apply slow-motion by changing speed
        # with_speed_scaled(factor) where factor > 1 = faster, < 1 = slower
        # To slow down by 0.5x, we use factor = 0.5 (plays at half speed)
        if speed != 1.0:
            # This makes the clip play slower, effectively making it longer
            clip = clip.with_effects([vfx.MultiplySpeed(speed)])
        
        # Trim to exact target duration
        if clip.duration > target_duration:
            clip = clip.subclipped(0, target_duration)
        
        # Apply color grading
        clip = clip.image_transform(apply_color_grade)
        
        # Add flash for specific cuts
        if i in flash_indices:
            flash = create_flash(0.05, video_size, 0.85)
            if clip.duration > 0.05:
                clip = clip.subclipped(0.05, clip.duration)
            clip = concatenate_videoclips([flash, clip])
        
        processed_clips.append(clip)
    
    print("\nConcatenating...")
    final = concatenate_videoclips(processed_clips, method="compose")
    
    print(f"Final duration: {final.duration:.2f}s (target: 18.2s)")
    
    # Add audio
    audio_trimmed = audio.subclipped(0, min(final.duration, audio.duration))
    final = final.with_audio(audio_trimmed)
    
    print(f"\nExporting to {OUTPUT}...")
    final.write_videofile(
        OUTPUT,
        fps=60,
        codec='libx264',
        audio_codec='aac',
        bitrate='12000k',
        preset='medium',
        threads=4
    )
    
    source.close()
    audio.close()
    final.close()
    
    print(f"\n✓ DONE! Output: {OUTPUT}")


if __name__ == "__main__":
    create_edit()
