"""
Deep analysis of target.mp4 to extract:
- Exact cut timestamps
- Speed changes (slow-mo vs normal)
- Flash/transition frames
- Motion/zoom detection
"""

from moviepy import *
import numpy as np
from PIL import Image
import os
import json

TARGET = "/Users/satyendra/Desktop/Atharv/Assets/target.mp4"
OUTPUT_DIR = "/Users/satyendra/Desktop/Atharv/Assets/target_analysis"

def analyze_video():
    print("=" * 60)
    print("DEEP ANALYSIS OF TARGET EDIT")
    print("=" * 60)
    
    video = VideoFileClip(TARGET)
    print(f"\nVideo: {video.duration:.2f}s @ {video.fps}fps, {video.size}")
    
    # Analysis data
    analysis = {
        "duration": video.duration,
        "fps": video.fps,
        "size": video.size,
        "cuts": [],
        "flashes": [],
        "speed_sections": [],
        "frame_data": []
    }
    
    prev_frame = None
    prev_brightness = None
    
    # Sample every frame for detailed analysis
    sample_interval = 1/30  # 30 samples per second
    
    print("\nAnalyzing frames...")
    
    cut_threshold = 30
    flash_threshold = 200
    
    for t in np.arange(0, video.duration, sample_interval):
        try:
            frame = video.get_frame(t)
            brightness = np.mean(frame)
            
            frame_info = {
                "time": round(t, 3),
                "brightness": round(brightness, 1)
            }
            
            if prev_frame is not None:
                diff = np.mean(np.abs(frame.astype(float) - prev_frame.astype(float)))
                frame_info["diff"] = round(diff, 1)
                
                # Detect cuts (high frame difference)
                if diff > cut_threshold:
                    if len(analysis["cuts"]) == 0 or (t - analysis["cuts"][-1]["time"]) > 0.1:
                        analysis["cuts"].append({
                            "time": round(t, 2),
                            "diff": round(diff, 1),
                            "type": "flash" if brightness > flash_threshold else "cut"
                        })
                        print(f"  {t:.2f}s: {'FLASH' if brightness > flash_threshold else 'CUT'} (diff={diff:.0f}, bright={brightness:.0f})")
            
            # Detect flashes (very bright frames)
            if brightness > flash_threshold:
                if len(analysis["flashes"]) == 0 or (t - analysis["flashes"][-1]) > 0.1:
                    analysis["flashes"].append(round(t, 2))
            
            analysis["frame_data"].append(frame_info)
            prev_frame = frame.copy()
            prev_brightness = brightness
            
        except Exception as e:
            continue
    
    video.close()
    
    # Analyze speed sections by looking at motion between cuts
    print("\n" + "=" * 60)
    print("EDIT STRUCTURE")
    print("=" * 60)
    
    cuts = [0.0] + [c["time"] for c in analysis["cuts"]] + [analysis["duration"]]
    
    print(f"\nTotal cuts detected: {len(analysis['cuts'])}")
    print(f"Total flashes: {len(analysis['flashes'])}")
    
    print("\n--- CLIP BREAKDOWN ---")
    for i in range(len(cuts) - 1):
        start = cuts[i]
        end = cuts[i + 1]
        duration = end - start
        
        # Determine if this section is slow-mo based on duration
        speed_guess = "SLOW" if duration > 1.0 else "FAST" if duration < 0.3 else "NORMAL"
        
        print(f"Clip {i+1:2d}: {start:5.2f}s - {end:5.2f}s ({duration:.2f}s) [{speed_guess}]")
    
    # Save analysis
    analysis_file = os.path.join(OUTPUT_DIR, "analysis.json")
    
    # Remove frame_data for cleaner output
    save_data = {k: v for k, v in analysis.items() if k != "frame_data"}
    
    with open(analysis_file, 'w') as f:
        json.dump(save_data, f, indent=2)
    
    print(f"\nAnalysis saved to: {analysis_file}")
    
    # Print summary for recreation
    print("\n" + "=" * 60)
    print("RECREATION TEMPLATE")
    print("=" * 60)
    print("\nCut timestamps (for your clips):")
    print("CUTS = [")
    for i in range(len(cuts) - 1):
        start = cuts[i]
        end = cuts[i + 1]
        print(f"    ({start:.2f}, {end:.2f}),  # Clip {i+1}")
    print("]")
    
    print("\nFlash timestamps:")
    print(f"FLASHES = {analysis['flashes']}")
    
    return analysis


if __name__ == "__main__":
    analyze_video()
