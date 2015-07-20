"""Implementation of a GeoIP based search source."""

from ichnaea.api.locate.constants import DataSource
from ichnaea.api.locate.source import (
    CountrySource,
    PositionSource,
    Source,
)


class GeoIPSource(Source):
    """A GeoIPSource returns search results based on a GeoIP database."""

    fallback_field = 'ipf'
    source = DataSource.geoip

    def search(self, query):
        result = self.result_type()
        source_used = False

        if query.ip:
            source_used = True

        # The GeoIP record is already available on the query object,
        # there's no need to do a lookup again.
        geoip = query.geoip
        if geoip:
            result = self.result_type(
                lat=geoip['latitude'],
                lon=geoip['longitude'],
                accuracy=geoip['accuracy'],
                country_code=geoip['country_code'],
                country_name=geoip['country_name'],
            )

        if source_used:
            query.emit_source_stats(self.source, result)

        return result


class GeoIPCountrySource(GeoIPSource, CountrySource):
    """A GeoIPSource returning country results."""


class GeoIPPositionSource(GeoIPSource, PositionSource):
    """A GeoIPSource returning position results."""
