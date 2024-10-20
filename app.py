from flask import Flask, render_template_string, request, send_file
import yt_dlp
import os

app = Flask(__name__)

# Function to download YouTube video
def download_youtube_video(url, folder):
    try:
        if not os.path.exists(folder):
            os.makedirs(folder)

        # yt-dlp options for the best video and audio quality
        ydl_opts = {
            'format': 'bestvideo+bestaudio/best',
            'outtmpl': os.path.join(folder, '%(title)s.%(ext)s'),
            'merge_output_format': 'mp4',
            'postprocessors': [{
                'key': 'FFmpegVideoConvertor',
                'preferedformat': 'mp4'
            }],
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=True)
            video_title = info_dict.get('title', None)
        return os.path.join(folder, video_title + ".mp4")
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

@app.route('/')
def index():
    # Inline HTML template
    html_template = '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>YouTube Video Downloader</title>
    </head>
    <body>
        <h1>YouTube Video Downloader</h1>
        <form action="/download" method="POST">
            <label for="url">Enter YouTube URL:</label>
            <input type="text" id="url" name="url" required>
            <button type="submit">Download</button>
        </form>
    </body>
    </html>
    '''
    return render_template_string(html_template)

@app.route('/download', methods=['POST'])
def download():
    print("Download route accessed")  # Debugging line
    url = request.form['url']
    folder = 'tmp'  # Temporary folder to store videos
    video_file_path = download_youtube_video(url, folder)
    
    if video_file_path and os.path.exists(video_file_path):
        # Send the file to the user for download
        return send_file(video_file_path, as_attachment=True, download_name=os.path.basename(video_file_path))
    else:
        return "An error occurred while downloading the video."

if __name__ == '__main__':
    app.run(debug=True)
