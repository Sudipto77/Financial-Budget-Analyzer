# -*- coding: utf-8 -*-
"""
Created on Tue Mar 26 00:14:13 2024

@author: KIIT
"""

import streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu
import time
import plotly.express as px



_INTERIM_BUDGET = """ 
        Finance Minister Nirmala Sitharaman presented the interim budget 
        for 2024-25 on 1 February. An interim budget is a short-term financial
        plan covering government expenditures until a new government takes 
        over after the elections
"""

def stream_data():
    for word in _INTERIM_BUDGET.split(" "):
        yield word + " "
        time.sleep(0.04)

data = pd.read_csv("C:/6th semester/TTL lab Project/India_budget_2021.csv")
#data.set_index('Department /Ministry', inplace=True)


with st.sidebar:
    
    selected = option_menu('Financial Budget Analyser',
                          
                          ['Home',
                           'View Annual Budget',
                           'View Budget Allocated To a Ministry',
                           'Compare Budget With  previous Years'],
                          icons=['house','bank','currency-rupee','bar-chart'],
                          default_index=-4)
    
   

if (selected == 'View Annual Budget'):
    
    # page title
    st.title('Annual Budget of :blue[2024-2025]')
    st.header('', divider='rainbow')
    st.write_stream(stream_data)
    selected_columns = ['Department /Ministry', 'Fund allotted24-25(Rs)(in crores)']
    df_selected = pd.DataFrame({key: data[key] for key in selected_columns})

# Display the selected columns as a table using st.write
    st.write(df_selected)
    
    department_totals = data.groupby('Department /Ministry')['Fund allotted24-25(Rs)(in crores)'].sum()
    total_budget = department_totals.sum()
    department_percentages = (department_totals / total_budget) * 100

# Combine departments with less than 2.5% share into "Others"
    threshold_percentage = 2.5
    others_total = department_totals[department_percentages < threshold_percentage].sum()
    department_totals = department_totals[department_percentages >= threshold_percentage]
    department_totals.loc['OTHERS'] = others_total
    
    
    st.bar_chart(department_totals)
    

    
    fig = px.pie(department_totals, values=department_totals, names=department_totals.index,
                 title=f'Percentage Share of Ministries',
                 height=350, width=250)
    fig.update_layout(margin=dict(l=20, r=20, t=30, b=0),)
    st.plotly_chart(fig, use_container_width=True)
    st.caption(':blue[_NOTE_ : ] Ministries with share of less than 2.5% is included in _OTHERS_ section of the pie chart')
    
    
    
    
