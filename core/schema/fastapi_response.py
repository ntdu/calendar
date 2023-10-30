# -*- coding: utf-8 -*-
from typing import Any, List

from core.abstractions.base_models import CustomBaseModel


class FastApiResponse(CustomBaseModel):
    success: bool = True
    data: List[Any] = []
    length: int = 0
    error: str = ""
    error_code: int = 0
