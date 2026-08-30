from flask import Flask, request, jsonify
from pytubefix import YouTube

app = Flask(__name__)

@app.route('/get_video', methods=['POST'])
def get_video():
    data = request.get_json()
    url = data.get('url') if data else None
    
    if not url:
        return jsonify({"error": "URL missing"}), 400
    
    try:
        yt = YouTube(url)
        stream = yt.streams.get_highest_resolution()
        
        return jsonify({
            "status": "success",
            "title": yt.title,
            "url": stream.url
        })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
  
