from infra.FlagDAO import CountryCodeDAO, CountryNameDAO
from domain.CountryCode import CountryCode
from domain.Constants import LANGUAGE
import json


class FlagRepository:
	languages = set([LANGUAGE.FRENCH, LANGUAGE.ENGLISH])

	def __init__(self) -> None:
		self.data: dict[str, CountryCode] = {}
		country_codes = self._get_all_country_code_by_code()
		nb_country = len(country_codes.keys())
		names = {language: self._get_all_names_by_code(language) for language in self.languages}
		for code, countryDAO in country_codes.items():
			self.data[code] = CountryCode(code, countryDAO.subCountry, countryDAO.emoji, countryDAO.subCountryOf, countryDAO.distinctFlag)
		for language, names_by_code in names.items():
			if len(names_by_code.keys()) != nb_country: raise Exception(f"Error in the file with names in '{language}', there is {len(names_by_code.keys())} codes instead of the {nb_country} expected")
			for code, countryNameDAO in names_by_code.items():
				if not code in self.data: raise Exception(f"Error in the file with names in '{language}', {code} is unknown")
				self.data[code].add_names(language, countryNameDAO.name, countryNameDAO.alt)

	def _get_country_code_url(self):
		return "./infra/json_db/codes.json"

	def _get_names_url(self, language: str):
		return f"./infra/json_db/names_{language}.json"

	def _get_all_country_code_by_code(self) -> dict[str, CountryCodeDAO]:
		with open(self._get_country_code_url(), 'r', encoding='utf-8') as file:
			data: dict[str, dict] = json.load(file)
		
		return {key: CountryCodeDAO(key, v) for key, v in data.items()}

	def _get_all_names_by_code(self, language: str) -> dict[str, CountryNameDAO]:
		if not language in self.languages:
			raise Exception("This language is not supported")

		with open(self._get_names_url(language), 'r', encoding='utf-8') as file:
			names: dict[str, dict] = json.load(file)
	
		return {key: CountryNameDAO(key, v) for key, v in names.items()}

	def _exist(self, country_code: str) -> bool:
		return country_code in self.data

	def _valid_country_code(self, country_code) -> None:
		if not self._exist(country_code):
			raise Exception(f"This country code is not valid: {country_code}")

	def get_emoji(self, country_code: str) -> str:
		self._valid_country_code(country_code)
		return self.data[country_code].emoji
	
	def get_all_names(self, country_code: str, language: str) -> set[str]:
		self._valid_country_code(country_code)
		return self.data[country_code].names[language]
	
	def get_all_countries(self, include_subCountry=True) -> list[CountryCode]:
		return [c for c in self.data.values() if include_subCountry or not c.subCountry]
	

