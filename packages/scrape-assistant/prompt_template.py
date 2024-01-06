def generate_prompt(html_data, json_data):
    return f"""
    I have HTML content and corresponding parsed JSON data. The goal is to identify any useful information in the HTML that might not have been captured in the JSON.

    HTML Content:
    {html_data}

    Parsed JSON Data Summary:
    {json_data}

    Question:
    1. Based on the HTML content, is there any important information such as dates, names, addresses, or other specific details that are not present in the JSON summary?
    2. If no additional information is found, please provide suggestions on how the parsing process could be improved for future cases.
    """