import streamlit as st
import google.generativeai as genai
from utils import load_csv_data, load_prompt

# load config
model_name = "gemini-2.5-flash-lite"
api_key = st.secrets["GOOGLE_API_KEY"]
genai.configure(api_key=api_key)

# load data and prompt
beer_data = load_csv_data("beers.csv").drop(columns=["Product Image"], errors="ignore")
beer_prompt = load_prompt("beer_prompt_v1.md")


def create_sidebar():
    with st.sidebar:
        st.markdown(
            """
            <style>
                /* Collapse button (inside sidebar) */
                [data-testid="stSidebarCollapseButton"] [data-testid="stIconMaterial"] {
                    opacity: 0 !important;
                }
                [data-testid="stSidebarCollapseButton"] button {
                    position: relative;
                    min-width: 80px;
                    padding: 0 8px;
                }
                [data-testid="stSidebarCollapseButton"] button::after {
                    content: "Feedback";
                    font-weight: 500;
                    font-size: 14px;
                    color: #444;
                    position: absolute;
                    left: 50%;
                    top: 50%;
                    transform: translate(-50%, -50%);
                    pointer-events: none;
                    white-space: nowrap;
                }
                /* Expand button (outside sidebar) */
                [data-testid="stExpandSidebarButton"] [data-testid="stIconMaterial"] {
                    opacity: 0 !important;
                }
                [data-testid="stExpandSidebarButton"] button {
                    position: relative;
                    min-width: 80px;
                    height: 36px;
                    background: #fff;
                    border: 1px solid #ccc;
                    border-radius: 6px;
                    padding: 0 8px;
                }
                [data-testid="stExpandSidebarButton"] button::after {
                    content: "Feedback";
                    font-weight: 500;
                    font-size: 14px;
                    color: #444;
                    position: absolute;
                    left: 50%;
                    top: 50%;
                    transform: translate(-50%, -50%);
                    pointer-events: none;
                    white-space: nowrap;
                }
            </style>
            """,
            unsafe_allow_html=True
        )
        # st.expander("Feedback & Contacts", expanded=True)
        st.image("logo.jpg", use_container_width=True)

        st.divider()

        st.subheader("Our contacts:")
        st.markdown("**[Our website](https://www.valhalla-beer.cz/)**")
        st.markdown("**[Instagram](https://www.instagram.com/valhalla_beer_club30/)**")
        st.markdown("[lucerna@valhalla-beer.cz](mailto:lucerna@valhalla-beer.cz)")

        st.divider()

        st.subheader("Our Team:")
        st.write("**Finn:** Beer Jarl")
        st.write("**John:** Beer Viking")
        st.write("**Anna:** Beer Valkyrie")

        st.divider()

        st.markdown("📝 **[Submit Feedback](https://docs.google.com/forms/u/1/d/e/1FAIpQLSeBKl46W85lykhEDy4HQtEdpUoRKg1LcBjidLKZVbhrySy16g/viewform?usp=header)**")


def main():

    st.set_page_config(page_title="Valhalla Beer Club", page_icon="🍺")
    create_sidebar()

    st.title("🍺 Valhalla Beer Chat")
    st.caption("⚠️ This app is a prototype and things may change in the future")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    # chat
    if beer_data is not None and beer_prompt is not None:

        for message in st.session_state.messages:
            with st.chat_message(message["role"]): st.markdown(message["content"])

        if prompt := st.chat_input("Ask away and we'll find you a good pint!"):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"): st.markdown(prompt)

            with st.chat_message("assistant"):
                with st.spinner("Finding the perfect pint for you..."):
                    try:
                        model = genai.GenerativeModel(model_name)
                        beer_data_json = beer_data.to_json(orient="records", lines=True)
                        full_prompt = f"""
{beer_prompt}
Available beers:{beer_data_json}
User input: {prompt}
Provide beer recommendation based on the user input and available beer data.
Always stick to the beer topic. Adapt to user language and respond in it.
"""

                        response = model.generate_content(full_prompt)
                        response_text = response.text
                        st.markdown(response_text)
                        st.session_state.messages.append({"role": "assistant", "content": response_text})

                    except Exception as e:
                        error_message = f"Error generating recommendation: {str(e)}"
                        st.error(error_message)
                        st.session_state.messages.append({"role": "assistant", "content": error_message})


if __name__ == "__main__":
    main()