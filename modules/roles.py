#roles
def roles_list(roles):
    roles = roles[1:]
    msg = '```\n'
    for role in roles:
        if not role.managed:
            msg += role.name+'\n'
    if len(msg) == 3:
        msg += 'No roles available\n```'
        return msg
    
    msg += '```'
    return msg

def roles_find(role_list, role):
    for r in role_list:
        if r.name.lower() == role.lower():
            return r
    return None