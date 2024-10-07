import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import math

st.title("Paul's Data App")

st.write("### The dataset used in the graphs below")
df = pd.read_csv("Superstore_Sales_utf8.csv", parse_dates=True)
st.dataframe(df)

# This bar chart will not have solid bars--but lines--because the detail data is being graphed independently
st.bar_chart(df, x="Category", y="Sales")

# Now let's do the same graph where we do the aggregation first in Pandas... (this results in a chart with solid bars)
st.dataframe(df.groupby("Category").sum())
# Using as_index=False here preserves the Category as a column.  If we exclude that, Category would become the datafram index and we would need to use x=None to tell bar_chart to use the index
st.bar_chart(df.groupby("Category", as_index=False).sum(), x="Category", y="Sales", color="#04f")

# Aggregating by time
# Here we ensure Order_Date is in datetime format, then set is as an index to our dataframe
df["Order_Date"] = pd.to_datetime(df["Order_Date"])
df.set_index('Order_Date', inplace=True)
# Here the Grouper is using our newly set index to group by Month ('M')
sales_by_month = df.filter(items=['Sales']).groupby(pd.Grouper(freq='M')).sum()

st.dataframe(sales_by_month)

# Here the grouped months are the index and automatically used for the x axis
st.line_chart(sales_by_month, y="Sales")

st.write("## My additions")
sub_categories_dict = {
    "Furniture": ["Bookcases", "Chairs", "Furnishings", "Tables"], 
    "Office Supplies": ["Appliances", "Art", "Binders", "Envelopes", "Fasteners", "Labels", "Paper", "Storage", "Supplies"], 
    "Technology": ["Accessories", "Copiers", "Machines", "Phones"]
}
categories = list(sub_categories_dict.keys())
selected_category = st.selectbox('Pick a category to view its corresponding subcategories in a graph', categories,
                                index=None,placeholder="Select a category")
st.write("You selected:", selected_category)
sub_categories = sub_categories_dict[selected_category]
selected_sub_categories = st.multiselect('Select the subcategories', sub_categories, 
                                placeholder="Select subcategories")

st.write(f'You selected subcategories: {selected_sub_categories}')

filtered_data = df[df['Sub_Category'].isin(selected_sub_categories)]
sub_categories_sales_by_month = filtered_data.filter(items=["Sales"]).groupby(pd.Grouper(freq='ME')).sum()
st.line_chart(sub_categories_sales_by_month, y="Sales")

total_sales = filtered_data['Sales'].sum()
total_profit = filtered_data['Profit'].sum()
overall_profit_margin = ((total_profit / total_sales) * 100) if total_sales > 0 else 0

overall_sales = df['Sales'].sum()
overall_profit = df['Profit'].sum()
overall_average_profit_margin = ((overall_profit / overall_sales) * 100) if overall_sales > 0 else 0
profit_margin_delta = overall_profit_margin - overall_average_profit_margin

st.metric(label="Total Sales", value=round(total_sales, 2))
st.metric(label="Total Profit", value=round(total_profit, 2))
st.metric(label="Overall Profit Margin", value=f"{round(overall_profit_margin, 2)}%", delta=f"{round(profit_margin_delta)}%")
