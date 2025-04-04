import os
import pandas as pd
from extract_table import extract_tables_from_pdf

def process_all_pdfs(pdf_folder, output_folder):
    """
    Processes all PDFs in a folder, extracts tables, and saves them to Excel.
    :param pdf_folder: Folder containing PDF files.
    :param output_folder: Folder to save Excel files.
    """
    os.makedirs(output_folder, exist_ok=True)

    for filename in os.listdir(pdf_folder):
        if filename.lower().endswith(".pdf"):
            pdf_path = os.path.join(pdf_folder, filename)
            output_filename = os.path.splitext(filename)[0] + ".xlsx"
            output_excel_path = os.path.join(output_folder, output_filename)

            print(f"\n Processing: {filename}")

            tables = extract_tables_from_pdf(pdf_path)

            if not tables:
                print(f"⚠️ No tables found in {filename}. Skipping...")
                continue

            # Save to Excel
            with pd.ExcelWriter(output_excel_path, engine='openpyxl') as writer:
                for page_num, df in tables.items():
                    sheet_name = f"Page_{page_num}"
                    df.to_excel(writer, sheet_name=sheet_name, index=False, header=False)

            print(f"✅ Saved tables to: {output_excel_path}")


pdf_folder = "pdfs"
output_folder = "excel_output"
process_all_pdfs(pdf_folder, output_folder)
