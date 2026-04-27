from pydantic import BaseModel, Field


class ErrorResponse(BaseModel):
    """Стандартный ответ при ошибке."""

    success: bool = Field(
        default=False,
        description="Флаг успешности запроса",
        examples=[False],
    )
    error_code: str = Field(
        description="Машиночитаемый код ошибки",
        examples=["INVALID_REFRESH_TOKEN"],
    )
    message: str = Field(
        description="Человекочитаемое сообщение об ошибке",
        examples=["Токен обновления недействителен"],
    )
    details: dict | None = Field(
        default=None,
        description="Дополнительные детали ошибки",
        examples=[
            {
                "errors": [
                    {
                        "field": "body → email",
                        "message": "Field required",
                        "type": "missing",
                    }
                ]
            }
        ],
    )
