import re

from SMHviz_layout.utils import *


def multi_pathogen_notes(pathogen, other_pathogen, website, style=None, ensemble=True):
    """Create a Div component with the notes associated with the multi-pathogen plot

    Make a html.Div() object containing the multi-pathogen plot associated notes, both pathogen names and
    additional pathogen associated website are changeable in the output notes.

    :parameter pathogen: Name of the pathogen
    :type pathogen: str
    :parameter other_pathogen: Name of the additional pathogen (string or list of multiple pathogens in the same order
      as the `website` parameter)
    :type other_pathogen: str | list
    :parameter website: Website link to the additional pathogen SMH hub website (string or list of multiple website
      in the same order as the `other_pathogen` parameter)
    :type website: str | list
    :parameter style: Style associated with the checkbox,
        if `None`: {"display": "inline-block", "margin-left": "5%", "width": "25%"}
    :type style: dict | str
    :parameter ensemble: Boolean to append the noted to say; "combining multi-model ensemble projections" (with or
      without the work "ensemble")
    :type ensemble: bool
    :return: a html.Div() component containing the multi-pathogen plot associated notes
    """
    if style is None:
        style = {"margin-left": "5%", "width": "95%"}
    if len(other_pathogen) > 1:
        other_pathogen_name = ", ".join(other_pathogen)
    else:
        other_pathogen_name = other_pathogen[0]
    if len(website) > 1:
        other_pathogen_website = list()
        for i in range(len(website)):
            web = html.A(other_pathogen[i] + " Scenario Modeling Hub Website", target="blank", href=website[i])
            if i < len(website) - 1:
                web = html.Span([web, ", "])
            other_pathogen_website.append(web)
    else:
        other_pathogen_website = html.A(other_pathogen[0] + " Scenario Modeling Hub Website", target="blank",
                                        href=website[0])
    if ensemble is True:
        ensemble = "ensemble "
    else:
        ensemble = ""
    notes = html.Div([
        html.P(["These projections were produced by combining separate multi-model " + ensemble + "projections of " +
                pathogen + ", " + other_pathogen_name +
                ". We do not account for any interaction between these diseases, which could include behavioral or "
                "immunological interactions that might modify the impacts of one or more of these viruses. For more "
                "information on " + other_pathogen_name + " projections and  scenarios, please consult the ",
                html.Span(other_pathogen_website), html.Span(".")]),
    ], style=style)
    return notes


def multi_pathogen_bar(pathogen, other_pathogen, quant_opt=None, sel_quant=0.5, bar_style=None, note_style=None,
                       clearable=False, css_class="plot_bar_sel", css_multi_radio="multi_bar_radio"):
    """Create Multi-pathogen specific top bar filter

    Create Multi-pathogen specific top bar filter containing:

    - a dropdown of quantiles value for each pathogen (median value selected by default):
         - the first one will have as id "<PATHOGEN>-quantile_dropdown"
         - the second one will have as id "other"
    - a radio items options of the additional pathogen selected round scenario (id: `other-scenario`)
    - a notes with link to additional information

    :parameter pathogen: Name of the principal pathogen
    :type pathogen: str
    :parameter other_pathogen: Dictionary containing the information for the other pathogens for the multi-pathogen
      plots. The dictionary should contain the keys: `scenario` (dictionary with `id` and `name` keys), `default_sel`
      (id(s) of the scenario selected by default), `name` (name of the pathogen), `round_int` (integer representing
      the specific round of the associated pathogen), `website` (associated website)
    :type other_pathogen: dict | list
    :parameter quant_opt: Value of the associated quantiles dropdowns. If `None`: [0.05, 0.25, 0.5, 0.75, 0.95]
    :type quant_opt: list
    :parameter sel_quant: Default selected value of the quantiles dropdowns
    :type sel_quant: int
    :parameter bar_style: Style associated with the checkbox,
        if `None`: {'width': '100%', 'display': 'flex'}
    :type bar_style: dict | str
    :parameter note_style: Style associated with the checkbox,
        if `None`: {"display": "inline-block", "margin-left": "5%", "width": "25%"}
    :type note_style: dict | str
    :parameter clearable: Boolean to indicate if the Dropdown is clearable or not
    :type clearable: bool
    :parameter css_class: string, name of the associated CSS element, see documentation
    :type css_class: str
    :parameter css_multi_radio: string, name of the associated CSS element, see documentation
    :type css_multi_radio: str
    :return: a Div component with the Multi-pathogen specific top bar
    """
    if bar_style is None:
        bar_style = {'width': '100%', 'display': 'flex'}
    if quant_opt is None:
        quant_opt = [0.05, 0.25, 0.5, 0.75, 0.95]
    other_scenario = other_pathogen["scenario"]
    other_scen_sel = list()
    for i in range(len(other_scenario["name"])):
        other_scen_sel.append(other_scenario["name"][i])
    other_scen_dict = dict(zip(other_scenario["id"], other_scen_sel))
    bar = html.Div([
        make_dropdown(pathogen + " Quantile", pathogen.lower() + "-quantile_dropdown", quant_opt, sel_quant,
                      clearable=clearable, css_class=css_class),
        make_radio_items(other_pathogen["name"] + " Round " + str(other_pathogen["round_int"]) +
                         " Scenario Selection" + ':', "other-scenario", options=other_scen_dict,
                         value=other_pathogen["default_sel"][0], css_class=css_multi_radio),
        make_dropdown(other_pathogen["name"] + " Quantile", "other-quantile_dropdown", quant_opt,
                      sel_quant, clearable=clearable, css_class=css_class)
    ], style=bar_style)
    plot_bar = [bar, multi_pathogen_notes(pathogen, [other_pathogen["name"]],
                                          [other_pathogen["website"]], style=note_style)]
    return html.Div(plot_bar)


