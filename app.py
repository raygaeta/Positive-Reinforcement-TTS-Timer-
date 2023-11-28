import os
from flask import send_from_directory
from flask import redirect
from flask import Flask, render_template, request, send_from_directory, send_file
from flask_socketio import SocketIO
import random
import time
from gtts import gTTS
import threading

app = Flask(__name__)
socketio = SocketIO(app)
quotes = [
    "You're making progress, one page at a time.",
    "Every study session is a step toward success.",
    "Believe in yourself. You've got this!",
    "Embrace the challenge, for it leads to growth.",
    "Your dedication today shapes your success tomorrow.",
    "Keep going. Each effort brings you closer to your goals.",
    "In the realm of learning, every effort counts.",
    "Strive for progress, not perfection.",
    "Learning is a journey, not a destination.",
    "Small steps forward create big achievements.",
    "Success is built on a foundation of hard work.",
    "Stay focused. Stay determined. Stay unstoppable.",
    "Challenges are opportunities in disguise.",
    "Your dedication fuels your education.",
    "Hard work now, success later.",
    "The journey of a thousand pages begins with a single word.",
    "Success is the sum of small efforts, repeated day in and day out.",
    "You're not here to be average; you're here to be awesome.",
    "Every study session is a chance to shine.",
    "Strive for excellence, and success will follow.",
    "You're capable of more than you know.",
    "Today's efforts are tomorrow's accomplishments.",
    "Success is earned, not given. Keep earning.",
    "Education is the key to unlocking your potential.",
    "Your commitment to learning sets you apart.",
    "Believe in your ability to learn and grow.",
    "The only limit is the one you set for yourself.",
    "Study with purpose, and success will follow.",
    "Education is the passport to the future.",
    "You are stronger than you think, smarter than you believe.",
    "Hard work is the bridge between goals and accomplishments.",
    "You're on the path to greatness. Keep going!",
    "Success is the result of preparation and perseverance.",
    "Invest in yourself through education.",
    "Learning today, leading tomorrow.",
    "Every challenge you face is an opportunity to grow.",
    "Your commitment to learning is your superpower.",
    "Knowledge is the key that unlocks the door to your dreams.",
    "You have the power to shape your own success story.",
    "You're not just studying; you're investing in your future.",
    "You're not alone; every study session is a shared journey.",
    "Your potential is limitless; embrace the journey.",
    "Each study session is a step toward mastery.",
    "In the world of learning, you are a shining star.",
    "You are a scholar in the making. Keep learning, keep growing.",
    "Your hard work today is a gift to your future self.",
    "Success is a journey, not a destination. Enjoy the process.",
    "The effort you put in today will become your success story.",
    "Your commitment to learning is your greatest asset.",
    "You are building the foundation for a bright future."
]

custom_interval = 10  # Reduced for testing purposes

@app.route('/')
def index():
    return render_template('index.html', interval=custom_interval)

@app.route('/set_interval', methods=['POST'])
def set_interval():
    global custom_interval
    interval = int(request.form['interval'])
    custom_interval = max(interval, 1)
    socketio.emit('update_interval', {'interval': custom_interval})
    return redirect('/')  # Redirect back to the index page

@app.route('/audio/<filename>')
def serve_audio(filename):
    return send_from_directory('audio', filename, mimetype="audio/mpeg")

# Modify the play_random_quote function
def play_random_quote():
    os.makedirs('audio', exist_ok=True)

    while True:
        random_quote = random.choice(quotes)
        tts = gTTS(random_quote)
        audio_file = f"audio/audio_{int(time.time())}.mpeg"  # Append a timestamp
        tts.save(audio_file)
        print(f"Generated audio: {audio_file}")
        socketio.emit('quote', {'quote': random_quote, 'audio_file': audio_file})
        time.sleep(custom_interval)


quote_thread = threading.Thread(target=play_random_quote)
quote_thread.start()

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5001, debug=True)