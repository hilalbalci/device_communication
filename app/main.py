from fastapi import FastAPI
import strawberry
from strawberry.fastapi import GraphQLRouter
from app.schema import Query

app = FastAPI()

schema = strawberry.Schema(query=Query)
graphql_app = GraphQLRouter(schema)


@app.get("/")
def read_root():
    return {"message": "IOT Device Communications App"}


app.include_router(graphql_app, prefix="/graphql")
