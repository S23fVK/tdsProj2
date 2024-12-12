# tdsProj2
Python script to automate data analysis and visualization using LLMs

**AutoLysis** is a Python-based script that automates the process of analyzing, visualizing, and narrating insights from a given CSV dataset. By using machine learning through GPT-4o-Mini, the script generates easy-to-understand reports, including visualizations and a narrative summary.

## Features
- Automatically loads and analyzes CSV datasets.
- Generates summary statistics and checks for missing values.
- Uses GPT-4o-Mini for suggesting advanced data analysis and insights.
- Creates meaningful visualizations such as correlation heatmaps and distribution plots.
- Generates a human-readable report summarizing the analysis, insights, and actionable recommendations.

## Requirements
Before running the script, make sure you have the following:
- Python 3.7 or higher
- The required Python libraries:
  - `pandas`
  - `matplotlib`
  - `seaborn`
  - `openai`

### Install required dependencies:
```bash
pip install pandas matplotlib seaborn openai
```

## Usage

### Running the Script

To use **AutoLysis**, run the script with the desired CSV file as an argument in the below format.

```bash
uv run autolysis.py dataset.csv
```

This will:
1. **Load the dataset** from `dataset.csv`.
2. Automatically analyze the dataset and perform basic checks (summary statistics, missing values, etc.).
3. Consult GPT-4o-Mini for advanced analysis suggestions.
4. Generate visualizations (such as a correlation heatmap and distribution plot).
5. Create a `README.md` report summarizing the analysis, insights, and visualizations.

### Expected Output

- **README.md**: A Markdown report summarizing the data analysis and insights, including recommendations for further actions.
- **PNG images**: Visualizations of the dataset such as correlation heatmaps and distribution plots, saved as `.png` files.
