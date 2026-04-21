#import of necessary libreries

import requests
from typing import Optional


#dichiaration of the endpoint for the RASFF API

endpoint = "https://webgate.ec.europa.eu/rasff-window/backend/public/notification/search/consolidated/en/" #endpoint for the notifications


#function to build the payload

def build_payload(
    page: int = 1,                                                  #default page number
    page_size: int = 25,                                            #default number of items per page
    subject: Optional[str] = None,                                  #subject of the notification
    origin_country: Optional[str] = None,                           #country of origin of the product
    risk_decision: Optional[str] = None,                            #decision regarding the risk associated with the notification
    product_category: Optional[str] = None,                         #category of the product associated with the notification
    hazard_category: Optional[str] = None,                          #category of the hazard associated with the notification
    notification_classification: Optional[str] = None,) -> dict:
    """Build the JSON payload for the RASFF search API"""
    
    return {
        "parameters": {"pageNumber": page, "itemsPerPage": page_size},
        "subject": subject,
        "originCountry": origin_country,
        "notificationReference": None,
        "notificationType": None,
        "notificationClassification": notification_classification,
        "notificationStatus": None,
        "notificationBasis": None,
        "riskDecision": risk_decision,
        "productCategory": product_category,
        "notifyingCountry": None,
        "distributionCountry": None,
        "hazardCategory": hazard_category,
        "actionTaken": None
    }

#function to send a POST request to the RASFF API with the specified payload and return the response data

def fetch_data(payload: dict) -> dict:
    """Send a POST request to the RASFF API with the specified payload and return the response data."""
    try:
        response = requests.post(endpoint, json=payload, timeout=30)    #make a POST request to the RASFF API with the specified payload and a timeout of 30 seconds
        response.raise_for_status()                                     #verify that the request was successful
        data = response.json() 
        return data                                                     #return the response data as a dictionary
    except requests.exceptions.RequestException as e:                   #if there is an error during the request, print the error message and return an empty list
        print(f"Error during the request: {e}")
        return {}

#function to extract data from notifications and return a list of dictionaries with relevant information

def fetch_notifications(max_pages=1, per_page=25, **filters):                                               #**filters allows to pass any number of keyword arguments as filters for the notifications
    """Extract data from notifications and return a list of dictionaries with relevant information."""
    notifications_total = []
    for page in range(1, max_pages + 1):
        payload = build_payload(page=page, page_size=per_page, **filters)                                   #build a payload for the current page and the specified filters
        data = fetch_data(payload)                                                                          #make a POST request to the RASFF API with the built payload and get the response data
        notifications = data.get("notifications", [])                                                       #extract the list of notifications from the response data, or return an empty list if there are no notifications
        if not notifications:                                                                               #if there are no notifications to extract, break the loop
            break
        notifications_total.extend(notifications)                                                           #add the extracted notifications to the total list
    return notifications_total                                                                              #return the total list of extracted notifications.

#main function to test the fetcher

if __name__ == "__main__":
    print("=== Test Fetcher RASFF ===\n")
    results = fetch_notifications(max_pages=1, per_page=5)
    print(f"Ricevute {len(results)} notifiche.\n")
    for n in results:
        print(f"  [{n['reference']}] {n['subject']}")
        print(f"    Rischio: {n['riskDecision']['description']}")
        print()