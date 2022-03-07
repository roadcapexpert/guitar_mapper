# TODO add logging

from flask import Flask, render_template, request
from scale_chart.scale_chart import FretBoard, scale_types, key_notes


def create_app():
    app = Flask(__name__)

    @app.route("/", methods=["POST", "GET"])
    def home():
        state = ""
        if request.method == "POST":
            key_note_input = request.form["key_note_select"]
            scale_type_input = request.form["scale_type_select"]
            state = {'scale_choice': scale_type_input, 'key_choice': key_note_input}
            fretboard = FretBoard(key_note=key_note_input, scale_type=scale_type_input)
        else:
            fretboard = FretBoard()
        return render_template("index.html",
                               key_note_data=key_notes,
                               scale_type_data=scale_types,
                               string=fretboard.draw_neck(),
                               state=state)

    return app
