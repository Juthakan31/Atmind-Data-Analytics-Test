import streamlit as st 
import pandas as pd
import altair as alt
import calendar


st.set_page_config(page_title="Sales Dashboard", layout='wide')
st.title("Sales Dashboard (Jun - Dec 2023)")
data = pd.read_csv("test_data.csv")


cols1 = st.columns(3)
with cols1[0]:
    st.markdown('**Number of Orders by Category food**')
    categoy_food = "food"
    filtered_data_food = data[data['Category'] == categoy_food]
    orders_food = filtered_data_food['Menu'].value_counts()
    st.bar_chart(orders_food, color='#ffaa00', use_container_width=True)

with cols1[1]:
    st.markdown('**Number of Orders by Category drink**')
    categoy_drink = "drink"
    filtered_data_drink = data[data['Category'] == categoy_drink]
    orders_drink = filtered_data_drink['Menu'].value_counts()
    st.bar_chart(orders_drink, use_container_width=True)

with cols1[2]:
    st.markdown('**Revenue by Category**')
    categoy_food = "food"
    categoy_drink = "drink"
    sum_orders_food_by_date = data[data['Category']==categoy_food].groupby('Date')['Price'].sum().reset_index()
    sum_orders_drink_by_date = data[data['Category']==categoy_drink].groupby('Date')['Price'].sum().reset_index()
    chart_data = pd.merge(sum_orders_food_by_date, sum_orders_drink_by_date, on='Date', how='outer')
    chart_data.columns = ['Date', 'categoy_food', 'categoy_drink']
    # chart_data.fillna(0, inplace=True)

    chart_data['Date'] = pd.to_datetime(chart_data['Date'],format='%d/%m/%Y')
    chart_data = chart_data.sort_values(by='Date')
    st.line_chart(chart_data, x="Date", y=["categoy_food", "categoy_drink"])


#-----------------------------------------------------------------------------------
    

cols2 = st.columns(3)
with cols2[0]:
    week = list(calendar.day_name)
    Day_of_week = pd.Categorical(data['Day Of Week'], categories=week, ordered=True)
    data['Day Of Week'] = Day_of_week

    average_Kitchen_Staff_by_day_of_week = data.groupby('Day Of Week')['Kitchen Staff'].mean().reset_index()
    average_Drinks_Staff_by_day_of_week = data.groupby('Day Of Week')['Drinks Staff'].mean().reset_index()

    categoy_food = "food"
    filtered_data_food = data[data['Category'] == categoy_food]
    filtered_data_food = filtered_data_food.groupby('Day Of Week')['Menu'].value_counts().reset_index(name='Ordersfood')
    filtered_data_food = filtered_data_food.groupby('Day Of Week')['Ordersfood'].mean().reset_index()

    categoy_drink = "drink"
    filtered_data_drink = data[data['Category'] == categoy_drink]
    filtered_data_drink = filtered_data_drink.groupby('Day Of Week')['Menu'].value_counts().reset_index(name='Ordersdrink')
    filtered_data_drink = filtered_data_drink.groupby('Day Of Week')['Ordersdrink'].mean().reset_index()

    # Create bar chart: avg Kitchen Staff
    chart1 = alt.Chart(average_Kitchen_Staff_by_day_of_week).mark_bar().encode(
        x=alt.X('Day Of Week', sort=week),
        y='Kitchen Staff',
        color=alt.value('#006400'),
        tooltip=['Day Of Week', 'Kitchen Staff']
    ).properties(width=400)

    # Create bar chart: avg Drinks Staff
    chart2 = alt.Chart(average_Drinks_Staff_by_day_of_week).mark_bar().encode(
        x=alt.X('Day Of Week', sort=week),
        y='Drinks Staff',
        color=alt.value('#3BB143'),
        tooltip=['Day Of Week', 'Drinks Staff']
    ).properties(width=400)

    # Create bar chart: avg food orders
    chart3 = alt.Chart(filtered_data_food).mark_bar().encode(
        x=alt.X('Day Of Week', sort=week),
        y='Ordersfood',
        color=alt.value('#ffaa00'),
        tooltip=['Day Of Week', 'Ordersfood']
    ).properties(width=400)

    # Create bar chart: avg drink orders 
    chart4 = alt.Chart(filtered_data_drink).mark_bar().encode(
        x=alt.X('Day Of Week', sort=week),
        y='Ordersdrink',
        tooltip=['Day Of Week', 'Ordersdrink']
    ).properties(width=400)

    grouped_bar_chart_staff = alt.layer(chart1, chart2).properties(title='Average Staff Counts by Day of the Week')
    grouped_bar_chart_drink = alt.layer(chart3, chart4).properties(title='Average Orders Counts by Day of the Week')
    
    st.altair_chart(grouped_bar_chart_drink | grouped_bar_chart_staff)
