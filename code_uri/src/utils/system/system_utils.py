from sys import platform
from src.utils.system.enum.system_platform import SystemPlatform


def check_platform() -> SystemPlatform:
    return SystemPlatform(platform)
