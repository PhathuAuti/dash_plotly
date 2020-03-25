
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.offline as pyo
import plotly.graph_objs as go
# import plotly.express as px
import pandas as pd
import numpy as np

mob_money = pd.read_csv('training.csv')

# changing index cols with rename()
mob_money = mob_money.rename(columns = {"Q1": "Age",
                                  "Q2": "Gender",
                                  "Q3": "Marital Status",
                                  "Q4": "Highest Qualification",
                                  "Q5": "Living Conditions",
                                  "Q6": "Land Ownership",
                                  "Q7": "Cellphone Ownership",
                                  "Q8_1": "Salaries/Wages",
                                  "Q8_2": "Trading",
                                  "Q8_3": "Service Provider",
                                  "Q8_4": "Piece Jobs",
                                  "Q8_5": "Rental Income",
                                  "Q8_6": "Investments",
                                  "Q8_7": "Pension",
                                  "Q8_8": "Social Welfare",
                                  "Q8_9": "Rely on Someone Else",
                                  "Q8_10": "No Money",
                                  "Q8_11": "Other",
                                  "Q9": "Employer",
                                  "Q10": "Trading Products",
                                  "Q11": "Services Provided",
                                  "Q12": "Sent Money(12months)",
                                  "Q13": "Last Sent Money",
                                  "Q14": "Received Money(12months)",
                                  "Q15": "Last Received Money",
                                  "Q16": "Mobile Money for GnS (12months)",
                                  "Q17": "Mobile Money for Bills (12months)",
                                  "Q18": "Literacy in Kiswhahili",
                                  "Q19": "Literacy in English"})

# changing columns using .columns()
mob_money.columns = ["ID","Age", "Gender","Marital Status","Highest Qualification","Living Conditions",
                    "Land Ownership", "Cellphone Ownership", "Salaries/Wages","Trading", "Service Provider",
                    "Piece Jobs", "Rental Income","Investments", "Pension","Social Welfare",
                    "Rely on Someone Else", "No Money","Other","Employer","Trading Products",
                    "Services Provided","Sent Money(12months)","Last Sent Money","Received Money(12months)",
                    "Last Received Money","Mobile Money for GnS (12months)", "Mobile Money for Bills (12months)",
                    "Literacy in Kiswhahili","Literacy in English","Latitude","Longitude","mobile_money","savings",
                    "borrowing","insurance","mobile_money_classification"]

# changing the values in columns from intergers to representative strings
mob_money['Gender']= ['Female' if each==2 else 'Male' for each in mob_money['Gender']]
mob_money['Land Ownership']= ['No' if each==2 else 'Yes' for each in mob_money['Land Ownership']]
mob_money['Sent Money(12months)']= ['No' if each==2 else 'Yes' for each in mob_money['Sent Money(12months)']]
mob_money['Received Money(12months)']= ['No' if each==2 else 'Yes' for each in mob_money['Received Money(12months)']]
mob_money['Last Sent Money'] = mob_money['Last Sent Money'].map({-1: "N/A", 4: "90Days", 2: "7Days", 5: "90+Days", 3: "30Days", 6: "6Mnth+", 1: "Y/Today"})
mob_money['Last Received Money'] = mob_money['Last Received Money'].map({-1: "N/A", 5: "90+Days", 1: "Y/Today", 3: "30Days", 4: "90Days", 6: "6Mnth+", 2: "7Days"})
mob_money['Mobile Money for GnS (12months)'] = mob_money['Mobile Money for GnS (12months)'].map({-1: "N/A", 1: "Never", 4: "Monthly", 5: "LessMnthly", 3: "Weekly", 2: "Daily"})
mob_money['Mobile Money for Bills (12months)'] = mob_money['Mobile Money for Bills (12months)'].map({-1: "N/A", 4: "Monthly", 1: "Never", 2: "Daily", 5: "LessMnthly", 3: "Weekly"})
mob_money['mobile_money']= ['No' if each==0 else 'Yes' for each in mob_money['mobile_money']]
mob_money['mobile_money_classification'] = mob_money['mobile_money_classification'].map({0: "None", 3: "MM_Plus", 2: "MM_Only", 1: "Other_Only"})
mob_money['Marital Status'] = mob_money['Marital Status'].map({3: "Widowed", 1: "Married", 4: "Single", 2: "Divorced"})

# creating an incomes dataframe to compare incomes with mobile money usage
incomes = mob_money.loc[:, 'Salaries/Wages':'Other']
incomes['mobile_money'] = mob_money['mobile_money']
incomes['Sent Money(12months)'] = mob_money['Sent Money(12months)']
incomes['Received Money(12months)'] = mob_money['Received Money(12months)']
incomes = pd.melt(incomes, id_vars = ['mobile_money', 'Sent Money(12months)', 'Received Money(12months)'], var_name='Income_Type') 
incomes = incomes[incomes['value'] == 1]
incomes.Income_Type.value_counts()

# creating necessary dataframes to help build the graphs
chart1 = pd.DataFrame(mob_money["mobile_money_classification"].value_counts()).reset_index()
chart2 = pd.DataFrame(mob_money['Mobile Money for GnS (12months)'].value_counts()).reset_index()
chart3 = pd.DataFrame(incomes['Income_Type'].value_counts()).reset_index()

app = dash.Dash()

colors = {
    'background': '#1f1f1f',
    'text': '#ff7f50'
}

