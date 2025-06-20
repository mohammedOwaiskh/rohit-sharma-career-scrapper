import requests
from bs4 import BeautifulSoup

__BASE_URL = "https://stats.espncricinfo.com"

__URL = (
    __BASE_URL
    + "/ci/engine/player/34102.html?class={};template=results;type=batting;view=innings"
)

__FORMATS = {
    1,  # Test
    2,  # ODI
    3,  # T20I
    6,  # IPL
}

__HEADER = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
}


def make_request(format_id: int):
    """
    Sends a GET request to the ESPN Crickinfo API for the provided format_id.
    Args:
        format_id (int): The format identifier to be inserted into the URL.
    Returns:
        BeautifulSoup: The Beautiful object resulting from the GET request.
    Raises:

    """
    url = __URL.format(format_id)
    page = requests.get(url, headers=__HEADER)
    if page.status_code != 200:
        raise Exception(f"Page not accessible. Error: {page.status_code}")
    return BeautifulSoup(page.text, "html.parser")


def fetch_text(tags: list):
    """
    Extracts and returns the non-empty, stripped text content from a list of tag-like objects.
    Args:
        tags (list): A list of objects (e.g., BeautifulSoup Tag objects) that have a 'text' attribute.
    Returns:
        list: A list of non-empty, whitespace-stripped strings extracted from the 'text' attribute of each tag.
    """

    return [tag.text.strip() for tag in tags if tag.text.strip() != ""]


def get_table():
    """
    Fetches and parses match data tables for different cricket formats.
    Iterates over predefined format identifiers, sends HTTP requests to retrieve
    HTML pages, and extracts the relevant match statistics table from each page.
    The function collects column headers (only once, from the first format) and
    appends an additional "Format" column. For each row in the table, it extracts
    the cell values and aggregates them into a data list.
    Returns:
        tuple: A tuple containing:
            - columns (list of str): The column headers for the table, including "Format".
            - data (list of list of str): The extracted data rows for all formats.
    """
    columns = []
    data = []

    for format_id in __FORMATS:

        soup = make_request(format_id)

        scores_table = soup.find_all("table", class_="engineTable")[3]

        # do not add data in columns list if it is already populated
        if len(columns) == 0:
            table_headers = scores_table.find_all("th")
            columns = fetch_text(table_headers)
            columns.append("Match_Url")

        rows = scores_table.find_all("tr", class_="data1")
        for row in rows:
            data_row = row.find_all("td")
            data.append(fetch_text(data_row))

    return columns, data
