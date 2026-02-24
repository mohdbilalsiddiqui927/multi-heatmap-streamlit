Multi-Heatmap Visualization App
This repository contains a Streamlit-based application for interactive scientific heatmap visualization.  

The app is intended for researchers, students, and data analysts who want to explore CSV data and generate high-quality, publication-ready heatmaps with minimal setup.

What This App Does
- Accepts CSV files as input
- Automatically detects numeric columns
- Generates multiple types of heatmaps
- Allows figure customization (size, font, color map)
- Exports figures in high resolution
- Generates reproducible Methods text for manuscripts

Supported Heatmap Types
- Correlation Heatmap (Pearson, Spearman, Kendall)
- Clustered (Hierarchical) Heatmap
- Distance Matrix Heatmap
- 2D Density Heatmap
- Confusion Matrix Heatmap

Project Structure
multi-heatmap-streamlit/

├── heatmap.py # Main Streamlit application

├── requirements.txt # Python dependencies

├── README.md # Documentation

├── LICENSE # MIT License

└── .gitignore


System Requirements
- Python 3.8 or higher
- Windows / Linux / macOS

Installation and Usage (Complete Steps)
Step 1: Clone the Repository
```bash
git clone https://github.com/mohdbilalsiddiqui927/multi-heatmap-streamlit.git
cd multi-heatmap-streamlit

Step 2: Create a Virtual Environment (Recommended)
python -m venv venv
Activate the environment:
Windows
venv\\Scripts\\activate
Linux / macOS
source venv/bin/activate

Step 3: Install Dependencies
pip install -r requirements.txt
Step 4: Run the Application

streamlit run heatmap.py
The app will open automatically in your default web browser.

Input Data Format
File type: CSV
Minimum requirement: at least two numeric columns
Rows with missing values are removed automatically
Non-numeric columns may be used for confusion matrix labels

Figure Export
All heatmaps can be exported in the following formats:
PNG (high resolution)
PDF (vector format)
SVG (editable vector format)
Export settings such as DPI, font, and figure size are applied consistently.

Reproducibility
The application allows exporting all analysis parameters as a JSON file.
This enables exact reproduction of figures and transparent sharing of analysis settings.

Dependencies
All required Python libraries are listed in requirements.txt.

License
This project is licensed under the MIT License.

Contributions
Suggestions, bug reports, and improvements are welcome through GitHub issues or pull requests.








