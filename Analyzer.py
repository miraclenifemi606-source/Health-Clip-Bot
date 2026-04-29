def find_hooks(transcript):
    keywords = [
        "danger", "never", "warning", "symptom",
        "doctor says", "study shows", "risk", "deadly"
    ]

    sentences = transcript.split(".")
    clips = []

    for i, s in enumerate(sentences):
        if any(k in s.lower() for k in keywords):
            start = max(0, i - 1)
            end = min(len(sentences), i + 2)
            clips.append((start, end))

    return clips if clips else [(0, len(sentences)//3)]
