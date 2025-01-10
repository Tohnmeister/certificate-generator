import argparse
import datetime

from PyPDF2 import PdfReader, PdfWriter
from PyPDF2.generic import NameObject, TextStringObject


def main():
    parser = argparse.ArgumentParser(
        prog='PDF Certificate Generator',
        description='Helps filling in dynamic input fields in a PDF course certificate')

    parser.add_argument('-i', '--input', required=True, help='Input PDF')
    parser.add_argument('-o', '--output', required=True, help='Output PDF')
    parser.add_argument('-n', '--name', required=True, help='Participant name')
    parser.add_argument('-c', '--course', required=True, help='Course name')
    parser.add_argument('-d', '--date', required=True, help='Date')

    args = parser.parse_args()

    # generate_using_py_pdf2(args)
    generate_using_pymupdf(args)

    print('Done')


def generate_using_py_pdf2(args):
    reader = PdfReader(args.input)
    page = reader.pages[0]
    all_objects = (annot.get_object() for annot in page['/Annots'])
    input_objects = [obj for obj in all_objects if obj.get('/Subtype') == '/Widget' and obj.get('/T')]
    field_object_mapping = {obj.get('/T'): obj for obj in input_objects}
    # This is very specific to my PDF.
    update_field_using_py_pdf2(field_object_mapping, 'Text3', args.name)
    update_field_using_py_pdf2(field_object_mapping, 'Text4', args.course)
    update_field_using_py_pdf2(field_object_mapping, 'Datum11_af_date', args.date)
    writer = PdfWriter()
    writer.add_page(page)
    # Write to output PDF
    with open(args.output, 'wb') as output_file:
        writer.write(output_file)


def generate_using_pymupdf(args):
    import fitz

    input_pdf = fitz.open(args.input)

    page = input_pdf[0]

    for field in page.widgets():
        if field.field_name == 'Text3':
            field.field_value = args.name
            field.update()
        elif field.field_name == 'Text4':
            field.field_value = args.course
            field.update()
        elif field.field_name == 'Datum11_af_date':
            field.field_value = args.date
            field.update()



    input_pdf.save(args.output)


def update_field_using_py_pdf2(field_object_mapping, field_name, value):
    field_object_mapping[field_name].update({
        NameObject("/V"): TextStringObject(value)
    })


if __name__ == "__main__":
    main()
