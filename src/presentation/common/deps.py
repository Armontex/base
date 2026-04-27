from fastapi import Request

from src.infra.bootstrap import Container


def get_container(request: Request) -> Container:
    return request.app.state.container