def multi_pathogen_bar_comp(pathogen, other_pathogen, bar_style=None, note_style=None):
    """Create Combine Multi-pathogen specific top bar filter

    Create Combine Multi-pathogen specific top bar filter containing:

    - a checkbox options of the additional pathogen selected round scenario (id: `other-scenario`)
    - a notes with link to additional information

    :parameter pathogen: Name of the principal pathogen
    :type pathogen: str
    :parameter other_pathogen: List of dictionaries containing the information for the other pathogens for the
       multi-pathogen plots. The dictionary should contain the keys: `scenario` (dictionary with `id` and `name` keys),
      `default_sel`(id(s) of the scenario selected by default), `name` (name of the pathogen), `round_int` (integer
      representing the specific round of the associated pathogen), `website` (associated website)
    :type other_pathogen: list | None
    :parameter bar_style: Style associated with the checkbox,
        if `None`: {'width': '100%', 'display': 'flex'}
    :type bar_style: dict | str
    :parameter note_style: Style associated with the checkbox,
        if `None`: {"display": "inline-block", "margin-left": "5%", "width": "25%"}
    :type note_style: dict | str
    :return: a Div component with the Multi-pathogen specific top bar
    """
    if bar_style is None:
        bar_style = {'width': '100%', 'display': 'flex'}
    list_bar = list()
    list_patho_name = list()
    list_website = list()
    width = round(99 / len(other_pathogen))
    for patho_information in other_pathogen:
        patho_scen_dict = list()
        for i in range(len(patho_information["scenario"]["name"])):
            patho_scen_dict.append({"label": patho_information["scenario"]["name"][i],
                                    "value": patho_information["scenario"]["id"][i]})
        bar = make_checkbox(patho_information["name"] + " Round " + str(patho_information["round_int"]) +
                            " Scenario Selection" + ':', "other-scenario_" + patho_information["name"].lower(),
                            options=patho_scen_dict, value=patho_information["default_sel"],
                            style={"display": "inline-block", "margin-left": "5%", "width": str(width) + "%"},
                            check_style={"display": "inline-grid"})
        list_bar.append(bar)
        list_patho_name.append(patho_information["name"])
        list_website.append(patho_information["website"])
    bar = html.Div(list_bar, style=bar_style)
    plot_bar = [bar, multi_pathogen_notes(pathogen, list_patho_name, list_website, style=note_style, ensemble=False)]
    return html.Div(plot_bar)


