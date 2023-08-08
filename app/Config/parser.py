import yaml


class Config:
    def __init__(self, file_path: str = 'Config/spirit_island.yaml') -> None:
        with open(file_path, 'r') as file:
            self._config = yaml.safe_load(file)

    def _get_values(self, key: str, expansions: list | None = None) -> list:
        """Return the list of values for the wanted key, according to the
        available expansions.

        :param key: The key to get the values for.
        :param expansions: The expansions to include when looking for values.
        :return: The list of values.
        """
        if expansions is None:
            expansions = self._config[key].keys()

        spirits = []
        for expansion in self._config[key].keys():
            if expansion in expansions or expansion == "Base Game":
                if self._config[key][expansion]:
                    for value in self._config[key][expansion]:
                        if isinstance(value, dict):
                            spirits += value.keys()
                        else:
                            spirits += [value]
        return spirits

    def get_spirits(self, expansions: list | None = None) -> list:
        """Get the available spirits.

        :expansions: The expansions to include when looking for spirits.
        :return: The available spirits.
        """
        return self._get_values('Spirits', expansions)

    def get_adversaries(self, expansions: list | None = None) -> list:
        """Get the available adversaries.

        :expansions: The expansions to include when looking for adversaries.
        :return: The available adversaries.
        """
        return self._get_values('Adversaries', expansions)

    def get_scenarios(self, expansions: list | None = None) -> list:
        """Get the available scenarios.

        :expansions: The expansions to include when looking for scenarios.
        :return: The available scenarios.
        """
        return self._get_values('Scenarios', expansions)


config = Config()
