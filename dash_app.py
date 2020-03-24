
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

chart1 = pd.DataFrame(mob_money["mobile_money_classification"].value_counts()).reset_index()

app = dash.Dash()

app.layout = html.Div([
    html.Div(html.H1(children="Hello World")),
    html.Label("Dash Graph1"),
    html.Div(
        dcc.Graph(id="Gender Graph",
                    figure={'data':[
                        #{"x":["Gender"],"y":["mobile_money_classification"],"type":"bar", "name":"None"},
                        {"x":[chart1[chart1["index"] == "None"]["mobile_money_classification"].values[0]],"y":[chart1[chart1["index"] == "None"]["index"].values[0]],"type":"bar", "name":"None"},
                        
                       # {"x":["Gender"],"y":["mobile_money_classification"],"type":"bar", "name":"MM_Plus"},
                        {"x":[chart1[chart1["index"] == "MM_Plus"]["mobile_money_classification"].values[0]],"y":[chart1[chart1["index"] == "MM_Plus"]["index"].values[0]],"type":"bar", "name":"MM_Plus"},
                        
                       # {"x":["Gender"],"y":["mobile_money_classification"],"type":"bar", "name":"MM_Only"},
                       {"x":[chart1[chart1["index"] == "MM_Only"]["mobile_money_classification"].values[0]],"y":[chart1[chart1["index"] == "MM_Only"]["index"].values[0]],"type":"bar", "name":"MM_Only"},
                        
                       # {"x":["Gender"],"y":["mobile_money_classification"],"type":"bar", "name":"Other_Only"},
                       {"x":[chart1[chart1["index"] == "Other_Only"]["mobile_money_classification"].values[0]],"y":[chart1[chart1["index"] == "Other_Only"]["index"].values[0]],"type":"bar", "name":"Other_Only"}
    
                    ],
                    "layout":{
                        "title":"Bar Plot"
                    }}
                )
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)

