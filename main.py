import os
import csv
import genanki

# Edit this with the name of all of your lectures
lecture_names = [
    '1 - Introduction',
    '2 - Processes',
    '3 - Syncronization: Mutual Exclusion',
    '4 - Thread-safe queue',
]

# edit this with what you want to name the csvs (this can be automated, but I prefer control)
csv_names = [
    'lecture1.csv',
    'lecture2.csv',
    'lecture3.csv',
    'lecture4.csv',
]

def read_data(csv_filename): 
    if os.path.exists(csv_filename):
        
        questions = []

        with open(csv_filename, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader, None)
            for row in reader: 
                questions.append(tuple(row))
        
        return questions

def parse_into_anki(question_answers, deck_name):
    my_model = genanki.Model(
    1607392319,
    'Simple Model',
    fields=[
        {'name': 'Question'},
        {'name': 'Answer'},
    ],
    templates=[
        {
        'name': 'Card 1',
        'qfmt': '{{Question}}',
        'afmt': '{{FrontSide}}<hr id="answer">{{Answer}}',
        },
    ])

    my_deck = genanki.Deck(
    2059400191,
    deck_name)

    for pair in question_answers: 
        notecard = genanki.Note(
            model = my_model,
            fields= [pair[0], pair[1]]
        )
        my_deck.add_note(notecard)

    output_name = deck_name + '.apkg'
    genanki.Package(my_deck).write_to_file(output_name)


def main():
    deck_index = input('What lecture are you on? ')
    deck_name = lecture_names[int(deck_index) - 1]
    filename = csv_names[int(deck_index) - 1]


    question_answers = read_data(filename)
    parse_into_anki(question_answers, deck_name)




if __name__ == "__main__":
    main()
