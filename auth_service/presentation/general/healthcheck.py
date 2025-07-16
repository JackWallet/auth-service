from fastapi import APIRouter, Request

healthcheck_router = APIRouter()


@healthcheck_router.get(path="/health")
async def healthcheck(_: Request) -> dict[str, str]:
    return {"status": "ok"}
