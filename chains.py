from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate,MessagesPlaceholder

reflection_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a viral twitter influencer grading a tweet. Generate critique and recommendations for the user's tweet."
            "Always provide detailed recommendations, including requests for length, virality, style, etc.",
        ),
        MessagesPlaceholder(variable_name="messages"),
    ]
)

# generation_prompt = ChatPromptTemplate.from_messages(
#     [
#         (
#             "system",
#             "You are a twitter techie influencer assistant tasked with writing excellent twitter posts."
#             " Generate the best twitter post possible for the user's request."
#             " If the user provides critique, respond with a revised version of your previous attempts.",    # revise previous answer instead of creating a new one
#         ),
#         MessagesPlaceholder(variable_name="messages"),
#     ]
# )

generation_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a twitter techie influencer assistant tasked with writing excellent twitter posts."
            " Generate the best twitter post possible for the user's request."
            " If the user provides critique, respond with a revised version of your previous attempts."
            " IMPORTANT: Output ONLY the raw tweet text itself. Do not include any preamble like"
            " 'Here's a revised version', do not explain your changes, do not add a summary of"
            " what you changed, and do not wrap the tweet in quotation marks. Your entire response"
            " must be exactly what should be posted to Twitter, nothing else.",
        ),
        MessagesPlaceholder(variable_name="messages"),
    ]
)


llm=ChatGroq(temperature=0.3,model="llama-3.1-8b-instant")
generate_chain = generation_prompt | llm
reflect_chain = reflection_prompt | llm