import re
import pprint

#import music_theory
#import guitar_theory

# The musical alphabet consists of seven letter from A through G
alphabet = ['C', 'D', 'E', 'F', 'G', 'A', 'B']

#notes of music, each index represents a unique note while each entry is another name for it
notes = [
    ['B#',  'C',  'Dbb'], #0  C
    ['B##', 'C#', 'Db'],  #1  C#
    ['C##', 'D',  'Ebb'], #2  D
    ['D#',  'Eb', 'Fbb'], #3  D#
    ['D##', 'E',  'Fb'],  #4  E
    ['E#',  'F',  'Gbb'], #5  F
    ['E##', 'F#', 'Gb'],  #6  F#
    ['F##', 'G',  'Abb'], #7  G
    ['G#',  'Ab'],        #8  G#
    ['G##', 'A',  'Bbb'], #9  A
    ['A#',  'Bb', 'Cbb'], #10 A#
    ['A##', 'B',  'Cb'],  #11 B
]

# Interval names that specify the distance between two notes
intervals = [
    ['P1', 'd2'],  # Perfect unison   Diminished second
    ['m2', 'A1'],  # Minor second     Augmented unison
    ['M2', 'd3'],  # Major second     Diminished third
    ['m3', 'A2'],  # Minor third      Augmented second
    ['M3', 'd4'],  # Major third      Diminished fourth
    ['P4', 'A3'],  # Perfect fourth   Augmented third
    ['d5', 'A4'],  # Diminished fifth Augmented fourth
    ['P5', 'd6'],  # Perfect fifth    Diminished sixth
    ['m6', 'A5'],  # Minor sixth      Augmented fifth
    ['M6', 'd7'],  # Major sixth      Diminished seventh
    ['m7', 'A6'],  # Minor seventh    Augmented sixth
    ['M7', 'd8'],  # Major seventh    Diminished octave
    ['P8', 'A7'],  # Perfect octave   Augmented seventh
]

# Interval names based off the notes of the major scale
intervals_major = [
    [ '1', 'bb2'],
    ['b2',  '#1'],
    [ '2', 'bb3',   '9'],
    ['b3',  '#2'],
    [ '3',  'b4'],
    [ '4',  '#3',  '11'],
    ['b5',  '#4', '#11'],
    [ '5', 'bb6'],
    ['b6',  '#5'],
    [ '6', 'bb7',  '13'],
    ['b7',  '#6'],
    [ '7',  'b8'],
    [ '8',  '#7'],
]

formulas = {
    # Scale formulas
    'scales': {
        # Basic chromatic scale
        'chromatic':          '1,b2,2,b3,3,4,b5,5,b6,6,b7,7',
        # Major scale, its modes, and minor scale
        'major':              '1,2,3,4,5,6,7',
        'minor':              '1,2,b3,4,5,b6,b7',
        # Melodic minor and its modes
        'melodic_minor':      '1,2,b3,4,5,6,7',
        # Harmonic minor and its modes
        'harmonic_minor':     '1,2,b3,4,5,b6,7',
        # Blues scales
        'major_blues':        '1,2,b3,3,5,6',
        'minor_blues':        '1,b3,4,b5,5,b7',
        # Penatatonic scales
        'pentatonic_major':   '1,2,3,5,6',
        'pentatonic_minor':   '1,b3,4,5,b7',
        'pentatonic_blues':   '1,b3,4,b5,5,b7',
        'hirajoshi':          '1,2,b3,5,b6'
    },
    'chords': {
        # Major
        'major':              '1,3,5',
        'major_6':            '1,3,5,6',
        'major_6_9':          '1,3,5,6,9',
        'major_7':            '1,3,5,7',
        'major_9':            '1,3,5,7,9',
        'major_13':           '1,3,5,7,9,11,13',
        'major_7_#11':        '1,3,5,7,#11',
        # Minor
        'minor':              '1,b3,5',
        'minor_6':            '1,b3,5,6',
        'minor_6_9':          '1,b3,5,6,9',
        'minor_7':            '1,b3,5,b7',
        'minor_9':            '1,b3,5,b7,9',
        'minor_11':           '1,b3,5,b7,9,11',
        'minor_7_b5':         '1,b3,b5,b7',
        # Dominant
        'dominant_7':         '1,3,5,b7',
        'dominant_9':         '1,3,5,b7,9',
        'dominant_11':        '1,3,5,b7,9,11',
        'dominant_13':        '1,3,5,b7,9,11,13',
        'dominant_7_#11':     '1,3,5,b7,#11',
        # Diminished
        'diminished':         '1,b3,b5',
        'diminished_7':       '1,b3,b5,bb7',
        'diminished_7_half':  '1,b3,b5,b7',
        # Augmented
        'augmented':          '1,3,#5',
        # Suspended
        'sus2':               '1,2,5',
        'sus4':               '1,4,5',
        '7sus2':              '1,2,5,b7',
        '7sus4':              '1,4,5,b7',
    },
}


