from flask import Flask, render_template, request, jsonify
import requests
import json
import pn

app = Flask(__name__, static_folder="client/build/static",
            template_folder="client/build")

@ app.route('/')
def hello():
    return render_template('index.html')

@app.route("/broadcast-message", methods=['GET'])
def broadcastMessage():
    response = pn.publish()
    return jsonify(response), 201



@ app.route('/profile')
def profile():
    return render_template('index.html')


# @app.route("/get-message", methods=['GET'])
# def getMessage():
#     response = pubsub.messages
#     return jsonify(response), 201

app.run(host='0.0.0.0', port=5002, debug=True)