def scen_comp_bar(max_horizon, panel_name, multi_panel=False, sidebar_option=False,
                  css_class="plot_bar_sel", tooltip=None, radio_comp_style=None):
    """Create Scenario Comparison specific top bar

    Create Scenario Comparison top bar filter containing (depending on the input):
     - "multi_panel"
         - if the parameter is `True`: include a RadioItems with each items being a potential panels, value for
            the panel names should be included in the parameter `panel_name` (first value selected by default)
         - if the parameter is `False`, the RadioItems is hidden (the panel names are still required, first value
            selected by default)
     - "sidebar_option":
         - if the parameter is `True`: include a slider for each possible weeks, value for the weeks should be
            included with the parameter `max_horizon`
         - if the parameter is `False`, the slider is hidden (the max_horizon is still required)

    :parameter max_horizon: Maximum required value of the horizon for the associated round
    :type max_horizon: int
    :parameter panel_name: Name of each panel for the scenario comparison plot
    :type panel_name: list | str
    :parameter multi_panel: Boolean to show or hide a RadioItems component with each panel as options
    :type multi_panel: bool
    :parameter sidebar_option:  Boolean to show or hide a slider with week information
    :type sidebar_option: bool
    :parameter css_class: string, name of the associated CSS element, see documentation
    :type css_class: str
    :parameter tooltip: style associated with the slider tooltip
        if `None`: {"placement": "bottom", "always_visible": True}
    :type tooltip: dict | str
    :parameter radio_comp_style: Style associated with the checkbox,
        if `None`: {"display": "inline-block", "margin-left": "5%", "width": "45%"}
    :type radio_comp_style: dict | str
    :return:  a Div component with the Scenario Comparison specific top bar
    """
    if radio_comp_style is None:
        radio_comp_style = {"display": "inline-block", "margin-left": "5%", "width": "45%"}
    week_slider = make_slider("Cumulative Starting From Projection Week:", "week-slider", 1,
                              max_horizon, 4, css_class=css_class, tooltip=tooltip)
    panel_choice = html.Div([
        html.Br(), dcc.RadioItems(id="multi-ref", options=panel_name, value=panel_name[0])], style=radio_comp_style)
    if sidebar_option is False:
        week_slider = html.Div(week_slider, hidden=True)
    if multi_panel is False:
        panel_choice = html.Div(panel_choice, hidden=True)
    plot_bar = [week_slider, panel_choice]
    return html.Div(plot_bar, style={"width": "100%"})


def spaghetti_bar(min_slide=10, max_slide=100, step_slide=10, checkbox_median=True, css_med="plot_bar_sel",
                  traj_slider_style=None, traj_by_model=False, traj_model_id="t_model_check"):
    """Create Individual Trajectories specific top bar filter

    Create Individual Trajectories top bar filter containing:
    - a slider with the number of individual trajectories to plot (10, by default) (id: "sample-slider")
    - a notes associated with the slider and plot performance impact
    - (if checkbox_median is True) a checkbox called "Show Median" (returns `True` if selected) (id: "median-checkbox")

    :parameter min_slide: Minimum value in the slider, by default 10
    :type min_slide: int
    :param max_slide: Maximum value in the slider, by default 100
    :type max_slide: int
    :parameter step_slide: Step in the slider, by default 10
    :type step_slide: int
    :parameter checkbox_median: Boolean, if True include the "median checkbox" in the output
    :type checkbox_median: bool
    :parameter css_med: string, name of the associated CSS element for the median checkbox, see documentation
    :type css_med: str
    :parameter traj_slider_style: Style associated with the checkbox,
        if `None`: {"display": "inline-block", "margin-left": "5%", "width": "60%"}
    :type traj_slider_style: dict | str
    :parameter traj_by_model: Boolean, add multiple checkbox to add models to include in the output
    :type traj_by_model: bool
    :parameter traj_model_id: Character, id name of the model checkbox, by default "t_model_check"
    :type traj_model_id: str
    :return: a Div component with the Individual Trajectories specific top bar
    """
    if traj_slider_style is None:
        traj_slider_style = {"display": "inline-block", "margin-left": "5%", "width": "60%"}
    traj_slider = html.Div([
        html.P("Number of Trajectories to plot"),
        html.Div([
            "The performance of the website might be impacted negatively by the selection of high "
            "number of trajectories to plot"
        ]),
        html.Br(),
        dcc.Slider(min_slide, max_slide, step_slide, value=step_slide, id='sample-slider')
    ], style=traj_slider_style)
    check_med = html.Div([
        dcc.Checklist(
            id="median-checkbox",
            options=[{
                "label": "Show Median",
                "value": True,
            }])
    ], className=css_med, hidden=not checkbox_median)
    if traj_by_model is True:
        model_checkbox = html.Div([
            html.P("Select Team-Model to include in the plot:",),
            dcc.Checklist(id=traj_model_id, options=[], style={"display": "inline-flex"},
                          labelStyle={"padding-right": 10})
        ], style={"display": "inline-block", "margin-left": "5%", "width": "95%"})
    else:
        model_checkbox = None
    plot_bar = [traj_slider, check_med, model_checkbox]
    return html.Div(plot_bar)


