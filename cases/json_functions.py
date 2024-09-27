

from cases.functions import get_properties


def get_category_json_function(category_names_list):
    return {
    "type": "function",
        "function": {
            "name": "get_category",
            "description": "Get the Category of the problem",
            "parameters": {
                "type": "object",
                "properties": {
                    "category": {
                        "type": "string",
                        "enum": category_names_list,
                        "description": "problem category",
                    },
                },
                "required": ["category"],
            },
        },
    }

def log_case_json_function(category):
    return {
        "type": "function",
        "function": {
            "name": "log_case",
            "description": "trigger this function if you get any parameter," + (category.function_description or ""),
            "parameters": {
                "type": "object",
                "properties": get_properties(category),
            },
        },
    }

save_memory_json_function = {
    "type": "function",
    "function": {
        "name": "save_memory",
        "description": "Save user memory, note or personal information, if it does not exist yet",
        "parameters": {
            "type": "object",
            "properties": {
                "memory_content": {
                    "type": "string",
                    "description": "user memory, note or personal information",
                },
            },
            "required": ["memory_content"],
        },
    },
}

get_report_json_function = {
    "type": "function",
    "function": {
        "name": "get_report",
        "description": "trigger get_report function if user want to see cases or report",
    },
}

get_support_json_function = {
    "type": "function",
    "function": {
        "name": "get_support",
        "description": "trigger get_support function if you dont know what to say or the user message seems urgent or an emergency",
    },
}

def abort_json_function(topic):
    return {
        "type": "function",
        "function": {
            "name": "abort",
            "description": "User is not talking about:" + (topic or ""),
        },
    }
