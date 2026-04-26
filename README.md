# stayease-ai-agent

## 1.1 System Overview

StayEase AI Agent is a conversational assistant that helps users search for rental properties, view listing details, and make bookings. 

The system uses a LangGraph-based agent to manage conversation flow and decision-making. A FastAPI backend receives user messages and forwards them to the agent. The agent uses an LLM (via Groq/OpenRouter) to understand intent and decide which tool to call. Tools interact with a PostgreSQL database to fetch listings, retrieve details, or create bookings.

If the request is outside supported actions (search, details, booking), the system escalates to a human.

```mermaid
flowchart TD
    User --> FastAPI
    FastAPI --> LangGraphAgent
    LangGraphAgent --> LLM
    LangGraphAgent --> Tools
    Tools --> PostgreSQL
    PostgreSQL --> Tools
    Tools --> LangGraphAgent
    LangGraphAgent --> FastAPI
    FastAPI --> User