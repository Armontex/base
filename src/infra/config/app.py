from pydantic import BaseModel, ConfigDict
from typing import Literal


class AppSettings(BaseModel):
    model_config = ConfigDict(frozen=True)

    debug: bool = False
    log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = "INFO"
