from infra.FlagRepository import FlagRepository
from domain.Constants import CONTINENT

import pytest


class Test_FlagRepository:
	_flagRepository = FlagRepository()

	@staticmethod
	def get_flagRepo():
		return Test_FlagRepository._flagRepository


def test_create_not_null():
	flagRep = Test_FlagRepository.get_flagRepo()
	assert not (flagRep.data is None or len(flagRep.data) == 0)

def test_France_is_correct():
	flagRep = Test_FlagRepository.get_flagRepo()
	assert "fr" in flagRep.data and flagRep.data["fr"].names["fr"].main == "France"

# see https://worldpopulationreview.com/country-rankings/list-of-countries-by-continent for more info
@pytest.mark.parametrize("continent,expected", [
	(CONTINENT.EUROPE, 47), # Kosovo is in the list and Russia, Cyprus, Turkey are European
	(CONTINENT.ASIA, 47), # Taiwan, Israel and Palestine are in the list and Armenia, Azerbaijan, Georgia, Kazakhstan are Asian
	(CONTINENT.AFRICA, 54), # Egypt is African
	(CONTINENT.SOUTH_AMERICA, 12),
	(CONTINENT.OCEANIA, 14),
	(CONTINENT.NORTH_AMERICA, 23) # including 13 in Carribbean and 8 in Central America
	])
def test_number_countries_by_continent(continent, expected):
	flagRep = Test_FlagRepository.get_flagRepo()
	countries = flagRep.get_all_country_codes(include_subCountry=False, continent=continent)
	assert len(countries) == expected

def test_check_all_countries_have_emoji():
	flagRep = Test_FlagRepository.get_flagRepo()
	countries = flagRep.get_all_country_codes(include_subCountry=False)
	for country in countries:
		assert (not country.emoji is None) and (not country.emoji == "")

@pytest.mark.parametrize("code", [("gb"),("us-mn"),("yt")])
def test_check_valid_country_code(code):
	flagRep = Test_FlagRepository.get_flagRepo()
	flagRep._valid_country_code(code) # this raises an error if code is not valid

@pytest.mark.parametrize("code", [("aa"),("20"),(""),(0)])
def test_check_unvalid_country_code(code):
	flagRep = Test_FlagRepository.get_flagRepo()
	with pytest.raises(Exception) as e_info:
		flagRep._valid_country_code(code)

def test_get_US_regions():
	flagRep = Test_FlagRepository.get_flagRepo()
	us_regions = flagRep.get_US_regions()
	assert len(us_regions) == 50 + 5 # 50 US states + 5 unincorporated territories