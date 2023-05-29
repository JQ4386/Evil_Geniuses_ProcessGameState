# Evil_Geniuses_ProcessGameState
This project employs a Python class, "ProcessGameState," utilizing ETL techniques, boundary checking, JSON parsing, and heatmap analysis for CounterStrike game data. The solution aims to minimize runtime, reduce external dependencies, and provide actionable insights to coaching staff.

The project is a Python script that utilizes several libraries and implements a class called `ProcessGameState` for processing and analyzing game data stored in a Parquet file.

- Libraries: The script imports various Python libraries including:
  - `numpy` (imported as `np`) for numerical computations.
  - `pandas` (imported as `pd`) for data manipulation and analysis.
  - `pyarrow.parquet` (imported as `pq`) for reading Parquet files.
  - `matplotlib.path` (imported as `path`) for defining and working with paths.
  - `matplotlib.pyplot` (imported as `plt`) for creating visualizations.
  - `seaborn` (imported as `sns`) for statistical data visualization.

- Class: The script defines a class called `ProcessGameState` that performs various operations on the game data:
  - Initialization: The class constructor takes the path to a Parquet file, a list of vertices representing a specified chokepoint, and a range of z-values. It reads the Parquet file into a DataFrame, stores the chokepoint vertices, and preprocesses the data.
  - Preprocessing: The `_preprocess` method adds additional columns to the DataFrame. It determines whether each row's location is inside the specified chokepoint, extracts the weapon class from the inventory column, and checks if a player has a rifle or SMG.
  - Question 2a: The `question_2a` method filters the DataFrame to include Team2 players playing as T and inside the chokepoint. It then removes duplicate values for the same player in the same round. The resulting DataFrame provides insights on whether passing through the specified chokepoint is a common strategy for Team2 on side T.
  - Question 2b: The `question_2b` method filters the DataFrame to include Team2 players playing as T, inside BombsiteB, and having a rifle or SMG. It then calculates the average timer (in seconds) for at least two such players to enter BombsiteB.
  - Question 2c: The `create_heatmap` method filters the DataFrame to include Team2 players playing as CT inside BombsiteB. It creates a KDE jointplot (heatmap) of the players' positions using seaborn.

- Usage: The script defines input variables including the vertices of the chokepoint, the z-value range, and the path to the Parquet file. An instance of the `ProcessGameState` class is created using these inputs. The `question_2a` and `question_2b` methods are called to obtain the respective results. Finally, the `create_heatmap` method generates a KDE heatmap of the players' positions.


The script also includes additional comments to explain the purpose of each section and method and to provide insights into implementation choices.
