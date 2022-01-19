# -*- coding: utf-8 -*-
"""
App's routes module
"""

from app.models import Game, Iteration, Cell, Status
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

    if collected_data:
        words = suggestions_from_answer(collected_data)
        return jsonify(words)


def suggestions_from_answer(answer):
    game = Game()
    log.debug(game)
    for word, status in answer.items():
        cells = [Cell(char, get_status_from_color(color)) for char, color in zip(word, status)]
        game.add_iteration(Iteration(*cells))
    words = game.get_suggestions()
    log.debug(answer)
    log.debug(words)
    log.debug(game)

    return words


def get_status_from_color(char: str) -> Status:
    chars = {"B": Status.black, "Y": Status.yellow, "G": Status.green}
    return chars.get(char)
