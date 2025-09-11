#!/usr/bin/env python3
INTEGER = r"(-)?(0|[1-9][0-9]*)"
STRING_INNER = r'([^"\\\x00-\x1F\x7F-\x9F]|\\["\\])'
# We'll limit this to just a max of 42 characters
STRING = f'"{STRING_INNER}{{1,42}}"'
# i.e. 1 is a not a float but 1.0 is.
FLOAT = rf"({INTEGER})(\.[0-9]+)([eE][+-][0-9]+)?"
BOOLEAN = r"(true|false)"
NULL = r"null"

simple_type_map = {
    "string": STRING,
    "any": STRING,
    "integer": INTEGER,
    "number": FLOAT,
    "float": FLOAT,
    "boolean": BOOLEAN,
    "null": NULL,
}

def build_dict_regex(props):
    out_re = r"\{"
    args_part = ", ".join(
        [f'"{prop}": ' + type_to_regex(props[prop]) for prop in props]
    )
    return out_re + args_part + r"\}"

def type_to_regex(arg_meta):
    arg_type = arg_meta["type"]
    if arg_type == "object":
        arg_type = "dict"
    if arg_type == "dict":
        try:
            result = build_dict_regex(arg_meta["properties"])
        except KeyError:
            return "Definition does not contain 'properties' value."
    elif arg_type in ["array","tuple"]:
        pattern = type_to_regex(arg_meta["items"])
        result = r"\[(" + pattern + ", ){0,8}" + pattern + r"\]"
    else:
        result = simple_type_map[arg_type]
    return result

type_to_regex({
    "type": "array",
    "items": {"type": "float"}
})

def build_standard_fc_regex(function_data):
    out_re = r"\[" + function_data["name"] + r"\("
    args_part = ", ".join(
        [
            f"{arg}=" + type_to_regex(function_data["parameters"]["properties"][arg])
            for arg in function_data["parameters"]["properties"]

            if arg in function_data["parameters"]["required"]
        ]
    )
    optional_part = "".join(
        [
            f"(, {arg}="
            + type_to_regex(function_data["parameters"]["properties"][arg])
            + r")?"
            for arg in function_data["parameters"]["properties"]
            if not (arg in function_data["parameters"]["required"])
        ]
    )
    return out_re + args_part + optional_part + r"\)]"


def build_regex_from_functions(fs):
    multi_regex = "|".join([
        rf"({build_standard_fc_regex(f)})" for f in fs
    ])
    return multi_regex
