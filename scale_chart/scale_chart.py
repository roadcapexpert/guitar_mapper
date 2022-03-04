import math

scale_types = [{"type": "Major (Ionian)", "scale_steps": [2, 2, 1, 2, 2, 2, 1]},
               {"type": "Minor (Aeolian)", "scale_steps": [2, 1, 2, 2, 1, 2, 2]},
               {"type": "Dorian", "scale_steps": [2, 1, 2, 2, 2, 1, 2]},
               {"type": "Phrygian", "scale_steps": [1, 2, 2, 2, 1, 2, 2]},
               {"type": "Lydian", "scale_steps": [2, 2, 2, 1, 2, 2, 1]},
               {"type": "Mixolydian", "scale_steps": [2, 2, 1, 2, 2, 1, 2]},
               {"type": "Locrian", "scale_steps": [1, 2, 2, 1, 2, 2, 2]}]
key_notes = [{"key": "A", "key_display": "A"},
             {"key": "A#", "key_display": "A♯ / B♭"},
             {"key": "B", "key_display": "B"},
             {"key": "C", "key_display": "C"},
             {"key": "C#", "key_display": "C♯ / D♭"},
             {"key": "D", "key_display": "D"},
             {"key": "D#", "key_display": "D♯ / E♭"},
             {"key": "E", "key_display": "E"},
             {"key": "F", "key_display": "F"},
             {"key": "F#", "key_display": "F♯ / G♭"},
             {"key": "G", "key_display": "G"},
             {"key": "G#", "key_display": "G♯ / A♭"}]
notes = [d["key"] for d in key_notes]
inlay_frets = [3, 5, 7, 9, 12, 15, 17, 19, 21]

class FretBoard:
    # TODO change scale_types to use id, maybe put in database
    def __init__(self, key_note="A", scale_type="Major (Ionian)", fret_num=22):
        self.fret = "|"
        self.note_tab = "0"
        self.root_tab = "X"
        self.empty_tab = "-"
        self.fret_num = fret_num
        self.fret_width = 7
        self.tuning = {
            1: "E",
            2: "B",
            3: "G",
            4: "D",
            5: "A",
            6: "E"
        }
        self.neck = {
            1: "",
            2: "",
            3: "",
            4: "",
            5: "",
            6: ""
        }

        self.scale_type = scale_type

        if key_note in notes:
            self.key_note = key_note
        else:
            raise RuntimeError("Invalid root note")

    # def create_fretboard2(self):


    def create_fretboard(self):
        """ Compile the fretboard """
        scale = self.compile_scale()

        current_fret = 0
        while current_fret < self.fret_num:
            for string in self.neck:
                # determine current note
                open_note = self.tuning[string]
                open_note_index = notes.index(open_note)
                current_note = notes[(open_note_index + current_fret + 1) % len(notes)]

                # add to string
                string_so_far = self.neck[string]
                updated_neck = string_so_far + self.create_string_tab(current_note, scale) 
                #+ self.fret
                self.neck[string] = updated_neck

            current_fret += 1

    def create_string_tab(self, note, scale):
        """ Checks if note is in scale and creates the string drawing """

        if note in scale:
            # I wanted the root note to be a different character
            # TODO refactor to remove duplicate code below
            if note == scale[0]:
                # string_tab = (self.empty_tab * (math.trunc(self.fret_width / 2))) + self.root_tab + (
                #             self.empty_tab * (math.trunc(self.fret_width / 2)))
                string_tab = '<span class="string-tab root note"></span>'
            else:
                # string_tab = (self.empty_tab * (math.trunc(self.fret_width / 2))) + self.note_tab + (
                #             self.empty_tab * (math.trunc(self.fret_width / 2)))
                string_tab = '<span class="string-tab note"></span>'
        else:
            # string_tab = self.empty_tab * self.fret_width
            string_tab = '<span class="string-tab"></span>'

        return string_tab

    def compile_scale(self):
        """ Determines the notes in the scale for a given key """

        scale_dict = [x for x in scale_types if x["type"] == self.scale_type][0]
        scale_steps = scale_dict["scale_steps"]

        scale = [self.key_note]

        i = 0
        while i < len(scale_steps):
            current_note_index = notes.index(scale[i])
            next_step = scale_steps[i]
            next_note = notes[(current_note_index + next_step) % len(notes)]
            scale.append(next_note)
            i += 1

        return scale

    def add_inlay_markers(self):
        inlay_list = ["&nbsp;"] * ((self.fret_width * self.fret_num) + (self.fret_num + 1))
        for inlay in inlay_frets:
            position = math.trunc(self.fret_width * (inlay - 0.5)) + inlay
            inlay_list[position] = "&bull;"
        inlay_markers = "".join(inlay_list)
        self.neck[7] = inlay_markers

    def draw_neck(self):
        """ Does the actual drawing of the neck """

        # draw the nut
        for string in self.neck:
            self.neck[string] = self.fret

        self.create_fretboard()
        # self.add_inlay_markers()

        # draw neck
        print(*[str(v) for k, v in self.neck.items()], sep='\n')
        return self.neck
