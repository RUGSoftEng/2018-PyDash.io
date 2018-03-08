"""
    This script converts your Google Sheet Document to a MarkDown file.
    Commit this markdown file to git

    Start by downloading your data from the Timetracking Google Sheet:
    - File -> Download as -> Comma-separated values (.csv, current sheet)

    Then run this script in your terminal with the following arguments:
    - 1. the file that you've downloaded (tip, rename to file.csv)
    - 2. You student number
    - 3. Your name (use quotes)

    Example: python ./timetracking.py file.csv s123456 "name name"
"""

import sys
import csv
import os


def read_data(input_file):
    """
    Reads the data from the file, and returns this.
    :return: list of dictionaries with the data.
    """
    result = []
    with open(input_file) as csvfile:
        data = csv.DictReader(csvfile, delimiter=',')
        for row in data:
            result.append(row)
    return result


def remove_file(filename):
    """
    Removes a file if it exists
    """
    try:
        os.remove(filename)
    except Exception as e:
        print('Can\'t delete file: {}'.format(e))


def write_to_file(filename, data):
    """ write the data to a file """
    remove_file(filename)
    with open(filename, 'w+') as file:
        for line in data:
            file.write(line + '\n')


if __name__ == '__main__':
    if len(sys.argv) != 4:
        print('Usage: python {} input_file s-number name'.format(sys.argv[0]))
        sys.exit()

    _, input_file, s_number, name = sys.argv
    output_file = '{}-{}.md'.format(s_number, name)

    output = ['# Timelog for {} ({})'.format(name, s_number), '']
    output.append('| Date         |   Timestamp | Description                                                       |')
    output.append('| :---:        |       :---: | :---:                                                             |')

    for line in read_data(input_file):
        if line['Task']:
            output.append('| *{}* | {}-{} | {} |'.format(line['Date'], line['Start'], line['End'], line['Task']))

    write_to_file(output_file, output)
