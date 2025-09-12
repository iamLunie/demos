import json
from textwrap import dedent
import outlines
from outlines.types import Regex
from transformers import AutoTokenizer
import warnings

from fn import build_regex_from_functions
from prompt import generate_prompt


class SmolMind:
    def __init__(self, functions):
        import mlx_lm

        self.functions = functions
        self.fn_regex = build_regex_from_functions(functions)

        # model_name = "HuggingFaceTB/SmolLM2-135M-Instruct-Q8-mlx"
        model_name = "HuggingFaceTB/SmolLM2-1.7B-Instruct-Q8-mlx"

        # ---- INITIALIZE OUTLINES MODEL ---- #
        mlx_model = mlx_lm.load(model_name)
        self.model = outlines.from_mlxlm(*mlx_model)
        self.generator = outlines.Generator(self.model, Regex(self.fn_regex))
        # ---- INITIALIZE OUTLINES MODEL ---- #

        self.tokenizer = AutoTokenizer.from_pretrained(model_name)

    def get_function_call(self, user_prompt):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            prompt = generate_prompt(user_prompt, self.functions, self.tokenizer)
            response = self.generator(prompt)
        return response
