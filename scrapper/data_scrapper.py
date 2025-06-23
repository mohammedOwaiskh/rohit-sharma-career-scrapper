import dis
import logging
from typing import Literal
import requests
import pandas as pd
from bs4 import BeautifulSoup

log = logging.getLogger(__name__)

__BASE_URL = "https://stats.espncricinfo.com"

__URL = (
    __BASE_URL
    + "/ci/engine/player/34102.html?template=results;class={format_id};type={type};view={view_by}"
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


def make_request(
    format_id: int,
    type: Literal["batting", "allround"],
    view_by: Literal["innings", "results", "awards_match", "dismissal_list"],
):
    """
    Sends an HTTP GET request to the ESPN Cricinfo URL and returns a BeautifulSoup object of the page content.
    Args:
        format_id (int): The format identifier to be used in the URL.
        type (Literal["batting", "allround"]): The type of data to request, either "batting" or "allround".
        view_by (Literal["innings", "results", "awards_match"]): The view mode for the data.
    Returns:
        BeautifulSoup: Parsed HTML content of the requested page.
    Raises:
        requests.exceptions.HTTPError: If the HTTP request fails with a status code other than 200.
    """
    url = __URL.format(format_id=format_id, type=type, view_by=view_by)
    page = requests.get(url, headers=__HEADER)
    if page.status_code != 200:
        raise requests.exceptions.HTTPError(
            f"Page not accessible. Error: {page.status_code}"
        )
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


def get_scores_table() -> pd.DataFrame:
    """
    Scrapes and compiles Rohit Sharma's career scores data from multiple cricket formats into a pandas DataFrame.
    Iterates over a list of format identifiers, sends HTTP requests to fetch the relevant HTML pages, and parses the
    scores table for each format. Extracts column headers and row data, including the match URL for each entry.
    Returns a DataFrame containing the consolidated scores data with appropriate columns.
    Returns:
        pd.DataFrame: A DataFrame containing the scores data for all formats, with columns for each statistic and the match URL.
    """
    log.debug("Scrapping scores table...")
    columns = []
    data = []

    for format_id in __FORMATS:

        soup = make_request(format_id, "batting", "innings")

        scores_table = soup.find_all("table", class_="engineTable")[3]

        # do not add data in columns list if it is already populated
        if len(columns) == 0:
            table_headers = scores_table.find_all("th")
            columns = fetch_text(table_headers)
            columns.append("format")
            columns.append("match_id")

        rows = scores_table.find_all("tr", class_="data1")
        for row in rows:
            row_data = row.find_all("td")
            trimmed_rd = fetch_text(row_data)

            match_url = row_data[-1].find("a").get("href").strip()
            match_id = match_url.split("/")[-1].split(".")[0]
            trimmed_rd.append(match_id)

            data.append(trimmed_rd)

    log.debug("Scrapped Scores table")

    scores_df = pd.DataFrame(data, columns=columns)
    return scores_df


def get_match_awards_table() -> pd.DataFrame:
    """
    Fetches and returns a DataFrame containing match awards won by Rohit Sharma across different formats.
    Returns:
        pd.DataFrame: A DataFrame with columns ['award', 'date', 'match_id'] where each row contains
        the award name, date of the match, and the match ID for each award received across all formats.
    Notes:
        - Uses the make_request and fetch_text helper functions to retrieve and process HTML data.
    """
    log.debug("Scrapping awards table")

    columns = ["award", "date", "match_id"]
    data = []

    for format_id in __FORMATS:

        soup = make_request(format_id, "allround", "awards_match")

        awards_table = soup.find_all("table", class_="engineTable")[3]

        rows = awards_table.find_all("tr", class_="data1")
        for row in rows:
            row_data = row.find_all("td")
            trimmed_rd = fetch_text(row_data)

            match_url = row_data[-1].find("a").get("href").strip()
            match_id = match_url.split("/")[-1].split(".")[0]
            trimmed_rd[-1] = match_id

            data.append([trimmed_rd[0], trimmed_rd[-2], trimmed_rd[-1]])

    log.debug("Scrapped Awards table")

    match_awards_df = pd.DataFrame(data, columns=columns)
    return match_awards_df


def get_match_results_table() -> pd.DataFrame:
    """
    Scrapes and returns a DataFrame containing results of matches played by Rohit Sharma across different cricket formats.
    Iterates over predefined cricket formats, sends HTTP requests to fetch match result tables,
    parses the HTML to extract relevant data (result, date, and match ID) for each match,
    and compiles the information into a pandas DataFrame.
    Returns:
        pd.DataFrame: A DataFrame with columns ['result', 'date', 'match_id'] containing
                      the match result, date, and unique match identifier for each match.
    """
    log.debug("Scrapping Results table")

    columns = ["result", "date", "match_id"]
    data = []

    for format_id in __FORMATS:

        soup = make_request(format_id, "allround", "results")

        scores_table = soup.find_all("table", class_="engineTable")[3]

        rows = scores_table.find_all("tr", class_="data1")
        for row in rows:
            row_data = row.find_all("td")
            trimmed_rd = fetch_text(row_data)

            match_url = row_data[-1].find("a").get("href").strip()
            match_id = match_url.split("/")[-1].split(".")[0]
            trimmed_rd[-1] = match_id

            data.append([trimmed_rd[0], trimmed_rd[-2], trimmed_rd[-1]])

    log.debug("Scrapped Results table")

    scores_df = pd.DataFrame(data, columns=columns)
    return scores_df


def get_dismissal_list() -> pd.DataFrame:
    """
    Scrapes and returns a DataFrame containing dismissal information for Rohit Sharma across different cricket formats.
    The function iterates over predefined cricket formats, scrapes the dismissal list table for each format,
    and extracts relevant details such as dismissal type, bowler, inning, and match ID. The data is compiled
    into a pandas DataFrame with columns: 'dismissal_type', 'bowler', 'inning', and 'match_id'.
    Returns:
        pd.DataFrame: A DataFrame containing dismissal details for each match and format.
    """

    log.debug("Scrapping Dissmisal List table")

    columns = ["dismissal_type", "bowler", "inning", "match_id"]
    data = []

    for format_id in __FORMATS:

        soup = make_request(format_id, "batting", "dismissal_list")

        scores_table = soup.find_all("table", class_="engineTable")[3]

        rows = scores_table.find_all("tr", class_="data1")
        for row in rows:
            row_data = row.find_all("td")
            trimmed_rd = fetch_text(row_data)

            match_url = row_data[-1].find("a").get("href").strip()
            match_id = match_url.split("/")[-1].split(".")[0]
            trimmed_rd[-1] = match_id

            dismissal_type = trimmed_rd[0]
            if dismissal_type in ("not out", "TDNB", "DNB", "retired notout"):
                data.append([dismissal_type, "", trimmed_rd[-5], trimmed_rd[-1]])
            elif dismissal_type in ("stumped", "caught"):
                data.append(
                    [dismissal_type, trimmed_rd[2], trimmed_rd[-5], trimmed_rd[-1]]
                )
            else:
                if len(trimmed_rd) == 7:
                    data.append([dismissal_type, "", trimmed_rd[-5], trimmed_rd[-1]])
                else:
                    data.append(
                        [dismissal_type, trimmed_rd[1], trimmed_rd[-5], trimmed_rd[-1]]
                    )
    log.debug("Scrapped Dismissal table")

    scores_df = pd.DataFrame(data, columns=columns)
    return scores_df
