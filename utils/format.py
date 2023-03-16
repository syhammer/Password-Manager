from scripts import init

def format(string,allowed_chars,replacer_char):
    formatted_string = ''

    for char in string:
        formatted_string+=char if char in allowed_chars else replacer_char

    return formatted_string

def from_name(string,format_name):
    config_format = init.get_config()['format'][format_name]
    
    return format(string,config_format['allowed_chars'],config_format['replacer_char'])
