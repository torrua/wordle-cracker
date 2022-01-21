# -*- coding: utf-8 -*-
"""
App's routes module
"""

from app.models import Game
from flask import Flask, jsonify, render_template, request
from config import log

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/get_suggestions", methods=["POST", "GET"])
def get_suggestions():
    collected_data = dict(request.form)
    log.debug(collected_data)
    if collected_data:
        game = Game()
        game.import_user_data(collected_data)
        words = game.get_suggestions()
        log.debug(words)
        return jsonify(words)
