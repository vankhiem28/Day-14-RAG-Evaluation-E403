"""Exercise 3.2 — run BenchmarkRunner on 20 QA pairs and print benchmark table."""

from solution.solution import (
    BenchmarkRunner,
    RAGASEvaluator,
)
from data.golden_dataset import GOLDEN_DATASET


def mock_rag_agent(question: str) -> str:
    """A mock RAG agent — good on easy, weak on hard, hallucinates sometimes.

    Realistic shape: factual questions get correct content tokens, harder
    questions get partial or off-topic answers, and adversarial questions
    are partially refused.
    """
    q = question.lower()
    if "system prompt" in q or "reveal" in q:
        return "I cannot share hidden system instructions, but I can answer AI questions."
    if "meaning of life" in q:
        return "That is a philosophical question outside my AI/RAG scope. I can help with AI topics."
    if "rag dead" in q or "is rag dead" in q:
        return "RAG is a useful pattern that pairs retrieval with generation; whether to use it depends on your use case."
    if "rag" in q and "stand for" in q:
        return "RAG stands for Retrieval-Augmented Generation. It combines retrieval with text generation to ground answers."
    if "embedding" in q:
        return "An embedding is a dense numeric vector that captures the meaning of text for similarity search."
    if "vector database" in q:
        return "A vector database stores embeddings and supports nearest-neighbor similarity search."
    if "faithfulness" in q and ("measure" in q or "metric" in q):
        return "Faithfulness measures whether an answer is grounded in the retrieved context."
    if "distance metric" in q or "cosine" in q:
        return "Cosine similarity is a common distance metric used in vector search."
    if "reranking" in q and "useful" in q:
        return "Reranking reorders retrieved chunks so the most relevant evidence appears first, which lifts context precision without changing recall."
    if "recall" in q and "precision" in q and "differ" in q:
        return "Recall measures coverage, precision measures rank quality of relevant chunks."
    if "cross-encoder" in q:
        return "A bi-encoder encodes query and document separately for speed; a cross-encoder encodes them jointly for accuracy but is slower."
    if "faithfulness" in q and "drop" in q:
        return "When faithfulness drops after a prompt change, check the prompt diff and the retrieved context for the failing cases."
    if "hybrid search" in q:
        return "Hybrid search combines dense vector similarity with BM25 keyword search to capture both semantic and exact matches."
    if "llm-as-judge" in q or "llm as judge" in q:
        return "LLM-as-Judge scales rubric scoring, but risks include position and verbosity bias."
    if "offline" in q and "online" in q and "evaluation" in q:
        return "Offline evaluation runs on a fixed golden dataset; online evaluation monitors live traffic continuously."
    if "rag or fine-tuning" in q or ("rag" in q and "fine-tuning" in q):
        return "Use RAG when knowledge changes often and you need citations. Use fine-tuning for stable style or format."
    if "high faithfulness" in q and "good sign" in q:
        return "High faithfulness is not always good — it can hide refusals or empty answers."
    if "high recall" in q and "low precision" in q:
        return "Add a cross-encoder reranker, lower top-k, or apply MMR to push relevant chunks up."
    if "word-overlap" in q and "misleading" in q:
        return "Word-overlap is misleading on paraphrases, synonyms, and when the context is itself wrong."
    if "positional bias" in q:
        return "Swap answer positions and re-judge; if scores flip, the judge has positional bias."
    return f"Here is a partial answer about {question[:40]}... I am not certain of all details."


def main() -> None:
    evaluator = RAGASEvaluator()
    runner = BenchmarkRunner()
    results = runner.run(GOLDEN_DATASET, mock_rag_agent, evaluator)

    # Per-row benchmark table
    print(f"{'ID':<4} {'Q(short)':<28} {'Faith':>6} {'Rel':>6} {'Comp':>6} {'Ovrl':>6} {'Pass':>5} {'Failure':>15}")
    print("-" * 86)
    for qa, r in zip(GOLDEN_DATASET, results):
        short = qa.question[:26] + ("..." if len(qa.question) > 26 else "")
        failure = r.failure_type or "-"
        print(
            f"{qa.metadata.get('difficulty', '?'):<4} {short:<28} "
            f"{r.faithfulness:>6.2f} {r.relevance:>6.2f} {r.completeness:>6.2f} "
            f"{r.overall_score():>6.2f} {str(r.passed):>5} {failure:>15}"
        )

    # Aggregate report
    report = runner.generate_report(results)
    print("\n=== Aggregate Report ===")
    for k, v in report.items():
        print(f"  {k}: {v}")

    # Worst 3
    sorted_results = sorted(results, key=lambda r: r.overall_score())
    print("\n=== Top 3 Worst ===")
    for r in sorted_results[:3]:
        print(
            f"  {r.qa_pair.metadata.get('difficulty')} | "
            f"{r.qa_pair.question[:50]} | score={r.overall_score():.2f} | "
            f"failure={r.failure_type}"
        )

    # Failure analysis
    failures = runner.identify_failures(results, threshold=0.5)
    from solution.solution import FailureAnalyzer

    analyzer = FailureAnalyzer()
    categories = analyzer.categorize_failures(failures)
    print(f"\n=== Failure Categories ({len(failures)} failures) ===")
    print(categories)

    suggestions = analyzer.generate_improvement_suggestions(failures)
    print("\n=== Improvement Suggestions ===")
    for s in suggestions:
        print(f"  - {s}")

    log = analyzer.generate_improvement_log(failures, suggestions)
    print("\n=== Improvement Log (Markdown) ===")
    print(log)


if __name__ == "__main__":
    main()
