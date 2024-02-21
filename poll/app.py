from flask import Flask, render_template, request, make_response, g
from redis import Redis
import os
import socket
import random
import json

option_a = os.getenv('OPTION_A')
option_b = os.getenv('OPTION_B')
option_c = os.getenv('OPTION_C')
option_d = os.getenv('OPTION_D')
hostname = socket.gethostname()

app = Flask(__name__)


def get_redis():
    if not hasattr(g, 'redis'):
        g.redis = Redis(host=os.getenv("HOST"), db=0, socket_timeout=5)
    return g.redis


@app.route("/", methods=['POST', 'GET'])
def hello():
    voter_id = request.cookies.get('voter_id')
    if not voter_id:
        voter_id = hex(random.getrandbits(64))[2:-1]

    vote = None

    if request.method == 'POST':
        redis = get_redis()
        vote = request.form['vote']
        data = json.dumps({'voter_id': voter_id, 'vote': vote})
        redis.rpush('votes', data)

    resp = make_response(render_template(
        'index.html',
        option_a=option_a,
        option_b=option_b,
        option_c=option_c,
        option_d=option_d,
        hostname=hostname,
        vote=vote,
    ))
    resp.set_cookie('voter_id', voter_id)
    return resp


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=os.getenv("PORT_ENV"), debug=True, threaded=True)
