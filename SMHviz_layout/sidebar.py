import re
import pandas as pd
from SMHviz_layout.utils import *


def scenario_selection(scen_check, invert_scen, unselect_scenario=None, div_type="radio",
                       disabled=False, css_check="checklist", css_radio="radioItems",
                       css_p_disabled="p disabled", css_check_disabled="checklist disabled",
                       css_radio_disabled="radioItems disabled"):
    """Create the expected Scenario component

    Creates the component to select (or not) Scenario information, depending
    on the `div_type` parameter:

    - For `div_type="checklist"`
        - a checklist is generated (id: `scenario-checklist`)
        - all the choice are selected by default (except the scenario id in the parameter
        `unselect_scenario`)
    - For `div_type="radio"`
        - a radioItem is generated (id: `scenario-radio`)
        - the 1st value in `scen_check` is selected (except if the scenario id is in the parameter
          `unselect_scenario`)
    - For all other `div_type`:
        - a disabled radioItem is generated (id: `scenario-radio`)

    If the `disabled` parameter is sel to True: no value is selected by default and no selection
    possible.

    :parameter scen_check: a dictionary with scenario id (key) and scenario id append to
        scenario full name (value)
    :type scen_check: dict
    :parameter invert_scen: a dictionary with scenario id (key) and digit (value)
    :type invert_scen: dict
    :parameter unselect_scenario: A list of scenario id to uncheck by default
    :type unselect_scenario: list
    :parameter div_type: Type of component to output: checklist ("checklist") or radioItems
      ("radio", default)
    :type div_type: str
    :parameter disabled: Boolean, to disabled to output component or not (False by default)
    :type disabled: bool
    :parameter css_check: string, name of the associated CSS element, see documentation
    :type css_check: str
    :parameter css_radio: string, name of the associated CSS element, see documentation
    :type css_radio: str
    :parameter css_p_disabled: string, name of the associated CSS element, see documentation
    :type css_p_disabled: str
    :parameter css_check_disabled: string, name of the associated CSS element, see documentation
    :type css_check_disabled: str
    :parameter css_radio_disabled: string, name of the associated CSS element, see documentation
    :type css_radio_disabled: str
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
                html.P("Scenario:", className=css_p_disabled),
                dcc.RadioItems(
                    id="scenario-radio", labelClassName=css_radio_disabled, options=list_opt)])
        else:
            scenario_sel = html.Div([
                html.P("Scenario:"),
                dcc.RadioItems(
                    id="scenario-radio", labelClassName=css_radio,
                    options=scen_choice, value=scen_value[0])
            ])
    elif div_type == "checklist":
        if disabled is True:
            scenario_sel = html.Div([
                html.P("Scenario:"),
                dcc.Checklist(
                    id="scenario-checklist", labelClassName=css_check_disabled,
                    options=list_opt)])
        else:
            scenario_sel = html.Div([
                html.P("Scenario:"),
                dcc.Checklist(
                    id="scenario-checklist", labelClassName=css_check,
                    options=scen_choice, value=scen_value)])
    else:
        scenario_sel = html.Div([
            html.P("Scenario:", className=css_p_disabled),
            dcc.RadioItems(
                id="scenario-radio", labelClassName=css_radio_disabled, options=list_opt)])
    return scenario_sel


def location_selection(location_info, sel_value="US", disabled=False, clearable=False,
                       css_drop="dropdown", css_drop_disabled="dropdown disabled",
                       css_p_disabled="p disabled"):
    """Create the expected Location component

    Creates the dropdown component to select (or not) Location information
    (id: `location-dropdown`).

    :parameter location_info: list of location
    :type location_info: list
    :parameter sel_value: The default selected value (should be included in the `location_info`
      list)
    :type sel_value: str | int | float | bool
    :parameter disabled: Boolean, to disabled to output component or not (False by default)
    :type disabled: bool
    :parameter clearable: Boolean to indicate if the Dropdown is clearable or not, by default
      `False`
    :type clearable: bool
    :parameter css_drop: string, name of the associated CSS element, see documentation
    :type css_drop: str
    :parameter css_drop_disabled: string, name of the associated CSS element, see documentation
    :type css_drop_disabled: str
    :parameter css_p_disabled: string, name of the associated CSS element, see documentation
    :type css_p_disabled: str
    :return: a Div component with Dropdown component for Location selection
    """
    if disabled is False:
        if sel_value not in location_info:
            sel_value = location_info[0]
        location_sel = html.Div([
            html.P("Location:"),
            dcc.Dropdown(
                id='location-dropdown', clearable=clearable, className=css_drop,
                options=location_info, value=sel_value)
        ])
    else:
        location_sel = html.Div([
            html.P("Location:", className=css_p_disabled),
            dcc.Dropdown(
                id='location-dropdown', clearable=False, className=css_drop_disabled,
                options=location_info, value=None, disabled=True)
        ])
    return location_sel


def target_selection(target_dict, def_target, title="Target:", id_name="target-radio",
                     disabled=False, css_p_disabled="p disabled", css_radio="radioItems",
                     css_radio_disabled="radioItems disabled"):
    """Create the expected Target or Age Group component

    Creates the component to select (or not) Target or Age Group information:
    a radioItem is generated (id: `target-radio` or `age_group-radio`) with the value in
    `def_target` selected.

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
    :parameter css_radio: string, name of the associated CSS element, see documentation
    :type css_radio: str
    :parameter css_p_disabled: string, name of the associated CSS element, see documentation
    :type css_p_disabled: str
    :parameter css_radio_disabled: string, name of the associated CSS element, see documentation
    :type css_radio_disabled: str
    :return: Component for Target selection
    """
    if disabled is True:
        list_opt = list()
        for i in target_dict:
            list_opt.append({"label": target_dict[i], "value": i, "disabled": True})
        target_sel = html.Div([
            html.P(title, className=css_p_disabled),
            dcc.RadioItems(
                id=id_name, labelClassName=css_radio_disabled, options=list_opt)
        ])
    else:
        target_sel = html.Div([
            html.P(title),
            dcc.RadioItems(
                id=id_name, labelClassName=css_radio,
                options=target_dict, value=def_target)
        ])
    return target_sel


def ui_selection(options, value, disabled=False, add_description=None,
                 css_radio="radioItems", css_p_disabled="p disabled",
                 css_radio_disabled="radioItems disabled"):
    """Create the expected Uncertainty Interval component

    Creates the component to select (or not) Uncertainty Interval information:
    a radioItem is generated (id: `ui-radio`) with the value in `value` selected.

    :parameter options: A dictionary with the "label" and "value" information (example:
      "{"label": "None", "value": 0}")
    :type options: dict
    :parameter value: Value indicating default uncertainty interval selection (for example: 0)
    :type value: str | int | bool
    :parameter disabled: Boolean, to disabled to output component or not (False by default)
    :type disabled: bool
    :parameter add_description: a Span component with a text to add below the radioItems
    :type add_description: dash.html.Span.Span
    :parameter css_radio: string, name of the associated CSS element, see documentation
    :type css_radio: str
    :parameter css_p_disabled: string, name of the associated CSS element, see documentation
    :type css_p_disabled: str
    :parameter css_radio_disabled: string, name of the associated CSS element, see documentation
    :type css_radio_disabled: str
    :return: Component for Uncertainty Interval selection
    """
    # Prerequisite
    if disabled is True:
        for i in options:
            i.update({"disabled": True})
        ui_sel = html.Div([
            html.P("Uncertainty Interval: ", className=css_p_disabled),
            dcc.RadioItems(
                id="ui-radio", labelClassName=css_radio_disabled,
                options=options)
        ])
    else:
        ui_sel = html.Div([
            html.P("Uncertainty Interval: "),
            dcc.RadioItems(
                id="ui-radio", labelClassName=css_radio,
                options=options, value=value)
        ])
        if add_description is not None:
            sel_comp = ui_sel.children + [html.Br(), add_description]
            ui_sel = html.Div(sel_comp)
    return ui_sel


def make_sidebar(round_number, tab, scenario_file, location_info, scenario_dict, target_dict,
                 def_target, age_group=None, race_ethnicity=None, ui_sel_list=None, ui_val=95,
                 unselect_scenario=None, cumulative=True, multi_ui=True, round_name=None,
                 css_left_col="column left", css_check="checklist", css_radio="radioItems",
                 css_p_disabled="p disabled", css_check_disabled="checklist disabled",
                 css_radio_disabled="radioItems disabled", css_drop="dropdown",
                 css_drop_disabled="dropdown disabled"):
    """Create the sidebar on the SMH visualization websites

    The sidebar is depending on the round and on the plot tab selected.

    For the "Scenario plot" only: if the `multi_ui` parameter is set to True, a "multi" choice
    will be appended to the uncertainty interval radioItems (`ui_sel_list`) with
    `{"label": "Multi", "value": -1}` and a small description will  be displayed: 'multi'
    displays 95%, 90%, 80%, and 50% uncertainty intervals, shaded from lightest (95%) to darkest
    (50%)"`, with a CSS: `className="span_sidebar"`

    :parameter round_number: Numeric identifier of a specific round tab (for example "13")
    :type round_number: str | int
    :parameter tab: Selected tab associated with the sidebar
    :type tab: str
    :parameter scenario_file: Path to CSV file containing scenario information per round
    :type scenario_file: str
    :parameter location_info: table containing location information in the SMH standard
    :type location_info: DataFrame
    :parameter scenario_dict: A dictionary with scenario id (value) and associated number (key)
    :type scenario_dict: dict
    :parameter target_dict: A dictionary with target name (as in submission file) as keys and
        target full name as value
    :type target_dict: dict
    :parameter def_target: Character indicating default target selection (for example: "hosp")
    :type def_target: str
    :parameter age_group: A dictionary with age group (value) and associated variable (key), if `
        None` (default), no age group filter in the output
    :type age_group: None | dict
    :parameter race_ethnicity:  A dictionary with race ethnicity (value) and associated variable
        (key), if `None` (default), no race ethnicity filter in the output
    :type race_ethnicity: None | dict
    :parameter ui_sel_list: A dictionary with the "label" and "value" information (example:
        "{"label": "None", "value": 0}"). If `None`: [{"label": "None", "value": 0},
        {"label": "50%", "value": 50}, {"label": "95%", "value": 95}]
    :type ui_sel_list: dict
    :parameter age_group: age group information, None if not included
    :type age_group: None | str | dict
    :parameter ui_val: Value indicating default uncertainty interval selection (default: 95).
    :type ui_val: int
    :parameter unselect_scenario: A list of scenario id to uncheck by default. If None, all selected
    :type unselect_scenario: list
    :parameter cumulative: [For risk map only] Boolean, to use cumulative (True) or incident
        target(s) (False)
    :type cumulative: bool
    :parameter multi_ui: [For scenario plot only] Boolean, to include a "multi" options in the
        uncertainty interval choices
    :type multi_ui: bool
    :parameter round_name: Name of the round to display, if None "Round <Number>"
    :type round_name: str
    :parameter css_left_col: string, name of the associated CSS element, see documentation
    :type css_left_col: str
    :parameter css_check: string, name of the associated CSS element, see documentation
    :type css_check: str
    :parameter css_radio: string, name of the associated CSS element, see documentation
    :type css_radio: str
    :parameter css_p_disabled: string, name of the associated CSS element, see documentation
    :type css_p_disabled: str
    :parameter css_check_disabled: string, name of the associated CSS element, see documentation
    :type css_check_disabled: str
    :parameter css_radio_disabled: string, name of the associated CSS element, see documentation
    :type css_radio_disabled: str
    :parameter css_drop: string, name of the associated CSS element, see documentation
    :type css_drop: str
    :parameter css_drop_disabled: string, name of the associated CSS element, see documentation
    :type css_drop_disabled: str
    :return: a Div component with the sidebar code associated with the round and tab selected
    """
    # Prerequisite
    if ui_sel_list is None:
        ui_sel_list = [{"label": "None", "value": 0},
                       {"label": "50%", "value": 50},
                       {"label": "95%", "value": 95}]
    # Tab-specific output
    # Scenario
    scen_info = pd.read_csv(scenario_file)
    scen_info = scen_info[scen_info["round"] == "round" + str(round_number)]
    scen_info = dict(zip(scen_info["scenario_id"], scen_info["scenario_fullname"]))
    scen_check = list()
    for i in scen_info:
        scen_check.append(i + " (" + scen_info[i] + ")")
    scen_check = dict(zip(scen_info.keys(), scen_check))
    invert_scen = {v: k for k, v in scenario_dict.items()}
    if tab in ["scenario", "model_distribution", "spaghetti", "multipat_plot", "proj_peaks",
               "peak_time_model", "peak_size", "multipat_plot_comb", "multipat_plot_comb1",
               "scenario_disp", "spaghetti_disp"]:
        scenario_sel = scenario_selection(scen_check, invert_scen, unselect_scenario,
                                          div_type="checklist", css_check=css_check,
                                          css_check_disabled=css_check_disabled,
                                          css_p_disabled=css_p_disabled,
                                          css_radio_disabled=css_radio_disabled,
                                          css_radio=css_radio)
    elif tab in ["state_deviation", "trend_map", "risk_map", "heatmap", "sample_peak",
                 "model_disp", "so_boxplot"]:
        scenario_sel = scenario_selection(scen_check, invert_scen, unselect_scenario,
                                          div_type="radio", css_check=css_check,
                                          css_check_disabled=css_check_disabled,
                                          css_p_disabled=css_p_disabled,
                                          css_radio_disabled=css_radio_disabled,
                                          css_radio=css_radio)
    else:
        scenario_sel = scenario_selection(scen_check, invert_scen, disabled=True,
                                          css_check=css_check,
                                          css_check_disabled=css_check_disabled,
                                          css_p_disabled=css_p_disabled,
                                          css_radio_disabled=css_radio_disabled,
                                          css_radio=css_radio)
    # Location
    list_location = list(location_info["location_name"])
    if 'U.S. Minor Outlying Islands' in list_location:
        list_location.remove('U.S. Minor Outlying Islands')
    if tab in ["scenario", "spaghetti", "model_specific", "scen_comparison", "model_distribution",
               "multipat_plot", "peak_size", "multipat_plot_comb", "multipat_plot_comb1",
               "scenario_disp", "spaghetti_disp", "model_disp", "scen_sample_comp",
               "scen_sample_comp_disp", "so_boxplot"]:
        location_sel = location_selection(list_location, css_drop=css_drop,
                                          css_drop_disabled=css_drop_disabled,
                                          css_p_disabled=css_p_disabled)
    else:
        location_sel = location_selection(list_location, disabled=True, css_drop=css_drop,
                                          css_drop_disabled=css_drop_disabled,
                                          css_p_disabled=css_p_disabled)
    # Target
    def_targ = str()
    for targ in target_dict.keys():
        if len(re.findall(def_target, targ)) > 0:
            def_targ = targ
            break
    if tab in ["scenario", "spaghetti", "scenario_disp", "spaghetti_disp"]:
        target_sel = target_selection(target_dict, def_targ)
    elif tab in ["state_deviation", "trend_map", "multipat_plot", "proj_peaks", "heatmap",
                 "sample_peak", "risk_map", "multipat_plot_comb", "multipat_plot_comb1",
                 "scen_sample_comp", "scen_sample_comp_disp"]:
        if tab == "risk_map" and cumulative is True:
            search_term = "cum "
        else:
            search_term = "inc "
        for targ in target_dict.keys():
            if len(re.findall(search_term + def_target, targ)) > 0:
                def_targ = targ
                break
        sel_target = list()
        for i in target_dict:
            if re.search(search_term, i) is not None:
                sel_target.append(i)
        target_dict = dict(zip(sel_target, [target_dict[x] for x in sel_target]))
        target_sel = target_selection(target_dict, def_targ, css_p_disabled=css_p_disabled,
                                      css_radio_disabled=css_radio_disabled, css_radio=css_radio)
    else:
        target_sel = target_selection(target_dict, def_targ, disabled=True,
                                      css_p_disabled=css_p_disabled,
                                      css_radio_disabled=css_radio_disabled, css_radio=css_radio)
    # UI
    if tab in ["scenario", "model_specific", "scenario_disp", "model_disp"]:
        if (multi_ui is True) and (tab in ["scenario", "scenario_disp"]):
            ui_sel_list.append({"label": "Multi", "value": -1})
            ui_text = html.Span("'multi' displays 95%, 90%, 80%, and 50% uncertainty "
                                "intervals, shaded from lightest (95%) to darkest (50%)",
                                className="span_sidebar")
        else:
            ui_text = None
        ui_sel = ui_selection(ui_sel_list, ui_val, add_description=ui_text,
                              css_p_disabled=css_p_disabled, css_radio_disabled=css_radio_disabled,
                              css_radio=css_radio)
    else:
        ui_sel = ui_selection(ui_sel_list, ui_val, disabled=True, css_p_disabled=css_p_disabled,
                              css_radio_disabled=css_radio_disabled, css_radio=css_radio)
    # Age group
    if age_group is not None:
        if tab in ["scenario", "spaghetti", "model_specific", "scen_comparison", "state_deviation",
                   "trend_map", "risk_map", "model_distribution", "scen_sample_comp", "so_boxplot"]:
            age_group_sel = target_selection(age_group, "0-130", title="Age Group:",
                                             id_name="age_group-radio")
        else:
            age_group_sel = target_selection(age_group, "0-130", disabled=True,
                                             title="Age Group:", id_name="age_group-radio",
                                             css_p_disabled=css_p_disabled,
                                             css_radio_disabled=css_radio_disabled,
                                             css_radio=css_radio)
    else:
        age_group_sel = None
    # Race ethnicity
    if race_ethnicity is not None:
        if tab in ["scenario", "spaghetti", "scenario_disp", "spaghetti_disp",
                   "scen_sample_comp_disp"]:
            race_ethnicity_sel = target_selection(race_ethnicity, "overall",
                                                  title="Race - Ethnicity:",
                                                  id_name="race_ethnicity-radio")
        else:
            race_ethnicity_sel = target_selection(race_ethnicity, "overall", disabled=True,
                                                  title="Race - Ethnicity:",
                                                  id_name="race_ethnicity-radio",
                                                  css_p_disabled=css_p_disabled,
                                                  css_radio_disabled=css_radio_disabled,
                                                  css_radio=css_radio)
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
        html.Br(),
        race_ethnicity_sel,
        html.Br(),
        ui_sel,
    ], className=css_left_col)
    return sidebar
