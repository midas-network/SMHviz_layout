from dash import html


def make_notes_definition(definitions, notes_left, notes_right,
                          css_title="title", css_column_left="column left",
                          css_column_right="column right",
                          css_column_notes_left="column_notes left_notes",
                          css_column_notes_right="column_notes right_notes", css_row="row",
                          css_row_bottom_notes="row bottom_notes", id_name="Notes"):
    """Create the Notes and Definitions on the SMH visualization websites

    Make the code for the Notes, Definitions and scenario table below the plot
    on the SMH visualization website.  The notes content is in the function.

    The output contains multiple CSS class information that need to be available:
        - `title`: style information for the "Notes" and "Definitions" title style
        - `column left` and `column right`: style information for the "Definitions" Div component
            (left) and for the Div component id `html-table` (right)
        - `column_notes left_notes` and `column_notes right_notes`: style information for the
            "Notes" Div component, left and right column respectively
        - `row`: style information for the Div component containing both the "Definitions" and HTML
            table
        - `row bottom_notes`: style information for the Div component containing the "Notes" section
    An example CSS files containing all the information is available in the documentation of the
    package.

    :parameter definitions: A Div component containing the content of the "Definitions" section
    :parameter notes_left:  A Div component containing the content of the "Notes" section
    :parameter notes_right:  A Div component containing the content of the "Notes" section
    :parameter css_title: string, name of the associated CSS element, see documentation
    :parameter css_column_left: string, name of the associated CSS element, see documentation
    :parameter css_column_right: string, name of the associated CSS element, see documentation
    :parameter css_column_notes_left: string, name of the associated CSS element, see documentation
    :parameter css_column_notes_right: string, name of the associated CSS element, see documentation
    :parameter css_row: string, name of the associated CSS element, see documentation
    :parameter css_row_bottom_notes: string, name of the associated CSS element, see documentation
    :parameter id_name: string, name of the element if containing the "Notes:, by default "Notes"
    :return: A Div component containing the content the definition, HTML table (id: html-table) and
        notes content and layout code associated with the hub
    """
    notes = html.Div([
        html.Div([
            html.Div([
                html.H2("Definitions", className=css_title),
                definitions
            ], className=css_column_left),
            html.Div(className=css_column_right, id="html-table")
        ], className=css_row),
        html.Div([
            html.H2("Notes", className=css_title, id=id_name),
            html.Div(notes_left, className=css_column_notes_left),
            html.Div(notes_right, className=css_column_notes_right)
        ], className=css_row_bottom_notes)
    ])
    return notes
