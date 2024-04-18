# all supporting data and functions for processing simple ABC-derived music notation to frequency and duration vectors for supercollider use.


# define the base notes
lower_notes = list("abcdefg")
capital_notes = [note.upper() for note in lower_notes]

# extend base_notes with capital notes and their respective octaves
base_notes = []
for cap_note, low_note in zip(capital_notes, lower_notes):
    base_notes.extend([cap_note + ("," * i) for i in range(4, 0, -1)])
    base_notes.extend([low_note + ("'" * i) for i in range(4, 0, -1)])
    
# add individual capital and lowercase notes
base_notes += capital_notes + lower_notes

# add special notes (accidentals) to the base notes
all_notes = base_notes + ["_" + note for note in base_notes] + \
    ["=" + note for note in base_notes] + ["^" + note for note in base_notes] + ["z"]




# to map all possible accidental expressions to smaller set for easier processing
accidental_map = {
    "a": {
        "_": "^g",
        "=": "a",
        "^": "^a"
    },
    "b": {
        "_": "^a",
        "=": "b",
        "^": "c"
    },
    "c": {
        "_": "b",
        "=": "c",
        "^": "^c"
    },
    "d": {
        "_": "^c",
        "=": "d",
        "^": "^d"
    },
    "e": {
        "_": "^d",
        "=": "e",
        "^": "f"
    },
    "f": {
        "_": "e",
        "=": "f",
        "^": "^f"
    },
    "g": {
        "_": "^f",
        "=": "g",
        "^": "^g"
    }
}

# to map ABC octave notations to numeric octave order corresponding to "middle C" == "C4"
octave_map = [
    (lambda x: ",,," in x, 1),
    (lambda x: ",," in x, 2),
    (lambda x: "," in x, 3),
    (lambda x: "'''" in x, 8),
    (lambda x: "''" in x, 7),
    (lambda x: "'" in x, 6),
    (lambda x: "".join([char for char in x if char.isalpha()]).isupper(), 4),
    (lambda x: "".join([char for char in x if char.isalpha()]).islower(), 5)
]

# to map each key note to numeric value with respect to C for frequency computations
note_map = {
    "c": 0,
    "^c": 1,
    "d": 2,
    "^d": 3,
    "e": 4,
    "f": 5,
    "^f": 6,
    "g": 7,
    "^g": 8,
    "a": 9,
    "^a": 10,
    "b": 11
}