def heatmap_bar(model_sel, scen_choice, hide_ens, quant_opt=None, sel_quant=0.5, method_list=None,
                clearable=False, css_class="plot_bar_sel", css_h_radio="radio_heatmap",
                css_h_drop="dropdown_heatmap", css_h_plot="plot_bar", style=None):
    """Create Heatmap specific top bar filter

    Create Heatmap (or Spatiotemporal Waves) top bar filter containing:
        - First line:
            - Dropdown with all the available team-model available
            - Checkbox to add the additional(s) ensemble(s) in the dropdown (if available)
            - Radio Items on the location (y-order) axis: Alphabetical or Geographical (default)
            - Dropdown with the possible approach (population size by default)
        - Second line:
            - Dropdown (clearable) with the scenario associated with the round (second one, by default)
            - Dropdown with the quantile to plot

    :parameter model_sel: a Div component with the team-model dropdown information
    :type model_sel: Div
    :parameter scen_choice: list of scenario id associated with the round (need to have at least 2 scenarios)
    :type scen_choice: list
    :parameter hide_ens: Boolean to hide (True) or show (False) the "Ensemble Checkbox" (show available additional
        ensemble in the plot)
    :type hide_ens: bool
    :parameter quant_opt: Value of the associated quantiles dropdowns. If `None`: [0.05, 0.25, 0.5, 0.75, 0.95]
    :type quant_opt: list
    :parameter sel_quant: Default selected value of the quantiles dropdowns
    :type sel_quant: int
    :parameter method_list: List of possible methods.
        If `None`: ["state sum", "population size", "all projection", "all sum"]
    :type method_list: list
    :parameter clearable: Boolean to indicate if the Dropdown is clearable or not
        (except scenario one, always clearable)
    :type clearable: bool
    :parameter css_class: string, name of the associated CSS element, see documentation
    :type css_class: str
    :parameter css_h_radio: string, name of the associated CSS element, see documentation
    :type css_h_radio: str
    :parameter css_h_drop: string, name of the associated CSS element, see documentation
    :type css_h_drop: str
    :parameter css_h_plot: string, name of the associated CSS element, see documentation
    :type css_h_plot: str
    :parameter style: Style associated with the complete Div component,
        if `None`: {"display": "inline-block", "width": "100%"}
    :type style: dict | str
    :return: a Div component with the Heatmap specific top bar
    """
    if style is None:
        style = {"display": "inline-block", "width": "100%"}
    if quant_opt is None:
        quant_opt = [0.05, 0.25, 0.5, 0.75, 0.95]
    if method_list is None:
        method_list = ["state sum", "population size", "all projection", "all sum"]

    checkbox = make_checkbox("", "ensemble-checkbox",
                             [{"label": "Show Additional Ensemble", "value": "True"}],
                             hide_ens, style={"display": "inline-block", "margin-left": "5%", "width": "15%"})
    quant_drop = make_dropdown("Quantile", "heatmap-quantile_dropdown", quant_opt, sel_quant,
                               clearable=clearable,
                               css_class=css_class)
    scenario_sel2 = make_dropdown("Comparison Scenario", "scenario2-dropdown", options=scen_choice,
                                  value=scen_choice[1], clearable=True)
    order_radio = make_radio_items("Location Order", id_name="order_heatmap", value="Geographical",
                                   options=["Alphabetical", "Geographical"], inline=True, css_class=css_h_radio)
    method_dropdown = make_dropdown("Standardization Approach", "method_dropdown", options=method_list,
                                    value=method_list[0], css_class=css_h_drop, clearable=clearable)
    plot_bar = html.Div([
        html.Div([model_sel, checkbox, order_radio, method_dropdown], className=css_h_plot),
        html.Br(),
        html.Div("Following options are not available for the model 'Ground Truth':",
                 style={"margin-left": "5%"}),
        html.Div([scenario_sel2, quant_drop], className=css_h_plot)
    ], style=style)
    return plot_bar


