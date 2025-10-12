from pathlib import Path

import xmlschema
from jinja2 import Environment, PackageLoader, select_autoescape, FileSystemLoader
from xmlschema import XMLSchema11


base_path = Path(__file__).resolve().parent.parent
env = Environment(
    loader=FileSystemLoader(base_path / 'soap' ),
    autoescape=select_autoescape(['html', 'xml'])
)

def xml_current_user(username: str) -> str:
    template = env.get_template('/xml/current_user.xml')
    return template.render({'username': username})

def xml_all_users_page(
        username: str,
        page: int,
        size: int,
        search_query: str,
        sort: str = 'username',
        direction: str = 'ASC',
) -> str:
    template = env.get_template('/xml/all_users_page.xml')
    return template.render({
        'username': username,
        'page': page,
        'size': size,
        'sort': sort,
        'direction': direction,
        'search_query': search_query
    })

def xml_friends_page(
        username: str,
        page: int,
        size: int,
        search_query: str,
        sort: str = 'username',
        direction: str = 'ASC'
) -> str:
    template = env.get_template('/xml/friends_page.xml')
    return template.render({
        'username': username,
        'page': page,
        'size': size,
        'sort': sort,
        'direction': direction,
        'search_query': search_query
    })

def xml_send_invitation(username: str, addressed_username: str):
    template = env.get_template('/xml/send_invitation.xml')
    return template.render({
        'username': username,
        'addressed_username': addressed_username
    })

def xml_accept_invitation(username: str, addressed_username: str):
    template = env.get_template('/xml/accept_invitation.xml')
    return template.render({
        'username': username,
        'addressed_username': addressed_username
    })

def xml_decline_invitation(username: str, addressed_username: str):
    template = env.get_template('/xml/decline_invitation.xml')
    return template.render({
        'username': username,
        'addressed_username': addressed_username
    })

def xml_remove_friend(username: str, addressed_username: str):
    template = env.get_template('/xml/remove_friend.xml')
    return template.render({
        'username': username,
        'addressed_username': addressed_username
    })

def xsd_response(operation: str) -> XMLSchema11:
    envelope_xsd = env.get_template('/xsd/envelope.xsd')
    rendered_xsd_response = envelope_xsd.render({
        'operation_xsd': f'{operation}.xsd',
        'operation': operation,
    })
    temp_file_path = f'{base_path}/soap/xsd/temp.xsd'
    with open(temp_file_path, 'w') as f:
        f.write(rendered_xsd_response)
    return xmlschema.XMLSchema11(temp_file_path)

def xsd_error_response() -> XMLSchema11:
    envelope_xsd = env.get_template('/xsd/envelope_fault.xsd')
    rendered_xsd_response = envelope_xsd.render({})
    temp_file_path = f'{base_path}/soap/xsd/temp_fault.xsd'
    with open(temp_file_path, 'w') as f:
        f.write(rendered_xsd_response)
    return xmlschema.XMLSchema11(temp_file_path, allow='sandbox')

