class ConfigError(ValueError):
    def __init__(self, variable_name: str) -> None:
        self._variable_name = variable_name

    def __str__(self) -> str:
        return f"Failed to parse {self._variable_name}. Have you specified it?"
