import asyncio
import uuid
import sys
from langgraph.checkpoint.sqlite import SqliteSaver

from src.graph.state import make_initial_state
from src.graph.graph import build_graph

async def main():
    if len(sys.argv) < 2:
        print("Usage: python main.py '<query>'")
        sys.exit(1)
        
    query = sys.argv[1]
    session_id = str(uuid.uuid4())
    
    print(f"\n--- Starting Banking Assistant Pipeline ---")
    print(f"Session ID: {session_id}")
    print(f"Query: '{query}'\n")

    # Initialize Graph & Checkpointer (Sqlite for memory)
    # Using 'in-memory' sqlite for the skeleton test. 
    # Can change to file-backed sqlite or postgres later.
    checkpointer = SqliteSaver.from_conn_string(":memory:")
    
    app_graph = build_graph()
    app = app_graph.compile(checkpointer=checkpointer)

    initial_state = make_initial_state(query=query, session_id=session_id)
    config = {"configurable": {"thread_id": session_id}}

    try:
        # Run the graph (async)
        # We await app.ainvoke, passing our dict config.
        final_state = await app.ainvoke(initial_state, config=config)
        
        print("\n--- Pipeline Complete ---")
        print(f"Final Response: {final_state.get('final_response')}")
        
    except Exception as e:
        print(f"\n[ERROR] Pipeline failed: {e}")

if __name__ == "__main__":
    asyncio.run(main())
