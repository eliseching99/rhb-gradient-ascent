import streamlit as st
import pandas as pd
# library
import matplotlib.pyplot as plt

fig, ax = plt.subplots(figsize=(6, 6))
wedgeprops = {'width':0.3, 'edgecolor':'black', 'linewidth':3}
#show number of average vs target
ax.pie([23,73], wedgeprops=wedgeprops, startangle=90, colors=['#5DADE2', '#515A5A'])
plt.text(0, 0, "23%", ha='center', va='center', fontsize=42)

fig2, ax2 = plt.subplots(figsize=(6, 6))
wedgeprops = {'width':0.3, 'edgecolor':'black', 'linewidth':3}
#show number of average vs target
ax2.pie([30,70], wedgeprops=wedgeprops, startangle=90, colors=['#FFC0CB', '#515A5A'])
plt.text(0, 0, "30%", ha='center', va='center', fontsize=42)


fig3, ax3 = plt.subplots(figsize=(6, 6))
wedgeprops = {'width':0.3, 'edgecolor':'black', 'linewidth':3}
#show number of average vs target
ax3.pie([50,50], wedgeprops=wedgeprops, startangle=90, colors=['#77dd77', '#515A5A'])
plt.text(0, 0, "50%", ha='center', va='center', fontsize=42)


st.title('Budget Buddy 💰')
st.metric("Current Account", "Rm15,000", "-RM2,500")
month = st.number_input('Choose month',1,12)

col1, col2 = st.columns(2)

with col1:
    st.subheader("Food")
    st.pyplot(fig)
    with st.expander("Change"):
        foodBudget = st.slider(
        'Select new target budget for Food',
        0, 100,25)

with col2:
    st.subheader("Entertainment")
    st.pyplot(fig2)
    with st.expander("Change"):
        entertainmentBudget = st.slider(
        'Select new target budget for Entertainment',
        0, 100,25)

col3,col4 = st.columns(2)

with col3:
    st.subheader("E-wallet")
    st.pyplot(fig3)
    with st.expander("Change"):
        walletBudget= st.slider(
        'Select new target budget for E Wallet',
        0, 100,25)

df= pd.read_csv("sample_creditcard_txn.csv")
df['TRANSACTION_DATE'] = pd.to_datetime(df['TRANSACTION_DATE'], errors='coerce')

## Getting a particular customer info
customerRecords=df[df['cust_number'] == 6]
print(customerRecords)
customerRecords = customerRecords[customerRecords['TRANSACTION_DATE'].dt.month == 4]
st.dataframe(customerRecords)
