from dash import html, dcc


def make_checkbox(title, id_name, options, hide=False, style=None, value=None, check_style=None):
    """Create a Div component with a Checkbox

    Make a Div component with a Checkbox and a title. For more information, please consult
    `dcc.Checklist()` from `dash` library.

    :parameter title: Title of the Checkbox (text on top of the Checkbox)
    :type title: str
    :parameter id_name: Internal identifier of the Checkbox
    :type id_name: str
    :parameter options: Possible options of the Checkbox
    :type options: str | list | int | float | bool |dict
    :parameter hide: Boolean to hide or not the checkbox in the output
    :type hide: bool
    :parameter style: Style associated with the checkbox,
        if `None`: {"display": "inline-block", "margin-left": "5%", "width": "25%"}
    :type style: dict | str
    :parameter value: Possible value selected by default
    :type value: str | list | int | float | bool |dict
    :parameter check_style: Style associated with each element of the checkbox, by default None
    :type check_style: dict | str
    :return: Div component with a Checkbox component
    """
    if style is None:
        style = {"display": "inline-block", "margin-left": "5%", "width": "25%"}
    if value is not None:
        checkbox = html.Div([
            html.P(title),
            dcc.Checklist(id=id_name, options=options, value=value, style=check_style)
        ], style=style)
    else:
        checkbox = html.Div([
            html.P(title),
            dcc.Checklist(id=id_name, options=options, style=check_style)
        ], style=style)
    if hide is True:
        checkbox = html.Div(checkbox, hidden=True)
    return checkbox


def make_radio_items(title, id_name, options, value, css_class="plot_bar_sel", inline=True):
    """Create a Div component with a RadioItems

    Make a Div component with a RadioItems and a title. For more information, please consult
    `dcc.RadioItems()` from `dash` library.

    :parameter title: Title of the RadioItems (text on top of the RadioItems)
    :type title: str
    :parameter id_name: Internal identifier of the RadioItems
    :type id_name: str
    :parameter options: Possible options of the RadioItems
    :type options: str | list | int | float | bool |dict
    :parameter value: The current select options
    :type value: str | list | int | float | bool |dict
    :parameter css_class: string, name of the associated CSS element, see documentation
    :type css_class: str
    :parameter inline: Boolean to indicate if the RadioItems should be inline or not
    :type inline: bool
    :return: Div component with a radioItems component
    """
    radio_item = html.Div([
        html.P(title),
        dcc.RadioItems(inline=inline, id=id_name, options=options, value=value)
    ], className=css_class)
    return radio_item


def make_dropdown(title, id_name, options, value, clearable=False, css_class="plot_bar_sel"):
    """Create a Div component with a Dropdown

    Make a Div component with a Dropdown and a title. For more information, please consult
    `dcc.Dropdown()` from `dash` library.

    :parameter title: Title of the RadioItems (text on top of the RadioItems)
    :type title: str
    :parameter id_name: Internal identifier of the Dropdown
    :type id_name: str
    :parameter options: Possible options of the Dropdown
    :type options: str | list | int | float | bool |dict
    :parameter value: The current select options
    :type value: str | list | int | float | bool |dict
    :parameter clearable: Boolean to indicate if the Dropdown is clearable or not
    :type clearable: bool
    :parameter css_class: string, name of the associated CSS element, see documentation
    :type css_class: str
    :return: Div component with a Dropdown component
    """
    model_sel = html.Div([html.P(title),
                          dcc.Dropdown(id=id_name, clearable=clearable, options=options, value=value)],
                         className=css_class)
    return model_sel


def make_slider(title, id_name, min_value, max_value, step, css_class="plot_bar_sel", tooltip=None):
    """Create a Div component with a Slider

    Make a Div component with a Slider and a title. For more information, please consult
    `dcc.Slider()` from `dash` library.

    :parameter title: Title of the Slider (text on top of the Slider)
    :type title: str
    :parameter id_name: Internal identifier of the Slider
    :type id_name: str
    :parameter min_value: Minimum value in the slider
    :type min_value: int
    :param max_value: Maximum value in the slider
    :type max_value: int
    :param step: Step value in the slider
    :type step: int
    :parameter css_class: string, name of the associated CSS element, see documentation
    :type css_class: str
    :parameter tooltip: style associated with the slider tooltip
        if `None`: {"placement": "bottom", "always_visible": True}
    :type tooltip: dict | str
    :return: Div component with a Dropdown component
    """
    if tooltip is None:
        tooltip = {"placement": "bottom", "always_visible": True}
    range_val = list(set(list(range(min_value, max_value, int(max_value/step))) + [max_value]))
    range_val.sort()
    range_lab = list()
    for i in range_val:
        range_lab.append(str(i))
    week_slider = html.Div([
        html.P(title),
        dcc.Slider(min=min_value, max=max_value, step=1, marks=dict(zip(range_val, range_lab)), value=min_value,
                   id=id_name, tooltip=tooltip)
    ], className=css_class)
    return week_slider
