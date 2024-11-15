import re
from SMHviz_layout.utils import *


def scenario_selection(scen_check, invert_scen, unselect_scenario=None, div_type="radio", disabled=False):
    """Create the expected Scenario component

    Creates the component to select (or not) Scenario information, depending
    on the `div_type` parameter:

    - For `div_type="checklist"`
        - a checklist is generated (id: `scenario-checklist`)
        - all the choice are selected by default (except the scenario id in the parameter `unselect_scenario`)
    - For `div_type="radio"`
        - a radioItem is generated (id: `scenario-radio`)
        - the 1st value in `scen_check` is selected (except if the scenario id is in the parameter `unselect_scenario`)
    - For all other `div_type`:
        - a disabled radioItem is generated (id: `scenario-radio`)

    If the `disabled` parameter is sel to True: no value is selected by default and no selection possible.

    :parameter scen_check: a dictionary with scenario id (key) and scenario id append to
        scenario full name (value)
    :type scen_check: dict
    :parameter invert_scen: a dictionary with scenario id (key) and digit (value)
    :type invert_scen: dict
    :parameter unselect_scenario: A list of scenario id to uncheck by default
    :type unselect_scenario: list
    :parameter div_type: Type of component to output: checklist ("checklist") or radioItems ("radio", default)
    :type div_type: str
    :parameter disabled: Boolean, to disabled to output component or not (False by default)
    :type disabled: bool
    :return: a Div component for Scenario selection
    """
    # Prerequisite
    scen_value = list()
    for i in list(scen_check.keys()):
        scen_value.append(invert_scen.get(i))
    scen_choice = dict(zip(scen_value, scen_check.values()))
    for i in list(scen_check.keys()):
        if unselect_scenario is not None:
            if i in unselect_scenario:
                scen_value.remove(invert_scen.get(i))
    list_opt = list()
    for i in scen_check:
        list_opt.append({"label": scen_check[i], "value": i, "disabled": True})
    # Div component
    if div_type == "radio":
        if disabled is True:
            scenario_sel = html.Div([
                html.P("Scenario:"),
                dcc.RadioItems(id="scenario-radio", options=list_opt)])
        else:
            scenario_sel = html.Div([
                html.P("Scenario:"),
                dcc.RadioItems(id="scenario-radio", options=scen_choice, value=scen_value[0])
            ])
    elif div_type == "checklist":
        if disabled is True:
            scenario_sel = html.Div([
                html.P("Scenario:"),
                dcc.Checklist(id="scenario-checklist", options=list_opt)])
        else:
            scenario_sel = html.Div([
                html.P("Scenario:"),
                dcc.Checklist(id="scenario-checklist", options=scen_choice, value=scen_value)])
    else:
        scenario_sel = html.Div([
            html.P("Scenario:"),
            dcc.RadioItems(id="scenario-radio", options=list_opt)])
    return scenario_sel


def location_selection(location_info, sel_value="US", disabled=False, clearable=False):
    """Create the expected Location component

    Creates the dropdown component to select (or not) Location information (id: `location-dropdown`).

    :parameter location_info: list of location
    :type location_info: list
    :parameter sel_value: The default selected value (should be included in the `location_info` list)
    :type sel_value: str | int | float | bool
    :parameter disabled: Boolean, to disabled to output component or not (False by default)
    :type disabled: bool
    :parameter clearable: Boolean to indicate if the Dropdown is clearable or not, by default `False`
    :type clearable: bool
    :return: a Div component with Dropdown component for Location selection
    """
    if disabled is False:
        location_sel = html.Div([
            html.P("Location:"),
            dcc.Dropdown(id='location-dropdown', clearable=clearable, options=location_info, value=sel_value)
        ])
    else:
        location_sel = html.Div([
            html.P("Location:"),
            dcc.Dropdown(id='location-dropdown', clearable=False, options=location_info, value=None, disabled=True)
        ])
    return location_sel


def prep_target(target_type, target_dict, def_target):
    def_targ = None
    if target_type != "all":
        search_term = target_type
        for targ in target_dict.keys():
            if len(re.findall(search_term + def_target, targ)) > 0:
                def_targ = targ
                break
        sel_target = list()
        for i in target_dict:
            if re.search(search_term, i) is not None:
                sel_target.append(i)
        target_dict = dict(zip(sel_target, [target_dict[x] for x in sel_target]))
    else:
        for targ in target_dict.keys():
            if len(re.findall(def_target, targ)) > 0:
                def_targ = targ
                break
    return {"def_targ": def_targ, "target_dict": target_dict}


def target_selection(target_dict, def_target, title="Target:", id_name="target-radio", disabled=False):
    """Create the expected Target or Age Group component

    Creates the component to select (or not) Target or Age Group information:
    a radioItem is generated (id: `target-radio` or `age_group-radio`) with the value in `def_target` selected.

    :parameter target_dict: A dictionary with target name (as in submission file) as keys and
       target full name as value
    :type target_dict: dict
    :parameter def_target: Character indicating default target selection (for example: "hosp")
    :type def_target: str
    :parameter title: Title of the filter
    :type title: str
    :parameter id_name: Internal identifier name
    :type id_name: str
    :parameter disabled: Boolean, to disabled to output component or not (False by default)
    :type disabled: bool
    :return: Component for Target selection
    """
    if disabled is True:
        list_opt = list()
        for i in target_dict:
            list_opt.append({"label": target_dict[i], "value": i, "disabled": True})
        target_sel = html.Div([
            html.P(title),
            dcc.RadioItems(id=id_name, options=list_opt)
        ])
    else:
        target_sel = html.Div([
            html.P(title),
            dcc.RadioItems(id=id_name, options=target_dict, value=def_target)
        ])
    return target_sel


