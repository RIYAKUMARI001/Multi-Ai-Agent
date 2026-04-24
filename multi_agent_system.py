import os
from typing import Annotated, TypedDict, List
from dotenv import load_dotenv

# Import LangChain and LangGraph components
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate
from langgraph.graph import StateGraph, END

# Load environment variables (for GOOGLE_API_KEY)
load_dotenv()

# Define the shared state between agents
class TravelState(TypedDict):
    destination: str
    interests: str
    itinerary: str
    budget: str
    tips: str
    final_report: str
    messages: Annotated[List[BaseMessage], "The messages in the conversation"]

# Global LLM placeholder
_llm = None

def get_llm():
    global _llm
    if _llm is None:
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("GOOGLE_API_KEY not found. Please set it in your .env file.")
        _llm = ChatGoogleGenerativeAI(model="gemini-flash-latest", temperature=0.7)
    return _llm

# --- Agent 1: Travel Planner ---
def planner_node(state: TravelState):
    print("--- TRAVEL PLANNER AGENT ---")
    prompt = ChatPromptTemplate.from_template(
        "You are a world-class Travel Planner. Create a detailed 3-day itinerary for a trip to {destination}. "
        "The traveler is interested in: {interests}. "
        "Focus on the flow of the trip and specific attractions."
    )
    chain = prompt | get_llm()
    response = chain.invoke({"destination": state["destination"], "interests": state["interests"]})
    return {"itinerary": response.content}

# --- Agent 2: Budget Analyst ---
def budget_analyst_node(state: TravelState):
    print("--- BUDGET ANALYST AGENT ---")
    prompt = ChatPromptTemplate.from_template(
        "You are a Budget Travel Analyst. Based on this itinerary for {destination}: \n\n {itinerary} \n\n"
        "Estimate a moderate budget (in USD) for this 3-day trip. Breakdown costs for: "
        "Accommodation, Food, Transportation, and Activities. Provide tips on how to save money."
    )
    chain = prompt | get_llm()
    response = chain.invoke({"destination": state["destination"], "itinerary": state["itinerary"]})
    return {"budget": response.content}

# --- Agent 3: Local Expert ---
def local_expert_node(state: TravelState):
    print("--- LOCAL EXPERT AGENT ---")
    prompt = ChatPromptTemplate.from_template(
        "You are a Local Expert living in {destination}. Look at this itinerary: \n\n {itinerary} \n\n"
        "Provide hidden gems, cultural etiquette, and specific local food recommendations that "
        "align with the traveler's interests: {interests}."
    )
    chain = prompt | get_llm()
    response = chain.invoke({
        "destination": state["destination"], 
        "itinerary": state["itinerary"],
        "interests": state["interests"]
    })
    return {"tips": response.content}

# --- Agent 4: Finalizer (Editor) ---
def finalizer_node(state: TravelState):
    print("--- FINALIZER AGENT ---")
    prompt = ChatPromptTemplate.from_template(
        "You are an Editor. Compile the following information into a beautiful, well-formatted "
        "Markdown travel report for {destination}.\n\n"
        "ITINERARY:\n{itinerary}\n\n"
        "BUDGET ESTIMATE:\n{budget}\n\n"
        "LOCAL TIPS & INSIGHTS:\n{tips}\n\n"
        "Ensure the report is professional, exciting, and easy to read."
    )
    chain = prompt | get_llm()
    response = chain.invoke({
        "destination": state["destination"],
        "itinerary": state["itinerary"],
        "budget": state["budget"],
        "tips": state["tips"]
    })
    return {"final_report": response.content}

# --- Graph Orchestration ---
def build_graph():
    # Define the graph
    workflow = StateGraph(TravelState)

    # Add nodes for each agent
    workflow.add_node("planner", planner_node)
    workflow.add_node("budget_analyst", budget_analyst_node)
    workflow.add_node("local_expert", local_expert_node)
    workflow.add_node("finalizer", finalizer_node)

    # Define edges (Sequential workflow)
    workflow.set_entry_point("planner")
    workflow.add_edge("planner", "budget_analyst")
    workflow.add_edge("budget_analyst", "local_expert")
    workflow.add_edge("local_expert", "finalizer")
    workflow.add_edge("finalizer", END)

    # Compile the graph
    return workflow.compile()

# --- Main Function ---
def main():
    print("="*50)
    print("WELCOME TO THE MULTI-AGENT TRAVEL ASSISTANT")
    print("="*50)

    # Check for API Key
    if not os.getenv("GOOGLE_API_KEY"):
        print("\n[WARNING] GOOGLE_API_KEY not found in environment variables.")
        print("Please ensure it is set in your .env file or environment.")
        # Proceeding anyway as requested by user, but it will likely fail at runtime.
    
    # Get Dynamic User Input
    destination = input("\nWhere do you want to go? (e.g., Tokyo, Paris): ")
    interests = input("What are your interests? (e.g., Food, History, Nature): ")

    if not destination or not interests:
        print("Error: Destination and interests are required!")
        return

    # Initialize state
    initial_state = {
        "destination": destination,
        "interests": interests,
        "itinerary": "",
        "budget": "",
        "tips": "",
        "final_report": "",
        "messages": []
    }

    # Build and run graph
    app = build_graph()
    
    print("\nStarting the Multi-Agent System. Please wait...\n")
    
    try:
        final_state = app.invoke(initial_state)
        
        print("\n" + "="*50)
        print(f"FINAL TRAVEL REPORT FOR {destination.upper()}")
        print("="*50 + "\n")
        
        report = final_state["final_report"]
        if isinstance(report, list):
            # Extract text from list of dicts if necessary
            report_text = "".join([item.get("text", "") if isinstance(item, dict) else str(item) for item in report])
            print(report_text)
        else:
            print(report)
        
    except Exception as e:
        print(f"\n[ERROR] An error occurred during execution: {e}")
        if "API_KEY_INVALID" in str(e) or "401" in str(e):
            print("Tip: Check if your GOOGLE_API_KEY is valid.")

if __name__ == "__main__":
    main()
