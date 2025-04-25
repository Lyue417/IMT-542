# IMDB Director Analysis Tool

## Overview
This script analyzes and visualizes data about film directors and their movies from the IMDB Top 1000 list. The tool provides insights into top directors by movie count and average ratings, and can analyze individual directors' performance across different decades.

This project was developed for the IMT 542 Portable Information Structures course, building on a previous data integration assignment that combined IMDB movie data with director information.

## Features
- Visualize the top directors by number of movies in the IMDB Top 1000
- Display average ratings alongside movie counts
- Analyze a specific director's performance across different decades
- Command-line interface for flexible usage

## Requirements
- Python 3.7+
- Required libraries:
  - pandas
  - matplotlib
  - numpy

## Installation

1. Clone this repository:

- git clone https://github.com/Lyue417/IMT-542-I3.git

- cd imdb-director-analysis

2. Install required dependencies:

- pip install -r requirements.txt

## Usage

### Basic usage - show top directors
python director_analysis.py

### Analyze a specific director
python director_analysis.py --director "Christopher Nolan"

### Change the number of top directors to display
python director_analysis.py --top_n 10

### Specify a different data file location
python director_analysis.py --data path/to/your/data.json

### Save output visualizations to a specific directory
python director_analysis.py --output_dir my_visualizations


## Data Structure

The tool uses integrated data that combines:
1. IMDB top 1000 movies dataset (CSV format)
2. Director information dataset (JSON format)

The integrated data is structured as a JSON file where each entry represents a director with the following information:
- Director ID
- Movies in top 1000 (titles, years, ratings)
- Average rating across all movies
- Decade-specific performance metrics

## Example Output

When you run the script, it will generate two types of visualizations:

1. **Top Directors Overview**: A bar chart showing the top directors by number of movies in the IMDB Top 1000, with their average ratings displayed.

2. **Director Career Analysis** (when specifying a director): A visualization showing how a specific director's movie count and average ratings have changed over decades.

## Future Enhancements

Potential ways to extend this application:
- Add genre analysis to explore which directors excel in specific genres
- Implement network analysis to visualize collaborations between directors and actors

## License

This project is available for academic and personal use.
