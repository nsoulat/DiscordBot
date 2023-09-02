class LANGUAGE:
    FRENCH = "fr"
    ENGLISH = "en"

    def trad(language: str) -> str:
        if language == LANGUAGE.FRENCH:
            return "French"
        if language == LANGUAGE.ENGLISH:
            return "English"
        else:
            raise Exception(f"Unknown language: {language}")


class CONTINENT:
    AFRICA = "AF"
    ASIA = "AS"
    EUROPE = "EU"
    NORTH_AMERICA = "NA"
    SOUTH_AMERICA = "SA"
    OCEANIA = "OC"
    ANTARTICA = "AN"


class DIFFICULTY:
    EASY = "easy"
    HARD = "hard"
    US = "us"
    EUROPE = "eu"
