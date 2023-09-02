class NameDict:
    def __init__(self, main, all) -> None:
        self.main: str = main
        self.all_names: set[str] = set(all)


class CountryCode:
    def __init__(
        self,
        code: str,
        subCountry: bool,
        emoji: str,
        continent: str,
        subCountryOf: str | None = None,
        distinctFlag: bool | None = None,
    ) -> None:
        self.code: str = code
        self.subCountry: bool = subCountry
        self.emoji: str | None = emoji
        self.continent: str | None = continent
        self.subCountryOf: str | None = subCountryOf
        self.distinctFlag: bool | None = distinctFlag
        self.names: dict[str, NameDict] = {}

    def add_names(self, language: str, main_name: str, alt_names: list[str]):
        if language in self.names:
            # we could raise an error instead as it shouldn't happen
            print(
                (
                    f"Warning: Names already set for this language."
                    f" {self.code} has already names in {language}.\n"
                    f" Previous: {self.names[language].all_names}.\n"
                    f"To add: {alt_names}"
                )
            )
            self.names[language].all_names.update(alt_names)
        else:
            self.names[language] = NameDict(main_name, [main_name] + alt_names)
