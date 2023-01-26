class CountryCodeDAO:
	def __init__(self, code: str, value: dict) -> None:
		self.code: str = code
		self.subCountry: bool = value.get("subCountry", False)
		self.emoji: str | None = value.get("emoji", None)
		self.subCountryOf: str | None = value.get("subCountryOf", None)
		self.distinctFlag: str | None = value.get("distinctFlag", None)
		self.continent: str | None = value["continent"]


class CountryNameDAO:
	def __init__(self, code: str, value: dict) -> None:
		self.code: str = code
		self.name: str = value["name"]
		self.alt: list[str] = value["alt"]