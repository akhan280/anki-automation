import os
import csv


def read_data(csv_filename): 
    if os.path.exists(csv_filename):
        
        questions = []

        with open(csv_filename, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader, None)
            for row in reader: 
                questions.append(tuple(row))
        
        print(questions)


def main():
    filename = input('Enter the name of the q/a csv')
    read_data(filename)



if __name__ == "__main__":
    main()
