import dash
from dash import Dash, html, callback ,Input, Output, State, dcc
from dash_bootstrap_templates import load_figure_template
import pandas as pd
import dash_ag_grid as dag
import dash_bootstrap_components as dbc
import plotly.express as px
load_figure_template (["slate", "vapor"])

df = pd.read_csv (r"https://raw.githubusercontent.com/datasciencedojo/datasets/refs/heads/master/titanic.csv")


dbc_css = r"https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates/dbc.min.css"

app = Dash (__name__ ,external_stylesheets =[ dbc.themes.SLATE, dbc_css])


# color_switch = html.Span ([

#         dbc.Label (className= "fa fa moon", 
#                    html_for= "switch"),

#         dbc.Switch (id = "color_switch", 
#                     value= False, 
#                     className= "d-inline-block ms-1",
#                       persistence= True),

#         dbc.Label (className= "fa fa sun", html_for = "switch")

# ])



app.layout = dbc.Container ([


        html.H1 ("This is a Pro Dashboard", 
                 className= "text-primary bg-secondary border rounded-2 mt-5 p-3 mb-4",
                 style= {"textAlign": "center"}),

        html.P ("hello there this is a description where you can actually input your text",
                className= "mb-4 fs-5",
                 style= {"textAlign": "center"}),


        

        dbc.Row ([
            dbc.Col ([
            dbc.Alert ("Attention this complicated dashboard is only meant for professionals",
                   className= "col-8 fs-5 mb-5 mx-auto bg-warning",
                   style = {"textAlign" : "center"},
                   duration= None),
            ], width = 12),


            dbc.Col ([

                
            dcc.RadioItems ([

                        {"label" : "Passenger's ID", "value" : "PassengerId"},
                        {"label" : "Survived", "value" : "Survived"},
                        {"label" : "Pclass", "value" : "Pclass"},

                    ], value = "PassengerId", id = "radio_options")],width= 9 ),
                
            dbc.Col ([
                dcc.Dropdown (options= ["Name", "Sex"],
                              value= "Name", 
                              id= "drop_down"),

            dcc.Slider (
                        min= 5,
                        max= 12,
                        step= 1,
                        value= 5,
                        className= "mt-5",
                        id = "slider")
                              
                              
                              ], width= 3),

            dbc.Col ([
                dbc.Button ("Submit", 
                            className= "mt-2 mb-3 col-6",n_clicks= 0,
                            id= "submit_button"),
                dbc.Alert ("it is recommeded to not select both the Survived and the Sex values for readability purposes",
                           className= "col-10 fs-6 mx-1 bg-warning",)
            ], width=9, lg= 4),

            dag.AgGrid (columnDefs= [{"field":i} for i in df.columns],
                        rowData= df.to_dict("records"),
                        defaultColDef= {"filter" : True},
                        dashGridOptions= {"animateRows" : True,
                                             "pagination" : True},
                        id= "grid"
                       )
                
                ], ),

            dcc.Graph (figure= {}, id= "graph") 



], fluid= True, className= "dbc dbc-ag-grid", )


@callback (
    Output (component_id= "grid", component_property= "columnDefs"),
    Output (component_id= "graph", component_property= "figure"),
    Input (component_id= "submit_button", component_property= "n_clicks"),
    
    State (component_id= "slider", component_property= "value"),
    State (component_id= "radio_options", component_property= "value"),
    State (component_id= "drop_down", component_property= "value"),
   

)

def option_selected (n_clicks, slider,  y_selected, x_selected):
    columns = df.columns [:slider]
    columnDefs = [{"field":i} for i in columns]
    
    fig = px.scatter (df, x= x_selected,
                      y= y_selected,
                      color = y_selected,
                      color_discrete_sequence= px.colors.sequential.Plasma_r,
                      )
    
    fig.update_layout ( xaxis = dict (showticklabels = False, visible = False))
    return columnDefs, fig

if __name__== "__main__":
    app.run (debug= True)