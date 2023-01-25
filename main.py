import mysql.connector
from st_aggrid import AgGrid, GridOptionsBuilder, JsCode, GridUpdateMode, ColumnsAutoSizeMode
import streamlit as st
import pandas as pd
import numpy as np
from st_aggrid.grid_options_builder import GridOptionsBuilder
import warnings
from js_config import *
warnings.filterwarnings("ignore")

st.set_page_config(layout="wide", page_title="Lithium Battery Comparison", initial_sidebar_state="collapsed")
# if 'sidebar_state' not in st.session_state:
#     st.session_state.sidebar_state = "collapsed"


# hide_menu_style = """
#         <style>
#         #MainMenu {visibility: hidden;}
#         </style>
#         """
# st.markdown(hide_menu_style, unsafe_allow_html=True)

hide = """
<style>
.css-k1ih3n  {
            padding-top: 0rem;
            padding-bottom: 0rem;
            padding-left: 1rem;
            padding-right: 1rem;
</style>
"""
st.markdown(hide, unsafe_allow_html=True)

DB_HOST = st.secrets.db_details.db_host
DB_PORT = st.secrets.db_details.db_port
DB_USERNAME = st.secrets.db_details.db_username
DB_PASSWORD = st.secrets.db_details.db_password
DB_DATABASE = st.secrets.db_details.db_database


mydb = mysql.connector.connect(
  host=DB_HOST,
  port=DB_PORT,
  user=DB_PASSWORD,
  database=DB_DATABASE
)

df_sql_query = pd.read_sql_query('''select * from Batteries''', mydb)
battery_df = pd.DataFrame(df_sql_query)
cost_per_ah_df = battery_df["Cost"] / battery_df["Capacity"]
battery_df.insert(3, "CostPerAH", cost_per_ah_df)


def make_slider(slider_title, filter_column):
    global battery_df
    slider_max = battery_df[filter_column].max().item()
    slider_min = battery_df[filter_column].min().item()
    if not slider_min >= slider_max:
        slider_choice = st.sidebar.slider(slider_title,  value=(slider_min, slider_max), min_value=slider_min, max_value=slider_max, key=filter_column)
        choice_min = slider_choice[0]
        choice_max = slider_choice[1]
        battery_df = battery_df.loc[(battery_df[filter_column] >= choice_min)]
        battery_df = battery_df.loc[(battery_df[filter_column] <= choice_max)]



make_slider("Capacity (AH)", "Capacity")
make_slider("Cost (AH)", "Cost")
st.sidebar.write("Battery Size")
make_slider("Length", "Length")
make_slider("Width", "Width")
make_slider("Height", "Height")




gb = GridOptionsBuilder.from_dataframe(battery_df)
#gb.configure_side_bar()
gb.configure_default_column(groupable=False, value=True, enableRowGroup=False, resizable=True, editable=False, sortable=True)
gb.configure_column("SKU", hide=True)
gb.configure_column("Brand", cellRenderer=brand_cell_renderer, headerTooltip="Click to go to seller URL")
gb.configure_column("CostPerAH", header_name="Cost Per AH", valueGetter=sparkline_data, cellRenderer="agSparklineCellRenderer", cellRendererParams=sparkline_config)
gb.configure_column("Cost", type=["numericColumn", "numberColumnFilter", "customCurrencyFormat"], custom_currency_symbol="$")
gb.configure_column("Notes", headerTooltip="Click to see cell data", onCellClicked=show_notes)
gb.configure_column("Min Charge Temp", maxWidth=135)
gb.configure_column("Max Charge Temp", maxWidth=135)
gb.configure_column("Parallel", maxWidth=100)
gb.configure_column("URL", cellRenderer=url_cell_renderer)

gridOptions = gb.build()


AgGrid(battery_df, gridOptions=gridOptions, columns_auto_size_mode=ColumnsAutoSizeMode.FIT_CONTENTS, width="100%", height=700,
       enable_enterprise_modules=True, allow_unsafe_jscode=True)

