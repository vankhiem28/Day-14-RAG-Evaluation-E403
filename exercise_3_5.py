"""Exercise 3.5 — measure Context Recall/Precision before vs after reranking."""

from solution.solution import RAGASEvaluator, rerank_by_overlap

RETRIEVAL_DATA = [
    {
        "id": "R01",
        "question": "What is the capital of France?",
        "expected": "Paris is the capital of France",
        "chunks": [
            "Bananas are a tropical fruit.",
            "The Eiffel Tower is in Paris.",
            "Paris is the capital city of France.",
        ],
    },
    {
        "id": "R02",
        "question": "What does RAG stand for?",
        "expected": "RAG stands for Retrieval-Augmented Generation",
        "chunks": [
            "LLMs can hallucinate facts.",
            "Retrieval-Augmented Generation (RAG) combines retrieval with generation.",
            "Vector databases store embeddings.",
        ],
    },
    {
        "id": "R03",
        "question": "When was the Eiffel Tower built?",
        "expected": "The Eiffel Tower was completed in 1889",
        "chunks": [
            "The tower is 330 metres tall.",
            "It is made of wrought iron.",
            "The Eiffel Tower was completed in 1889 for the World's Fair.",
        ],
    },
    {
        "id": "R04",
        "question": "What is gradient descent?",
        "expected": "Gradient descent minimizes a loss function by following the negative gradient",
        "chunks": [
            "Neural networks have layers.",
            "Gradient descent updates weights along the negative gradient to minimize loss.",
            "Learning rate controls step size.",
        ],
    },
    {
        "id": "R05",
        "question": "What is overfitting?",
        "expected": "Overfitting is when a model memorizes training data and fails to generalize",
        "chunks": [
            "Regularization adds a penalty term.",
            "Dropout randomly disables neurons.",
            "Overfitting means the model memorizes training data and generalizes poorly.",
        ],
    },
    {
        "id": "R06",
        "question": "What is backpropagation?",
        "expected": "Backpropagation is an algorithm that computes gradients for neural network training",
        "chunks": [
            "Activation functions introduce non-linearity.",
            "Backpropagation computes gradients of the loss with respect to each weight.",
            "Optimizers update model parameters.",
        ],
    },
    {
        "id": "R07",
        "question": "What is a vector database?",
        "expected": "A vector database stores and retrieves high-dimensional embeddings for similarity search",
        "chunks": [
            "SQL databases store tabular rows.",
            "Embeddings are dense numeric vectors that represent meaning.",
            "A vector database indexes embeddings and returns nearest neighbors by similarity.",
        ],
    },
    {
        "id": "R08",
        "question": "What is prompt engineering?",
        "expected": "Prompt engineering is the practice of designing inputs to guide LLM behavior",
        "chunks": [
            "Tokens are sub-word units used by language models.",
            "Temperature controls the randomness of model outputs.",
            "Prompt engineering crafts instructions and examples to steer LLM behavior.",
        ],
    },
]


def main() -> None:
    evaluator = RAGASEvaluator()
    rows: list[tuple[str, float, float, float, float]] = []

    sum_recall = 0.0
    sum_p_before = 0.0
    sum_p_after = 0.0
    n = len(RETRIEVAL_DATA)

    print(f"{'ID':<5} {'Recall':>7} {'P(before)':>10} {'P(after)':>10} {'Δ':>8}")
    print("-" * 44)
    for row in RETRIEVAL_DATA:
        recall = evaluator.evaluate_context_recall(row["chunks"], row["expected"])
        p_before = evaluator.evaluate_context_precision(row["chunks"], row["expected"])
        reranked = rerank_by_overlap(row["chunks"], row["expected"])
        p_after = evaluator.evaluate_context_precision(reranked, row["expected"])
        delta = p_after - p_before
        sum_recall += recall
        sum_p_before += p_before
        sum_p_after += p_after
        rows.append((row["id"], recall, p_before, p_after, delta))
        print(f"{row['id']:<5} {recall:>7.4f} {p_before:>10.4f} {p_after:>10.4f} {delta:>+8.4f}")

    print("-" * 44)
    print(
        f"{'Avg':<5} {sum_recall/n:>7.4f} {sum_p_before/n:>10.4f} "
        f"{sum_p_after/n:>10.4f} {(sum_p_after-sum_p_before)/n:>+8.4f}"
    )


if __name__ == "__main__":
    main()
