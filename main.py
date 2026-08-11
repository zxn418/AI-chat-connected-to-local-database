import os
import pandas as pd
import pandasai as pai
import pyodbc
import streamlit as st
from pandasai import Agent
from dotenv import load_dotenv
from pandasai_litellm.litellm import LiteLLM


st.set_page_config(
    page_title="PandasAI SQL Query",
    page_icon="🤖",
    layout="wide",
)

st.title("AI Query Assistant")

load_dotenv()


# --------------------------------------------------
# PandasAI LLM configuration
# --------------------------------------------------
llm = LiteLLM(
    model="gpt-4o",
    api_key=os.getenv("OPENAI_API_KEY"),
)

pai.config.set({
    "llm": llm,
})


# --------------------------------------------------
# Load SQL Server data
# --------------------------------------------------
@st.cache_data(ttl=6000, show_spinner="Loading service request data...")
def load_food_items():
    server = os.getenv("DB_SERVER")
    database = os.getenv("DB_DATABASE")
    username = os.getenv("DB_USERNAME")
    password = os.getenv("DB_PASSWORD")

    connection_string = (
        "DRIVER={ODBC Driver 18 for SQL Server};"
        f"SERVER={server};"
        f"DATABASE={database};"
        f"UID={username};"
        f"PWD={password};"
        "Encrypt=yes;"
        "TrustServerCertificate=yes;"
    )

    query = "SELECT * FROM dbo.FoodItem;"

    with pyodbc.connect(connection_string) as connection:
        return pd.read_sql_query(
            sql=query,
            con=connection,
            #params=(start_date, end_date),
        )

# --------------------------------------------------
# Display PandasAI response
# --------------------------------------------------
def render_response(response):
    response_type = getattr(response, "type", None)
    value = getattr(response, "value", response)

    if response_type == "dataframe":
        st.dataframe(value, use_container_width=True)

    elif response_type == "chart":
        st.image(value)

    elif response_type == "number":
        st.markdown(f"### {value}")

    elif response_type == "string":
        st.markdown(str(value))

    elif isinstance(value, pd.DataFrame):
        st.dataframe(value, use_container_width=True)

    elif isinstance(value, (int, float)):
        st.markdown(f"### {value}")

    elif isinstance(value, str):
        if value.lower().endswith(
            (".png", ".jpg", ".jpeg", ".webp")
        ):
            st.image(value)
        else:
            st.markdown(value)

    else:
        st.write(value)


# --------------------------------------------------
# Application
# --------------------------------------------------
try:
    pandas_df = load_food_items() 

    # Convert normal Pandas DataFrame into PandasAI DataFrame
    dataset = pai.DataFrame(
        pandas_df,
        name="food_items",
        description="Food items data from SQL Server 2022",
    )
    
    agent = Agent(dataset)

    with st.expander("Preview data"):
        st.write(f"Rows loaded: {len(pandas_df):,}")
        st.dataframe(
            pandas_df.head(5),
            use_container_width=True,
        )

except Exception as error:
    st.error(f"Database connection error: {error}")
    st.stop()


prompt = st.chat_input(
    "Ask a question about the food item data"
)

if prompt:
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Analyzing data..."):
            try:
                response = agent.chat(prompt)
                render_response(response)

            except Exception as error:
                st.error(f"An error occurred: {error}")