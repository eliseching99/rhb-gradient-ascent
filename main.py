from calendar import month_name
import calendar
from email.mime import base
import streamlit as st
# import pandas as pd
# library
import matplotlib.pyplot as plt
import streamlit.components.v1 as components

from gsheetsdb import connect

# Create a connection object.
conn = connect()

# Perform SQL query on the Google Sheet.
# Uses st.cache to only rerun when the query changes or after 10 min.
@st.cache(ttl=15)
def run_query(query):
    rows = conn.execute(query, headers=1)
    return rows

sheet_url = st.secrets["public_gsheets_url"]
rows = run_query(f'SELECT * FROM "{sheet_url}"')

for row in rows:
    if row.category=="Food":
        foodExpense= row.amount
    if row.category=="Transport":
        transportExpense= row.amount
    if row.category=="Insurance":
        insuranceExpense= row.amount
    if row.category=="Grocery":
        groceryExpense= row.amount

def donutGenerator(target,income,color1,color2):
    budgetPercentage=target/income*100
    leftOverPercentage = 100-budgetPercentage
    fig, ax = plt.subplots(figsize=(6, 6))
    wedgeprops = {'width':0.3, 'edgecolor':'black', 'linewidth':3}
    ax.pie([budgetPercentage,leftOverPercentage], wedgeprops=wedgeprops, startangle=90, colors=[color1, color2])
    budgetStr = str(int(budgetPercentage))
    targetStr= "RM"+str(target)
    incomeStr= "RM"+str(income)
    outputStr= targetStr+"/"+incomeStr
    plt.text(0, 0, budgetStr+"%", ha='center', va='center', fontsize=42)
    # place a text box in upper left in axes coords
    ax.text(0.35, 0.05, outputStr, transform=ax.transAxes, fontsize=14,
            verticalalignment='top')
    # plt.text(0, 50, , ha='center', va='center', fontsize=10)

    return fig,ax 

def donutGeneratorOverBudget(target,income,color1,color2):
    budgetPercentage=target/income*100
    leftOverPercentage = 100-budgetPercentage
    fig, ax = plt.subplots(figsize=(6, 6))
    wedgeprops = {'width':0.3, 'edgecolor':'black', 'linewidth':3}
    ax.pie([100,0], wedgeprops=wedgeprops, startangle=90, colors=[color1, color2])
    budgetStr = str(int(budgetPercentage))
    targetStr= "RM"+str(target)
    incomeStr= "RM"+str(income)
    outputStr= targetStr+"/"+incomeStr
    plt.text(0, 0, budgetStr+"%", ha='center', va='center', fontsize=42,color="red")
    # place a text box in upper left in axes coords
    ax.text(0.35, 0.05, outputStr, transform=ax.transAxes, fontsize=14,
            verticalalignment='top')
    # plt.text(0, 50, , ha='center', va='center', fontsize=10)

    return fig,ax 

st.sidebar.image("rhbpic.png", use_column_width=True)
page = st.sidebar.selectbox(
    "Navigation",
    ("Accounts", "Expenses")
)
st.title('Budget Buddy 💰')
if page=="Accounts":
    st.header("Financial Performance")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Income This Month", "RM7230", "222.7%")
    with col2:
        st.metric("Expenses This Month", "RM3901", "2.8%",delta_color="inverse")
    with col3:
        st.metric("CA/SA Growth", "RM3329", "313%")
    st.header("Net Worth")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("CASA Balance", "RM4,109")
    with col2:
        st.metric("CC Balance", "0")
    with col3:
        st.metric("Net Worth", "RM4109")

    st.header("Forecasts 📈")
    col1, col2 = st.columns(2)
    with col1:
        components.iframe("https://docs.google.com/spreadsheets/d/e/2PACX-1vTeh-OmritLrP4YuPMuk3SveyAetRPrC3DmvLzeZ3EUfivTd2h_2FUZbVCXhZEfHT3GPgDPmr3Wn3n3/pubchart?oid=1766636204&amp;format=interactive",width=500,height=371, scrolling=True)   
    with col2:
        components.iframe("https://docs.google.com/spreadsheets/d/e/2PACX-1vTeh-OmritLrP4YuPMuk3SveyAetRPrC3DmvLzeZ3EUfivTd2h_2FUZbVCXhZEfHT3GPgDPmr3Wn3n3/pubchart?oid=572396902&amp;format=interactive",width=500,height=371, scrolling=True)

