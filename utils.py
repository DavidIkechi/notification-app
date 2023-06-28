from enum import Enum
from datetime import datetime
import re
import datetime as dt
from datetime import datetime

# for adding utlity functions
def get_offset(page: int, page_size: int) -> int:
    return (page - 1) * page_size
    
def exclude_none_values(data):
    """
    Helper function to exclude None values from a dictionary.
    """
    return {k: v for k, v in data.items() if v is not None}

def format_datetime(date_value):
    formatted_date = datetime.strptime(date_value, "%Y-%m-%d %H:%M:%S")
    # Format the datetime object as a string without the T and Z characters
    return formatted_date.strftime("%Y-%m-%d %H:%M:%S.%f")


def format_text(body_text: str, data: dict, variable):
    # replace new lines with line breaks, to look like html texts.
    body_text = fr'{body_text}'
    new_text = body_text.replace(r'\n', '<br>')
    # start formatting.
    placeholders = re.findall(r'{{(.*?)}}', new_text)

    # Replace placeholders with values from the dictionary
    formatted_text = new_text
    for placeholder in placeholders:
        # only replace when it's present in the list.
        if placeholder in variable:
            value = data.get(placeholder.strip(), '')
            formatted_text = formatted_text.replace('{{' + placeholder + '}}', str(value))
    
    return formatted_text


def get_noti_data(noti_sample, schedule_data: dict, variable):
    mess_body = format_text(noti_sample.message_body, 
                            schedule_data.noti_variables, variable)
    
    noti_data ={
        'client_id': noti_sample.client_id,
        'trans_channel_id': noti_sample.trans_channel_id,
        'noti_type_id': noti_sample.noti_type_id,
        'message_body': mess_body,
        'subject': noti_sample.subject,
        'sender_id': noti_sample.sender_id,
        'sender_email': noti_sample.sender_email,
        'carbon_copy': noti_sample.carbon_copy,
        'blind_copy': noti_sample.blind_copy,
        'scheduled_at': schedule_data.scheduled_at,
        'recipients': schedule_data.recipients
    }
    
    return exclude_none_values(noti_data)
