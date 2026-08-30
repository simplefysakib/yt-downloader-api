from flask import Flask, request, jsonify
import yt_dlp
import os

app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return "Server is running with yt-dlp & Cookies!"

@app.route('/get_video', methods=['GET', 'POST'])
def get_video():
    if request.method == 'GET':
        url = request.args.get('url')
    else:
        data = request.get_json(silent=True)
        url = data.get('url') if data else None
    
    if not url:
        return jsonify({"error": "URL missing"}), 400
    
    try:
        # MAGIC LINE: Cookies ko use karne ka rasta
        ydl_opts = {
            'format': 'best',
            'quiet': True,
            'no_warnings': True,
            'nocheckcertificate': True
        }
        
        # Check karte hain ki cookie file maujood hai ya nahi
        if os.path.exists('cookies.txt'):
            ydl_opts['cookiefile'] = 'cookies.txt'
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            direct_url = info.get('url')
            title = info.get('title', 'YouTube Video')
        
        return jsonify({
            "status": "success",
            "title": title,
            "url": direct_url
        })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
    
