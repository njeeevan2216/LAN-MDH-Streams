from flask import Flask, render_template, send_from_directory, request, abort
import os   
from datetime import datetime
from flask_socketio import SocketIO, emit


app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")  # Enable CORS

ip="10.130.234.27:5000"
current_playback_time = 0


# Configuration
MEDIA_FOLDER = os.path.join(app.root_path, 'static', 'media')
# Configuration
BROADCAST_FOLDER = os.path.join(MEDIA_FOLDER, 'broadcast')
BROADCAST_FILE = 'q.mp3'  # The looping broadcast file

# Home Route - Redirect to Explore
@app.route('/')
def home():
    return explore()

# Broadcast Route
@app.route('/broadcast')
def broadcast():
    return render_template('broadcast.html')


# Broadcast Route
@app.route('/broadcast-admin')
def broadcast_admin():
    return render_template('broadcastadmin.html')

# Route to stream the live broadcast file
@app.route('/broadcast/stream')
def stream_broadcast():
    return send_from_directory(BROADCAST_FOLDER, BROADCAST_FILE)

# WebSocket event for synchronization
@socketio.on('sync')
def handle_sync(data):
    global current_playback_time
    if 'currentTime' in data:
        current_playback_time = data['currentTime']
    emit('sync', {'currentTime': current_playback_time}, broadcast=True)

# WebSocket event when a new client connects
@socketio.on('connect')
def handle_connect():
    global current_playback_time
    emit('sync', {'currentTime': current_playback_time})

# Explore Route
@app.route('/explore')
def explore():
    audio_results = search_media('audio')
    video_results = search_media('video')
    return render_template('explore.html', audio_results=audio_results, video_results=video_results)

# Search Route
@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('q', '').lower()
    audio_results = search_media('audio', query)
    video_results = search_media('video', query)
    return render_template('search_results.html', query=query, audio_results=audio_results, video_results=video_results)

# Route to play audio files
@app.route('/play/audio/<filename>')
def play_audio(filename):
    media_path = os.path.join(MEDIA_FOLDER, 'audio')
    if filename not in os.listdir(media_path):
        abort(404)
    return render_template('play_audio.html', filename=filename)

# Route to play video files
@app.route('/play/video/<filename>')
def play_video(filename):
    media_path = os.path.join(MEDIA_FOLDER, 'video')
    if filename not in os.listdir(media_path):
        abort(404)
    return render_template('play_video.html', filename=filename)

# Route to stream audio files
@app.route('/audio/<filename>')
def stream_audio(filename):
    return send_from_directory(os.path.join(MEDIA_FOLDER, 'audio'), filename)

# Route to stream video files
@app.route('/video/<filename>')
def stream_video(filename):
    return send_from_directory(os.path.join(MEDIA_FOLDER, 'video'), filename)

# Helper Functions
def get_media_files(media_type, sort_by='name'):
    """
    Get media files sorted by the specified attribute.
    :param media_type: 'audio' or 'video'
    :param sort_by: 'name', 'date', 'popularity', 'featured', or 'classic'
    :return: Sorted list of media files
    """
    media_path = os.path.join(MEDIA_FOLDER, media_type)
    files = os.listdir(media_path)

    # Mock metadata for demonstration (e.g., you can replace this with a database)
    metadata = {
        'song1.mp3': {'popularity': 5, 'date': '2024-07-01', 'featured': True, 'classic': False},
        'song2.mp3': {'popularity': 2, 'date': '2024-06-20', 'featured': False, 'classic': True},
        'movie1.mp4': {'popularity': 8, 'date': '2024-07-03', 'featured': True, 'classic': False},
        'clip1.mp4': {'popularity': 4, 'date': '2024-07-10', 'featured': False, 'classic': False}
    }

    # Attach metadata to each file
    files_with_metadata = [
        (file, metadata.get(file, {'popularity': 0, 'date': '2024-01-01', 'featured': False, 'classic': False}))
        for file in files
    ]

    # Sort by the given attribute
    if sort_by == 'popularity':
        files_with_metadata.sort(key=lambda x: x[1]['popularity'], reverse=True)
    elif sort_by == 'date':
        files_with_metadata.sort(key=lambda x: datetime.strptime(x[1]['date'], '%Y-%m-%d'), reverse=True)
    elif sort_by == 'featured':
        files_with_metadata.sort(key=lambda x: x[1]['featured'], reverse=True)
    elif sort_by == 'classic':
        files_with_metadata.sort(key=lambda x: x[1]['classic'], reverse=True)
    else:
        files_with_metadata.sort(key=lambda x: x[0])  # Default: sort by name

    # Return only filenames in sorted order
    return [file[0] for file in files_with_metadata]

def search_media(media_type, query=None):
    """
    Search media files based on the query string.
    :param media_type: 'audio' or 'video'
    :param query: Search query
    :return: List of matching media files
    """
    media_path = os.path.join(MEDIA_FOLDER, media_type)
    files = os.listdir(media_path)
    if query==None:
        return [file for file in files ]
    return [file for file in files if query in file.lower()]

# Error handling for 404
@app.errorhandler(404)
def page_not_found(e):
    return render_template('error.html'), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
