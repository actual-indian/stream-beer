import os
from openai import OpenAI
import json
import streamlit as st

aip_proxy = os.environ.get('это не нужно')
my_api_key = os.environ.get('SvVKRpyeo1EUf2ZY7GaOc6')

client = OpenAI(api_key="SvVKRpyeo1EUf2ZY7GaOc6")

pivis = [
    {"name": "Guinness Draught", "type": "Stout", "abv": "4.2%",
     "description": "Creamy, smooth body with roasted malt and coffee notes"},
    {"name": "Heineken", "type": "Lager", "abv": "5.0%", "description": "Crisp, clean lager with a light bitterness"},
    {"name": "Sierra Nevada Pale Ale", "type": "Pale Ale", "abv": "5.6%",
     "description": "Bold hops with citrus and pine aroma"},
    {"name": "Blue Moon Belgian White", "type": "Witbier", "abv": "5.4%",
     "description": "Smooth wheat beer with hints of orange and coriander"},
    {"name": "Budweiser", "type": "Lager", "abv": "5.0%",
     "description": "Light-bodied lager with subtle malt sweetness"},
    {"name": "Stella Artois", "type": "Pilsner", "abv": "5.2%",
     "description": "Crisp pilsner with a slightly bitter, dry finish"},
    {"name": "Samuel Adams Boston Lager", "type": "Lager", "abv": "5.0%",
     "description": "Balanced malt sweetness with a smooth hop bite"},
    {"name": "Hoegaarden", "type": "Witbier", "abv": "4.9%",
     "description": "Refreshing wheat beer with citrus and spice notes"},
    {"name": "Chimay Blue", "type": "Belgian Strong Ale", "abv": "9.0%",
     "description": "Rich, dark ale with caramel, spice, and dark fruit flavors"},
    {"name": "Pilsner Urquell", "type": "Pilsner", "abv": "4.4%",
     "description": "Classic Czech pilsner with a crisp, floral hop taste"},
    {"name": "Corona Extra", "type": "Lager", "abv": "4.6%",
     "description": "Light and refreshing with a smooth, mild flavor"},
    {"name": "Weihenstephaner Hefeweissbier", "type": "Hefeweizen", "abv": "5.4%",
     "description": "Banana and clove aromas with a smooth wheat body"},
    {"name": "Dogfish Head 90 Minute IPA", "type": "Imperial IPA", "abv": "9.0%",
     "description": "Strong hop character with rich malt backbone"},
    {"name": "Bass Pale Ale", "type": "Pale Ale", "abv": "5.1%",
     "description": "Balanced caramel malt with earthy English hops"},
    {"name": "Delirium Tremens", "type": "Belgian Strong Ale", "abv": "8.5%",
     "description": "Spicy, fruity ale with a warming finish"},
    {"name": "Lagunitas IPA", "type": "IPA", "abv": "6.2%",
     "description": "Hoppy IPA with floral and citrus zest notes"},
    {"name": "Goose Island Bourbon County Stout", "type": "Imperial Stout", "abv": "14.7%",
     "description": "Thick, rich stout with chocolate, bourbon, and vanilla"},
    {"name": "Paulaner Salvator", "type": "Doppelbock", "abv": "7.9%",
     "description": "Malty and sweet with hints of caramel and toasted bread"},
    {"name": "Newcastle Brown Ale", "type": "Brown Ale", "abv": "4.7%",
     "description": "Smooth brown ale with nutty and caramel flavors"},
    {"name": "Founders All Day IPA", "type": "Session IPA", "abv": "4.7%",
     "description": "Light-bodied, refreshing IPA with citrusy hops"}
]

pivis_json_str = json.dumps(pivis, indent=2)
beer_lookup = {beer["name"]: beer for beer in pivis}


def get_beer_recommendation(prompt_to_send):
    try:
        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": """You are a beer tasting expert. Your goal is to provide beer recommendations in a structured JSON format.
                - Only support conversations about beer.
                - If the user asks about something other than beer, respond with: {"error": "I am a beer assistant and cannot help with that."}
                - If you cannot find a good match in the provided list, respond with an empty list: {"recommendations": []}
                - Otherwise, respond with a JSON object containing a 'recommendations' key. This key should hold a list of 1-2 recommended beers.
                - Each item in the list must have two keys: 'name' (the exact name from the provided list) and 'reason' (a concise explanation of why it's a good match).
                """},
                {"role": "user", "content": prompt_to_send}
            ],
            temperature=0.2,
        )

        recommendation_data = json.loads(response.choices[0].message.content)
        return recommendation_data

    except Exception as e:
        return {"error": f"An error occurred: {e}"}



st.title("🍺 Beer Recommendation App")
st.write("Tell me what you're in the mood for, and I'll suggest a beer from our list!")

user_request = st.text_input(
    "What are you up to today? (e.g., 'a hot day by the pool', 'something strong and dark for a cold night', 'a classic hoppy ale')",
    key="beer_input"
)

prompt = f"""
A user wants a beer recommendation. Their request is: "{user_request}"

Based on this request, recommend 1-2 beers from the following JSON list.
For each recommendation, provide the beer's 'name' and a 'reason' for the choice.
Only recommend beers that exist on this list.

Available beers:
{pivis_json_str}
"""

if st.button("Get Recommendations"):
    if user_request:
        with st.spinner("Finding the perfect pint..."):
            result = get_beer_recommendation(prompt)

            if "error" in result:
                st.error(result["error"])
            elif "recommendations" in result and not result["recommendations"]:
                st.warning(
                    "Sorry, I couldn't find a perfect match in our list for your request. Please try describing your preference differently.")
            elif "recommendations" in result:
                st.success("Here are your recommendations!")

                for rec in result["recommendations"]:
                    beer_details = beer_lookup.get(rec["name"])

                    if beer_details:
                        with st.container(border=True):
                            st.subheader(beer_details["name"])

                            col1, col2 = st.columns(2)
                            with col1:
                                st.write(f"**Type:** {beer_details['type']}")
                            with col2:
                                st.write(f"**ABV:** {beer_details['abv']}")

                            st.write(f"*{beer_details['description']}*")

                            st.divider()
                            st.markdown(f"**Why it's a good match:** {rec['reason']}")
                    else:
                        st.warning(f"Could not find details for recommended beer: {rec['name']}")

    else:
        st.warning("Please tell me what you're looking for in a beer.")