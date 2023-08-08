"""A CSV parser file."""

import csv


class CSV:
    def __init__(self, file_path: str) -> None:
        self._file_path = file_path
        with open(self._file_path, 'r') as file:
            csv_reader = csv.reader(file)
            self._header = next(csv_reader)
            self._data = list(csv_reader)
        self._number_of_columns = len(self._header)

    def _column_max_number_of_characters(self, column_index: int) -> int:
        """Returns the maximum number of characters in a column.

        :param column_index: The index of the column.
        :return: The maximum number of characters in the column.
        """
        column = [self._header[column_index]]
        for row in self._data:
            column.append(row[column_index])
        return max([len(x) for x in column])

    @staticmethod
    def _print_table_separator(column_lengths: list, header: bool = False) -> None:
        """Prints a separator line, when printing the CSV as a table.

        :param column_lengths: The column lengths.
        :param header: Whether or not the current separator is a header.
        """
        separator_char = '|' if not header else '+'
        separator = separator_char + \
            separator_char.join(
                ['-' * length for length in column_lengths]) + separator_char
        print(separator)

    @staticmethod
    def _print_table_line(row: list, column_lengths: list) -> None:
        """Prints a line, when printing the CSV as a table.

        :param row: The row.
        :param column_lengths: The column lengths.
        """
        print('|' + '|'.join([str(x).ljust(length)
              for x, length in zip(row, column_lengths)]) + '|')

    def print_table(self, sort_key: str | None = None, descending: bool = False, secondary_sort_key: str | None = None) -> None:
        """Print the csv data, as a table.

        :param sort_key: The column to sort by.
        :param descending: Whether or not to sort in descending order.
        :param secondary_sort_key: The secondary sort key. This is used when the
            sort key is equal.
        """
        column_lengths = [self._column_max_number_of_characters(
            column_index) for column_index in range(self._number_of_columns)]

        def get_sort_key(row: list) -> str:
            if sort_key is None:
                return row[0]
            if secondary_sort_key is None:
                return row[self._header.index(sort_key)]
            return row[self._header.index(sort_key)] + '\0' + row[self._header.index(secondary_sort_key)]

        sorted_table = self._data
        if sort_key is not None:
            sorted_table = sorted(
                self._data, key=get_sort_key, reverse=descending)

        self._print_table_separator(column_lengths, True)
        self._print_table_line(self._header, column_lengths)
        self._print_table_separator(column_lengths)
        for row in sorted_table:
            self._print_table_line(row, column_lengths)
        self._print_table_separator(column_lengths, True)

    def write(self, file_path: str | None = None) -> None:
        """Writes the csv data to a file.

        :param file_path: The path to the file. When omitted, the data is
            written to the original file.
        """
        if file_path is None:
            file_path = self._file_path

        with open(file_path, 'w') as file:
            csv_writer = csv.writer(file)
            csv_writer.writerow(self._header)
            csv_writer.writerows(self._data)

    def add_row(self, row: list) -> None:
        """Adds a row to the csv data.

        :param row: The row.
        """
        self._data.append(row)

    def add_row_interactive(self) -> None:
        """Adds a row to the csv data, interactively."""
        self._data.append([input(x + ": ") for x in self._header])
