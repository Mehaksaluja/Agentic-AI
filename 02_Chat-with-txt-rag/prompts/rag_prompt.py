SYSTEM_PROMPT = """
You are a helpful AI Assistant.

Answer ONLY using the provided context.

If the answer is not available in the context,
say:

"I couldn't find the answer in the provided document."

Keep answers concise.
"""


def build_prompt(

    context,

    question

):

    context = "\n\n".join(context)

    return f"""
Context:

{context}

Question:

{question}

Answer:
"""