#TODO
# - enforce odd fret width only
# - make major/minor selectable
# - add argeparser
# - change root note

import math


class FretBoard():

    def __init__(self):

        self.edge = "="
        self.fret = "|"
        self.note_tab = "0"
        self.root_tab = "X"
        self.empty_tab = "-"
        self.fret_num = 22
        self.fret_width = 7

        self.key = "G"
        self.notes = ["A", "A#", "B", "C", "C#", "D", "D#", "E", "F", "F#", "G", "G#"]
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

    def create_fretboard(self):
        """ Compile the fretboard """
        scale = self.compile_scale()

        current_fret = 0
        while current_fret < self.fret_num:
            for string in self.neck:
                # determine current note
                open_note = self.tuning[string]
                open_note_index = self.notes.index(open_note)
                current_note = self.notes[(open_note_index + current_fret + 1) % len(self.notes)]

                # add to string
                string_so_far = self.neck[string]
                updated_neck = string_so_far + self.create_string_tab(current_note, scale) + self.fret
                self.neck[string] = updated_neck

            current_fret += 1

    def create_string_tab(self, note, scale):
        """ Checks if note is in scale and creates the string drawing """

        if note in scale:
            if note == scale[0]:
                string_tab = (self.empty_tab * (math.trunc(self.fret_width / 2))) + self.root_tab + (
                            self.empty_tab * (math.trunc(self.fret_width / 2)))
            else:
                string_tab = (self.empty_tab * (math.trunc(self.fret_width / 2))) + self.note_tab + (
                            self.empty_tab * (math.trunc(self.fret_width / 2)))
        else:
            string_tab = self.empty_tab * self.fret_width

        return string_tab

    def compile_scale(self):
        """ Determines the notes in the scale for a given key """

        major_scale = [2, 2, 1, 2, 2, 2, 1]
        minor_scale = [2, 1, 2, 2, 1, 2, 2]
        scale = [self.key]

        i = 0
        while i < len(major_scale):
            current_note_index = self.notes.index(scale[i])
            next_step = major_scale[i]
            next_note = self.notes[(current_note_index + next_step) % len(self.notes)]
            scale.append(next_note)
            i += 1

        return scale

    def draw_neck(self):
        """ Does the actual drawing of the neck """

        # draw the nut
        for string in self.neck:
            self.neck[string] = self.fret

        self.create_fretboard()

        # draw neck
        print(*[str(v) for k,v in self.neck.items()], sep='\n')


def main():
    FretBoard().draw_neck()


if __name__ == '__main__':
    main()


