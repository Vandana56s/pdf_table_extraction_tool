import fitz  # PyMuPDF
import pandas as pd

def extract_tables_from_pdf(pdf_path, row_spacing_threshold=5):
    doc = fitz.open(pdf_path)
    extracted_data = {}

    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        words = page.get_text("words")  
        words.sort(key=lambda w: (w[1], w[0]))  # Sort by Y (row), then X (column)

        rows = []
        current_row = []
        last_y = None

        for w in words:
            x0, y0, x1, y1, word, *_ = w
            word = word.strip()
            if not word:
                continue

            if last_y is None or abs(y0 - last_y) > row_spacing_threshold:
                if current_row:
                    rows.append(current_row)
                current_row = [word]
                last_y = y0
            else:
                current_row.append(word)

        if current_row:
            rows.append(current_row)

        df = pd.DataFrame(rows)

        # Clean up
        df.replace('', pd.NA, inplace=True)
        df.dropna(how='all', inplace=True)
        df = df.applymap(lambda x: str(x).strip() if pd.notna(x) else x)

        # Remove duplicate headers
        df = df.drop_duplicates()

        if not df.empty:
            extracted_data[page_num + 1] = df

    return extracted_data