elif (selected == 'View Budget Allocated To a Ministry'):
    
    data.set_index('Department /Ministry', inplace=True)
    st.title('Budget Allocated To :blue[Ministries]')
    st.header('', divider='rainbow')
    #st.write_stream(stream_data)
    option = st.selectbox(
    '',
    ('MINISTRY OF AGRICULTURE', 'DEPARTMENT OF ATOMIC ENERGY',
     'MINISTRY OF AYURVEDA, YOGA', 'MINISTRY OF CHEMICALS AND FERTILISER',
     'MINISTRY OF CIVIL AVIATION', 'MINISTRY OF COAL',
     'MINISTRY OF COMMERCE AND INDUSTRY', 'MINISTRY OF COMMUNICATION',
     'MINISTRY OF CONSUMER AFFAIRS', 'MINISTRY OF CORPORATE AFFAIRS',
     'MINISTRY OF CULTURE', 'MINISTRY OF DEFENCE',
     'MINISTRY OF DEVELOPMENT OF NORTH EASTERN REGION',
     'MINISTRY OF EARTH SCIENCES', 'MINISTRY OF EDUCATION',
     'MINISTRY OF ELECTRONICS AND INFORMATION TECHNOLOGY',
     'MINISTRY OF ENVIRONMENT, FOREST', 'MINISTRY OF EXTERNAL AFFAIRS',
     'MINISTRY OF FINANCE', 'MINISTRY OF FISHERIES, ANIMAL HUSBANDRY',
     'MINISTRY OF FOOD PROCESSING INDUSTRIES',
     'MINISTRY OF HEALTH AND FAMILY WELFARE', 'MINISTRY OF HEAVY INDUSTRIES',
     'MINISTRY OF HOME AFFAIRS', 'MINISTRY OF HOUSING AND URBAN AFFAIRS',
     'MINISTRY OF INFORMATION AND BROADCASTING', 'MINISTRY OF JAL SHAKTI',
     'MINISTRY OF LABOUR AND EMPLOYMENT', 'MINISTRY OF LAW AND JUSTICE',
     'MINISTRY OF MICRO, SMALL AND MEDIUM ENTERPRISES', 'MINISTRY OF MINES',
     'MINISTRY OF MINORITY AFFAIR', 'MINISTRY OF NEW AND RENEWABLE ENERGY',
     'MINISTRY OF PANCHAYATI RAJ', 'MINISTRY OF PARLIAMENTARY AFFAIRS',
     'MINISTRY OF PERSONNEL, PUBLIC GRIEVANCES',
     'MINISTRY OF PETROLEUM AND NATURAL GAS', 'MINISTRY OF PLANNING',
     'MINISTRY OF PORTS, SHIPPING', 'MINISTRY OF POWER',
     'THE PRESIDENT, PARLIAMENT, UNION PUBLIC SERVICE COMMISSION',
     'MINISTRY OF RAILWAYS', 'MINISTRY OF ROAD TRANSPORT AND HIGHWAY',
     'MINISTRY OF RURAL DEVELOPMENT', 'MINISTRY OF SCIENCE AND TECHNOLOGY',
     'MINISTRY OF SKILL DEVELOPMENT', 'MINISTRY OF SOCIAL JUSTICE AND EMPOWERMENT',
     'DEPARTMENT OF SPACE', 'MINISTRY OF STATISTICS', 'MINISTRY OF STEEL',
     'MINISTRY OF TEXTILES', 'MINISTRY OF TOURISM',
     'MINISTRY OF TRIBAL AFFAIRS', 'MINISTRY OF WOMEN AND CHILD DEVELOPMENT',
     'MINISTRY OF YOUTH AFFAIRS AND SPORTS'),
    index=None,
   placeholder="Select a Ministry",
    )
    if(option != None):
        st.write("")
        st.write("") 
        st.subheader(f'Showing Budget Allocated to :blue[{option}]')
        st.header('', divider='rainbow')
        st.write('In the financial year 2024-2025 the government have decided to allocate ',data.loc[option]['Fund allotted24-25(Rs)(in crores)'] , ' Crore INR to ', option)
        selected_ministry = data.loc[option]
        per_inc = (data.loc[option]['Fund allotted24-25(Rs)(in crores)'] - data.loc[option]['Fund allotted23-24(Rs)(in crores)'])/data.loc[option]['Fund allotted23-24(Rs)(in crores)']
        st.line_chart(selected_ministry)
          
        st.write(' Percentage Growth in ',option, ' is ',round(per_inc*100,2),'% compared to financial year 2023-2024')
    
elif (selected == 'Compare Budget With  previous Years'):
    
    
    st.title('Budget Comparison :blue[Visualised]')
    st.header('', divider='rainbow')
    st.write("With a steady growth rate India's GDP has Increased rapidly over a last few years , consistently being the fastest growing economy for a long time now. India is the 5th largest economy on its way to claim the third spot overtaking Japan and Germany by 2030.")
    #st.write_stream(stream_data)
    totals24_25= data['Fund allotted24-25(Rs)(in crores)'].sum()
    totals23_24= data['Fund allotted23-24(Rs)(in crores)'].sum()
    totals22_23= data['Fund allotted22-23(Rs)(in crores)'].sum()
    totals21_22= data['Fund allotted21-22(Rs)(in crores)'].sum()
    bar_data = {
        
        'Budget' : [totals21_22 , totals22_23, totals23_24 , totals24_25],
        'year' : [ '2021-2022' , '2022-2023' , '2023-2024' ,'2024-2025' ]
        }
    df = pd.DataFrame(bar_data)

# Group by year and sum the budget
    df_grouped = df.groupby('year')['Budget'].sum()

# Display the bar chart
    st.bar_chart(df_grouped , width=0.5 ,color = '#c8b6ff')
    growth_perc = ((totals24_25 - totals23_24)/totals23_24)*100
    st.write("India's budget has increased by ", round(growth_perc ,2) ,"% from last year ")
    st.line_chart(df_grouped, color = '#c8b6ff')
else:
    st.title("Financial Budget :blue[Analyser]")
    st.header('', divider='rainbow')
    st.header('Understanding _Budget_ made  :blue[easier] ')
    st.write('')
    st.subheader('Key Takeaways from :blue[India’s Interim Budget:]')
    st.write('Fiscal deficitfor year through March 2025pegged at 5.1% of GDPis much lower than this year’s revised gap of 5.8%. Economists had expected the shortfall at 5.3% of GDP for the coming year')
    st.write('Market borrowings will also be lower given the tax buoyancy. Prime Minister Narendra Modi’s administration aims to borrow 14.13 trillion rupees ($170 billion) in the next fiscal year. That’s lower than the 15.2 trillion rupees estimate in a Bloomberg survey.')
    st.write('Bonds predictably roseafter the numbers; the yield on the benchmark 10-year debt fell as much as 9 basis points to 7.05%.Stocks were little changedas the government announced no major surprises either on spending or tax generating measures; the benchmark Sensex index was flat just after midday India time')