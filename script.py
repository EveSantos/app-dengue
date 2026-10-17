"""
# My first app
Here's our first attempt at using data to create a table:
"""

import streamlit as st
import pandas as pd

import numpy as np

dataframe = np.random.randn(10, 20)
st.dataframe(dataframe)
