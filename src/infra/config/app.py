from typing import Literal

from pydantic import BaseModel, ConfigDict


class AppSettings(BaseModel):
    model_config = ConfigDict(frozen=True)

    debug: bool = False
    log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = "INFO"
