# Learning Python for Data with Harry Potter

## Setting Up Your Environment

### Sign Up for GitHub
If you don't already have a github.com account, go to [https://github.com/signup](https://github.com/signup) and create one.

### Install the Applications
#### GitHub Desktop

GitHub Desktop is a graphical interface that simplifies using Git and GitHub. It allows you to manage your repositories and collaborate on projects easily.

1. **Download GitHub Desktop**:
   - Navigate to [https://desktop.github.com/download/](https://desktop.github.com/download/).
   - Click the "Download for [Your OS]" button. The website should detect your operating system automatically.

2. **Install GitHub Desktop**:
   - Once the download is complete, open the installer file.
   - Follow the on-screen instructions to complete the installation.

3. **Set Up GitHub Desktop**:
   - Launch GitHub Desktop.
   - Sign in to your GitHub account or create a new one if you don't have an account yet.
   - You can configure your Git settings (name and email) within the application, which will be used for commits.

#### Miniconda

Miniconda is a minimal installer for Conda, which includes only Conda and its dependencies. It allows you to manage Python packages and environments efficiently.

1. **Download Miniconda**:
   - Visit the [Miniconda download page](https://docs.conda.io/en/latest/miniconda.html).
   - Choose the installer for your operating system (Windows, macOS, or Linux) and your preferred Python version (usually Python 3.x).

2. **Install Miniconda**:
   - Run the installer and follow the on-screen instructions.
   - During installation, you can choose whether to add Miniconda to your system's PATH. It's recommended to do so for easy access to the `conda` command.
   - After installation, you may need to restart your terminal or command prompt for the changes to take effect.

3. **Verify Installation**:
   - Open a terminal or command prompt.
   - Type `conda --version` to verify that Conda is installed correctly. You should see the version number displayed.

#### PyCharm Community Edition

PyCharm is a popular integrated development environment (IDE) for Python, providing features like code editing, debugging, and testing tools. The Community Edition is free and open-source.

1. **Download PyCharm**:
   - Go to the [PyCharm download page](https://www.jetbrains.com/pycharm/download/).
   - Choose the Community edition for your operating system.

2. **Install PyCharm**:
   - Download the installer for your operating system.
   - Run the installer and follow the on-screen instructions to install PyCharm.

### Configure the Environment


## Data Analysis with Pandas
This section details how [harry_potter_analysis_pandas.py](harry_potter_analysis_pandas.py) uses pandas to process data
and visualize it with Plotly.

The data is sourced from CSV files related to the "Harry Potter" movies to identify the characters who most
frequently dared to say Voldemort's name out loud.

### 1. Importing Libraries

The script starts by importing the necessary libraries:

```python
import pandas as pd
import pathlib
import plotly.express as px
```

- `pandas`: For data manipulation and analysis.
- `pathlib`: For handling file paths.
- `plotly.express`: For creating visualizations.

### 2. Defining File Paths

The paths to the CSV files are defined using `pathlib.Path`:

```python
harry_potter_data = pathlib.Path("data", "harry potter movies")
dialogue_file = pathlib.Path(harry_potter_data, "Dialogue.csv")
characters_file = pathlib.Path(harry_potter_data, "Characters.csv")
chapters_file = pathlib.Path(harry_potter_data, "Chapters.csv")
movies_file = pathlib.Path(harry_potter_data, "Movies.csv")
```

### 3. Reading CSV Files

The data from the CSV files is read into pandas DataFrames:

```python
dialogue_df = pd.read_csv(dialogue_file)
characters_df = pd.read_csv(characters_file)
chapters_df = pd.read_csv(chapters_file)
movies_df = pd.read_csv(movies_file)
```

### 4. Flagging Dialogues Mentioning Voldemort

A new column is added to the `dialogue_df` DataFrame to flag dialogues that mention "Voldemort", all casing is
converted to lowercase to ensure every instance is found, regardless of casing:

```python
dialogue_df['says_voldemort'] = dialogue_df['Dialogue'].str.lower().str.contains('voldemort')
```

### 5. Filtering Dialogues

The dialogue DataFrame is filtered to include only those dialogues that mention Voldemort:

```python
dialogue_filtered_df = dialogue_df[dialogue_df['says_voldemort']]
```

### 6. Merging DataFrames

The DataFrames are merged to combine all relevant information, including character names, movie titles, and dialogues:

```python
merged_df = (dialogue_filtered_df.merge(characters_df, left_on='Character ID', right_on='Character ID')
             .merge(chapters_df, left_on='Chapter ID', right_on='Chapter ID')
             .merge(movies_df, left_on='Movie ID', right_on='Movie ID'))
```

### 7. Counting Lines per Character per Movie

The script counts the number of lines each character has in each movie, specifically those that mention Voldemort:

```python
movie_count = (merged_df.groupby(['Movie Title', 'Character Name'])
               .size()
               .reset_index(name='num_lines'))
```

### 8. Ordering Movies and Characters

The movies and characters are ordered based on certain criteria, such as the order of appearance and the number of lines mentioning Voldemort. This order is used to maintain consistency in the visualization.

```python
# Get the order of movies by Movie ID
movie_order = movies_df.sort_values('Movie ID')['Movie Title'].tolist()

# Get the order of characters by total number of lines mentioning Voldemort
character_order = (movie_count.groupby('Character Name')['num_lines']
                   .sum()
                   .sort_values(ascending=False)
                   .index
                   .tolist())
```

### 9. Creating the Bar Chart

Finally, a bar chart is created using Plotly Express, visualizing the number of lines each character has per movie that mention Voldemort:

```python
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
```

This visualization provides insights into which characters mention Voldemort the most across the Harry Potter movies.

## Data Analysis with DuckDB

This section details how [harry_potter_analysis_duckdb.py](harry_potter_analysis_duckdb.py) uses DuckDB to process data
and visualize it with Plotly.

The data is sourced from CSV files related to the "Harry Potter" movies to identify the characters who most
frequently dared to say Voldemort's name out loud.

### 1. Importing Libraries

The script starts by importing the necessary libraries:

```python
import duckdb
import pathlib
import plotly.express as px
```

- `duckdb`: For performing SQL-like queries on the data.
- `pathlib`: For handling file paths.
- `plotly.express`: For creating visualizations.

### 2. Defining File Paths

The paths to the CSV files are defined using `pathlib.Path`:

```python
harry_potter_data = pathlib.Path("data", "harry potter movies")
dialogue_file = pathlib.Path(harry_potter_data, "Dialogue.csv")
characters_file = pathlib.Path(harry_potter_data, "Characters.csv")
chapters_file = pathlib.Path(harry_potter_data, "Chapters.csv")
movies_file = pathlib.Path(harry_potter_data, "Movies.csv")
```

### 3. SQL Query for Filtering Dialogues

An SQL query is written to filter the dialogues mentioning Voldemort's name and join relevant tables
to include character and movie information, all dialogue casing is
converted to lowercase to ensure every instance is found, regardless of casing:

```python
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
```

### 4. Executing the Query

The query is executed using DuckDB, and the result is stored in the `filtered_dialogue` variable:

```python
filtered_dialogue = duckdb.sql(filter_dialogue_sql)
```

### 5. Counting Lines per Character per Movie

This subsequent SQL query counts the number of lines each character has per movie that mention Voldemort's name,
note that the `filtered_dialogue` variable, where we stored the result of the previous query, is used as the
`from` table in this SQL query:

```python
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
```

The result is stored in the `movie_count` variable:

```python
movie_count = duckdb.sql(movie_count_sql)
```

### 6. Ordering Movies and Characters

To display a consistent order in the visualization, the script fetches the sort order of movies and characters:

```python
# Get the order of movies by Movie ID (movies in release order) for consistent plotting
movie_order_sql = f"""
    select distinct "Movie Title"
    from read_csv('{movies_file}')
    order by "Movie ID"
"""
movie_order_result = duckdb.sql(movie_order_sql).fetchall()
movie_order = [movie[0] for movie in movie_order_result]

# Get the order of characters by total number of lines mentioning Voldemort's name
character_order_sql = f"""
    select
        character,
        sum(num_lines) as total_num_lines
    from movie_count
    group by
        character
    order by total_num_lines desc
"""
character_order_result = duckdb.sql(character_order_sql).fetchall()
character_order = [character[0] for character in character_order_result]
```

### 7. Creating the Bar Chart

A bar chart is created using Plotly Express to visualize the number of lines each character has in each movie that
mention Voldemort by name. The chart is stored in the variable `fig`:

```python
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
```

## 8. Displaying the Plot

Finally, the plot is displayed:

```python
fig.show()
```

This visualization provides insights into which characters mentioned Voldemort the most across the Harry Potter movies.
