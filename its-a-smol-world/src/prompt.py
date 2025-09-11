from textwrap import dedent


def format_functions(functions):
    formatted_functions = []
    for func in functions:
        function_info = f"{func['name']}: {func['description']}\n"
        if 'parameters' in func and 'properties' in func['parameters']:
            for arg, details in func['parameters']['properties'].items():
                description = details.get('description', 'No description provided')
                function_info += f"- {arg}: {description}\n"
        formatted_functions.append(function_info)
    return "\n".join(formatted_functions)

SYSTEM_PROMPT_FOR_CHAT_MODEL = dedent("""
    You are an expert designed to call the correct function to solve a problem based on the user's request.
    The functions available (with required parameters) to you are:
    {functions}

    You will be given a user prompt and you need to decide which function to call.
    You will then need to format the function call correctly and return it in the correct format.
    The format for the function call is:
    [func1(params_name=params_value]
    NO other text MUST be included.

    For example:
    Request: I want to order a cheese pizza from Pizza Hut.
    Response: [order_food(restaurant="Pizza Hut", item="cheese pizza", quantity=1)]

    Request: Is it raining in NY.
    Response: [get_weather(city="New York")]

    Request: I need a ride to SFO.
    Response: [order_ride(destination="SFO")]

    Request: I want to send a text to John saying Hello.
    Response: [send_text(to="John", message="Hello!")]
""")


ASSISTANT_PROMPT_FOR_CHAT_MODEL = dedent("""
    I understand and will only return the function call in the correct format.
    """
)
USER_PROMPT_FOR_CHAT_MODEL = dedent("""
    Request: {user_prompt}.
""")

def generate_prompt(question, functions, tokenizer):
    messages = [
        {"role": "user", "content": SYSTEM_PROMPT_FOR_CHAT_MODEL.format(functions=format_functions(functions))},
        {"role": "assistant", "content": ASSISTANT_PROMPT_FOR_CHAT_MODEL },
        {"role": "user", "content": USER_PROMPT_FOR_CHAT_MODEL.format(user_prompt=question)},
    ]
    fc_prompt = tokenizer.apply_chat_template(messages, tokenize=False)
    return fc_prompt
