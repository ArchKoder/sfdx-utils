from sys import platform

from sfdxUtilitesConstants import (PLATFORM_LINUX, PLATFORM_OS_X,
                                   PLATFORM_WINDOWS)


class PlatformHelper:
    def __init__(this) -> None:
        if PLATFORM_LINUX in platform:
            this.platform = PLATFORM_LINUX

        elif "darwin" == platform:
            this.platform = PLATFORM_OS_X

        elif "win32" == platform:
            this.platform == PLATFORM_WINDOWS

        this.__lineEnding = None
    
        @property
        def lineEnding(this):
            if this.__lineEnding == None:
                platform2LineEnding = {
                    PLATFORM_LINUX : 'LF',
                    PLATFORM_OS_X : 'LF',
                    PLATFORM_WINDOWS : 'CRLF'
                }
                this.__lineEnding = platform2LineEnding.get(this.platform,None)
            return this.__lineEnding

        @property.setter
        def lineEnding(this,value):
            raise Exception('This property is os-dependant and can not be set')