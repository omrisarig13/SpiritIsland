import argparse
from Results import parser

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-a', '--add-row', action='store_true')
    return parser.parse_args()

def main():
    args = parse_args()

    c = parser.CSV('results.csv')
    if args.add_row:
        c.add_row_interactive()

    c.print_table()
    c.write()

if '__main__' == __name__:
        main()

