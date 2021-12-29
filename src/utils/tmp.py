import uuid

def create_tmpfile_name(suffix:str):
    '''
    create a temp filename with suffix(ex: .png)
    '''
    prefix = str(uuid.uuid4())
    return f"/tmp/{prefix}{suffix}"