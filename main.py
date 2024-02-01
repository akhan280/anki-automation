import streamlit as st
import genanki
import io
import csv
import pandas as pd
import numpy as np 


def parse_input(input_data):
    reader = csv.reader(io.StringIO(input_data), delimiter=',')
    data = list(reader)
    header = data[0] if data else []  # Capture header
    return header, data[1:]

def display_data(header, data):
    if header and data:
        df = pd.DataFrame(data, columns=header)
        st.dataframe(df)

        st.subheader("Data Summary")
        st.write(f"Number of Rows: {df.shape[0]}")
        st.write(f"Number of Columns: {df.shape[1]}")

        st.subheader("Column Data Types")
        st.write(df.dtypes)

        if df.select_dtypes(include=[np.number]).shape[1] > 0:
            st.subheader("Basic Statistics")
            st.write(df.describe())

        st.subheader("Filter Data")
        col = st.selectbox("Select column to filter", df.columns)
        if df[col].dtype == 'object':
            value = st.selectbox("Select value", df[col].unique())
            st.dataframe(df[df[col] == value])
        else:
            min_value, max_value = st.slider("Select range", df[col].min(), df[col].max(), (df[col].min(), df[col].max()))
            st.dataframe(df[(df[col] >= min_value) & (df[col] <= max_value)])

        st.subheader("Graphical Visualizations")
        plot_type = st.selectbox("Select plot type", ["Bar", "Line", "Pie"])
        selected_column = st.selectbox("Select column for plotting", df.columns)

        if plot_type == "Bar":
            st.bar_chart(df[selected_column])
        elif plot_type == "Line":
            st.line_chart(df[selected_column])
        elif plot_type == "Pie" and df[selected_column].dtype == 'object':
            st.pyplot(df[selected_column].value_counts().plot.pie(autopct='%1.1f%%'))

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
        ]
    )

    my_deck = genanki.Deck(
        2059400191,
        deck_name
    )

    for pair in question_answers:
        notecard = genanki.Note(
            model=my_model,
            fields=[pair[0], pair[1]]
        )
        my_deck.add_note(notecard)

    output_name = deck_name + '.apkg'
    genanki.Package(my_deck).write_to_file(output_name)
    return output_name

def main():
    st.title("Areeb's CSV to Anki Converter")

    st.text_area("How to Use:",
                 ("1. Take your lecture.\n"
                  "2. Fine tune a GPT to take in the material, ask it to make a CSV in a Question, Answer format for Anki Flash cards.\n"
                  "3. Paste the csv here.\n"
                  "4. Download the generated .apkg file and import it into Anki.\n"
                  "5. Will be adding support soon which does this process from start to end"),
                 height=100, disabled= True)

    deck_name = st.text_input("Enter the name of the deck:", "Urdu 172 Vocab List 2")

    user_input = st.text_area("Enter your data (CSV format):", 
                              "Question,Answer\nSample Question,Sample Answer")

    if st.button('Preview Data'):
        header, data = parse_input(user_input)
        display_data(header, data)

    if st.button('Convert to Anki Deck'):
        _, question_answers = parse_input(user_input)
        if deck_name and question_answers:  # Check if deck name is not empty and data is present
            output_file = parse_into_anki(question_answers, deck_name)
            st.success("Anki Deck Created Successfully!")
            st.download_button(
                label="Download Anki Deck",
                data=open(output_file, "rb"),
                file_name=output_file,
                mime="application/octet-stream"
            )

if __name__ == "__main__":
    main()
