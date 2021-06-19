from people.models import Individual
from dateutil import parser, tz
from datetime import tzinfo
import pytz


def get_timestamp(timestring, tzname="America/Denver"):
    #zone = tz.tzoffset("MDT", -21600)
    stamp = parser.parse(timestring)
    return stamp

def get_individual_by_maker(maker_string):
    names = maker_string.split(",")
    try:
        last_name, *middle_names, first_name = tuple(map(str.strip, names))
    except ValueError:
        first_name = maker_string.strip()
        middle_names = []
        last_name = ""

    middle_name = " ".join(middle_names)

    params = {
        "first_name": first_name,
        "last_name": last_name,
    }

    if middle_name:
        params["middle_name"] = middle_name

    return (
        Individual
        .objects
        .get_or_create(
            **params
        )
    )

def get_pac(pac_string):
    _, pac, *subpac = pac_string.split(".")
    return {
        "pac": int(pac),
        "subpac": int(subpac[0]) if subpac else 0
    }


common_misspellings = {
    'accwepted': 'accepted',
    "acepted": "accepted",
    "proejct": "project",
    "puchased": "purchased",
}


def normalize_event_type(event_type_string):
    tokens = tuple(map(str.strip, event_type_string.split()))
    normalized = []
    for token in tokens:
        # Correct for spelling
        corrected = common_misspellings.get(token.lower(), token.lower())

        # Capitalize each token
        corrected = corrected[0].upper() + corrected[1:]
        normalized.append(corrected)

    return " ".join(normalized)