def sample_peak_bar(tf_options=None, clearable=False, css_class="plot_bar_sel", css_bar_plot="plot_bar"):
    """Create Peak specific top bar filter

    Create Peak top bar filter containing:
        - a Dropdown with team-model information (without Ensemble(s)), with an "Ensemble" (peak specific ensemble)
        - a Dropdown with time frame options (or a Slider)
        - a hidden checkbox for additional ensemble set to False (for internal purposes)

    :parameter tf_options: List of possible time frames for the Peak plot. First value selected by default
        If `None`: ["summer 2023", "winter 2023", "year 2023", "summer 2024", "winter 2024", "year 2024"].
    :type tf_options: list
    :parameter clearable: Boolean to indicate if the Dropdown is clearable or not
        (except scenario one, always clearable)
    :type clearable: bool
    :parameter css_class: string, name of the associated CSS element, see documentation
    :type css_class: str
    :parameter css_bar_plot: string, name of the associated CSS element, see documentation
    :type css_bar_plot: str
    :return: a Div component with the Peak specific top bar
    """
    if tf_options is None:
        tf_options = ["summer 2023", "winter 2023", "year 2023", "summer 2024", "winter 2024", "year 2024"]
    model_tf_sel = make_dropdown(title="Model", id_name='model_dropdown', options="Ensemble", value="ensemble",
                                 css_class=css_class, clearable=clearable)
    tf_drop = make_dropdown(title="Time Frame", id_name='tf_dropdown', options=tf_options, value=tf_options[0],
                            css_class=css_class, clearable=clearable)
    checkbox = make_checkbox("", "ensemble-checkbox",
                             [{"label": "Show Additional Ensemble", "value": "False"}], hide=True, style={})
    plot_bar = html.Div([
        html.Div([model_tf_sel, tf_drop], className=css_bar_plot),
        html.Div(checkbox)
    ], className="plot_bar")
    return plot_bar