app.layout = html.Div([
    html.Div(html.H1(children="Tanzania Mobile Money")),
    html.Label("Dashboard Indicating Mobile Money Usage in Tanzania"),
    html.Div([
        dcc.Graph(id="Bar Plot1",
                        figure={'data':[
                            {"x":[chart1[chart1["index"] == "None"]["index"].values[0]], "y":[chart1[chart1["index"] == "None"]["mobile_money_classification"].values[0]],"type":"bar", "name":"None"},
                            {"x":[chart1[chart1["index"] == "MM_Plus"]["index"].values[0]], "y":[chart1[chart1["index"] == "MM_Plus"]["mobile_money_classification"].values[0]],"type":"bar", "name":"MM_Plus"},
                            {"x":[chart1[chart1["index"] == "MM_Only"]["index"].values[0]], "y":[chart1[chart1["index"] == "MM_Only"]["mobile_money_classification"].values[0]],"type":"bar", "name":"MM_Only"},
                            {"x":[chart1[chart1["index"] == "Other_Only"]["index"].values[0]], "y":[chart1[chart1["index"] == "Other_Only"]["mobile_money_classification"].values[0]],"type":"bar", "name":"Other_Only"}
                        ],
                        "layout":{
                            "title":"Mobile Money Classification"
                        }}
                    )
        ]),
    html.Div([
        dcc.Graph(id="Bar Plot2",
                        figure={'data':[
                            {"x":[chart2[chart2["index"] == "Never"]["index"].values[0]], "y":[chart2[chart2["index"] == "Never"]['Mobile Money for GnS (12months)'].values[0]],"type":"bar", "name":"Never"},
                            {"x":[chart2[chart2["index"] == "LessMnthly"]["index"].values[0]], "y":[chart2[chart2["index"] == "LessMnthly"]['Mobile Money for GnS (12months)'].values[0]],"type":"bar", "name":"LessMnthly"},
                            {"x":[chart2[chart2["index"] == "Monthly"]["index"].values[0]], "y":[chart2[chart2["index"] == "Monthly"]['Mobile Money for GnS (12months)'].values[0]],"type":"bar", "name":"Monthly"},
                            {"x":[chart2[chart2["index"] == "Weekly"]["index"].values[0]], "y":[chart2[chart2["index"] == "Weekly"]['Mobile Money for GnS (12months)'].values[0]],"type":"bar", "name":"Weekly"},
                            {"x":[chart2[chart2["index"] == "Daily"]["index"].values[0]], "y":[chart2[chart2["index"] == "Daily"]['Mobile Money for GnS (12months)'].values[0]],"type":"bar", "name":"Daily"}
                        ],
                        "layout":{
                            "title":"Mobile Money Used For Goods and Services In Past Year"
                        }}
                    )
        ]),
    html.Div([
        dcc.Graph(id="Bar Plot3",
                        figure={'data':[
                            {"x":[chart3[chart3["index"] == "Salaries/Wages"]["index"].values[0]], "y":[chart3[chart3["index"] == "Salaries/Wages"]['Income_Type'].values[0]],"type":"bar", "name":"Salaries/Wages"},
                            {"x":[chart3[chart3["index"] == "Trading"]["index"].values[0]], "y":[chart3[chart3["index"] == "Trading"]['Income_Type'].values[0]],"type":"bar", "name":"Trading"},
                            {"x":[chart3[chart3["index"] == "Rental Income"]["index"].values[0]], "y":[chart3[chart3["index"] == "Rental Income"]['Income_Type'].values[0]],"type":"bar", "name":"Rental Income"},
                            {"x":[chart3[chart3["index"] == "Service Provider"]["index"].values[0]], "y":[chart3[chart3["index"] == "Service Provider"]['Income_Type'].values[0]],"type":"bar", "name":"Service Provider"},
                            {"x":[chart3[chart3["index"] == "Investments"]["index"].values[0]], "y":[chart3[chart3["index"] == "Investments"]['Income_Type'].values[0]],"type":"bar", "name":"Investments"},
                            {"x":[chart3[chart3["index"] == "Piece Jobs"]["index"].values[0]], "y":[chart3[chart3["index"] == "Piece Jobs"]['Income_Type'].values[0]],"type":"bar", "name":"Piece Jobs"},
                            {"x":[chart3[chart3["index"] == "Social Welfare"]["index"].values[0]], "y":[chart3[chart3["index"] == "Social Welfare"]['Income_Type'].values[0]],"type":"bar", "name":"Social Welfare"},
                            {"x":[chart3[chart3["index"] == "Pension"]["index"].values[0]], "y":[chart3[chart3["index"] == "Pension"]['Income_Type'].values[0]],"type":"bar", "name":"Pension"},
                            {"x":[chart3[chart3["index"] == "Rely on Someone Else"]["index"].values[0]], "y":[chart3[chart3["index"] == "Rely on Someone Else"]['Income_Type'].values[0]],"type":"bar", "name":"Rely on Someone Else"},
                            {"x":[chart3[chart3["index"] == "No Money"]["index"].values[0]], "y":[chart3[chart3["index"] == "No Money"]['Income_Type'].values[0]],"type":"bar", "name":"No Money"},
                            {"x":[chart3[chart3["index"] == "Other"]["index"].values[0]], "y":[chart3[chart3["index"] == "Other"]['Income_Type'].values[0]],"type":"bar", "name":"Other"}
                        ],
                        "layout":{
                            "title":"Types of Income"
                        }}
                    )
        ])
    ])

# running the server
if __name__ == '__main__':
    app.run_server(debug=True)

