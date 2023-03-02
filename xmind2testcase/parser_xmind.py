#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time:2023/3/1 18:34
# @Author:boyizhang
from abc import ABCMeta, abstractmethod


class ParseXmind(metaclass=ABCMeta):

    @abstractmethod
    def parse_testsuites(self, xmind_content_dict):
        raise NotImplementedError
