import subprocess
import os
import glob
import shutil

def recreate_pngs():
    # Step 1: Generate the video MOV with Manim
    print("Generating video with Manim...")
    result = subprocess.run(["python", "utils/animar_svg_manim.py"], capture_output=True, text=True)
    if result.returncode != 0:
        print("Error generating video:", result.stderr)
        return
    print("Video generated successfully.")

    # Step 2: Extract frames PNG from MOV
    video_dir = "media/videos/900p15"
    print("Extracting frames from video...")
    result = subprocess.run(["ffmpeg", "-i", "SVGAnimation.mov", "%04d.png"], cwd=video_dir, capture_output=True, text=True)
    if result.returncode != 0:
        print("Error extracting frames:", result.stderr)
        return
    print("Frames extracted successfully.")

    # Step 3: Move PNGs to images directory (removing old ones)
    images_dir = "media/images/animar_svg_manim"
    # Remove old PNGs
    old_pngs = glob.glob(os.path.join(images_dir, "*.png"))
    for png in old_pngs:
        os.remove(png)
    print("Old PNGs removed.")

    # Move new PNGs
    new_pngs = glob.glob(os.path.join(video_dir, "*.png"))
    for png in new_pngs:
        shutil.move(png, images_dir)
    print("New PNGs moved successfully.")

    print("All tasks completed. PNGs are ready in", images_dir)

if __name__ == "__main__":
    recreate_pngs()