currentIncome=7230
averageMYFood = 2500
averageMYTransport = 400
averageMYInsurance = 400
averageGrocery= 800
if page=="Expenses":
    with st.expander("Change Current Budget"):

    # month = st.number_input('Choose month',1,12)

        col1, col2 = st.columns(2)

        #donut chart of current spending vs target budget
        with col1:
            st.subheader("Food 🍔")
            foodBudget = st.slider(
            'Select new target budget for Food',
            0, currentIncome,3000,help="The maximum budget you can choose is based on your current income")
            if foodExpense>foodBudget:
                figure,ax=donutGeneratorOverBudget(foodExpense,foodBudget,'#5DADE2', '#515A5A')
            else:
                figure,ax= donutGenerator(foodExpense,foodBudget,'#5DADE2', '#515A5A')
            st.pyplot(figure)
            
            if foodBudget>averageMYFood:
                balance= foodBudget-averageMYFood
                st.warning("⚠️ Looks like your spending RM" + str(balance)+" more than your average Malaysian")
            if foodExpense>foodBudget:
                balance= foodExpense-foodBudget
                st.warning("⚠️ Looks like your spending RM" + str(balance)+" more than your target budget")

        with col2:
            st.subheader("Transport 🚗")
            transportBudget = st.slider(
            'Select new target budget for Transport',
            0, currentIncome,700)
            if transportExpense>transportBudget:
                figure2,ax2= donutGeneratorOverBudget(transportExpense,transportBudget,'#FFC0CB', '#515A5A')
            else:
                figure2,ax2= donutGenerator(transportExpense,transportBudget,'#FFC0CB', '#515A5A')
            st.pyplot(figure2)
            if transportBudget>averageMYTransport:
                balance= transportBudget-averageMYTransport
                st.warning("⚠️ Looks like your spending RM" + str(balance)+" more than your average Malaysian")
            if transportExpense>transportBudget:
                balance= transportExpense-transportBudget
                st.warning("⚠️ Looks like your spending RM" + str(balance)+" more than your target budget")


        col3,col4 = st.columns(2)

        with col3:
            st.subheader("Grocery 🛒")
            groceryBudget= st.slider(
            'Select new target budget for Grocery',
            0, currentIncome,500)
            if groceryExpense>groceryBudget:
                figure3,ax3= donutGeneratorOverBudget(groceryExpense,groceryBudget,'#77dd77', '#515A5A')
            else:
                figure3,ax3= donutGenerator(groceryExpense,groceryBudget,'#77dd77', '#515A5A')
            st.pyplot(figure3)
            if groceryBudget>averageGrocery:
                balance= groceryBudget-averageGrocery
                st.warning("⚠️ Looks like your spending RM" + str(balance)+" more than your average Malaysian")
            if groceryExpense>groceryBudget:
                balance= groceryExpense-groceryBudget
                st.warning("⚠️ Looks like your spending RM" + str(balance)+" more than your target budget")

        with col4:
            st.subheader("Insurance 💊")
            insuranceBudget= st.slider(
            'Select new target budget for Insurance',
            0, currentIncome,700)
            if insuranceExpense>insuranceBudget:
                figure4,ax4= donutGeneratorOverBudget(insuranceExpense,insuranceBudget,'#FDFD96', '#515A5A')
            else:
                figure4,ax4= donutGenerator(insuranceExpense,insuranceBudget,'#FDFD96', '#515A5A')
            st.pyplot(figure4)
            if insuranceBudget>averageMYInsurance:
                balance= insuranceBudget-averageMYInsurance
                st.warning("⚠️ Looks like your spending RM" + str(balance)+" more than your average Malaysian")
            if insuranceExpense>insuranceBudget:
                balance= insuranceExpense-insuranceBudget
                st.warning("⚠️ Looks like your spending RM" + str(balance)+" more than your target budget")
    st.header("My Budget")
    fig, ax = plt.subplots(figsize=(6, 6))
    wedgeprops = {'width':0.3, 'edgecolor':'black', 'linewidth':3}
    names=["Food","Transport","Grocery","Insurance","Savings"]
    disposableIncome=currentIncome-foodBudget-transportBudget-groceryBudget-insuranceBudget
    totalExpenses= foodBudget+transportBudget+groceryBudget+insuranceBudget
    proportionExpenses= str(int(totalExpenses/currentIncome*100))
    outputStr= "RM"+str(totalExpenses)+"/"+"RM"+str(currentIncome)
    # explosion
    explode = (0.0, 0.00, 0.00, 0.00, 0.1)
    ax.pie([foodBudget,transportBudget,groceryBudget,insuranceBudget,disposableIncome],explode=explode,labels=names,autopct='%1.1f%%', wedgeprops=wedgeprops, startangle=90, colors=["#5DADE2",'#FFC0CB','#77dd77','#515A5A','#FDFD96'])
    plt.text(0, 0, proportionExpenses+"%", ha='center', va='center', fontsize=42)
    ax.text(0.35, -0.05, outputStr, transform=ax.transAxes, fontsize=14,
            verticalalignment='top')
    st.pyplot(fig)
    savingsSurplus= disposableIncome/currentIncome *100
    baselineForFDSuggestion=30
    if savingsSurplus>baselineForFDSuggestion:
        st.success("You have more than "+str(baselineForFDSuggestion)+"% of savings. Grow your money by using RHB's Fixed Deposit Plan")
        link = '[Know More](https://www.rhbgroup.com/238/index.html?utm_source=carousel_banner&utm_medium=carousel_banner&utm_campaign=RHBTD)'
        st.markdown(link, unsafe_allow_html=True)

