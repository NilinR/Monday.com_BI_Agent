import requests
import json

# --- CONFIGURATION ---
API_TOKEN = "eyJhbGciOiJIUzI1NiJ9.eyJ0aWQiOjY4NDg2MTM4MywiYWFpIjoxMSwidWlkIjoxMTA0NzEzOTEsImlhZCI6IjIwMjYtMDctMjFUMDg6NDQ6MjIuNjYyWiIsInBlciI6Im1lOndyaXRlIiwiYWN0aWQiOjM2MTMxMzU5LCJyZ24iOiJhcHNlMiJ9.dBqrnfNNtzp4fAL16bU7fC8dCpZeHpO_j1AhBKVQOBI"
DEALS_BOARD_ID = 5030093635  # Replace with your actual Deals Board ID
WORK_ORDERS_BOARD_ID = 5030093942 # Replace with your actual Work Orders Board ID

HEADERS = {
    "Authorization": API_TOKEN,
    "API-Version": "2024-01",
    "Content-Type": "application/json"
}
URL = "https://api.monday.com/v2"

def fetch_board_data(board_id):
    """Fetches the first 100 items from a given board to test the connection."""
    
    # GraphQL query using items_page
    query = """
    query ($boardId: [ID!]) {
      boards(ids: $boardId) {
        name
        items_page(limit: 100) {
          items {
            name
            column_values {
              column {
                title
              }
              text
            }
          }
        }
      }
    }
    """
    
    variables = {
        "boardId": [board_id]
    }
    
    payload = {
        "query": query,
        "variables": variables
    }
    
    response = requests.post(URL, json=payload, headers=HEADERS)
    
    if response.status_code == 200:
        return response.json()
    else:
        return f"Error {response.status_code}: {response.text}"

def clean_monday_data(raw_json):
    """Flattens the deeply nested GraphQL JSON into a clean list of dictionaries."""
    cleaned_items = []
    
    try:
        # Navigate the standard monday.com GraphQL response structure
        items = raw_json['data']['boards'][0]['items_page']['items']
    except (KeyError, IndexError, TypeError):
        print("Warning: Unexpected JSON structure or empty board.")
        return []

    for item in items:
        # Start the dictionary with the primary item name
        row_data = {"Item Name": item.get('name', 'Unknown')}
        
        # Flatten the dynamic column values
        for col in item.get('column_values', []):
            # Extract the actual column title and its text value
            title = col['column']['title']
            raw_text = col.get('text')
            
            # Data Resilience: Handle messy, missing, or null data gracefully
            if raw_text is None or raw_text == "" or raw_text.lower() == "null":
                row_data[title] = "Unknown" 
            else:
                row_data[title] = raw_text
                
        cleaned_items.append(row_data)
        
    return cleaned_items

# --- RUN THE TEST ---
if __name__ == "__main__":
    print("Fetching raw Deals Data...\n")
    raw_deals = fetch_board_data(DEALS_BOARD_ID)
    
    print("Cleaning Deals Data...\n")
    cleaned_deals = clean_monday_data(raw_deals)
    
    # Print the first 2 cleaned items to verify the flattening worked
    print(json.dumps(cleaned_deals[:2], indent=2))