def ui_selection(options, value, disabled=False, add_description=None):
    """Create the expected Uncertainty Interval component

    Creates the component to select (or not) Uncertainty Interval information:
    a radioItem is generated (id: `ui-radio`) with the value in `value` selected.

    :parameter options: A dictionary with the "label" and "value" information (example: "{"label": "None", "value": 0}")
    :type options: dict
    :parameter value: Value indicating default uncertainty interval selection (for example: 0)
    :type value: str | int | bool
    :parameter disabled: Boolean, to disabled to output component or not (False by default)
    :type disabled: bool
    :parameter add_description: a Span component with a text to add below the radioItems
    :type add_description: dash.html.Span.Span
    :return: Component for Uncertainty Interval selection
    """
    # Prerequisite
    if disabled is True:
        for i in options:
            i.update({"disabled": True})
        ui_sel = html.Div([
            html.P("Uncertainty Interval: "),
            dcc.RadioItems(id="ui-radio", options=options)
        ])
    else:
        ui_sel = html.Div([
            html.P("Uncertainty Interval: "),
            dcc.RadioItems(id="ui-radio", options=options, value=value)
        ])
        if add_description is not None:
            sel_comp = ui_sel.children + [html.Br(), add_description]
            ui_sel = html.Div(sel_comp)
    return ui_sel


def make_sidebar(round_number, scen_check, invert_scen, type_scen, scen_disabled, unselect_scenario,
                 list_location, loc_disabled,
                 target_dict, def_targ, targ_disabled,
                 ui_sel_list, ui_val, ui_text, ui_disabled,
                 age_group=None, age_group_def=None, age_group_disabled=True,
                 race_ethnicity=None, race_ethnicity_def=None, race_ethnicity_disabled=True,
                 round_name=None):
    """Create the sidebar on the SMH visualization websites

    The sidebar is depending on the round and on the plot tab selected.

    For the "Scenario plot" only: if the `multi_ui` parameter is set to True, a "multi" choice will be appended to the
    uncertainty interval radioItems (`ui_sel_list`) with `{"label": "Multi", "value": -1}` and a small description will
    be displayed: `"'multi' displays 95%, 90%, 80%, and 50% uncertainty intervals, shaded from lightest (95%) to darkest
    (50%)"`, with a CSS: `className="span_sidebar"`

    :parameter round_number: Numeric identifier of a specific round tab (for example "13")
    :type round_number: str | int
    :parameter target_dict: A dictionary with target name (as in submission file) as keys and
        target full name as value
    :type target_dict: dict
    :parameter ui_sel_list: A dictionary with the "label" and "value" information (example: "{"label": "None", "value":
        0}"). If `None`: [{"label": "None", "value": 0}, {"label": "50%", "value": 50}, {"label": "95%", "value": 95}]
    :type ui_sel_list: dict
    :parameter ui_val: Value indicating default uncertainty interval selection (default: 95).
    :type ui_val: int
    :parameter unselect_scenario: A list of scenario id to uncheck by default. If None, all selected
    :type unselect_scenario: list
    :parameter round_name: Name of the round to display, if None "Round <Number>"
    :type round_name: str
    :return: a Div component with the sidebar code associated with the round and tab selected
    """

    # Tab-specific output
    # Scenario
    scenario_sel = scenario_selection(scen_check, invert_scen, unselect_scenario, div_type=type_scen,
                                      disabled=scen_disabled)
    # Location
    location_sel = location_selection(list_location, disabled=loc_disabled)

    # Target
    target_sel = target_selection(target_dict, def_targ, disabled=targ_disabled)

    # UI
    ui_sel = ui_selection(ui_sel_list, ui_val, add_description=ui_text, disabled=ui_disabled)
    # Age group (optional)
    if age_group is not None:
        age_group_sel = html.Div([target_selection(age_group, age_group_def, disabled=age_group_disabled,
                                                   title="Age Group:", id_name="age_group-radio"),
                                 html.Br()])
    else:
        age_group_sel = None
    # Race Ethnicity
    if race_ethnicity is not None:
        race_ethnicity_sel = html.Div([target_selection(race_ethnicity, race_ethnicity_def,
                                                        disabled=race_ethnicity_disabled, title="Race Ethnicity Group:",
                                                        id_name="race_ethnicity-radio"),
                                       html.Br()])
    else:
        race_ethnicity_sel = None
    # Round name
    if round_name is None:
        round_name = "Round " + str(round_number)
    # Sidebar
    sidebar = html.Div([
        html.H2("Model Projection", className="title"),
        html.Div("New scenario for models are defined in each round"),
        html.H3(round_name, className="title"),
        scenario_sel,
        html.Hr(className="hr-notes"),
        location_sel,
        html.Br(),
        target_sel,
        html.Br(),
        age_group_sel,
        race_ethnicity_sel,
        ui_sel,
    ])
    return sidebar
