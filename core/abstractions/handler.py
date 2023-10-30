# -*- coding: utf-8 -*-
from abc import ABC, abstractmethod


class AbsHandler(ABC):
    @abstractmethod
    async def handle(self, *args, **kwargs):
        raise NotImplementedError
