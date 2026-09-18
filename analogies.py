#!/usr/bin/env python3
"""analogies.py

Small interactive script demonstrating word analogies using a
pretrained Word2Vec model (Google News vectors via gensim).

Run the script directly to play an interactive analogy game:

    python3 analogies.py

Note: the pretrained model download is large (~1.6GB) and may take
some time on first run.
"""

import gensim.downloader as api
import numpy as np
from typing import List, Tuple

print("loading (and downloading if needed) Word2Vec model...\n")
# download and load Word2Vec model - size ~ 1.6GB
word2vec_model = api.load('word2vec-google-news-300')
print("Word2Vec model loaded successfully.")

def cosine_similarity(vec1: np.ndarray, vec2: np.ndarray) -> float:
    """
    Calculate the cosine similarity between two vectors.

    Args:
        vec1 (np.ndarray): First vector.
        vec2 (np.ndarray): Second vector.

    Returns:
        float: Cosine similarity between vec1 and vec2.
    """
    dot_product = np.dot(vec1, vec2)
    norm_vec1 = np.linalg.norm(vec1)
    norm_vec2 = np.linalg.norm(vec2)
    
    if norm_vec1 == 0 or norm_vec2 == 0:
        return 0.0
    
    return dot_product / (norm_vec1 * norm_vec2)

def find_similar_words(word: str, top_n: int = 10) -> List[Tuple[str, float]]:
    """
    Find the most similar words to a given word using the Word2Vec model.

    Args:
        word (str): The input word.
        top_n (int): Number of similar words to return.

    Returns:
        List[Tuple[str, float]]: A list of tuples containing similar words and their similarity scores.
    """
    if word not in word2vec_model:
        raise ValueError(f"The word '{word}' is not in the Word2Vec model vocabulary.")
    
    return word2vec_model.most_similar(word, topn=top_n)

def vector_arithmetic(*words_and_weights: Tuple[str, float]) -> np.ndarray:
    """
    Perform vector arithmetic on the Word2Vec embeddings of the given words.

    Args:
        *words_and_weights (Tuple[str, float]): Tuples of words and their corresponding weights.

    Returns:
        np.ndarray: The resulting vector after performing the weighted sum of the word vectors.
    """
    result_vector = np.zeros(word2vec_model.vector_size)
    
    for word, weight in words_and_weights:
        if word not in word2vec_model:
            raise ValueError(f"The word '{word}' is not in the Word2Vec model vocabulary.")
        
        result_vector += weight * word2vec_model[word]
    
    return result_vector

def print_analogy_result(result_vector: np.ndarray, original_words: List[str], top_n : int = 10):
    """
    Print the most similar words to the resulting vector from vector arithmetic.

    Args:
        result_vector (np.ndarray): The resulting vector from vector arithmetic.
        original_words (List[str]): The list of original words used in the vector arithmetic.
        top_n (int): Number of similar words to return.
    """
    similar_words = word2vec_model.similar_by_vector(result_vector, topn=top_n)
    print("\nVector arithmetic: " + " + ".join(original_words))
    print("Most similar words:")

    for word, similarity in similar_words:
        # only show words that were not part of the original inputs
        if word not in original_words:
            print(f"{word}: {similarity:.4f}")

def compute_analogy():
    """
    Compute the analogy based on user input and print the results.
    """
    word1 = input("Enter the first word (e.g., 'king'): ")
    word2 = input("Enter the second word (e.g., 'man'): ")
    word3 = input("Enter the third word (e.g., 'woman'): ")

    try:
        result_vector = vector_arithmetic((word1, 1), (word2, -1), (word3, 1))
        print(f"\n{word1} is to {word2} as {word3} is to ?")
        print_analogy_result(result_vector, [word1, word2, word3], top_n=5)

        print("\n Play again? (y/n): ")
        play_again = input().lower()
        if play_again == "y":
            compute_analogy()

    except ValueError as e:
        print(e)

if __name__ == "__main__":
    compute_analogy()

