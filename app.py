#TODO
# - logging
# - enhance CSS
# - add more scale types (modes)
# - dockerize


from flask import Flask, render_template, request
from scale_chart import FretBoard, scale_types, key_notes

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
                           tab=fretboard.draw_neck(),
                           state=state)


if __name__ == "__main__":
    app.run()
