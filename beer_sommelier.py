import streamlit as st
import google.generativeai as genai
from utils import load_data, load_prompt
import pandas as pd

# load config
model_name = "gemini-1.5-flash"
api_key = st.secrets["GOOGLE_API_KEY"]
genai.configure(api_key=api_key)

# load data and prompt
beer_data = load_data("beers.csv")
beer_prompt = load_prompt("beer_prompt.md")


def get_random_beer():
    if beer_data is not None:
        return beer_data.sample(n=2)
    return None


def display_beer_card(beer_row):
    def pretty_display(value, default="Ask Dima for details!"):
        if pd.isna(value) or value == "":
            return default
        return value

    with st.container():
        st.subheader(pretty_display(beer_row['name']))
        st.write(f"**Brewery:** {pretty_display(beer_row.get('brewery'))}")
        st.write(f"**Type:** {pretty_display(beer_row.get('type'))}")
        st.write(f"**ABV/IBU:** {pretty_display(beer_row.get('ABV/IBU'))}")
        st.write(f"**Description:** {pretty_display(beer_row.get('description'))}")
        st.write(f"**URL:** {pretty_display(beer_row.get('url'))}")
        st.write(f"**Other Info:** {pretty_display(beer_row.get('other_info'))}")


def create_sidebar():
    with st.sidebar:
        st.header("🍺 Beer Chat Menu")
        st.subheader("Contacts:")
        st.write("**Email:** loh@peedr.cz")
        st.write("**Instagram:** azaza")

        st.divider()

        st.subheader("Our Team:")
        st.write("**Dima:** Beer lover")
        st.write("**Valentina:** Physics lover")
        st.write("**Simon:** Gay lover")

        st.divider()

        st.markdown("📝 **[Submit Feedback](https://docs.google.com/forms/u/1/d/e/1FAIpQLSeBKl46W85lykhEDy4HQtEdpUoRKg1LcBjidLKZVbhrySy16g/viewform?usp=header)**")


def main():
    st.set_page_config(page_title="The Beer Chat", page_icon="🍺")
    create_sidebar()
    st.title("🍺 The Beer Chat")
    st.markdown("""
    Tell us **what you're after** and we'll recommend you a good pint! Or try the **Random beer** button!
    """)

    if "messages" not in st.session_state:
        st.session_state.messages = []

    if "random_beers" not in st.session_state:
        random_beers = get_random_beer()
        if random_beers is not None:
            st.session_state.random_beers = random_beers

    # chat
    if beer_data is not None and beer_prompt is not None:

        for message in st.session_state.messages:
            with st.chat_message(message["role"]): st.markdown(message["content"])

        if prompt := st.chat_input("Tell us what you want"):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"): st.markdown(prompt)

            with st.chat_message("assistant"):
                with st.spinner("Finding the perfect pint for you..."):
                    try:
                        model = genai.GenerativeModel(model_name)
                        beer_data_str = beer_data.to_string(index=False)
                        full_prompt = f"""
{beer_prompt}
Available beers:{beer_data_str}
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

    # add random beers
    if st.button("Get random 🍺"):
        random_beers = get_random_beer()
        if random_beers is not None:
            st.session_state.random_beers = random_beers

    if "random_beers" in st.session_state:
        col1, col2 = st.columns(2)

        with col1:
            display_beer_card(st.session_state.random_beers.iloc[0])

        with col2:
            display_beer_card(st.session_state.random_beers.iloc[1])

if __name__ == "__main__":
    main()