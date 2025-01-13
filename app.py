from flask import Flask, request, send_file
import pandas as pd
import os

app = Flask(__name__)

# Create folders for uploads and outputs
UPLOAD_FOLDER = "uploads"
OUTPUT_FOLDER = "outputs"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

def process_files(file_paths):
    """Process uploaded files and consolidate data into an Excel file."""
    data = []
    for file_path in file_paths:
        if file_path.endswith(".csv"):
            # Read CSV files
            df = pd.read_csv(file_path)
            data.append(df)
        elif file_path.endswith(".xlsx"):
            # Read Excel files
            df = pd.read_excel(file_path)
            data.append(df)
    # Combine all data into one DataFrame
    consolidated_df = pd.concat(data, ignore_index=True)
    return consolidated_df

@app.route('/upload', methods=['POST'])
def upload_files():
    """Handle file uploads and return a consolidated Excel file."""
    files = request.files.getlist("files")  # Get uploaded files
    file_paths = []

    # Save uploaded files to the uploads folder
    for file in files:
        file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(file_path)
        file_paths.append(file_path)

    # Process files
    consolidated_df = process_files(file_paths)

    # Save the consolidated file to the outputs folder
    output_file = os.path.join(OUTPUT_FOLDER, "Consolidated_Data.xlsx")
    consolidated_df.to_excel(output_file, index=False)

    # Return the Excel file for download
    return send_file(output_file, as_attachment=True)

if __name__ == '__main__':
    app.run(port=5000)