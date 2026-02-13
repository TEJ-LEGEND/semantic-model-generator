import streamlit as st
from snowflake.connector import DatabaseError
from snowflake.connector.connection import SnowflakeConnection

import pandas as pd

import snowflake.connector

import streamlit as st

st.write("Python OK")

st.write("Pandas:", pd.__version__)

st.write("Snowflake connector:", snowflake.connector.__version__)
 

# set_page_config must be the first Streamlit call
st.set_page_config(layout="wide", page_icon="💬", page_title="Semantic Model Generator")

from app_utils.shared_utils import (
    GeneratorAppScreen,
    get_snowflake_connection,
    set_account_name,
    set_host_name,
    set_sit_query_tag,
    set_snowpark_session,
    set_streamlit_location,
    set_user_name,
)
from semantic_model_generator.snowflake_utils.env_vars import (
    SNOWFLAKE_ACCOUNT_LOCATOR,
    SNOWFLAKE_HOST,
    SNOWFLAKE_USER,
)


# 🔄 UPDATED: Streamlit >=1.37 uses st.dialog (not st.experimental_dialog)
@st.dialog("Connection Error")
def failed_connection_popup() -> None:
    """
    Renders a dialog box when Snowflake connection fails.
    """
    st.markdown(
        """It looks like the credentials provided could not be used to connect to the account."""
    )
    st.stop()


def verify_environment_setup() -> SnowflakeConnection:
    """
    Ensures that environment variables are correctly set and Snowflake connection works.
    """
    try:
        with st.spinner(
            "Validating your connection to Snowflake. If you are using MFA, please check your authenticator app for a push notification."
        ):
            return get_snowflake_connection()
    except DatabaseError:
        failed_connection_popup()


if __name__ == "__main__":
    from journeys import builder, iteration, partner

    st.session_state["sis"] = set_streamlit_location()

    def onboarding_dialog() -> None:
        """
        Renders the initial home screen.
        """

        st.markdown(
            """
            <div style="text-align: center;">
                <h1>Welcome to the Snowflake Semantic Model Generator! ❄️</h1>
                <p>⚠️ The Streamlit app is no longer supported for semantic model creation.</p>
                <p>👉 Use the Snowsight UI in Snowflake to create/update semantic models.</p>
                <p>✅ Return here to run model evaluations — still best done in this app.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown("<div style='margin: 60px;'></div>", unsafe_allow_html=True)

        _, center, _ = st.columns([1, 2, 1])
        with center:
            if st.button(
                "**[⚠️ Deprecated] 🛠 Create a new semantic model**",
                use_container_width=True,
                type="primary",
            ):
                builder.show()

            st.markdown("")

            if st.button(
                "**✏️ Edit an existing semantic model**",
                use_container_width=True,
                type="primary",
            ):
                iteration.show()

            st.markdown("")

            if st.button(
                "**[⚠️ Deprecated] 📦 Start with partner semantic model**",
                use_container_width=True,
                type="primary",
            ):
                set_sit_query_tag(
                    get_snowflake_connection(),
                    vendor="",
                    action="start",
                )
                partner.show()

    conn = verify_environment_setup()
    set_snowpark_session(conn)

    set_account_name(conn, SNOWFLAKE_ACCOUNT_LOCATOR)
    set_host_name(conn, SNOWFLAKE_HOST)
    set_user_name(conn, SNOWFLAKE_USER)

    # Initial page state
    if "page" not in st.session_state:
        st.session_state["page"] = GeneratorAppScreen.ONBOARDING

    # Routing logic
    if st.session_state["page"] == GeneratorAppScreen.ITERATION:
        iteration.show()
    else:
        onboarding_dialog()
