import readline
import os.path
import datetime

from Utils import csv_parser
from Config.parser import config


class CSV(csv_parser.CSV):
    _HEADER = ['Date', 'Points', 'Victory', 'Kristina\'s Spirit',
               'Omri\'s spirit', 'Adversary', 'Adv. Level', 'Scenario',
               'Difficulty', 'Time', 'Branch and Claw', 'Jagged Earth']

    def __init__(self, file_path: str) -> None:
        if not os.path.isfile(file_path):
            with open(file_path, 'w') as file:
                csv_writer = csv.writer(file)
                csv_writer.writerow(self._HEADER)
        super().__init__(file_path)

    def _get_completer_function(self, column: str) -> str:
        if column.startswith("Spirit #"):
            matchings = config.get_spirits() + ['None']
        else:
            match column:
                case 'Date':
                    matchings = [datetime.date.today().strftime('%y.%m.%d')]
                case 'Victory':
                    matchings = ['Yes', 'No']
                case 'Adversary':
                    matchings = config.get_adversaries() + ['None']
                case 'Scenario':
                    matchings = config.get_scenarios() + ['None']
                case 'Branch and Claw':
                    matchings = ['Yes', 'No']
                case 'Jagged Earth':
                    matchings = ['Yes', 'No']
                case other:
                    return None

        def complete(text, state):
            for current_match in matchings:
                if current_match.startswith(text):
                    if not state:
                        return current_match
                    else:
                        state -= 1
        return complete

    def add_row_interactive(self) -> None:
        """Adds a row to the csv data, interactively."""
        new_row = []

        readline.parse_and_bind("tab: complete")
        delims = readline.get_completer_delims()
        readline.set_completer_delims('')
        for column in self._header:
            readline.set_completer(self._get_completer_function(column))
            new_row.append(input(column + ": "))

        readline.set_completer_delims(delims)
        readline.set_completer(None)

        self._data.append(new_row)
