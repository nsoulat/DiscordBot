class CountryCodeDAO:
	code: str
	subCountry: bool
	emoji: str

	# Optional
	subCountryOf: str | None
	distinctFlag: bool | None

	def __init__(self, code: str, subCountry: bool, emoji: str, subCountryOf: str = None, distinctFlag: bool = None) -> None:
		self.code = code
		self.subCountry = subCountry
		self.emoji = emoji
		self.subCountryOf = subCountryOf
		self.distinctFlag = distinctFlag


class CountryNameDAO:
	code: str
	name: str
	alt: list[str]

	def __init__(self, code: str, name: str, alt: list[str]) -> None:
		self.code = code
		self.name = name
		self.alt = alt