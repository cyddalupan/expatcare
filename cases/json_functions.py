

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
        "description": "Save a memory, note or personal information about the user, if it does not exist yet",
        "parameters": {
            "type": "object",
            "properties": {
                "memory_content": {
                    "type": "string",
                    "description": "The memory or note to be saved about the employee",
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

def abort_json_function(topic):
    return {
        "type": "function",
        "function": {
            "name": "abort",
            "description": "User is not talking about:" + (topic or ""),
        },
    }
