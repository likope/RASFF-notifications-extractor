import json

#function to load the filter configuration from a JSON file

def load_config(path="config/filters.json") -> dict:
    """Load the filter configuration from a JSON file."""
    try:
        with open(path, "r") as file:                                                               #open the specified JSON file for reading
            config = json.load(file)                                                                #configuration is loaded as a dictionary from the JSON file
            return config                                                                           #return the loaded configuration as a dictionary
    except FileNotFoundError:
        print(f"Configuration file not found at {path}. Please check the path and try again.")      #if the specified JSON file is not found, print an error message and return an empty dictionary
        return {}


#function to check if a notification matches the specified filters in the configuration and return a list of filtered notifications

def match_filters(notifications: list, config: dict):
    """Check if a notification matches the specified filters in the configuration."""
    filtered = []                                                                                         
    risk_levels = config.get("risk_levels", [])                                                     #get the filters from the configuration file
    product_categories = config.get("product_categories", [])
    origin_countries = config.get("origin_countries", [])
    keywords = config.get("keywords", [])
    for n in notifications:
        risk = n["riskDecision"]["description"]                                                     #extract relevant information from the notification
        category = n["productCategory"]["description"]
        origins = [c["isoCode"] for c in n["originCountries"]]
        subject = n["subject"].lower()
        risk_match = risk in risk_levels if risk_levels else False
        category_match = category in product_categories if product_categories else False
        country_match = any(o in origin_countries for o in origins) if origin_countries else False
        keyword_match = any(kw in subject for kw in keywords) if keywords else False
        if risk_match or country_match or category_match or keyword_match:                          #if any of the filters match, add the notification to the filtered list
            filtered.append(n)
    return filtered


if __name__ == "__main__":
    from fetcher import fetch_notifications

    print("=== Test Filter RASFF ===\n")
    config = load_config()
    notifications = fetch_notifications(max_pages=1, per_page=25)
    print(f"Fetched {len(notifications)} notifications\n")
    
    filtered = match_filters(notifications, config)
    print(f"Filtered: {len(filtered)} match\n")
    
    for n in filtered:
        print(f"  [{n['reference']}] {n['subject']}")
        print(f"    Risk: {n['riskDecision']['description']}")
        print()