import streamlit as st 
import pandas as pd
import matplotlib.pyplot as plt
import altair as alt

st.set_page_config(page_title="Sales Dashboard", layout='wide')
st.title("Sales Dashboard (Jun - Dec 2023)")
data = pd.read_csv("test_data.csv")


cols1 = st.columns(3)
with cols1[0]:
    st.markdown('**Number of Orders by Category food**')
    categoy_display = "food"
    filtered_data = data[data['Category'] == categoy_display]
    menu_counts = filtered_data['Menu'].value_counts()
    st.bar_chart(menu_counts, color='#ffaa00', use_container_width=True)

with cols1[1]:
    st.markdown('**Number of Orders by Category drink**')
    categoy_display = "drink"
    filtered_data = data[data['Category'] == categoy_display]
    menu_counts = filtered_data['Menu'].value_counts()
    st.bar_chart(menu_counts, use_container_width=True)

with cols1[2]:
    st.markdown('**Revenue by Category**')
    categoy_food_display = "food"
    categoy_drink_display = "drink"
    groupbyDate = pd.to_datetime(data['Date'], format='%d/%m/%Y')
    sum_orders_by_date_food = data[data['Category']==categoy_food_display].groupby('Date')['Price'].sum().reset_index()
    sum_orders_by_date_drink = data[data['Category']==categoy_drink_display].groupby('Date')['Price'].sum().reset_index()
    chart_data = pd.merge(sum_orders_by_date_food, sum_orders_by_date_drink, on='Date', how='outer')
    chart_data.columns = ['Date', 'Food_income', 'Drink_income']
    chart_data.fillna(0, inplace=True)


    chart_data['Date'] = pd.to_datetime(chart_data['Date'],format='%d/%m/%Y')
    chart_data = chart_data.sort_values(by='Date')

    st.line_chart(chart_data, x="Date", y=["Food_income", "Drink_income"])

#-----------------------------------------
cols2 = st.columns(3)
with cols2[0]:
    Day_of_week = data['Day Of Week'].sort_values().unique()

    average_Kitchen_Staff_by_day_of_week = data.groupby('Day Of Week')['Kitchen Staff'].mean().reset_index()
    average_Drinks_Staff_by_day_of_week = data.groupby('Day Of Week')['Drinks Staff'].mean().reset_index()

    categoy_display_food = "food"
    filtered_data_food = data[data['Category'] == categoy_display_food]
    filtered_data_food = filtered_data_food.groupby('Day Of Week')['Menu'].value_counts().reset_index(name='Countfood')
    filtered_data_food = filtered_data_food.groupby('Day Of Week')['Countfood'].mean().reset_index()


    categoy_display_drink = "drink"
    filtered_data_drink = data[data['Category'] == categoy_display_drink]
    filtered_data_drink = filtered_data_drink.groupby('Day Of Week')['Menu'].value_counts().reset_index(name='Countdrink')
    filtered_data_drink = filtered_data_drink.groupby('Day Of Week')['Countdrink'].mean().reset_index()


    data['Date'] = pd.to_datetime(data['Date'], format='%d/%m/%Y')
   

    # Create bar chart for average Kitchen Staff by day of the week
    chart1 = alt.Chart(average_Kitchen_Staff_by_day_of_week).mark_bar().encode(
        x='Day Of Week:N',
        y='Kitchen Staff:Q',
        color=alt.value('#006400'),
        tooltip=['Day Of Week', 'Kitchen Staff']
    ).properties(width=400)

    # Create bar chart for average Drinks Staff by day of the week
    chart2 = alt.Chart(average_Drinks_Staff_by_day_of_week).mark_bar().encode(
        x='Day Of Week:N',
        y='Drinks Staff:Q',
        color=alt.value('#3BB143'),
        tooltip=['Day Of Week', 'Drinks Staff']
    ).properties(width=400)

    # Create bar chart for average food orders by date
    chart3 = alt.Chart(filtered_data_food).mark_bar().encode(
        x='Day Of Week:N',
        y='Countfood:Q',
        color=alt.value('#ffaa00'),
        tooltip=['Day Of Week', 'Countfood']
    ).properties(width=400)

    # Create bar chart for average drink orders by date
    chart4 = alt.Chart(filtered_data_drink).mark_bar().encode(
        x='Day Of Week:N',
        y='Countdrink:Q',
        tooltip=['Day Of Week', 'Countdrink']
    ).properties(width=400)

    grouped_bar_chart_staff = alt.layer(chart1, chart2).properties(title='Average Staff Counts by Day of the Week')
    grouped_bar_chart_drink = alt.layer(chart3, chart4).properties(title='Average Orders Counts by Day of the Week')

    # Display the grouped bar chart in Streamlit
    st.altair_chart(grouped_bar_chart_drink | grouped_bar_chart_staff)
