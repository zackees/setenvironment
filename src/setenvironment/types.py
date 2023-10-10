# dataclass

from dataclasses import dataclass


@dataclass
class Environment:
    vars: dict[str, str]
    paths: list[str]
