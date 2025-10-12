from enum import Enum

class FriendshipDBStatus(str, Enum):
    PENDING = "PENDING"
    ACCEPTED = "ACCEPTED"

class FriendshipAPIStatus(str, Enum):
    INVITE_SENT = "INVITE_SENT"
    INVITE_RECEIVED = "INVITE_RECEIVED"
    FRIEND = "FRIEND"
    VOID = "VOID"