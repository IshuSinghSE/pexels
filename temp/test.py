# Import subprocess and textwrap modules
import subprocess
import textwrap

# Define the input video file name
input_video = "pexels.mp4"

# Define the output video file name
output_video = "output.mp4"

# Define the text to be added
text = "This is a long text that needs to be wrapped into multiple lines to fit the video frame."

# Define the font file path
font_file = "Roboto.ttf"

# Define the font color
font_color = "white"

# Define the font size
font_size = 75

# Define the text position
text_x = 20  # distance from the left edge of the video
text_y = 500  # distance from the top edge of the video

# Define the maximum line length in characters
max_line_length = 10

# Wrap the text into multiple lines using textwrap module
wrapped_text = textwrap.fill(text, max_line_length)

# Replace newlines with backslash n for ffmpeg
ffmpeg_text = "write code for adding text\n to a video using ffmpeg in python"

# Define the ffmpeg command with drawtext filter
ffmpeg_command = [
    "ffmpeg",
    "-i", input_video,  # input video file
    # video filter with drawtext parameters
    "-vf", f"drawtext=fontfile={font_file}:text='{ffmpeg_text}':fontcolor={font_color}:fontsize={font_size}:x=(w-text_w)/2:y=(h-text_h)/2",
    "-c:a", "copy",  # copy the audio stream without re-encoding
    output_video  # output video file
]

# Run the ffmpeg command using subprocess
# subprocess.check_call("python -h",stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
subprocess.check_call("python -h")

# subprocess.Popen(["sleep", "10"])
# subprocess.Popen('ffmpeg', shell=True)