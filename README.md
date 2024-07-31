# Learning Python for Data with Harry Potter

## Setting Up Your Environment

### Sign Up for GitHub
If you don't already have a github.com account, go to [https://github.com/signup](https://github.com/signup) and create one.

### Run and Develop in GitHub Codespaces

This guide will walk you through the steps to fork a repository on GitHub, navigate to your fork, and start a [GitHub Codespaces environment](https://docs.github.com/en/codespaces/overview) for development.

#### 1. Navigating to the Repository

1. **Log in to GitHub**:
   - Go to [github.com](https://github.com/) and log in with your credentials.

2. **Access the Repository**:
   - Visit the repository URL: [https://github.com/jharris126/learn-python-data-analytics-with-harry-potter](https://github.com/jharris126/learn-python-data-analytics-with-harry-potter).

#### 2. Forking the Repository

1. **Fork the Repository**:
   - On the repository's page, click the "Fork" button in the top-right corner. This button is usually located near the "Star" button.
   - You don't need to change anything on the "Create a new fork" page. Click the green "Create fork" button in the bottom right to finish creating your own fork of the code.
   - GitHub will create a copy of the repository under your account. This forked repository will now be in your GitHub account, where you can make changes without affecting the original repository.

#### 3. Navigating to Your Fork

1. **Go to Your Fork**:
   - After forking, GitHub will redirect you to the forked repository. If not, navigate to your profile by clicking on your profile picture in the top-right corner and selecting "Your repositories."
   - In the list of repositories, click on the forked repository, which will have the same name as the original but will be under your username (e.g., `https://github.com/yourusername/learn-python-data-analytics-with-harry-potter`).

#### 4. Starting a GitHub Codespace

GitHub Codespaces provides a cloud-based development environment. Here's how to start one:

1. **Open Codespaces**:
   - On your forked repository page, click on the "Code" button (usually green) near the top-right of the page, next to the "Add file" button.
   - Select "Codespaces" on the ribbon, then "Create codespace on main".

2. **Create a New Codespace**:
   - GitHub will set up the environment, which may take a few minutes. This setup includes installing the necessary dependencies and configuring the environment based on the repository's settings.
   - After the `postCreateCommand` finishes running in the "TERMINAL", you should see something like: `/workspaces/learn-python-data-analytics-with-harry-potter (main) $ `. This means your Codespaces environment is ready to use.

3. **Test Run and Start Developing**:
   - Click on `harry_potter_analysis_pandas.py` in the "EXPLORER" pane on the left to open the file to test run.
   - Click the play button triangle in the top right to run the python code in the file, this should run the code and launch a new browser tab with the bar chart analysis. To dive deeper into what this code does and how, see the [Data Analysis with Pandas](#data-analysis-with-pandas) section below.
   - You can now tweak the existing files or add your own analyses with no affect on the original code repository this was forked from.


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
