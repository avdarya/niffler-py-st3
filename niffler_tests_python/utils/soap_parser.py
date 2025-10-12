from xml.etree import ElementTree
from xml.etree.ElementTree import Element

from typing import Any, Optional

namespace = {
    'soap': 'http://schemas.xmlsoap.org/soap/envelope/',
    'nif': 'niffler-userdata'
}

def _find_text(element: Element, tag: str, ns: dict[str, str]) -> Optional[str] :
    el = element.find(tag, ns)
    return el.text if el is not None else None

def parsed_xml_user(response_text: str) -> dict[str, Any]:
    root  = ElementTree.fromstring(response_text)
    data = root.find('.//nif:user', namespace)
    user = {
        'id': _find_text(data, 'nif:id', namespace),
        'username': _find_text(data, 'nif:username', namespace),
        'fullname': _find_text(data, 'nif:fullname', namespace),
        'currency': _find_text(data, 'nif:currency', namespace),
        'friendship': _find_text(data, 'nif:friendshipStatus', namespace),
    }
    return user

def parsed_xml_users_page(response_text: str) -> dict[str, Any]:
    root = ElementTree.fromstring(response_text)
    users_response = root.find('.//nif:usersResponse', namespace)
    user_elements = root.findall('.//nif:user', namespace)
    users_list = []
    for user in user_elements:
        users_list.append({
        'id': _find_text(user, 'nif:id', namespace),
        'username': _find_text(user, 'nif:username', namespace),
        'currency': _find_text(user, 'nif:currency', namespace),
        'friendship': _find_text(user, 'nif:friendshipStatus', namespace),
        })
    result = {
        'users': users_list,
        'size': int(_find_text(users_response, 'nif:size', namespace) or 0),
        'number': int(_find_text(users_response, 'nif:number', namespace) or 0),
        'totalElements': int(_find_text(users_response, 'nif:totalElements', namespace) or 0),
        'totalPages': int(_find_text(users_response, 'nif:totalPages', namespace) or 0),
    }
    return result

def parsed_xml_fault(response_text: str) -> dict[str, Any]:
    root  = ElementTree.fromstring(response_text)
    fault = root.find('.//soap:Fault', namespace)

    if fault is None:
        return {'error': 'No SOAP Fault found'}

    faultcode = _find_text(fault, 'faultcode', {})
    faultstring = _find_text(fault, 'faultstring', {})
    return {
        'faultcode': faultcode,
        'faultstring': faultstring,
    }
