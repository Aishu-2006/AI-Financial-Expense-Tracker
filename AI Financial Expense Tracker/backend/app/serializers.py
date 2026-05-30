from typing import Any, Dict


def serialize_document(document: Dict[str, Any]) -> Dict[str, Any]:
    data = dict(document)
    data["id"] = str(data.pop("_id"))
    if "userId" in data:
        data["userId"] = str(data["userId"])
    return data


def serialize_user(document: Dict[str, Any]) -> Dict[str, Any]:
    data = serialize_document(document)
    data.pop("passwordHash", None)
    return data
