from flask import Flask, render_template
from apscheduler.schedulers.background import BackgroundScheduler
from flask_socketio import SocketIO, emit

app = Flask(__name__)
socketio = SocketIO(app)

#defines the job
def job():
    # new_price = get_new_price()
    new_price = "new_price"
    print(new_price)
    #job emits on websocket
    socketio.emit('price update', new_price, broadcast=True)

#schedule job
scheduler = BackgroundScheduler()
running_job = scheduler.add_job(job, 'interval', seconds=4, max_instances=1)
scheduler.start()

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0')