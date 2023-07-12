from dash import dcc, html


def make_tab_plots(sel_plot, tab_name_dict, show=None, plot_sel=None, css_plot_tabs="plot_tabs",
                   css_plot_tabs_container="plot_tabs-container", css_right_sidebar="column right-sidebar",
                   css_plot_tab="plot_tab", css_plot_tab_sel="plot_tab--selected"):
    """Create the plot tabs on the SMH visualization websites

    Output a Div component with the plot tabs information with the Tabs component identified as `tab_plot`, and each
    individual tab with the internal id tab name informed in the `sel_plot` parameter.

    By default, the first tab in the `sel_plot` list is selected.

    The output contains multiple CSS class information that need to be available:
        - `plot_tabs`: parent style information for the tab bar containing all the tabs
                - `plot_tabs-container`: style about the tabs component holding a collection of tab
        - `column right-sidebar`: style information for the right side of the page in the plot content (right of the
            sidebar)
        - `plot_tab`, `plot_tab--selected`: style information for an individual tab (and when selected)
    An example CSS files containing all the information is available in the documentation of the package.


    :parameter sel_plot: List of internal id tab names of each plot to include in the tabs
    :type sel_plot: list
    :parameter tab_name_dict: A dictionary with internal id tab names as keys and list of full tab name as value
    :type tab_name_dict: dict
    :parameter show: A character string to replace all the tabs is `sel_plot` is set to None
    :type show: str
    :parameter plot_sel: A character string corresponding of the internal id tab name of the plot to select by default,
        first on the `sel_plot` list, if parameter set to `None`
    :type plot_sel: str
    :parameter css_plot_tabs: string, name of the associated CSS element, see documentation
    :type css_plot_tabs: str
    :parameter css_plot_tabs_container: string, name of the associated CSS element, see documentation
    :type css_plot_tabs_container: str
    :parameter css_right_sidebar: string, name of the associated CSS element, see documentation
    :type css_right_sidebar: str
    :parameter css_plot_tab: string, name of the associated CSS element, see documentation
    :type css_plot_tab: str
    :parameter css_plot_tab_sel: string, name of the associated CSS element, see documentation
    :type css_plot_tab_sel: str
    :return: a Div component with the plot tabs information with the Tabs component identified as `tab_plot` with the
    content identified as `plot_tabs-content`
    """
    if sel_plot is None:
        plot_tab = html.Div([
            dcc.Tabs(id="tabs-plot", parent_className=css_plot_tabs,
                     className=css_plot_tabs_container, children=list()),
            html.Br(),
            html.Div(show, id="plot_tabs_content")
        ], className=css_right_sidebar)
    else:
        plot_tab_list = list()
        for i in sel_plot:
            tab = dcc.Tab(label=tab_name_dict.get(i), value=i, className=css_plot_tab,
                          selected_className=css_plot_tab_sel)
            plot_tab_list.append(tab)
        if plot_sel is None:
            plot_sel = sel_plot[0]
        plot_tab = html.Div([
            dcc.Tabs(id="tabs-plot", value=plot_sel, parent_className=css_plot_tabs,
                     className=css_plot_tabs_container, children=plot_tab_list),
            html.Div(id="plot_tabs-content")
        ], className=css_right_sidebar)
    return plot_tab


def make_round_tab(list_round, css_round_tab="round_tab", css_round_tab_sel="round_tab--selected"):
    """Make tab for each element of list_round

     The output contains multiple CSS class information that need to be available:
        - `round_tab`, `round_tab--selected`: style information for an individual tab (and when selected)
    An example CSS files containing all the information is available in the documentation of the package.


    :parameter list_round : list of round written as "Round 1" for example
    :type list_round: list
    :parameter css_round_tab: string, name of the associated CSS element, see documentation
    :type css_round_tab: str
    :parameter css_round_tab_sel: string, name of the associated CSS element, see documentation
    :type css_round_tab_sel: str
    :return: list of Tab with round information written as "Round 1" for example
    """
    round_tab_list = list()
    for i in list_round:
        tab = dcc.Tab(label=i, value=i, className=css_round_tab, selected_className=css_round_tab_sel)
        round_tab_list.append(tab)
    return round_tab_list
