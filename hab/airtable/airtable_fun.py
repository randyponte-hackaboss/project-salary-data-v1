def get_table_id(table_name, tables):

    for key, value in tables.items():

        if value["table_name"] == table_name:
            
            return key
        
    else:
        return f"No table_name: {table_name}"