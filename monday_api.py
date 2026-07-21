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

# --- RUN THE TEST ---
if __name__ == "__main__":
    print("Fetching Deals Data...\n")
    deals_data = fetch_board_data(DEALS_BOARD_ID)
    print(json.dumps(deals_data, indent=2))