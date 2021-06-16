from people.models import Artist


def get_artist_by_maker(maker_string):
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
        Artist
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
