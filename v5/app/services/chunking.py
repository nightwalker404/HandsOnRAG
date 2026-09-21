def chunk_text(text: str, chunk_size: int = 800, overlap: int = 100) -> list[str]:
    """ chunk the text from document for embedding """
    chunks = []
    start = 0
    text_legth = len(text)

    while start < text_legth:
        end = start + chunk_size
        chunk = text[start:end]

        if end < text_legth:
            last_period = chunk.rfind(". ")
            last_newline = chunk.rfind("\n")

            cut_point = max(last_newline, last_period)

            if cut_point > chunk_size // 2:
                end = start + cut_point + 1
                chunk = text[start:end]

        chunks.append(chunk.strip())
        start = end - overlap

    return [c for c in chunks if c]