#scale here is used to specify the list of the notes and their equivalents
def find_note_index(scale, search_note):
    ''' Given a scale, find the index of a particular note '''
    for i, note in enumerate(scale):
        # Deal with situations where we have a list of enharmonic
        # equivalents, as well as just a single note as and str.
        if type(note) == list:
            if search_note in note:
                return i
        elif type(note) == str:
            if search_note == note:
                return i


def rotate(scale, n):
    ''' Left-rotate a scale by n positions. '''
    return scale[n:] + scale[:n]


def chromatic(key):
    ''' Generate a chromatic scale in a given key. '''
    # Figure out how much to rotate the notes list by and return
    # the rotated version.
    num_rotations = find_note_index(notes, key)
    return rotate(notes, num_rotations)

def find_note_by_root(notes, root):
    '''
    Given a list of notes, find it's alphabet. Useful for figuring out which
    enharmonic equivalent we must use in a particular scale.
    '''
    for note in notes:
        if note[0] == root:
            return note
        
def make_intervals(root):
    labeled = {}
    c = chromatic(root)
    start_index = find_note_index(alphabet, root[0])
    for i, interval in enumerate(intervals):
        for interval_name in interval:
            interval_index = int(interval_name[1]) - 1
            note = c[i % len(c)]
            note_root = alphabet[(start_index + interval_index) % len(alphabet)]
            if note_root is not None:
                labeled[interval_name] = find_note_by_root(note, note_root)
    return labeled


def make_intervals_major(root):
    labeled = {}
    c = chromatic(root)
    start_index = find_note_index(alphabet, root[0])
    for i, interval in enumerate(intervals_major):
        for interval_name in interval:
            interval_index = int(re.sub('[b#]', '', interval_name)) - 1
            note = c[i % len(c)]
            note_root = alphabet[(start_index + interval_index) % len(alphabet)]
            if note_root is not None:
                labeled[interval_name] = find_note_by_root(note, note_root)
    return labeled

def make_intervals_standard(key):
    # Our labeled set of notes mapping interval names to notes
    labels = {}
    
    # Step 1: Generate a chromatic scale in our desired key
    chromatic_scale = chromatic(key)
    
    # The alphabets starting at provided key's alphabet
    alphabet_key = rotate(alphabet, find_note_index(alphabet, key[0]))
    
    # Iterate through all intervals (list of lists)
    for index, interval_list in enumerate(intervals):
    
        # Step 2: Find the notes to search through based on degree
        notes_to_search = chromatic_scale[index % len(chromatic_scale)]
        
        for interval_name in interval_list:
            # Get the interval degree
            degree = int(interval_name[1]) - 1 # e.g. M3 --> 3, m7 --> 7
            
            # Get the alphabet to look for
            alphabet_to_search = alphabet_key[degree % len(alphabet_key)]
            
            try:
                note = [x for x in notes_to_search if x[0] == alphabet_to_search][0]
            except:
                note = notes_to_search[0]
            
            labels[interval_name] = note

    return labels

def make_formula(formula, labeled):
    '''
    Given a comma-separated interval formula, and a set of labeled
    notes in a key, return the notes of the formula.
    '''
    return [labeled[x] for x in formula.split(',')]

def main():
    print("Hello World!")
    print(f"Index of note E: {(find_note_index(notes,'E'))}")
    #print(f"Chromatic scale of E using only chromatic func: {chromatic('E')}")
    #print(f"Key of E: {make_intervals_standard('E')}") 
    #print(keyOfE)
    #keyofE = make_formula(formulas['scales']['hirajoshi'],make_intervals_major('E'))
    print(f"E scale: {make_formula(formulas['scales']['hirajoshi'],make_intervals_major('E'))}")
    
if __name__ == "__main__":
    main()
