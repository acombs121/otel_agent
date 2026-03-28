import sys
from dotenv import load_dotenv
from .telemetry import flush_telemetry
from .agent import adk_app

def main():
    # 1. Load local environment variables
    load_dotenv()

    # 2. Get query from CLI or use default
    query = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else "What is 10 + 10?"
    
    try:
        # 3. Stream and print agent response
        for response in adk_app.stream_query(message=query, user_id="user_123"):
            print(response, end="", flush=True)
        print()
                
    finally:
        # 4. Ensure telemetry is sent before exit
        flush_telemetry()
            
if __name__ == "__main__":
    main()