def make_plot_bar(val_default, max_horizon, hide_ens, sc_panel_name, sc_multi_panel, sc_sidebar_option, pathogen,
                  scen_choice, other_pathogen, plot_tab,
                  quant_opt=None, sel_quant=0.5, method_list=None, tf_options=None, traj_min=10, traj_max=100,
                  traj_step=10, check_med=True, style_checkbox=None, css_sel="plot_bar_sel",
                  inline_radio=True, clearable=False, tooltip=None, radio_comp_style=None, multi_note_style=None,
                  multi_bar_style=None, css_multi_radio="multi_bar_radio", traj_slider_style=None,
                  css_h_radio="radio_heatmap", css_h_drop="dropdown_heatmap", css_bar_plot="plot_bar",
                  heatmap_style=None, traj_by_model=False, mod_drop_id="model_dropdown"):
    """Create plot specific top bar filter

    Create plot top bar filter depending on the round and on the plot tab selected

    :parameter val_default: Name of the default ensemble for the associated round.
    :type val_default: str
    :parameter max_horizon: Maximum required value of the horizon for the associated round
    :type max_horizon: int
    :parameter hide_ens: Boolean to hide (True) or show (False) the "Ensemble Checkbox" (show available additional
        ensemble in the plot)
    :type hide_ens: bool
    :parameter sc_panel_name: Name of each panel for the scenario comparison plot
    :type sc_panel_name: list | str
    :parameter sc_multi_panel: Boolean to show or hide a RadioItems component with each panel as options, for the
        scenario comparison plot
    :type sc_multi_panel: bool
    :parameter sc_sidebar_option:  Boolean to show or hide a slider with week information, in the scenario
        comparison plot
    :type sc_sidebar_option: bool
    :parameter pathogen: Name of the principal pathogen
    :type pathogen: str
    :parameter scen_choice: list of scenario id associated with the round (need to have at least 2 scenarios)
    :type scen_choice: list
    :parameter other_pathogen: List of dictionaries containing the information for the other pathogens for the
       multi-pathogen plots. The dictionary should contain the keys: `scenario` (dictionary with `id` and `name` keys),
      `default_sel`(id(s) of the scenario selected by default), `name` (name of the pathogen), `round_int` (integer
      representing the specific round of the associated pathogen), `website` (associated website). For the
      multi-pathogen plot (not combined) only the first element of the list will be used.
    :type other_pathogen: list | None
    :parameter plot_tab: The id name of the plot selected tab ("scenario" for example, associated with "Scenario Plot")
    :type plot_tab: str
    :parameter quant_opt: Value of the associated quantiles dropdowns. If `None`: [0.05, 0.25, 0.5, 0.75, 0.95]
    :type quant_opt: list
    :parameter sel_quant: Default selected value of the quantiles dropdowns
    :type sel_quant: int
    :parameter method_list: List of possible methods for the Heatmap plot.
        If `None`: ["population size", "all projection"]
    :type method_list: list
    :parameter tf_options: List of possible time frames for the Peak plot. First value selected by default
        If `None`: ["summer 2023", "winter 2023", "year 2023", "summer 2024", "winter 2024", "year 2024"].
    :type tf_options: list
    :parameter traj_min: Minimum value in the slider, by default 10, for the individual trajectories plot only
    :type traj_min: int
    :param traj_max: Maximum value in the slider, by default 100, for the individual trajectories plot only
    :type traj_max: int
    :parameter traj_step: Step in the slider, by default 10, for the individual trajectories plot only
    :type traj_step: int
    :parameter check_med: Boolean, if True include the "median checkbox" in the output, for the individual
        trajectories plot only
    :type check_med: bool
    :parameter style_checkbox: Style associated with the checkbox,
        if `None`: {"display": "inline-block", "margin-left": "5%", "width": "25%"}
    :type style_checkbox: dict | str
    :parameter css_sel: string, name of the associated CSS element, see documentation
    :type css_sel: str
    :parameter inline_radio: Boolean to indicate if the RadioItems should be inline or not
    :type inline_radio: bool
    :parameter clearable: Boolean to indicate if the Dropdown is clearable or not
    :type clearable: bool
    :parameter tooltip: style associated with the slider tooltip
        if `None`: {"placement": "bottom", "always_visible": True}
    :type tooltip: dict | str
    :parameter radio_comp_style: Style associated with the checkbox,
        if `None`: {"display": "inline-block", "margin-left": "5%", "width": "45%"}
    :type radio_comp_style: dict | str
    :parameter multi_bar_style: Style associated with the checkbox,
        if `None`: {'width': '100%', 'display': 'flex'}
    :type multi_bar_style: dict | str
    :parameter multi_note_style: Style associated with the checkbox,
        if `None`: {"display": "inline-block", "margin-left": "5%", "width": "25%"}
    :type multi_note_style: dict | str
    :parameter css_multi_radio: string, name of the associated CSS element, see documentation
    :type css_multi_radio: str
    :parameter traj_slider_style: Style associated with the checkbox,
        if `None`: {"display": "inline-block", "margin-left": "5%", "width": "60%"}
    :type traj_slider_style: dict | str
    :parameter css_h_radio: string, name of the associated CSS element, see documentation
    :type css_h_radio: str
    :parameter css_h_drop: string, name of the associated CSS element, see documentation
    :type css_h_drop: str
    :parameter css_bar_plot: string, name of the associated CSS element, see documentation
    :type css_bar_plot: str
    :parameter heatmap_style: Style associated with the complete Div component,
        if `None`: {"display": "inline-block", "width": "100%"}
    :type heatmap_style: dict | str
    :parameter traj_by_model: Boolean, add multiple checkbox to add models to include in the output
    :type traj_by_model: bool
    parameter mod_drop_id: String, id of the model dropdown, by default `"model_dropdown"`
    :type mod_drop_id: str
    :return: a Div component with the Individual Trajectories specific top bar
    """
    # Prepare Specific Plot tab Selection component
    if method_list is None:
        method_list = ["population size", "all projection"]
    checkbox = make_checkbox("", "ensemble-checkbox", [{"label": "Show Additional Ensemble",
                                                        "value": "True"}], hide_ens, style=style_checkbox)
    radio_target = make_radio_items(
        title="Outcome type", id_name="target_type-radio", value="inc",
        options=[{"label": "Incident", "value": "inc"}, {"label": "Cumulative", "value": "cum"}],
        css_class=css_sel, inline=inline_radio)
    model_sel = make_dropdown(title="Model", id_name=mod_drop_id, options=[val_default], value=val_default,
                              css_class=css_sel, clearable=clearable)
    radio_yaxis = make_radio_items(
        title="Y-axis Scale", id_name="yaxis-scale-radio",
        options=[{"label": "Linear", "value": "linear"}, {"label": "Log", "value": "log"}], value='linear',
        css_class=css_sel, inline=inline_radio)
    week_slider = make_slider("Wks to Show Beyond Observed Data", "week-slider", 6, max_horizon,
                              4, css_class=css_sel, tooltip=tooltip)
    radio_week = make_radio_items("Week", "week-radio", [max_horizon / 2, max_horizon],
                                  max_horizon / 2, css_class=css_sel, inline=inline_radio)
    # Prepare plot bar
    if plot_tab in ["scenario", "scenario_disp"]:
        plot_bar = [checkbox]
    elif plot_tab in ["model_specific", "model_disp"]:
        plot_bar = [radio_target, model_sel, checkbox]
    elif plot_tab in ["scen_sample_comp"]:
        radio_type_target = make_radio_items(title="Type", id_name="comp-type-radio", value="abs",
                                             options=[{"label": "Absolute", "value": "abs"},
                                                      {"label": "Relative", "value": "rel"}],
                                             css_class=css_sel, inline=inline_radio)
        plot_bar = [radio_type_target, checkbox]
    elif plot_tab in ["scen_comparison"]:
        plot_bar = scen_comp_bar(max_horizon, sc_panel_name, multi_panel=sc_multi_panel,
                                 sidebar_option=sc_sidebar_option, css_class=css_sel, tooltip=tooltip,
                                 radio_comp_style=radio_comp_style)
    elif plot_tab in ["state_deviation"]:
        plot_bar = [radio_yaxis]
    elif plot_tab in ["trend_map"]:
        plot_bar = [model_sel, checkbox, week_slider]
    elif plot_tab in ["model_distribution"]:
        plot_bar = [checkbox, radio_target, radio_week]
    elif plot_tab in ["multipat_plot"]:
        plot_bar = multi_pathogen_bar(pathogen, other_pathogen[0],
                                      quant_opt=quant_opt, sel_quant=sel_quant, bar_style=multi_bar_style,
                                      note_style=multi_note_style,  clearable=clearable, css_class=css_sel,
                                      css_multi_radio=css_multi_radio)
    elif plot_tab in ["multipat_plot_comb", "multipat_plot_comb1"]:
        plot_bar = multi_pathogen_bar_comp(pathogen, other_pathogen,
                                           bar_style=multi_bar_style, note_style=multi_note_style)
    elif plot_tab in ["spaghetti", "spaghetti_disp"]:
        traj_model_id = "t_model_check"
        if len(re.findall("_disp$", plot_tab)):
            traj_model_id = "t_disp_model_check"
        plot_bar = spaghetti_bar(
            min_slide=traj_min, max_slide=traj_max, step_slide=traj_step, checkbox_median=check_med, css_med=css_sel,
            traj_slider_style=traj_slider_style, traj_by_model=traj_by_model, traj_model_id=traj_model_id)

    elif plot_tab in ["heatmap"]:
        plot_bar = heatmap_bar(model_sel, scen_choice, hide_ens, quant_opt=quant_opt, sel_quant=sel_quant,
                               method_list=method_list, clearable=clearable, css_class=css_sel,
                               css_h_radio=css_h_radio, css_h_drop=css_h_drop, css_h_plot=css_bar_plot,
                               style=heatmap_style)
    elif plot_tab in ["sample_peak"]:
        plot_bar = sample_peak_bar(tf_options=tf_options, clearable=clearable, css_class=css_sel,
                                   css_bar_plot=css_bar_plot)
    elif plot_tab in ["peak_time_model"]:
        checkbox_hide = make_checkbox("", "ensemble-checkbox", hide=True, style={},
                                      options=[{"label": "", "value": "False"}])
        order_radio = make_radio_items("Location Order", id_name="order_heatmap", value="Geographical",
                                       options=["Alphabetical", "Geographical"], inline=True, css_class=css_h_radio)
        plot_bar = [model_sel, checkbox_hide, order_radio]
    else:
        plot_bar = []
    # return
    return html.Div(plot_bar, className="plot_bar")
