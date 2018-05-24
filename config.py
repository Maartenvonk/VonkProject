from enum import Enum
import logging


def calculate_direction(direction_text):
    logger = logging.getLogger(__name__)
    direction_text = direction_text.lower()
    if direction_text == 'outbound':
        direction = Direction.Outbound
    elif direction_text == 'inbound':
        direction = Direction.Inbound
    elif direction_text == 'all' or direction_text == '':
        direction = Direction.All
    else:
        direction = Direction.Unknown
        logger.warning('Strange direction found %r in row %r' % (direction_text, str(row)))
    return direction


class Direction(Enum):
    Outbound = 0
    Inbound = 1
    Non = 2
    All = 3
    Unknown = 4


class MatchType(Enum):
    Match_Fare = 0
    Match_Subclass = 1
    Match_Unknown = 2


class Config:
    EXCEL_DATE_FORMAT = {'num_format': 'yyyy/mm/dd'}
