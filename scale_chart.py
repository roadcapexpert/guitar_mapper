import math

# These should probably go in a config file or something
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
        self.scale = []
        self.scale_type = scale_type

        if key_note in notes:
            self.key_note = key_note
        else:
            raise RuntimeError("Invalid root note")

    def create_fretboard(self):
        """ Compile the fretboard """
        self.scale = self.compile_scale()

        for string in self.neck:
            self.neck[string] = self.get_tuning_html(self.tuning[string])

        current_fret = 0
        while current_fret < self.fret_num:
            for string in self.neck:
                # determine current note
                open_note = self.tuning[string]
                open_note_index = notes.index(open_note)
                current_note = notes[(open_note_index + current_fret + 1
                                      ) % len(notes)]

                # add to string
                string_so_far = self.neck[string]
                updated_neck = string_so_far + self.create_string_tab(current_fret, current_note)
                # + self.fret
                self.neck[string] = updated_neck

            current_fret += 1

    def create_string_tab(self, fret, note):
        """ Checks if note is in scale and creates the string drawing """
        is_note = False
        is_root = False
        is_inlay = False

        if note in self.scale:
            if note == self.scale[0]:
                # string_tab = (self.empty_tab * (math.trunc(self.fret_width / 2))) + self.root_tab + (
                #             self.empty_tab * (math.trunc(self.fret_width / 2)))
                # string_tab = '<span class="string-tab root note"></span>'
                # classes = ' root note fret-' + str(fret)
                is_note = True
                is_root = True
            else:
                # string_tab = (self.empty_tab * (math.trunc(self.fret_width / 2))) + self.note_tab + (
                #             self.empty_tab * (math.trunc(self.fret_width / 2)))
                # string_tab = '<span class="string-tab note"></span>'
                # classes = ' note fret-' + str(fret)
                is_note = True
        # else:
            # # string_tab = self.empty_tab * self.fret_width
            # string_tab = '<span class="string-tab"></span>'
            # classes = ' fret-' + str(fret)

        # frets were off by one, probably should make fret start at 1 instead of 0
        if fret + 1 in inlay_frets:
            # classes = classes + ' inlay'
            is_inlay = True

        return self.get_string_tab_html(note, is_note, is_root, is_inlay)
        # return '<span class="string-tab' + classes + '"></span>'

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
        """ Adds bullets below inlay frets """

        inlay_list = ["&nbsp;"] * ((self.fret_width * self.fret_num) + (self.fret_num + 1))
        for inlay in inlay_frets:
            position = math.trunc(self.fret_width * (inlay - 0.5)) + inlay
            inlay_list[position] = "&bull;"
        inlay_markers = "".join(inlay_list)
        self.neck[7] = inlay_markers

    def get_tuning_html(self, note):

        # Should probably change this to use flags like Corey's
        html = '<span class="string-tuning'
        if note in self.scale:
            html = html + ' note'
            # return '<span class="string-tuning note root">' + note + '</span>'
        if note == self.scale[0]:
            html = html + ' root'
            # return '<span class="string-tuning note">' + note + '</span>'
        html = html + '">'

        if note in self.scale:
            html = html + '<span class="note-indicator">' + note + '</span>'
        else:
            html = html + note

        html = html + '</span>'

        return html

    @staticmethod
    def get_string_tab_html(note, is_note, is_root, is_inlay):
        html = '<span class="string-tab'
        if is_note:
            html = html + ' note'
        if is_root:
            html = html + ' root'
        if is_inlay:
            html = html + ' inlay'
        html = html + '">'

        if is_note:
            html = html + '<span class="note-indicator">' + note + '</span>'
        else:
            html = html + '&nbsp;'
        html = html + '</span>'
        return html

    def draw_neck(self):
        """ Does the actual drawing of the neck """
        # draw the tuning of each string
        # for string in self.neck:
        #     self.neck[string] = self.get_tuning_html(self.tuning[string])

        self.create_fretboard()
        # self.add_inlay_markers()

        # TODO make this logging
        # print(*[str(v) for k, v in self.neck.items()], sep='\n')
        return self.neck