# parse ABC notation in a voice line to extract notes, durations, and types
def parse_voice_abc(line):
    # initialize a list to store parsed notes along with their properties
    parsed_notes = []
    
    # define duration for grace notes and track grace note count
    grace_time = 0.25
    grace_count = 0
    
    # split the line into note groups by spaces
    note_groups = line.split(' ')
    trip_count = 0
    
    # process each note group to extract note type, original format, parsed format without duration, and duration as float
    for note_group in [groups for groups in note_groups if len(groups) > 0]:
        # remove spaces from the note group
        note_group = note_group.replace(' ', '')
        
        # check if the note group is a single note without a time measure and not part of a triplet
        if note_group in all_notes and trip_count == 0:
            # calculate duration based on grace note count
            duration = 1.0 - grace_count
            # reduce grace count if grace notes are present
            if grace_count > 0:
                grace_count = 0
            # append the parsed note to the list with type, original note, parsed note (without duration), and duration
            parsed_notes.append(("single", note_group, note_group, duration))
            
        # check if the note group is a single note with added time measure and not part of a triplet or chord
        elif ''.join([char for char in note_group if char.isalpha() or char in ["_", "^", "=", ",", "'"]]) in all_notes and note_group[0] not in ["[", "{"] and trip_count == 0:
            # extract the duration from the note group
            duration = ''.join([char for char in note_group if char.isdigit() or char in ["/"]])
            duration = 0.5 if duration == "/" else float(duration)
            
            # adjust duration based on grace note count
            duration -= grace_count
            if grace_count > 0:
                grace_count = 0
                
            # append the parsed note to the list with type, original note, parsed note (without duration), and duration
            parsed_notes.append(("single", note_group, 
                                 ''.join([char for char in note_group if char.isalpha() or char in ["_", "^", "=", ",", "'"]]), 
                                 duration))
            
        # check if broken markers appear between two notes
        elif ">" in note_group:
            # split the note group by the broken marker '>'
            notes = note_group.split(">")
            k = 0
            for nt in notes:
                # set the duration factor based on the position of the note relative to the broken marker
                if k == 0:
                    c = 0.75 * 2
                elif k == 1:
                    c = 0.25 * 2
                k += 1
                
                # append the parsed broken note to the list if it's a valid note
                if nt in all_notes:
                    parsed_notes.append(("broken", note_group, nt, c))
                
                # handle broken notes with added time measure
                elif ''.join([char for char in nt if char.isalpha() or char in ["_", "^", "=", ",", "'"]]) in all_notes and note_group[0] not in ["[", "{"]:
                    # extract the duration from the note group
                    duration = ''.join([char for char in note_group if char.isdigit() or char in ["/"]])
                    duration = 1.0 if duration == '' else float(duration)
                    duration = 0.5 if duration == "/" else float(duration)
                    # append the parsed broken note to the list with adjusted duration
                    parsed_notes.append(("broken", note_group, nt, c * duration, ">"))
                
        # check if triplets appear or if already in a triplet
        elif note_group == "(3" or trip_count > 0:
            # exclude the case where the note group is only the triplet marker "(3"
            if note_group != "(3":
                # extract the duration from the note group
                duration = ''.join([char for char in note_group if char.isdigit() or char in ["/"]])
                duration = 1.0 if duration == '' else float(duration)
                duration = 0.5 if duration == "/" else float(duration)
                
                # adjust duration based on grace note count
                duration -= grace_count
                if grace_count > 0:
                    grace_count = 0
                    
                # append the parsed triplet note to the list with adjusted duration
                parsed_notes.append(("triplet", note_group,
                                     ''.join([char for char in note_group if char.isalpha() or char in ["_", "^", "=", ",", "'"]]),
                                     round(duration * 2/3, 4)
                                    ))
            
            # increment triplet count and reset if over 3 triplets
            trip_count += 1
            if trip_count > 3:
                trip_count = 0
               
        # check if chords and grace notes appear in the note group
        elif note_group[0] in ["[", "{"]:
            # extract the prefix and suffix from the note group, i.e. () or {} or []
            prefix, suffix = note_group[0], note_group[-1]
            note_group = note_group[1:-1]
            group = []
            i = 0
            while i < len(note_group):
                # check for largest size notes first, then smaller ones next
                for note_size in range(4, 0, -1):
                    if i + note_size <= len(note_group):
                        note = note_group[i:i+note_size]
                        # check if the note is a valid note or a special character
                        if note in all_notes + ["[", "]", "(", "/", "{", "}"]:
                            # add any trailing digits, if any
                            tail = note_group[i+note_size:]
                            digits = ''
                            for char in tail:
                                if char.isdigit():
                                    digits += char
                                else:
                                    break
                            if digits:
                                note += digits
                            
                            # append the note to the group if prefix is '['
                            if prefix == "[":
                                group.append(note)
                                
                            # handle grace notes if prefix is '{'
                            elif prefix == "{":
                                parsed_notes.append(("grace", "".join([prefix] + [note_group] + [suffix]), note, grace_time))
                                grace_count += grace_time
                                
                            note_group = note_group[i+note_size-1:]
                            i = 0
                            break
                i += 1
            
            # handle chords if the prefix is '['
            if prefix == "[":
                # extract duration from the first note in the group
                duration = ''.join([char for char in group[0] if char.isdigit() or char in ["/"]])
                duration = 1.0 if duration == '' else float(duration)
                duration = 0.5 if duration == "/" else float(duration)
                
                # adjust duration based on grace note count
                duration -= grace_count
                if grace_count > 0:
                    grace_count = 0
                    
                # modify the group to remove special characters and create a modified group
                mod_group = ["".join([char for char in nt if char.isalpha() or char in ["_", "^", "=", ",", "'"]]) for nt in group]
                
                # append the parsed chord to the list with adjusted duration and modified group
                parsed_notes.append(("chord", "".join([prefix] + group + [suffix]), " ".join(mod_group), duration))
                
    # loop over parsed notes to extract accidentals
    for n in range(len(parsed_notes)):
        # split the parsed note to extract individual notes
        notes = parsed_notes[n][2].split(" ")
        
        # initialize a list to store accidentals for each note
        accidentals = []
        for note in notes:
            # check if the note has an accidental and append the appropriate symbol to the accidentals list
            if "_" in note:
                accidentals.append("_")
            elif "^" in note:
                accidentals.append("^")
            else:
                accidentals.append("=")
                
        # add the accidentals as a tuple to the parsed note
        parsed_notes[n] += (" ".join(accidentals),)
        
        # remove accidentals from the parsed note and add the modified note as a tuple
        parsed_notes[n] += ("".join([char for char in parsed_notes[n][2] if char not in ["_", "^", "="]]),)
            
    return parsed_notes




