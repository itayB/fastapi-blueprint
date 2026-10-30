from typing import Literal

from pydantic import BaseModel


class Liveness(BaseModel):
    status: Literal["ok"] = "ok"
