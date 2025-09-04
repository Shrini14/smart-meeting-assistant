from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os
from langchain_core.output_parsers import JsonOutputParser
import json

load_dotenv()

# Initialize Groq LLM
llm = ChatGroq(
    model_name="gemma2-9b-it",
    temperature=0.3,
    max_tokens=500,
    groq_api_key=os.getenv("GROQ_API_KEY")
)

# Initialize JSON parser
json_parser = JsonOutputParser()


def analyze_meeting_groq(transcript_text):
    """
    Analyze meeting transcript and extract structured information
    Returns parsed JSON object
    """
    prompt = f"""
    You are a Smart Meeting Assistant.
    Analyze the following meeting transcript and extract:
    1. Action items
    2. Deadlines
    3. Decisions made
    4. Participant mentions
    5. Summarize key points in 3-5 bullet points

    Return ONLY valid JSON format with keys: action_items, deadlines, decisions, participants, summary.
    No preamble, no explanation, just the JSON.

    Transcript:
    \"\"\"{transcript_text}\"\"\"
    """

    try:
        # Get response from LLM
        response = llm.invoke(prompt)

        # Parse the JSON string response
        parsed_result = json_parser.parse(response.content)

        return parsed_result

    except json.JSONDecodeError as e:
        # Fallback if JSON parsing fails
        return {
            "error": "Failed to parse JSON response",
            "raw_response": response.content,
            "parse_error": str(e)
        }
    except Exception as e:
        return {
            "error": "Failed to analyze meeting",
            "error_message": str(e)
        }


def get_meeting_summary(transcript_text):
    """
    Get a simple summary of the meeting
    """
    prompt = f"""
    Provide a brief 2-3 sentence summary of this meeting transcript.
    No preamble, just the summary.

    Transcript:
    \"\"\"{transcript_text}\"\"\"
    """

    try:
        response = llm.invoke(prompt)
        return response.content.strip()
    except Exception as e:
        return f"Error generating summary: {str(e)}"