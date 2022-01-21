import streamlit as st
import pandas as pd
st.title('Budget Buddy 💰')
st.metric("Current Account", "Rm15,000", "-RM2,500")

col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("Food")
    st.image("https://static.streamlit.io/examples/cat.jpg")

with col2:
    st.header("Entertainment")
    st.image("https://static.streamlit.io/examples/dog.jpg")

with col3:
    st.header("E-wallet")
    st.image("https://static.streamlit.io/examples/owl.jpg")
# col2.metric("Wind", "9 mph", "-8%")
# col3.metric("Humidity", "86%", "4%")
df= pd.read_csv("sample_creditcard_txn.csv")
print(df.head)
df['TRANSACTION_DATE'] = pd.to_datetime(df['TRANSACTION_DATE'], errors='coerce')

df2 = df[df['TRANSACTION_DATE'].dt.month == 11]
print(df2.head)
