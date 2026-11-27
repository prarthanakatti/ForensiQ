import re


def chunk_text(text, chunk_size=1000, overlap=150):
    """
    Split text into chunks while preserving sentence boundaries
    and avoiding chunks that start in the middle of a word.
    """

    # Normalize whitespace
    text = re.sub(r"\s+", " ", text).strip()

    # Split into sentences
    sentences = re.split(r"(?<=[.!?])\s+", text)

    chunks = []
    current_chunk = ""

    for sentence in sentences:

        # If adding the sentence stays within the chunk size
        if len(current_chunk) + len(sentence) + 1 <= chunk_size:

            if current_chunk:
                current_chunk += " " + sentence
            else:
                current_chunk = sentence

        else:

            # Save current chunk
            if current_chunk:
                chunks.append(current_chunk.strip())

            # Start a new chunk
            current_chunk = sentence

    # Add final chunk
    if current_chunk:
        chunks.append(current_chunk.strip())

    return chunks