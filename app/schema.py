import strawberry
from typing import List
from app.graphql_resolvers import list_devices, get_last_location


@strawberry.type
class Device:
    id: int
    name: str


@strawberry.type
class Location:
    latitude: float
    longitude: float
    timestamp: str


@strawberry.type
class Query:
    list_devices: List[Device] = strawberry.field(resolver=list_devices)
    last_location: List[Location] = strawberry.field(resolver=get_last_location)
