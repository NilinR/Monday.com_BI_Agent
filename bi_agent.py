import json
from openai import OpenAI
import os
from dotenv import load_dotenv

# Import the functions and IDs from your previous script
from monday_api import fetch_board_data, clean_monday_data, DEALS_BOARD_ID, WORK_ORDERS_BOARD_ID

# --- CONFIGURATION ---
load_dotenv()

# We initialize the standard OpenAI client, but point it directly at Gemini's servers
client = OpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/" 
) 

def get_founder_insight(user_question):
    print("Fetching real-time data from monday.com...")
    
    deals_data = clean_monday_data(fetch_board_data(DEALS_BOARD_ID))
    work_orders_data = clean_monday_data(fetch_board_data(WORK_ORDERS_BOARD_ID))
    
    system_prompt = f"""
    You are an expert Business Intelligence AI Agent for Skylark Drones.
    Your job is to answer founder-level business questions using the provided monday.com data.
    
    RULES FOR RESPONSES:
    1. LEAD WITH THE ANSWER: If asked for a calculation, metric, or sector breakdown, state the exact number or present the clean table immediately in the first sentence. Do not start with warnings or disclaimers.
    2. CONCRETE INSIGHTS: Provide professional analysis, clear breakdowns, and commercially focused recommendations.
    3. CAVEATS AT THE END: If there are missing values, "Unknown" fields, or data quality issues that affect the calculation, always place them in a dedicated "Data Quality Notes & Caveats" section at the very end of your response, explaining briefly how they impact the figures.
    4. TONE: Confident, concise, analytical, and authoritative.

    DATA CONTEXT:
    --- DEALS BOARD ---
    {json.dumps(deals_data)}
    
    --- WORK ORDERS BOARD ---
    {json.dumps(work_orders_data)}
    """

    print("Analyzing data and generating insights...\n")
    
    response = client.chat.completions.create(
        model="gemini-3.1-flash-lite", # Swapped to the Lite model to bypass high demand
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_question}
        ],
        temperature=0.2 
    )
    
    return response.choices[0].message.content

# --- RUN THE TEST ---
if __name__ == "__main__":
    test_question = "How many deals are currently in the 'Open' status, and what is their total value? Are there any data quality issues I should know about?"
    
    answer = get_founder_insight(test_question)
    print("========== AGENT RESPONSE ==========")
    print(answer)