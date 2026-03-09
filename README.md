# Automated Data Report & Dashboard Generator

An automated data analysis tool that generates interactive dashboards and HTML reports from CSV files.

## Features

- **Automated Data Analysis** - Generates summary statistics, correlations, and key insights automatically
- **Interactive Dashboard** - Real-time data exploration with Streamlit
- **HTML Report Generation** - Creates polished reports with charts and visualizations
- **Data Quality Checks** - Identifies missing values, duplicates, and data issues
- **Upload Your Own Data** - Support for any CSV file

## Project Structure

```
automated_report/
├── data/
│   └── sample_data.csv        # Sample sales data
├── src/
│   ├── analyzer.py            # Data analysis module
│   └── generator.py           # HTML report generator
├── output/
│   ├── report.html           # Generated HTML report
│   └── charts/               # Generated chart images
├── main.py                   # Report generation script
├── dashboard.py              # Streamlit dashboard
└── requirements.txt         # Python dependencies
```

## Installation

```bash
pip install -r requirements.txt
```

## Usage

### Generate HTML Report

```bash
python main.py
```

The report will be saved to `output/report.html`

### Run Dashboard

```bash
streamlit run dashboard.py
```

The dashboard will open in your browser at `http://localhost:8501`

## Sample Data

The project includes sample sales data with the following columns:
- date, product, category, sales, quantity, profit, customer_age, customer_city

## Tech Stack

- **Python** - Programming language
- **Pandas** - Data manipulation and analysis
- **Matplotlib/Seaborn** - Data visualization
- **Streamlit** - Interactive dashboard framework
- **HTML/CSS** - Report generation

## Customization

To analyze your own data:
1. Replace `data/sample_data.csv` with your CSV file
2. Run `python main.py` for HTML report
3. Or run `streamlit run dashboard.py` and upload your file directly

## License

MIT
