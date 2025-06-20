import os
import re

import pandas as pd
from dash import dash_table, html, dcc


def make_dt_metadata(metadata_file):
    """Create the Data Table output

    Output the table in a  DataTable format with the information for the metadata information

    :parameter metadata_file: Path to the CSV file containing the metadata information
    :type metadata_file: str
    :return: the DataTable information
    """
    df = pd.read_csv(metadata_file)
    output = dash_table.DataTable(df.to_dict('records'), [{"name": i, "id": i} for i in df.columns],
                                  style_data={
                                      'whiteSpace': 'normal',
                                      'height': 'auto'
                                  },
                                  style_cell={'textAlign': 'center', 'padding': '7px'},
                                  style_cell_conditional=[{
                                      'if': {'column_id': 'Description'},
                                      'textAlign': 'left'}
                                  ])
    return output


def make_abstract_tab(round_number, path="./visualization/data-visualization/model_abstracts/",
                      id_append="", pattern="\d{4}-\d{2}-\d{2}-|-(A|a)bstract.md"):
    """Create the abstract page

    Create the SMH round specific layout page for the abstract, with a dropdown containing the name
     of all available abstract for the round.

    :parameter round_number: Numeric identifier of a specific round tab (for example "13")
    :type round_number: str
    :parameter path: Relative path to the folder containing the abstracts information for all round
    :type path: str
    :parameter id_append: Character to append to the objects IDs.
    :type id_append: str
    :parameter pattern: pattern to extract team-model name from the file, by default
        `"\d{4}-\d{2}-\d{2}-|-(A|a)bstract.md"`
    :type pattern: str
    :return: Div component associated with the round, tab selected and associated abstract
    """
    file_list = os.listdir(path + "round" + str(round_number))
    checkbox_list = list()
    for i in file_list:
        checkbox_entry = re.sub(pattern, "", i)
        checkbox_list.append(checkbox_entry)
    checkbox_list.sort()
    output = html.Div([
        dcc.Dropdown(
            id='abstract' + id_append + '-dropdown', clearable=False,
            options=checkbox_list, value=checkbox_list[0]),
        html.Br(),
        html.Div(id="abstract" + id_append + "-output")
    ])
    return output


def render_abstract(round_number, round_date, team_model_name,
                    path="./visualization/data-visualization/model_abstracts/",
                    file_append=["-abstract", "-Abstract"], file_extension=".md"):
    """Create the abstract content

    Return the content of a specific abstract.
    The function assumed that the abstract filepath and filename followed the SMH standard:
    `"PATH/TO/roundX/YYY-MM-DD-team_model-(A|a)bstract.md"` with:
        - "PATH/TO/": path to a folder storing the abstract by round
        - "roundX": round information with X a number associated with a specific round
        - "YYYY-MM-DD": date information associated with the specific round X
        - "team-model": standard name of the team and model associated with the abstract
            (same code name as in the submission files)

    :parameter round_number: Numeric identifier of a specific round tab (for example "13")
    :type round_number: str
    :parameter round_date: Date identifier of a specific round tab in a YYYY-MM-DD format
        (for example "2022-03-13")
    :type round_date: str
    :parameter team_model_name: Name of a team_model (same as in the filename) specifying which
        abstract content to read
    :type team_model_name: str
    :parameter path: Relative path to the folder containing the abstracts information for all round
    :type path: str
    :parameter file_append: List of possible additional text in the filename, if None (default), no
        additional text
    :type file_append: list | None
    :parameter file_extension: Character string, extension of the file, ".md" by default
    :type file_extension: str
    :return: Div component associated with a specific abstract
    """
    if file_append is None:
        filename = (path + "round" + str(round_number) + "/" + round_date + "-" + team_model_name +
                    file_extension)
    else:
        for i in file_append:
            filename = (path + "round" + str(round_number) + "/" + round_date + "-" +
                        team_model_name + i + file_extension)
            if os.path.isfile(filename):
                break
    with open(filename, "r") as f:
        markdown_text = f.read()
    return html.Div([
        dcc.Markdown(markdown_text)
    ])
