# SMH Visualization - Layout

[![Lifecycle:
experimental](https://img.shields.io/badge/lifecycle-experimental-orange.svg)](https://lifecycle.r-lib.org/articles/stages.html#experimental)

This is the Python Package containing the code for the Scenario Modeling 
Hub (SMH) websites layout pages.

## Installation

To install the package locally:

- clone this repository
- `pip install .`

To install the package from GitHub.com

`pip install git+https://github.com/midas-network/SMHViz_layout`

## SMH Specific Modules

To access and easily use all the functions in these modules, multiple requirements 
need to be validated:
- The package needs to be used in the context of Scenario Modeling Hub 
visualization, multiple inputs are link to the SMH visualization standard, 
for example:
  - the output of all the function is adapted to be used in a Python
  Dash visualization app. For more information, please consult the
  [Dash documentation website](https://dash.plotly.com/)
  - some function have a default behavior that is currently not adjustable.
  - The output contains multiple CSS element information that need to be 
  available: an [example of a CSS file](#css) containing all the information is 
  available in the documentation of the package.

### Utils

This module contains 4 functions, that are used to generate the component of
the sidebar and the top plot bar of the SMH websites:
- `make_checkox()`: Generate a Div component with a Checkbox and a title
- `make_radio_items()`: Generate a Div component with a RadioItems and a title
- `make_dropdown()`: Generate a Div component with a Dropdown and a title
- `make_slider()`: Generate a Div component with a Slider and a title

Some functions have additional parameter allowing the "hide" the component,
"clear" the component or change the tooltip style. Please refer to the documentation
associated with each function. 

All the function assumes some CSS class information and/or style information
by default, for additional information please verify any `style` or `css_*`
parameter and please consult the [CSS section](#css) as the bottom of the page.

```python
from SMHviz_layout.utils import *

# Checkbox
make_checkbox("Checkbox Title", "checkbox-id", ["option1", "option2"])

# Slider
make_slider("Slider Title", "slider-id", 0, 100, 10)

# Dropdown
make_dropdown("Dropdown Title", "drop-id", ["option1", "option2"], "option1")

# RadioItems
make_radio_items("RadioItems Title", "radio-id", ["option1", "option2"], "option2")
```

### Metadata Content

This module contains 3 functions, that are used to generate the layout of
the "Model Metadata" pages of the SMH websites:
- `make_dt_metadata()`: take a path to a CSV file as input and returns a 
DataTable object of the inputted CSV file. By default, all columns have
the text content aligned center with a padding of 7px, except any column
called "Description" that has the text content aligned on the left. 
- `make_abstract_tab()`: output the HTML code for the SMH round specific 
page for the abstract, with a dropdown containing the name of all available 
abstract for the round and a `html.Div(id="abstract-output")` section that
can be used to print the associated abstract.  
- `render_abstract()`: works in association with "make_abstract_tab()" and 
returns the content of a specific abstract by a specific round and team-model

**Remarks**: The function associated with the abstracts assumed that the 
abstract filepath and filename followed the SMH standard:
`"PATH/TO/roundX/YYY-MM-DD-team_model-Abstract.md"` with:
- "PATH/TO/": path to a folder storing the abstract by round
- "roundX": round information with X a number associated with a specific round
- "YYYY-MM-DD": date information associated with the specific round X
- "team-model": standard name of the team and model associated with the abstract 
(same code name as in the submission files)

```python
from SMHviz_layout.metadata_content import make_dt_metadata, make_abstract_tab, render_abstract

# Metadata DataTable
make_dt_metadata("path/to/metadata_table.csv")

# Abstracts (for a round 13 for example)
make_abstract_tab("13")
render_abstract("13", "2022-03-13", "team_model")
```

### Notes Definition

This module contains the function to generate the Div component containing
the information for the Notes, Definitions and scenario table below the plot
on the SMH visualization website. The output does not contain the code for
the HTML scenario table as the content is round specific. However, it contains
a Div component with the id: `html-table` that can be used to embed an HTML 
file. 

```python
from dash import html
from SMHviz_layout.notes_definition import make_notes_definition

definition=html.Div([
  html.B("Epiweek: "),
  html.Span("Epidemiological Week as defined by MMWR")
])

left_note=html.Div([
  html.B("Ensemble"),
  html.Span(" is obtained by calculating the weighted median of each submitted quantile.")
])

right_note=html.Div([
  html.U([html.B("Disclaimer:")]),
  html.Span("The content of the Scenario Modeling Hub is solely the responsibility "
            "of the participating teams and the Hub maintainers and does not represent the "
            "official views of any related funding organizations.")
])

make_notes_definition(definition,left_note,right_note)
```

### Tabs

This module contains the functions to generate tabs information:
- 'make_tab_plots': complex function to generate a Div component with the 
plot tabs information with the "Tabs" component identified as `tab_plot`, 
with the content of the tab identified as `plot_tabs-content`.
- 'make_round_tab':  simple function to generate a list of Tab 
component (one per input).

```python
from SMHviz_layout.tabs import make_tab_plots, make_round_tab

tab_name_dict = {
  "spaghetti": "Individual Trajectories",
  "scenario": "Scenario Plot"
}

make_tab_plots(["scenario", "spaghetti"], tab_name_dict)

make_round_tab(["Round 1", "Round 2"])
```

### Plots Tab Bar 

This module contains the functions to generate the bar on top of some SMH 
plots and that contains different Div components to filter/update/modify 
the associated plots.

**The functions in this module are SMH oriented and not standardize for other
hubs, please refer to each function documentation for usage**

The principal functions are:
- `multi_pathogen_bar()`: generates a Div component with the "Multi-pathogen" 
  specific top bar information
- `scen_comp_bar()`: generates a Div component with the "Scenario Comparison" 
  specific top bar information
- `spaghetti_bar()`: generates a Div component with the "Individual Trajectories" 
  specific top bar information
- `heatmap_bar()`: generates a Div component with the "Spatiotemporal Waves" 
  specific top bar information
- `sample_peak_bar()`: generates a Div component with the "Peak" 
  specific top bar information (if necessary)
- `make_plot_bar`: generated a Div component for the inputted top bar
  information (contains all the possible plots' information)

#### Plot tab and associated elements:


| Plot tab name (internal id)               | Top Bar                                                                                                                                                                                                                                                                                                                                                                                                                          |
|:------------------------------------------|:---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Scenario Plot (`scenario`)                | Checkbox to add additional ensemble(s)                                                                                                                                                                                                                                                                                                                                                                                           |
| Model Specific Plot (`model_specific`)    | RadioItems to select incident/cumulative target <br/>Dropdown of team_model and Ensemble(s) <br/>Checkbox to add additional ensemble(s)                                                                                                                                                                                                                                                                                          |
| Scenario Comparison (`scen_comparison`)   | Depending on the round: <br/> - Slider to select week end date OR <br/>- RadioItems to select panel of Comparison OR <br/>- *None*                                                                                                                                                                                                                                                                                               |
| State Deviation (`state_deviation`)       | RadioItems to select the format of the y-axis (log or not)                                                                                                                                                                                                                                                                                                                                                                       |
| Trend Map (`trend_map`)                   | Dropdown of team_model and Ensemble(s) <br/>Checkbox to add additional ensemble(s) <br/>Slider to select week end date                                                                                                                                                                                                                                                                                                           |
| Risk Map (`risk_map`)                     | *None*                                                                                                                                                                                                                                                                                                                                                                                                                           |
| Model Distribution (`model_distribution`) | Checkbox to add additional ensemble(s) <br/> RadioItems to select incident/cumulative target <br/>RadioItems to select end date or mid-horizon end date                                                                                                                                                                                                                                                                          |
| Multi-Pathogen Plot (`multipat_plot`)     | One dropdown of quantiles value for each pathogen (median value selected by default) <br/> A RadioItems of the additional pathogen available scenario <br/>A note with link to additional information                                                                                                                                                                                                                            |
| Individual Trajectories (`spaghetti`)     | A slider with the number of individual trajectories to plot <br/>A note associated with the slider and plot performance impact <br/>A checkbox called "Show Median" (to add the median on the plot)                                                                                                                                                                                                                              |
| Projection Peaks (`proj_peaks`)           | *None*                                                                                                                                                                                                                                                                                                                                                                                                                           |
| Spatiotemporal Waves (`heatmap`)          | Two Lines:<br/>- First line: <br/>Dropdown of team_model and Ensemble(s) <br/>Checkbox to add additional ensemble(s) <br/>RadioItems on the yaxis order: Alphabetical or Geographical (default) <br/>Dropdown with the possible approach (population size by default) <br/>- Second Line: <br/>Dropdown (clearable) with the scenario associated with the round (second one, by default) <br/>Dropdown with the quantile to plot |
| Peak Timing (`sample_peak`)               | Dropdown of team_model and Ensemble ("Ensemble": peak specific ensemble) <br/>Dropdown with time frame options (or a Slider) <br/>Hidden checkbox for additional ensemble set to `False` (for internal purposes)                                                                                                                                                                                                                 |

### Sidebar

This module contains the functions to generate the sidebar on the left side of 
the SMH plots, containing different Div components to filter/update/modify 
the associated plots.

**The functions in this module are SMH oriented and not standardize for other
hubs, please refer to each function documentation for usage**

The principal functions are:
- `scenario_selection()`: generates a Div component with the "Scenario" filter 
  in the sidebar
- `location_selection()`: generates a Div component with the "Location" filter 
  in the sidebar
- `target_selection()`: generates a Div component with the "Target" filter 
  in the sidebar
- `ui_selection()`: generates a Div component with the "Uncertainty Interval"
  filter in the sidebar
- `make_sidebar`: generated a Div component for the inputted tab, round and
  additional setting information (contains all the possible plots' information).
  Currently, the function is SMH specific and assume tab id name as in the table
  below and with the associated behavior. This function also requires multiple 
  dictionaries as input, each one should follow the SMH format as in the 
  documentation. 

#### Plot tab and associated sidebar

| Plot tab name (internal id)               |  Scenario  |  Location  |                       Target                        |                     Uncertain Internal                     |
|:------------------------------------------|:----------:|:----------:|:---------------------------------------------------:|:----------------------------------------------------------:|
| Scenario Plot (`scenario`)                | Checklist  |  Dropdown  |               RadioItems (all target)               | RadioItems: None, 50%, 95%, multi (depending on the round) |
| Model Specific Plot (`model_specific`)    | *Disabled* |  Dropdown  |                     *Disabled*                      |                         RadioItems                         |
| Scenario Comparison (`scen_comparison`)   | *Disabled* |  Dropdown  |                     *Disabled*                      |                         *Disabled*                         |
| State Deviation (`state_deviation`)       | RadioItems | *Disabled* |              RadioItems ("inc" target)              |                         *Disabled*                         |
| Trend Map (`trend_map`)                   | RadioItems | *Disabled* |              RadioItems ("inc" target)              |                         *Disabled*                         |
| Risk Map (`risk_map`)                     | RadioItems | *Disabled* | RadioItems ("inc" or "cum" target, round dependent) |                         *Disabled*                         |
| Model Distribution (`model_distribution`) | Checklist  |  Dropdown  |                     *Disabled*                      |                         *Disabled*                         |
| Multi-Pathogen Plot (`multipat_plot`)     | Checklist  |  Dropdown  |              RadioItems ("inc" target)              |                         *Disabled*                         |
| Individual Trajectories (`spaghetti`)     | Checklist  |  Dropdown  |               RadioItems (all target)               |                         *Disabled*                         |
| Projection Peaks (`proj_peaks`)           | Checklist  | *Disabled* |              RadioItems ("inc" target)              |                         *Disabled*                         |
| Spatiotemporal Waves (`heatmap`)          | RadioItems | *Disabled* |              RadioItems ("inc" target)              |                         *Disabled*                         |
| Peak Timing (`sample_peak`)               | RadioItems | *Disabled* |              RadioItems ("inc" target)              |                         *Disabled*                         |

## CSS

An important number of functions in the package assumes some CSS information, please
find below an example of a CSS file with all the required class associated with the 
functions in these packages.

**If you plan to use the function(s) from these package we strongly advice to copy
and modify, if necessary, the example CSS**

```css
.column {
  float: left;
}

.right-sidebar {
    border-left: 2px solid #bfbfbf;
    width: 73%;
}

.left {
    width: 25%;
}

.right {
    width: 75%;
}

.column_notes {
    float: left;
    width: 45%;
}

/* Clear floats after the columns */
.row:after {
  content: "";
  display: table;
  clear: both;
}

.hr-notes {
    height: 0.5px;
    color: #bfbfbf;
    background-color: #bfbfbf;
    margin: 15px;
}

.title {
    color: #2d5973
}


.span_sidebar {
    color: dimgray;
    font-size: 16px;
}

.disabled {
    color: dimgray;
}

.checklist {
    font-size: 14px;
    display: inline-block;
    padding-bottom: 5px;
}

.dropdown {
    font-size: 14px;
    margin-right: 15px;
}

.radioItems {
    font-size: 14px;
    display: block;
    padding-bottom: 5px;
}

.plot_tabs {
    border-top-left-radius: 3px;
}

.plot_tabs-container {
    width: 100%;
    border-bottom: 2px solid #2daed8;
    margin-left: 5px;
    margin-right: 5px;
}

.plot_tab {
    border-top: 3px solid transparent !important;
    border-left: 2px solid white !important;
    border-right: 2px solid white !important;
    border-bottom: 1px solid #2daed8 !important;
    outline-color: #2daed8 !important;
    padding: 12px !important;
    display: flex !important;
    font-size: 14px;
    align-items: center;
    justify-content: center;
}

.plot_tab--selected {
    color: white !important;
    border-left: 1px solid lightgrey !important;
    border-right: 1px solid lightgrey !important;
    background-color: #2daed8 !important;
    border-top:  3px solid #2daed8 !important;
}

.round_tabs{
    margin: 0 0 10px 0;
    width: 100%;
}

.round_tab {
    border-bottom: 3px solid #2daed8 !important;
    padding: 15px 30px !important;
    display: flex !important;
    font-size: 14px;
    justify-content: center;
    white-space: nowrap;
}

.round_tab--selected {
    color: white !important;
    border-left: 1px solid lightgrey !important;
    border-right: 1px solid lightgrey !important;
    background-color: #2daed8 !important;
    border-top:  3px solid #2daed8 !important;
}


.bottom_notes {
    margin: 50px 13% 50px 13%;
    border: 2px solid #bfbfbf !important;
    padding-left: 25px;
    padding-bottom:25px;
}

.left_notes {
    border-right: 2px solid #bfbfbf;
    padding-right:25px
}

.right_notes {
    margin-left: 25px;
}

.menu_pages {
    background-color: white;
    float: right;
    border-radius: 30px;
    border: 1.5px solid #2d5973;
    color: #2d5973;
    padding: 5px 15px 5px;
    display: block;
    margin: 5px 5px 35px 5px;
    text-decoration: none;
}

img {
    width: 65%;
    height: 80%;
}

.plot_bar {
    width: 100%;
    display: flex;
}

.plot_bar_sel {
    width: 25%;
    display: inline-block;
    margin-left: 5%;
}

.scenario_table {
    height: 1000px;
    width: 100%;
}

.multi_bar_radio {
    margin-left: 5%;
    width: 60%
}

.radio_heatmap {
    margin-left: 5%;
    width: 15%;
    display: inline-grid;
}

.dropdown_heatmap {
    margin-left: 5%;
    width: 20%;
    display: inline-block;
}

```