from typing import List, Optional

import strawberry

from app.graphql_resolvers import (create_device, delete_device, get_device,
                                   list_devices, list_location_by_device,
                                   list_locations)


@strawberry.type
class Device:
    id: int
    name: str
    description: Optional[str]


@strawberry.type
class DeviceLocation:
    latitude: float
    longitude: float
    timestamp: str
    device_id: int


@strawberry.type
class Query:
    list_devices: List[Device] = strawberry.field(resolver=list_devices)
    list_locations: List[DeviceLocation] = strawberry.field(resolver=list_locations)

    @strawberry.field
    def list_location_by_device(self, device_id: int) -> List[DeviceLocation]:
        return list_location_by_device(device_id)

    @strawberry.field
    def get_device_by_id(self, device_id: int) -> List[Device]:
        return get_device(device_id)


@strawberry.type
class Mutation:
    @strawberry.mutation
    def create_device(self, name: str, description: Optional[str] = None) -> Device:
        return create_device(name, description)

    @strawberry.mutation
    def delete_device(self, device_id: int) -> bool:
        result = delete_device(device_id)
        if not result:
            return False
        return True
