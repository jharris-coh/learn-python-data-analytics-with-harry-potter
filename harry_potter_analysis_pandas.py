import pandas as pd
import pathlib
import plotly.express as px

# define file paths
harry_potter_data = pathlib.Path("data", "harry potter movies")
dialogue_file = pathlib.Path(harry_potter_data, "Dialogue.csv")
characters_file = pathlib.Path(harry_potter_data, "Characters.csv")
chapters_file = pathlib.Path(harry_potter_data, "Chapters.csv")
movies_file = pathlib.Path(harry_potter_data, "Movies.csv")

# read csv files into pandas dataframes
dialogue_df = pd.read_csv(dialogue_file)
characters_df = pd.read_csv(characters_file)
chapters_df = pd.read_csv(chapters_file)
movies_df = pd.read_csv(movies_file)

# flag dialogues mentioning Voldemort
dialogue_df['says_voldemort'] = dialogue_df['Dialogue'].str.lower().str.contains('voldemort')

# filter for dialogues mentioning voldemort
dialogue_filtered_df = dialogue_df[dialogue_df['says_voldemort']]

# merge dataframes to include character, movie, and dialogue information
merged_df = (dialogue_filtered_df.merge(characters_df, left_on='Character ID', right_on='Character ID')
             .merge(chapters_df, left_on='Chapter ID', right_on='Chapter ID')
             .merge(movies_df, left_on='Movie ID', right_on='Movie ID'))

# count the number of lines per character per movie mentioning voldemort
movie_count = (merged_df.groupby(['Movie Title', 'Character Name'])
               .size()
               .reset_index(name='num_lines'))

# get the order of movies by Movie ID
movie_order = movies_df.sort_values('Movie ID')['Movie Title'].tolist()

# get the order of characters by total number of lines mentioning Voldemort
character_order = (movie_count.groupby('Character Name')['num_lines']
                   .sum()
                   .sort_values(ascending=False)
                   .index
                   .tolist())

# chart as a bar chart using plotly express
fig = px.bar(
    movie_count,
    x="num_lines",
    y="Character Name",
    color="Movie Title",
    title="Who Mentioned He Who Shall Not Be Named The Most?",
    category_orders={
        "Movie Title": movie_order,
        "Character Name": character_order
    },
    labels={
        "Character Name": "Character",
        "num_lines": "# of Lines",
        "Movie Title": "Movie"
    }
)
fig.show()
