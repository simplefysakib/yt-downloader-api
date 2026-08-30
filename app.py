from flask import Flask, request, jsonify
from pytubefix import YouTube

app = Flask(__name__)

# Ye naya rasta hai taaki aap browser mein check kar sakein
@app.route('/', methods=['GET'])
def home():
    return "Mubarak ho! Aapka Python Server ekdum Sahi Chal Raha Hai!"

# Ye hamara video nikalne wala rasta hai (Ab GET aur POST dono support karega)
@app.route('/get_video', methods=['GET', 'POST'])
def get_video():
    # Chrome browser (GET) aur Java App (POST) dono se URL lega
    if request.method == 'GET':
        url = request.args.get('url')
    else:
        data = request.get_json(silent=True)
        url = data.get('url') if data else None
    
    if not url:
        return jsonify({"error": "Bhai URL to daal"}), 400
    
    try:
        yt = YouTube(url)
        # 720p HD video nikalna
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
    
