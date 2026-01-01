"""
Analyze the reference "The Legend" edit to extract exact cut timings
"""

from moviepy import *
import numpy as np
import os

REFERENCE = "/Users/satyendra/Desktop/Atharv/Assets/＂The Legend🗿＂ - Steve Harrington 'Stranger Things 5 World premiere' Edit ｜ MONTAGEM NOCHE (Slowed) [1aJ2hJ48HU8].mp4"

def detect_cuts(video_path, threshold=30):
    """Detect scene cuts by analyzing frame differences"""
    print(f"Loading: {video_path}")
    video = VideoFileClip(video_path)
    
    print(f"Duration: {video.duration:.2f}s")
    print(f"FPS: {video.fps}")
    print(f"Size: {video.size}")
    
    cuts = [0.0]  # Start
    prev_frame = None
    
    # Sample at higher rate for accuracy
    sample_rate = 0.05  # Every 50ms
    
    print("\nAnalyzing frames for cuts...")
    for t in np.arange(0, video.duration, sample_rate):
        try:
            frame = video.get_frame(t)
            
            if prev_frame is not None:
                # Calculate difference
                diff = np.mean(np.abs(frame.astype(float) - prev_frame.astype(float)))
                
                if diff > threshold:
                    # Check if it's not too close to last cut
                    if len(cuts) == 0 or (t - cuts[-1]) > 0.15:
                        cuts.append(round(t, 2))
                        print(f"  Cut detected at {t:.2f}s (diff: {diff:.1f})")
            
            prev_frame = frame.copy()
        except:
            continue
    
    video.close()
    
    print(f"\n=== DETECTED {len(cuts)} CUTS ===")
    for i, cut in enumerate(cuts):
        print(f"  {i+1}. {cut:.2f}s")
    
    return cuts


def analyze_brightness_curve(video_path):
    """Analyze brightness over time to detect flashes"""
    video = VideoFileClip(video_path)
    
    print("\n=== BRIGHTNESS ANALYSIS (detecting flashes) ===")
    flashes = []
    
    for t in np.arange(0, video.duration, 0.033):  # ~30fps sampling
        try:
            frame = video.get_frame(t)
            brightness = np.mean(frame)
            
            if brightness > 200:  # Very bright = flash
                if len(flashes) == 0 or (t - flashes[-1]) > 0.1:
                    flashes.append(round(t, 2))
                    print(f"  Flash at {t:.2f}s (brightness: {brightness:.0f})")
        except:
            continue
    
    video.close()
    return flashes


if __name__ == "__main__":
    print("=" * 60)
    print("ANALYZING REFERENCE EDIT: The Legend - Steve Harrington")
    print("=" * 60)
    
    cuts = detect_cuts(REFERENCE, threshold=25)
    flashes = analyze_brightness_curve(REFERENCE)
    
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"Total cuts: {len(cuts)}")
    print(f"Total flashes: {len(flashes)}")
    print(f"\nCut timestamps: {cuts}")
    print(f"\nFlash timestamps: {flashes}")
