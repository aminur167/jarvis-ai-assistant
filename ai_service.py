# -*- coding: utf-8 -*-
from openai import OpenAI

from memory import get_memory_context


def ai_process(command, answer_mode="short"):
    try:
        client = OpenAI()
        memory_context = get_memory_context()
        style = "Give short, helpful responses." if answer_mode == "short" else "Give a clear, detailed, helpful response."
        system_content = f"You are a virtual assistant named Jarvis. {style}"
        if memory_context:
            system_content += f"\n\n{memory_context}"

        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": system_content,
                },
                {"role": "user", "content": command},
            ],
        )
        return completion.choices[0].message.content
    except Exception:
        return "Sorry, I could not connect to my AI service right now."
