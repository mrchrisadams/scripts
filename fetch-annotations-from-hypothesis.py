

import datetime
import json
import os

# import the somewhat official python library for working with hypthesis
# https://github.com/judell/Hypothesis
import hypothesis


# fetch latest annotations from hypothesis using the hypothesis api
# https://h.readthedocs.io/en/latest/api/
# https://h.readthedocs.io/en/latest/api-reference/#tag/annotations
# https://h.readthedocs.io/en/latest/api-reference/#operation/fetch_annotation
# https://h.readthedocs.io/en/latest/api-reference/#operation/fetch_annotations

TOKEN = os.getenv('HYPOTHESIS_TOKEN')
USER = os.getenv('HYPOTHESIS_USER')

# your h username and api token (from https://hypothes.is/account/developer)
hc = hypothesis.Hypothesis(username=USER, token=TOKEN)  

default_params = {
    'user':USER,
    'limit':100, 
    'order': "desc"
}

# fetch my 200 latest annotations
has_next = True
first_date = None
last_date = None

def get_next_page(
        default_params=default_params, 
        first_date=first_date, 
        last_date=last_date, 
        has_next=has_next
    ) -> dict:
    """
    Fetch the next page of annotations from the API, returning a dict containing
    the rows, and the first and last dates of the annotations.
    """
    params = default_params.copy()
    # we use the search_after as it's recommended for pagination in the API
    if last_date:
        params.update({'search_after':last_date})

    data = hc.search(params=params)
    rows = data.get('rows', [])
    if rows:
        first_date = rows[-1].get('created')
        last_date = rows[-1].get('created')
    else:
        has_next = False

    return {
        "rows": rows,
        "has_next": has_next,
        "first_date": first_date,
        "last_date": last_date,
    } 

def _formatted_date(date_string) -> str:
    """
    Convert the date string from the API to a format that can be used in a filename.
    """
    date_obj = datetime.datetime.fromisoformat(last_date)
    formatted_date = date_obj.strftime("%Y-%m-%d--%H-%M")
    return formatted_date

def write_to_file(rows, last_date=None, first_date=None) -> None:
    """
    Write the annotations to a file in the ./hypothesis-data directory,
    with a filename that includes the date range of the annotations.
    """
    assert last_date and first_date
    from_date = _formatted_date(first_date)
    until_date = _formatted_date(last_date)

    filename = f'annotations-from-{from_date}-to-{until_date}.json'
    with open(f"./hypothesis-data/{filename}", 'a') as f:
        f.write(json.dumps(rows, indent=4))

while has_next is True:
    data = get_next_page(
        default_params=default_params, 
        first_date=first_date, 
        last_date=last_date, 
        has_next=has_next
    )
    has_next = data.get('has_next') 
    first_date = data.get('first_date')
    last_date = data.get('last_date')
    write_to_file(data.get('rows'), last_date=last_date, first_date=first_date)
    



