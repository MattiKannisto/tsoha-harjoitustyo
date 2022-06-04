from database import db


def get_tables_text_field_error_messages_by_min_and_max_length(table_name, column_name, content, min_length, max_length):
    error_messages = []
    if len(content) < min_length:
        error_messages.append(column_name.capitalize() + " needs to be at least " + str(min_length) + " characters!")
    if len(content) >= max_length:
        error_messages.append(column_name.capitalize() + " cannot be over " + str(max_length) + " characters!")
    if get_one_by_table_name_column_name_and_column_content(table_name, column_name, content):
        error_messages.append(column_name.capitalize() + " already taken, please choose another one!")
    return error_messages

def get_passwords_dont_match_error_message(password, retyped_password):
    error_messages = []
    if password != retyped_password:
        error_messages.append("Passwords do not match!")        
    return error_messages

def get_password_error_message_by_min_and_max_length(password, min_length, max_length):
    error_messages = []
    if len(password) < min_length:
        error_messages.append("Password needs to be at least " + str(min_length) + " characters!")
    if len(password) >= max_length:
        error_messages.append("Password cannot be over " + str(max_length) + " characters!")
    return error_messages


def get_one_by_table_name_column_name_and_column_content(table_name, column_name, content):
    # Here '*' needs to be used since different tables have different columns
    sql = "SELECT * FROM " + table_name + " WHERE " + column_name + "=:content"
    return db.session.execute(sql, {"content":content}).fetchone()
