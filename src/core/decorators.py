#!usr/bin/python3
# -*- coding: UTF-8 -*-

import time
from functools import wraps


def exception_handler(func):
    @wraps(func)
    def exceptions(*args, **kwargs):
        logger = args[0].logger
        self, *args = args
        try:
            try:
                result = func(self, *args, **kwargs)
            except TypeError:
                if args: 
                    result = func(*args, **kwargs)
                else:
                    result = func(**kwargs)
            return result
        except Exception as e:
            logger.error(f"{func.__name__} error : {e}")
            raise e
    return exceptions


def exec_retry(func, max_tries=3, delay_seconds=2):
    @wraps(func)
    def retry(*args, **kwargs):
        logger = args[0].logger
        self, *args = args
        for i in range(max_tries + 1):
            try:
                try:
                    return func(self, *args, **kwargs)
                except TypeError:
                    if args: 
                        return func(*args, **kwargs)
                    return func(**kwargs)
            except Exception as exc:
                if i < max_tries:
                    logger.error(f"Function {func.__name__} raised {exc.__class__.__name__}. Retrying ({i + 1}/{max_tries}) after {delay_seconds} seconds...")
                    time.sleep(delay_seconds)
                else:
                    raise exc
    return retry