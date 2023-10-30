# -*- coding: utf-8 -*-
from abc import ABC, abstractmethod


class AbsManager(ABC):
    @abstractmethod
    def bind_context(self, context):
        raise NotImplementedError

    @abstractmethod
    async def process(self, *args, **kwargs):
        raise NotImplementedError
