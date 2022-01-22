from calendar import month_name
import calendar
import streamlit as st
# import pandas as pd
# library
import matplotlib.pyplot as plt
import streamlit.components.v1 as components

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

page = st.sidebar.selectbox(
    "Navigation",
    ("Accounts", "Expenses","Forecasts")
)



st.title('Budget Buddy 💰')
if page=="Accounts":

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Income This Month", "RM5689", "8.8%")
    with col2:
        st.metric("Expenses This Month", "RM3245", "8.1%",delta_color="inverse")
    with col3:
        st.metric("Net Saving This Month", "RM2444", "2%")

currentIncome=5689
averageMYFood = 1200
averageMYTransport = 300
averageMYInsurance = 400
averageGrocery= 500
if page=="Expenses":

    # month = st.number_input('Choose month',1,12)

    col1, col2 = st.columns(2)

    #donut chart of budget for food vs income
    with col1:
        st.subheader("Food 🍔")
        foodBudget = st.slider(
        'Select new target budget for Food',
        0, currentIncome,1000,help="The maximum budget you can choose is based on your current income")
        figure,ax= donutGenerator(foodBudget,currentIncome,'#5DADE2', '#515A5A')
        st.pyplot(figure)
        if foodBudget>averageMYFood:
            balance= foodBudget-averageMYFood
            st.warning("⚠️ Looks like your spending RM" + str(balance)+" more than your average Malaysian")

    with col2:
        st.subheader("Transport 🚗")
        transportBudget = st.slider(
        'Select new target budget for Transport',
        0, currentIncome,500)
        figure2,ax2= donutGenerator(transportBudget,currentIncome,'#FFC0CB', '#515A5A')
        st.pyplot(figure2)
        if transportBudget>averageMYTransport:
            balance= transportBudget-averageMYTransport
            st.warning("⚠️ Looks like your spending RM" + str(balance)+" more than your average Malaysian")

    col3,col4 = st.columns(2)

    with col3:
        st.subheader("Grocery 🛒")
        groceryBudget= st.slider(
        'Select new target budget for Grocery',
        0, currentIncome,0)
        figure3,ax3= donutGenerator(groceryBudget,currentIncome,'#77dd77', '#515A5A')
        st.pyplot(figure3)
        if groceryBudget>averageGrocery:
            balance= groceryBudget-averageGrocery
            st.warning("⚠️ Looks like your spending RM" + str(balance)+" more than your average Malaysian")
    with col4:
        st.subheader("Insurance 💊")
        insuranceBudget= st.slider(
        'Select new target budget for Insurance',
        0, currentIncome,200)
        figure4,ax4= donutGenerator(insuranceBudget,currentIncome,'#FDFD96', '#515A5A')
        st.pyplot(figure4)
        if insuranceBudget>averageMYInsurance:
            balance= insuranceBudget-averageMYInsurance
            st.warning("⚠️ Looks like your spending RM" + str(balance)+" more than your average Malaysian")
        
if page=="Forecasts":
    st.header("Forecasts 📈")
    col1, col2 = st.columns(2)
    with col1:
        components.iframe("https://docs.google.com/spreadsheets/d/e/2PACX-1vTeh-OmritLrP4YuPMuk3SveyAetRPrC3DmvLzeZ3EUfivTd2h_2FUZbVCXhZEfHT3GPgDPmr3Wn3n3/pubchart?oid=1766636204&amp;format=interactive",width=401,height=371, scrolling=False)   
    with col2:
        components.iframe("https://docs.google.com/spreadsheets/d/e/2PACX-1vTeh-OmritLrP4YuPMuk3SveyAetRPrC3DmvLzeZ3EUfivTd2h_2FUZbVCXhZEfHT3GPgDPmr3Wn3n3/pubchart?oid=572396902&amp;format=interactive",width=401,height=371, scrolling=False)


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

