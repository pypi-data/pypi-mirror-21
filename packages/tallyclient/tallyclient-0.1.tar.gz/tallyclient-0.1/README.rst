tallyclient
-----------

tallyclient is a super simple metrics client that has two data structures similar to statsd,
counters and gauges. While statsd is simple, it still does some under the hood aggregation
to support high volumes. tallyclient's server is about simple collecting and simply stores
the time series data in a sql database to be used later.

here is some usage::

    >>> from tallyclient import TallyClient
    >>> client = TallyClient('localhost', 8173)
    >>> client.count("login.success")
    >>> client.gauge("login.response_time", 422)  # only int values allowed
