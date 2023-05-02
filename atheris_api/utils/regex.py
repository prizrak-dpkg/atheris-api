# Python imports
from enum import Enum
import re


class RegexEnum(Enum):
    CELL_PHONE_NUMBER = {
        "regex": r"^(3)[\d]{9}$",
        "msg": "El campo * debe tener 10 dígitos y cumplir con el formato: 3xxxxxxxxx.",
    }
    DOCUMENT_NUMBER = {
        "regex": r"^(?!0)[\d]{6,10}$",
        "msg": "El campo * debe tener entre 6 y 10 dígitos.",
    }
    ADDRESS = {
        "regex": r"^[\da-záéíóúñ #.-]{5,}$",
        "msg": "El campo * sólo admite letras, números, ., #, - y debe tener 5 o más caracteres.",
    }
    EMAIL = {
        "regex": r"^[a-z0-9]{1}[a-z0-9._-]{3,}@[a-z0-9_-]{2,}(\.{1}[a-z0-9_-]{2,})+$",
        "msg": "El campo * debe cumplir con el formato: user@example.info.",
    }
    WORD = {
        "regex": r"^[a-záéíóúñ ]{2,}$",
        "msg": "El campo * sólo admite letras, espacios y debe tener 2 o más caracteres.",
    }
    TEXT = {
        "regex": r"^[\wáéíóúñ'\-\",.;:¿?¡!(){} ]{2,}$",
        "msg": "El campo * sólo admite caracteres alfanumericos, espacios, signos de puntuación y debe tener 2 o más caracteres.",
    }


class RegexValidators:
    def __init__(
        self,
        regex: RegexEnum,
        value: str,
        optional: bool = False,
        flags: tuple[re.RegexFlag] = (re.IGNORECASE,),
    ):
        self.regex = regex.value.get("regex")
        self.value = value
        self.message = regex.value.get("msg")
        self.optional = optional
        self.flags = flags

    def getFormatText(self, value):
        whitespace_regex: re.Pattern[str] = re.compile(r"(\s)+")
        return re.sub(whitespace_regex, " ", value).strip()

    @property
    def validate(self):
        regex_test: re.Pattern[str] = re.compile(self.regex, *self.flags)
        value = self.getFormatText(self.value).title()
        if self.optional:
            return {
                "match": value == "" or regex_test.match(value) is not None,
                "value": value,
                "message": self.message,
            }
        return {
            "match": regex_test.match(value) is not None,
            "value": value,
            "message": self.message,
        }