# convert parsed ABC notation into standardized notes, octaves, and durations.
def convert_abc_parsed(parsed_abc_notes):
    # initialize a list to store compressed notes (i.e., compressing rest values)
    compressed_notes = []
    
    # initialize variables to handle rests
    temp_rest = [] # temporary storage for consecutive rest notes
    is_rest = False # flag to track if current note group is a rest
    for note_group in parsed_abc_notes:
        # check if the note group is a rest
        if note_group[2] == "z":
            is_rest = True
            temp_rest.append(note_group) # add rest note to temporary storage
        else:
            # check if the previous note group was a rest, compress the rests into a single rest note
            if is_rest:
                # append a compressed rest note to the compressed_notes list
                compressed_notes.append(
                    ('single', 'zt', 'z', 
                     sum([rest[3] for rest in temp_rest]), # sum the durations of consecutive rest notes
                     '=', 'z')
                )
                temp_rest = [] # reset the temporary storage
                is_rest = False # reset the rest flag
                
            # add the non-rest note group to compressed_notes
            compressed_notes.append(note_group) 
            
    # extract notes, octaves, and durations from compressed notes
    processed_notes = []
    
    # loop through each note group in the compressed notes list
    for note_group in compressed_notes:
        # initialize lists to store standard notes and standard octaves
        std_notes = []
        std_octaves = []
        
        # iterate over each note and its corresponding accidental in the note group
        for note, accidental in zip(note_group[5].split(" "), note_group[4].split(" ")):
            if note == "z": # if the note is a rest, add it directly to std_notes
                std_notes.append(note)
            else:
                # map the note to its standard form using the accidental map
                std_note = accidental_map["".join([char for char in note.lower() if char.isalpha()]).lower()][accidental]
                std_notes.append(str(note_map[std_note]))
                
                # map the octave of the note using the octave map
                for condition, octave in octave_map:
                    # check if the note meets the condition for the octave mapping
                    if condition(note):
                        std_octaves.append(str(octave))
                        break # break the loop after finding the appropriate octave mapping
            
        # add the processed note information (standard notes, standard octaves, and duration) to processed_notes
        processed_notes.append(
            (" ".join(std_notes), " ".join(std_octaves), note_group[3])
        )
            
    return processed_notes




# transform standardized notes, octaves, and durations into frequencies and durations for sound generation.
def transform2freq(converted_notes, tempo = 60):
    base_freq = 261.63 # frequency of middle C (C4) in Hz.
    base_octave = 4 # base octave for frequency calculation.
    frequencies, durations = [], [] # initialize lists to store frequencies and durations.
    
    # iterate over each group of converted notes.
    for notes_group in converted_notes:
        # split notes and octaves (useful for chord processing)
        notes = notes_group[0].split(" ")
        orders = notes_group[1].split(" ")
        
        # check if the note is a rest.
        if notes_group[0] == "z":
            # calculate rest duration.
            duration = round(float(notes_group[2]) / (tempo / 60), 5)
            note_freq = f"Rest({duration})" # supercollider notation for rests in frequency arrays
            note_dura = str(duration) # rest duration
        # check if it's a chord (multiple notes).
        elif len(notes) > 1:
            # initialize list to store individual chord frequencies.
            chord_notes = [] 
            for note, order in zip(notes, orders):
                # calculate frequency for each note in the chord.
                freq = round(base_freq * (2 ** (int(note) / 12) ) * (2 ** (int(order) - base_octave) ), 4)
                chord_notes.append(str(freq))
            note_freq = f"[{', '.join(chord_notes)}]" # format chord frequencies as a list for supercollider chord notation
            note_dura = str(round(float(notes_group[2]) / (tempo / 60), 5)) # calculate chord duration.
        # if it's a single note.
        else:
            # calculate frequency for the single note.
            note_freq = str(round(base_freq * (2 ** (int(notes_group[0]) / 12) ) * (2 ** (int(notes_group[1]) - base_octave) ), 4))
            # calculate single note duration.
            note_dura = str(round(float(notes_group[2]) / (tempo / 60), 5))
        
        # append calculated frequency and duration to their respective lists.
        frequencies.append(note_freq)
        durations.append(note_dura)
        
    # return the lists of frequencies and durations.
    return frequencies, durations