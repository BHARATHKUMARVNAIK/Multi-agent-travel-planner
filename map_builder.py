
#  Interactive Map

# We want to show all recommended places on a map. The challenge is the itinerary output is just a long text string

# 1) Parse place names from the text using the LLM
# 2) Geocode each place name to get lat/lon
# 3) Plot them on an interactive map using Folium

import folium
import requests
from streamlit_folium import st_folium


def geocode_places(place_name, destination):

    """
    Convert places names into lat/lon using open-meteo geocoding API.
    We can use the destination as a hint to improve accuracy.
    """

    url = "https://geocoding-api.open-meteo.com/v1/search"
    params = {
        "name" : f"{place_name}, {destination}",
        "count" : 1,
        "language" : "en",
    }
    response = requests.get(url, params=params)
    data = response.json()

    if data.get("results"):
        results = data['results'][0]
        return {
            "name" : results['name'],
            "latitude" : results['latitude'],
            "longitude" : results['longitude']
        }
    return None # return None if geocoding fails


def extract_places(itinerary_text):

    """
    Use the LLM to extract place names from the itinerary text.
    We can prompt the LLM to return a list of place names mentioned in the text.
    """

    # Example prompt:
    # "Extract a list of place names mentioned in the following itinerary: {itinerary_text}"
    # The LLM should return something like: ["Eiffel Tower", "Louvre Museum", "Notre-Dame Cathedral"]

    places = [] # replace with LLM output
    keywords = ["Visit", "Stop at","Explore","See","Go To", "Tour", "Check Out"] # example keywords to look for in the text

    for line in itinerary_text.split("\n"):
        for keyword in keywords:
            if keyword.lower() in line.lower():
                # extract the part after the keyword
                parts = line.lower().split(keyword.lower())
                if len(parts) > 1:
                    # clean up the place name — take first 40 chars
                    place = parts[1].strip()[:40]
                    # remove common punctuation
                    place = place.replace(".","").replace(",","").replace(";","")

                    if len(place) > 3: # ignore very short strings
                        places.append(place)

                break # stop checking other keywords for this line

    return list(set(places)) # remove duplicates




def build_map(itinerary_text, destination):

    """Build and return a folium map with all places marked"""
    # Step 1 — get destination center coordinates for map
    center = geocode_places(destination, "")
    if not center:
        return None # return None if we can't geocode the destination
    
    # Step 2 — create folium map centered on destination
    m = folium.Map(
        location = [center['latitude'], center['longitude']],
        zoom_start=12
    )

    # Step 3 — extract places from text
    places = extract_places(itinerary_text)

    # Step 4 — geocode each place and add a marker
    for place in places:
        coords = geocode_places(place, destination)
        if coords:
            folium.Marker(
                location = [coords['latitude'], coords['longitude']],
                popup = coords['name'].title(),
                tooltip= coords['name'].title(),
                icon = folium.Icon(color='blue', icon='info-sign')
            ).add_to(m)

    
    # Step 5 — add a special red marker for the destination itself
    folium.Marker(
        location = [center['latitude'], center['longitude']],
        popup = destination,
        tooltip= f" {destination} (Destination)",
        icon = folium.Icon(color='red', icon='star')
    ).add_to(m)


    return m, len(places)

