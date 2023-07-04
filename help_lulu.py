import PyPDF2
from openpyxl import Workbook
import os

units = ['Sq', 'Ssk', 'Sal', 'Str', 'Sk', 'Spk', 'Svk', 'Smr1',
         'Smr2', 'Sdq', 'Sdr', 'Vv', 'Vmp', 'Vmc', 'Vvc', 'Vvv', 'Spc', 'Sds']


def extract_text_from_pdf(file_path):
    extracted_data = []
    for file in os.listdir(file_path):
        if file.endswith(".pdf"):
            with open(os.path.join(file_path, file), 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                extracted_text = ''
                for page in reader.pages:
                    extracted_text += page.extract_text()
                lines = extracted_text.split('\n')
                lines = list(filter(lambda x: any(unit in x for unit in units) and any(
                    char.isdigit() for char in x), lines))[:-4]
                print(lines)
                lines = lines[:-1] #seems like we dont want the last 4 lines

                for i, line in enumerate(lines):
                    line = line.split(' ')
                    lines[i] = {
                        'label': line[0],
                        'value': float(line[1])
                    }

                lines.insert(
                    0, {'label': 'filename', 'value': file.name.split('/')[-1]})
                extracted_data.append(lines)

    return extracted_data


def write_to_excel(data, output_file):
    workbook = Workbook()
    sheet = workbook.active
    for row_idx, row in enumerate(data):
        for col_idx, value in enumerate(row):
            sheet.cell(row=row_idx + 1, column=col_idx +
                       1, value=value['value'])
    workbook.save(output_file)
    print(f"\n\n\nData written to '{output_file}' successfully.")


# Main script
pdf_file_path = './assets/data/'
output_excel_file = './assets/data/data.xlsx'

extracted_data = extract_text_from_pdf(pdf_file_path)
write_to_excel(extracted_data, output_excel_file)
