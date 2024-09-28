# from openai import OpenAI
# OPENAI_API_KEY = "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"
# client = OpenAI(api_key=OPENAI_API_KEY)

# completion = client.chat.completions.create(
#     model="gpt-4o-mini",
#     messages=[
#         {"role": "system", "content": "You are a helpful assistant."},
#         {
#             "role": "user",
#             "content": "Write a haiku about recursion in programming."
#         }
#     ]
# )

import os

username = os.environ.get('USER') or os.environ.get('USERNAME')

if username:
    print(f"The current user is: {username}")
else:
    print("Username not found in environment variables.")