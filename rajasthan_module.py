conversation_history = []
def ask_rajasthan(question):
    global conversation_history

    question_lower = question.lower().strip()

    # ---------------- RESET MEMORY ----------------
    if question_lower in ["reset", "clear chat", "start over"]:
        conversation_history = []
        return "Chat has been reset. How can I help you explore Rajasthan?"

    # Save user message
    conversation_history.append({"role": "user", "content": question})

    cities = ["jaipur", "udaipur", "jodhpur", "jaisalmer", "bikaner"]

    # ---------------- WEATHER ----------------
    if any(word in question_lower for word in ["weather", "temperature", "climate", "hot", "cold", "rain"]):

        detected_city = None

        # Check current question
        for city in cities:
            if city in question_lower:
                detected_city = city
                break

        # Check memory if not found
        if not detected_city:
            for msg in reversed(conversation_history):
                for city in cities:
                    if city in msg["content"].lower():
                        detected_city = city
                        break
                if detected_city:
                    break

        if detected_city:
            response = get_weather(detected_city.capitalize())
            conversation_history.append({"role": "assistant", "content": response})
            return response

        return "Please specify a Rajasthan city for weather information."


    # ---------------- ITINERARY ----------------
    if any(word in question_lower for word in ["plan", "itinerary", "trip", "travel plan"]):

        # Detect city from question or memory
        detected_city = None

        for city in cities:
            if city in question_lower:
                detected_city = city
                break

        if not detected_city:
            for msg in reversed(conversation_history):
                for city in cities:
                    if city in msg["content"].lower():
                        detected_city = city
                        break
                if detected_city:
                    break

        itinerary_prompt = f"""
You are a Rajasthan travel expert.

Create a detailed, structured itinerary.

Rules:
- Break it Day-wise (Day 1, Day 2, etc.)
- Include major attractions
- Suggest food experiences
- Keep tone friendly
- Keep it practical and realistic

User request: {question}
City detected: {detected_city if detected_city else "Not specified"}
"""
        response = llm.invoke(itinerary_prompt)
        conversation_history.append({"role": "assistant", "content": response.content})
        return response.content


    # ---------------- RAG KNOWLEDGE ----------------
    retrieved_docs = retriever.invoke(question)
    context = "\n\n".join([doc.page_content for doc in retrieved_docs])

    history_text = "\n".join(
        [f"{msg['role']}: {msg['content']}" for msg in conversation_history]
    )

    final_prompt = f"""
You are a friendly Rajasthan Tourism AI Assistant.

Conversation so far:
{history_text}

Answer ONLY using the provided context.
If information is not found, say:
"I don't have that information in my Rajasthan guide."

Context:
{context}

Question:
{question}
"""

    response = llm.invoke(final_prompt)
    conversation_history.append({"role": "assistant", "content": response.content})

    return response.content