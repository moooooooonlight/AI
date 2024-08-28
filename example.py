import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns



st.title("Matplotlib and Seaborn Plots")

@st.cache_data
def load_data():
    iris = sns.load_dataset('iris')
    return iris

st.code("""
# data loading
@st.cache_data # caching data

def load_data():
    iris = sns.load_dataset('iris')
    return iris
""")
        
st.code("""
iris = load_data()

st.write(iris)

fig, ax = plt.subplots()
ax.scatter(iris['sepal_length'], iris['sepal_width'])
ax.set_xlabel('Sepal Length')
ax.set_ylabel('Sepal Width')
st.pyplot(fig)

fig =  sns.pairplot(data=iris, hue='species')
st.pyplot(fig)

fig, ax = plt.subplots()
sns.boxplot(data=iris, x='species', y='petal_length')
st.pyplot(fig)
""")

iris = load_data()

st.write(iris)

fig, ax = plt.subplots()
ax.scatter(iris['sepal_length'], iris['sepal_width'])
ax.set_xlabel('Sepal Length')
ax.set_ylabel('Sepal Width')
st.pyplot(fig)

fig =  sns.pairplot(data=iris, hue='species')
st.pyplot(fig)

fig, ax = plt.subplots()
sns.boxplot(data=iris, x='species', y='petal_length')
st.pyplot(fig)