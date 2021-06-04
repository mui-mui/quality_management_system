from asamm.asamm_config import AsammConfiguration
from utils.handlers import AllExceptionsHandled

exception_handler = AllExceptionsHandled(logged_call=True)

__ALL__ = [AsammConfiguration, exception_handler]