import argparse
import datetime

from PyPDF2 import PdfReader, PdfWriter

def main():
    parser = argparse.ArgumentParser(
        prog='PDF Certificate Generator',
        description='Helps filling in dynamic input fields in a PDF course certificate')

    parser.add_argument('-i', '--input', required=True, help='Input PDF')
    parser.add_argument('-o', '--output', required=True, help='Output PDF')
    parser.add_argument('-n', '--name', required=True, help='Participant name')
    parser.add_argument('-c', '--course', required=True, help='Course name')
    parser.add_argument('-d', '--date', type=datetime.date.fromisoformat, required=True, help='Date in dd/mm/yyyy')

    args = parser.parse_args()
    print(args.input, args.output, args.name, args.course, args.date)


if __name__ == "__main__":
    main()
