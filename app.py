import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent
AGENTS_DIR = PROJECT_ROOT / "src" / "agents"

sys.path.append(str(AGENTS_DIR))

from orchestrator_agent import OrchestratorAgent


def main():
    agent = OrchestratorAgent()

    print("\nEnterprise AI Data Intelligence Platform")
    print("=" * 50)
    print("Ask a business question. Type 'exit' to quit.")

    while True:
        query = input("\nYour question: ")

        if query.lower() in ["exit", "quit"]:
            print("Goodbye.")
            break

        result = agent.run(query)

        print("\nFinal Answer")
        print("=" * 50)
        print(result["final_answer"])

        print("\nEvaluation")
        print("=" * 50)
        for key, value in result["evaluation"].items():
            print(f"{key}: {value}")


if __name__ == "__main__":
    main()