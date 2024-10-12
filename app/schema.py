from typing import List, Optional

import strawberry

from app.graphql_resolvers import create_device, list_devices, list_locations


@strawberry.type
class Device:
    id: int
    name: str


@strawberry.type
class DeviceLocation:
    latitude: float
    longitude: float
    timestamp: str


@strawberry.type
class Query:
    list_devices: List[Device] = strawberry.field(resolver=list_devices)
    list_locations: List[DeviceLocation] = strawberry.field(resolver=list_locations)


@strawberry.type
class Mutation:
    @strawberry.mutation
    def create_device(self, name: str, description: Optional[str] = None) -> Device:
        return create_device(name, description)
