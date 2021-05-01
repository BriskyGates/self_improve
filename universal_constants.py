import arrow

TIME_FORMAT = 'YYYYMMDD-HHmmss'

FORMAT_TIME = arrow.utcnow().format(TIME_FORMAT)
