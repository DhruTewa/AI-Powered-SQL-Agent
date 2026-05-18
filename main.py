import sys
from core.agent import run_agent

if __name__ == "__main__":
    
    question = sys.argv[1]        # reads the first argument from the terminal
    sql, result = run_agent(question)
    print(f"SQL:\n{sql}\n")
    print(result.to_string(index=False))