# df= pd.read_csv("sample_creditcard_txn.csv")
# df['TRANSACTION_DATE'] = pd.to_datetime(df['TRANSACTION_DATE'], errors='coerce')

# ## Getting a particular customer info
# ## Get total amount of expenditure per month
# customerRecords=df[df['cust_number'] == 46]
# customerRecords= customerRecords[customerRecords['TRANSACTION_DATE'].dt.year == 2021]
# monthSpecificCustomerRecords = customerRecords[customerRecords['TRANSACTION_DATE'].dt.month == month]
# st.dataframe(monthSpecificCustomerRecords)
# #get total expenses of the month
# Total = monthSpecificCustomerRecords['TRANSACTION_AMT'].sum()
# st.write("Total Expenses: "+calendar.month_name[month])
# st.write(Total)

# food = monthSpecificCustomerRecords.loc[monthSpecificCustomerRecords['TRAN_DESC_DETAIL'].str.contains("foodpanda|food|mcd|kfc", case=False)]
# st.write("Food expenses")
# st.dataframe(food)
# ewallet= monthSpecificCustomerRecords.loc[monthSpecificCustomerRecords['TRAN_DESC_DETAIL'].str.contains("shopee|grab|boost|bigpay|fave pay|lazada", case=False)]
# st.write("E-wallet expenses")
# st.dataframe(ewallet)

# for i in range (1,13):
#     monthSpecificCustomerRecords= customerRecords[customerRecords['TRANSACTION_DATE'].dt.month == i]
#     total = monthSpecificCustomerRecords['TRANSACTION_AMT'].sum()
#     difference=0
#     if i>1:
#         lastMonthSpecificCustomerRecords= customerRecords[customerRecords['TRANSACTION_DATE'].dt.month == i-1]
#         lastMonthTotal = lastMonthSpecificCustomerRecords['TRANSACTION_AMT'].sum()

#         difference = total-lastMonthTotal
#     st.write("Month:", i, "Total Expenses:",total)
#     st.write("difference between last month: ",difference)


