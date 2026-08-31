import json
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

from app.llm import generate_response


DATASET_PATH = Path(__file__).parent / "dataset.json"


def evaluate_answer(answer: str, keywords: list[str]) -> bool:
    answer = answer.lower()
    return all(keyword.lower() in answer for keyword in keywords)


def main():
    with open(DATASET_PATH, encoding="utf-8") as f:
        dataset = json.load(f)

    passed = 0
    total = len(dataset)

    print("\n========== LLM EVALUATION ==========\n")

    for i, item in enumerate(dataset, start=1):
        question = item["question"]
        keywords = item["keywords"]

        print(f"[{i}/{total}] {question}")

        response, input_tokens, output_tokens = generate_response(question)

        success = evaluate_answer(response, keywords)

        if success:
            passed += 1
            status = "PASS"
        else:
            status = "FAIL"

        print(f"  Keywords: {keywords}")
        print(f"  Status: {status}")
        print(f"  Output tokens: {output_tokens}")
        print()

    score = (passed / total) * 100

    print("====================================")
    print(f"Passed: {passed}/{total}")
    print(f"Score:  {score:.1f}%")
    print("====================================\n")

    if score < 80:
        print("Evaluation FAILED: score below 80%")
        sys.exit(1)

    print("Evaluation PASSED!")


if __name__ == "__main__":
    main()
