import duckdb
import pathlib
import plotly.express as px

# Define file paths for the data
harry_potter_data = pathlib.Path("data", "harry potter movies")
dialogue_file = pathlib.Path(harry_potter_data, "Dialogue.csv")
characters_file = pathlib.Path(harry_potter_data, "Characters.csv")
chapters_file = pathlib.Path(harry_potter_data, "Chapters.csv")
movies_file = pathlib.Path(harry_potter_data, "Movies.csv")

# SQL query to filter dialogues mentioning 'voldemort' and join relevant tables
filter_dialogue_sql = f"""
    select
        d."Dialogue ID" as dialogue_id,
        c."Character Name" as character,
        m."Movie Title" as movie,
        d."Dialogue" as dialogue
    from read_csv('{dialogue_file}') d
    inner join read_csv('{characters_file}') c
        on d."Character ID" = c."Character ID"
    inner join read_csv('{chapters_file}') ch
        on d."Chapter ID" = ch."Chapter ID"
    inner join read_csv('{movies_file}') m
        on ch."Movie ID" = m."Movie ID"
    where contains(lower(d."Dialogue"), 'voldemort')
"""

# Execute the query and store the result in a variable
filtered_dialogue = duckdb.sql(filter_dialogue_sql)

# SQL query to count the number of lines per character per movie mentioning 'Voldemort'
movie_count_sql = """
    select
        movie,
        character,
        count(dialogue_id) as num_lines
    from filtered_dialogue
    group by
        movie,
        character
"""

# Execute the query to get the count of dialogues mentioning 'Voldemort'
movie_count = duckdb.sql(movie_count_sql)

# SQL query to get the order of movies by Movie ID for consistent plotting
movie_order_sql = f"""
    select distinct "Movie Title"
    from read_csv('{movies_file}')
    order by "Movie ID"
"""

# Fetch the movie titles in the order of their IDs
movie_order_result = duckdb.sql(movie_order_sql).fetchall()
movie_order = [movie[0] for movie in movie_order_result]

# SQL query to get the order of characters based on the total number of lines mentioning 'voldemort'
character_order_sql = f"""
    select
        character,
        sum(num_lines) as total_num_lines
    from movie_count
    group by
        character
    order by total_num_lines desc
"""

# Fetch the characters ordered by the total number of lines mentioning 'voldemort'
character_order_result = duckdb.sql(character_order_sql).fetchall()
character_order = [character[0] for character in character_order_result]

# Plot the data using Plotly Express
fig = px.bar(
    movie_count.df(),   # Data source
    x="num_lines",      # X-axis: number of lines mentioning 'Voldemort'
    y="character",      # Y-axis: characters
    color="movie",      # Color by movie
    title="Who Mentioned He Who Shall Not Be Named The Most?",  # Chart title
    category_orders={   # Order the categories by the specified lists
        "movie": movie_order,
        "character": character_order
    },
    labels={            # Label the axes
        "character": "Character",
        "num_lines": "# of Lines",
        "movie": "Movie"
    }
)

# Show the plot
fig.show()
