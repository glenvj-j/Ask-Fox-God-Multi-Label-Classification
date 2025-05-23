import pandas as pd
import streamlit as st
import pickle
import datetime
import numpy as np
import base64

st.set_page_config(
    page_title="Ask Fox God",
    layout="wide"
)

def set_background(image_path):
    with open(image_path, "rb") as img_file:
        encoded = base64.b64encode(img_file.read()).decode()
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("data:image/png;base64,{encoded}");
            background-size: cover;
            background-position: center;
            background-repeat: repeat;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# Call the function with your file path
set_background("https://raw.githubusercontent.com/glenvj-j/Ask-Fox-God-Multi-Label-Classification/refs/heads/main/image/background.png")

# Set black background and white text
st.markdown(
    """
    <style>
    body {
        background-color: black;
        color: white;
    }
    .stApp {
        background-color: black;
    }
    </style>
    """,
    unsafe_allow_html=True
)
st.markdown(
    """
    <h1 style='text-align: center;'>🦊 Unveil the BABYMETAL Setlist Prophecy</h1>
    <p style='text-align: center; font-size: 20px;'>Speak your preferences… and the Fox God shall reveal the songs.</p>
    """,
    unsafe_allow_html=True
)


# Load dataset
url = '../dataset/clean_dataset.csv'
df = pd.read_csv(url, index_col=None)

def selection_input():
    global new_album
    global new_songs_list
    df_country_city = df.groupby('country')['city'].unique().reset_index()
    df_city_venue = df.groupby('city')['venue'].unique().reset_index()

    Selected_country = st.selectbox("Select Country", options=df_country_city['country'])
    allowed_option_city = df_country_city[df_country_city['country'] == Selected_country]['city'].iloc[0].tolist()
    Selected_city = st.selectbox("Select City", options=allowed_option_city)
    allowed_option_venue = df_city_venue[df_city_venue['city'] == Selected_city]['venue'].iloc[0].tolist()
    Selected_venue = st.selectbox("Select Venue", options=allowed_option_venue)

    Festival = st.radio("Is Festival?", options=[False, True], horizontal=True)
    new_album = st.radio("New Album?", options=[False, True], horizontal=True)
    if new_album == True :
        new_songs = st.text_area("Enter three New Songs, separated by commas",value="from me to u,  Song 3,  Kon! Kon!")
        if new_songs:
            new_songs_list = [t.strip() for t in new_songs.split(",")]
            if len(new_songs_list) == 3:
                st.write('')
            else:
                st.warning("Please enter exactly songs texts separated by commas.")
    else :
        new_songs_list = ['from me to u',  'Song 3',  'Kon! Kon!']

    date = st.date_input(
        "Select Concert Date",
        format="DD/MM/YYYY",
    )
    date_ts = pd.Timestamp(date)

    last_concert = pd.to_datetime(df['eventDate'].tail(1).values[0])
    days_since_last_concert = date_ts - last_concert

    days_since_new_album = st.number_input('Days Since New Album', min_value=0, max_value=365, step=1, value=0)

    year_input = date.year
    month_input = date.month

    selected_dataframe = pd.DataFrame({
        'country': Selected_country,
        'city': Selected_city,
        'venue': Selected_venue,
        'days_since_last_concert': days_since_last_concert.days,
        'days_since_new_album': days_since_new_album,
        'month': month_input,
        'year': year_input,
        'festival': Festival,
        'new_album': new_album
    }, index=[0])
    return selected_dataframe

col1, col2,col3 = st.columns([2,1,3])


col1, col2, col3 = st.columns([3, 2, 3])  # Adjust ratio to center col2

with col1:
    selected_dataframe = selection_input()

with col2:
    st.markdown(
    "<h6 style='text-align: center;'>Ready to summon your setlist predictions?</h6>",
    unsafe_allow_html=True
)    
    ask_button = st.button("🦊 **Ask Fox God**", use_container_width=True)

with col3:
    if ask_button:
        # Load model
        loaded_model = pickle.load(open(f'../dataset/Prediction_Model.sav', 'rb'))
        y_pred_proba = loaded_model.predict_proba(selected_dataframe) * 100

        rounded_y_pred_proba = np.round(y_pred_proba, 0)

        song_name = df.loc[:, '4 no Uta':].columns
        predicted_song = pd.DataFrame(rounded_y_pred_proba, columns=song_name)
        predicted_song = predicted_song.T.reset_index().rename(columns={0: 'Percentage', 'index': 'Song Name'}).sort_values(by='Percentage', ascending=False).head(9)

        if new_album:
            predicted_song = predicted_song.iloc[:-3]
            new_song = pd.DataFrame(100, columns=new_songs_list, index=[0]).T.reset_index().rename(columns={0: 'Percentage', 'index': 'Song Name'})
            predicted_song = pd.concat([new_song, predicted_song], axis=0)

        predicted_song = predicted_song.reset_index(drop=True)
        predicted_song['Percentage'] = predicted_song['Percentage'].apply(lambda x: str(int(x)) + ' %')
        st.success('Here is your answer:')
        # st.dataframe(predicted_song)
        predicted_song['Search'] = predicted_song['Song Name'].apply(
            lambda name: f"<a href='https://www.youtube.com/results?search_query={name}+BABYMETAL' target='_blank'>🎧 Search</a>"
        )

        # Drop index to keep it clean
        st.write(predicted_song[['Song Name', 'Percentage', 'Search']].to_html(escape=False, index=False), unsafe_allow_html=True, use_container_width=True)
    else :
        # st.info('Your Answer will showed here')
        st.markdown(
    """
    <div style="background-color: #142536; padding: 1em; text-align: center; color: #C7EBFF; border-radius: 12px;">
        Your Answer will be shown here
    </div>
    """,
    unsafe_allow_html=True
)
        # st.markdown("<p style='text-align: center;'>Your Answer will showed here</p>", unsafe_allow_html=True)


st.markdown(
    """
    <hr>
    <p style='text-align: center; font-size: 13px; color: gray;'>
        This project is created for personal and educational purposes only.<br>
        All rights to the music, images, and content related to <strong>BABYMETAL</strong> belong to <strong>Amuse Inc.</strong> and their respective copyright holders.<br>
        No copyright infringement intended. This is a fan-made, non-commercial project.
    </p>
    """,
    unsafe_allow_html=True
)





