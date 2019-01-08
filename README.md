# composite-earth
Generates a sequence of composite images of Earth in the last 24 hours.
Uses the API of http://rammb-slider.cira.colostate.edu/

## Converting images generated in a folder to a video using ffmpeg
`ffmpeg -r 30 -i "\Earth_%4d.jpg" -c:v libx264 -vf "fps=25,format=yuv420p" output.mp4`

Example output: https://www.youtube.com/watch?v=VGo55z7c4w0
