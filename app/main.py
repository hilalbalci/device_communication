import logging
import sys

import strawberry
from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter

from app.schema import Mutation, Query

app = FastAPI()

schema = strawberry.Schema(query=Query, mutation=Mutation)
graphql_app = GraphQLRouter(schema)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
stream_handler = logging.StreamHandler(sys.stdout)
log_formatter = logging.Formatter("%(asctime)s [%(processName)s: %(process)d] [%(threadName)s: %(thread)d] [%("
                                  "levelname)s] %(name)s: %(message)s")
stream_handler.setFormatter(log_formatter)
logger.addHandler(stream_handler)


@app.get("/")
def read_root():
    return {"message": "IOT Device Communications App"}


app.include_router(graphql_app, prefix="/graphql")
