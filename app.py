import streamlit as st
st.title("Dependency Check")

def check(label, code):
    try:
        exec(code, {})
        st.success(f"{label} import OK")
    except Exception as e:
        st.error(f"{label} import FAILED: {e!r}")

check("streamlit", "import streamlit")
check("strictyaml", "import strictyaml")
check("ruamel.yaml", "from ruamel import yaml as _y")
check("snowflake-snowpark-python", "import snowflake.snowpark as _s")
check("snowflake-connector-python", "import snowflake.connector as _c")
