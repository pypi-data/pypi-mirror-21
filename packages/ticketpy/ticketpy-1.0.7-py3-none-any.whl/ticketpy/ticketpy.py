"""Client/library for Ticketmaster's Discovery API"""
import requests
from datetime import datetime


class ApiClient:
    """ApiClient for the Ticketmaster Discovery API

    Request URLs end up looking like:
    http://app.ticketmaster.com/discovery/v2/events.json?apikey={api_key}
    """
    base_url = "https://app.ticketmaster.com"
    _method_tmpl = "{url}/{method}.{response_type}"

    def __init__(self, api_key, version='v2', response_type='json'):
        """Initialize the API client.

        :param api_key: Ticketmaster discovery API key
        :param version: API version (default: v2)
        :param response_type: Data format (JSON, XML...) (default: json)
        """
        self.__api_key = api_key  #: Ticketmaster API key
        self.response_type = response_type  #: Response type (json, xml...)
        self.version = version
        self.events = _EventSearch(api_client=self)
        self.venues = _VenueSearch(api_client=self)
        self.attractions = _AttractionSearch(api_client=self)
        self.classifications = _ClassificationSearch(api_client=self)

    @property
    def url(self):
        """Root URL"""
        return "{}/discovery/{}".format(self.base_url, self.version)

    @property
    def events_url(self):
        """URL for */events/*"""
        return self._method_tmpl.format(url=self.url,
                                        method='events',
                                        response_type=self.response_type)

    @property
    def venues_url(self):
        """URL for */venues/*"""
        return self._method_tmpl.format(url=self.url,
                                        method='venues',
                                        response_type=self.response_type)

    @property
    def attractions_url(self):
        """URL for */attractions/*"""
        return self._method_tmpl.format(url=self.url,
                                        method='attractions',
                                        response_type=self.response_type)

    @property
    def classifications_url(self):
        """URL for */attractions/*"""
        return self._method_tmpl.format(url=self.url,
                                        method='classifications',
                                        response_type=self.response_type)

    @property
    def api_key(self):
        """API key"""
        return {'apikey': self.__api_key}

    @api_key.setter
    def api_key(self, api_key):
        self.__api_key = api_key

    def _search(self, method, **kwargs):
        """Generic method for API requests.
        :param method: Search type (events, venues...)
        :param kwargs: Search parameters, ex. venueId, eventId, 
            latlong, radius..
        :return: ``PageIterator``
        """
        # Get basic request URL
        if method == 'events':
            search_url = self.events_url
        elif method == 'venues':
            search_url = self.venues_url
        elif method == 'attractions':
            search_url = self.attractions_url
        elif method == 'classifications':
            search_url = self.classifications_url
        else:
            raise ValueError("Received: '{}' but was expecting "
                             "one of: {}".format(method, ['events', 'venues']))

        # Make updates to parameters. Add apikey, make sure params that
        # may be passed as integers are cast, and cast bools to 'yes' 'no'
        kwargs = {k: v for (k, v) in kwargs.items() if v is not None}
        updates = self.api_key

        for k, v in kwargs.items():
            if k in ['includeTBA', 'includeTBD', 'includeTest']:
                updates[k] = self.__yes_no_only(v)
            elif k in ['size', 'radius', 'marketId']:
                updates[k] = str(v)

        kwargs.update(updates)
        response = requests.get(search_url, params=kwargs).json()

        if 'errors' in response:
            raise ApiException(search_url, kwargs, response)

        return PageIterator(self, **response)

    @staticmethod
    def __yes_no_only(s):
        if s in ['yes', 'no', 'only']:
            pass
        elif s == True:
            s = 'yes'
        elif s == False:
            s = 'no'
        else:
            s = s.lower()
        return s


class ApiException(Exception):
    """Exception thrown for API-related error messages"""
    def __init__(self, url, params, response):
        self.url = url
        del params['apikey']
        self.params = params
        self.errors = response['errors']
        super().__init__()

    def __str__(self):
        tmpl = ("Reason: {detail}\n"
                "Request URL: {url}\n"
                "Query parameters: {sp}\n"
                "Code: {code} ({link})\n"
                "Status: {status}")
        msgs = []
        for e in self.errors:
            msgs.append(tmpl.format(
                url=self.url,
                sp=', '.join('({}={})'.format(k, v) for
                             (k, v) in self.params.items()),
                code=e['code'],
                status=e['status'],
                detail=e['detail'],
                link=e['_links']['about']['href']
            ))
        return '\n'.join(msgs)


class PageIterator:
    """Iterates through API response pages"""

    def __init__(self, api_client, **kwargs):
        self.api_client = api_client  #: Parent API client
        self.page = None  #: Current page
        self.page = self.__page(**kwargs)

        self.start_page = self.page.number  #: Initial page number
        self.current_page = self.start_page  #: Current page number
        self.end_page = self.page.total_pages  #: Final page number

    def __iter__(self):
        return self

    def limit(self, max_pages=10):
        """Limit the number of page requests. Default: 5

        With a default page size of 20, ``limit(max_pages=5`` would 
        return a maximum of 200 items (fewer, if there are fewer results).

        Use this to contain the number of API calls being made, as the 
        API restricts users to a maximum of 5,000 per day. Very 
        broad searches can return a large number of pages.

        To contrast, ``all()`` will automatically request every 
        page available.

        :param max_pages: Maximum number of pages to request. 
            Default: *10*. Set to *None* (or use ``all()``) to return 
            all pages.
        :return: Flat list of results from pages
        """
        if max_pages is None:
            return self.all()

        all_items = []
        for i in range(0, max_pages):
            try:
                all_items += self.next()
            except StopIteration:
                break
        return all_items

    def all(self):
        """Returns a flat list of all results. Queries all possible pages.

        Use ``limit()`` to restrict the number of calls being made.

        :return: Flat list of results
        """
        return [i for item_list in self for i in item_list]

    @staticmethod
    def __page(**kwargs):
        """Instantiate and return a Page(list)"""
        page = kwargs['page']

        links = kwargs['_links']

        if 'next' not in links:
            links_next = None
        else:
            links_next = links['next']['href']

        return Page(
            page['number'],
            page['size'],
            page['totalElements'],
            page['totalPages'],
            links['self']['href'],
            links_next,
            kwargs.get('_embedded', {})
        )

    def next(self):
        # Return initial Page result if we haven't yet
        if self.page.number == self.current_page:
            self.current_page += 1
            return [i for i in self.page]

        # StopIteration if we know we've run out of pages.
        # Check for current>end as empty results still return
        # a page and increment the counter.
        if self.current_page >= self.end_page:
            raise StopIteration

        # Otherwise, +1 our count and pull the next page
        self.current_page += 1
        r = requests.get(self.page.link_next,
                         params=self.api_client.api_key).json()

        self.page = self.__page(**r)

        # If 'next' link goes missing, there were fewer pages than
        # expected for some reason, so bump current_page to end_page to
        # throw StopIteration next time next() is called
        if self.page.link_next is None:
            self.current_page = self.end_page

        return [i for i in self.page]

    __next__ = next


class Page(list):
    """API response page"""

    def __init__(self, number, size, total_elements, total_pages,
                 link_self, link_next, embedded):
        super().__init__([])
        self.number = number  #: Page number
        self.size = size  #: Page size
        self.total_elements = total_elements  #: Total elements (all pages)
        self.total_pages = total_pages  #: Total pages

        self._link_self = link_self  #: Link to this page
        self._link_next = link_next  #: Link to the next page

        # Parse embedded objects and add them to ourself
        items = []
        if 'events' in embedded:
            items = [Event.from_json(e) for e in embedded['events']]
        elif 'venues' in embedded:
            items = [Venue.from_json(v) for v in embedded['venues']]
        elif 'attractions' in embedded:
            items = [Attraction.from_json(a) for a in embedded['attractions']]
        elif 'classifications' in embedded:
            items = [Classification.from_json(cl)
                     for cl in embedded['classifications']]

        for i in items:
            self.append(i)

    @property
    def link_next(self):
        """Link to the next page"""
        link = "{}{}".format(ApiClient.base_url, self._link_next)
        return link.replace('{&sort}', '')

    @property
    def link_self(self):
        """Link to this page"""
        return "{}{}".format(ApiClient.base_url, self._link_self)


# Query/search classes


class BaseSearch:
    attr_map = {
        'start_date_time': 'startDateTime',
        'end_date_time': 'endDateTime',
        'onsale_start_date_time': 'onsaleStartDateTime',
        'onsale_end_date_time': 'onsaleEndDateTime',
        'country_code': 'countryCode',
        'state_code': 'stateCode',
        'venue_id': 'venueId',
        'attraction_id': 'attractionId',
        'segment_id': 'segmentId',
        'segment_name': 'segmentName',
        'classification_name': 'classificationName',
        'classification_id': 'classificationId',
        'market_id': 'marketId',
        'promoter_id': 'promoterId',
        'dma_id': 'dmaId',
        'include_tba': 'includeTBA',
        'include_tbd': 'includeTBD',
        'client_visibility': 'clientVisibility',
        'include_test': 'includeTest',
        'keyword': 'keyword',
        'id': 'id',
        'sort': 'sort',
        'page': 'page',
        'size': 'size',
        'locale': 'locale',
        'latlong': 'latlong'
    }

    def __init__(self, api_client, method, model):
        self.api_client = api_client
        self.method = method
        self.model = model

    def __get(self, **kwargs):
        response = self.api_client._search(self.method, **kwargs)
        return response

    def _get(self, keyword=None, entity_id=None, sort=None, include_test=None,
             page=None, size=None, locale=None, **kwargs):
        """Basic API search request, with only the parameters common to all 
        search functions. Specific searches pass theirs through **kwargs.
        
        :param keyword: Keyword to search on
        :param entity_id: ID of the object type (such as an event ID...)
        :param sort: Sort method
        :param include_test: ['yes', 'no', 'only'] to include test objects in 
            results. Default: *no*
        :param page: Page to return (default: 0)
        :param size: Page size (default: 20)
        :param locale: Locale (default: *en*)
        :param kwargs: Additional search parameters
        :return: 
        """
        # Combine universal parameters and supplied kwargs into single dict,
        # then map our parameter names to the ones expected by the API and
        # make the final request
        search_args = dict(kwargs)
        search_args.update({
            'keyword': keyword,
            'id': entity_id,
            'sort': sort,
            'include_test': include_test,
            'page': page,
            'size': size,
            'locale': locale
        })
        params = self._search_params(**search_args)
        return self.__get(**params)

    def by_id(self, entity_id):
        """Get a specific object by its ID"""
        get_tmpl = "{}/{}/{}"
        get_url = get_tmpl.format(self.api_client.url, self.method, entity_id)
        r = requests.get(get_url, params=self.api_client.api_key).json()
        return self.model.from_json(r)

    def _search_params(self, **kwargs):
        # Update search parameters with kwargs
        kw_map = {}
        for k, v in kwargs.items():
            # If arg is API-friendly (ex: stateCode='GA')
            if k in self.attr_map.keys():
                kw_map[self.attr_map[k]] = v
            elif k in self.attr_map.values():
                kw_map[k] = v

        return {k: v for (k, v) in kw_map.items() if v is not None}


class _VenueSearch(BaseSearch):
    """Queries for venues"""

    def __init__(self, api_client):
        """Init VenueSearch
        
        :param api_client: Instance of `ticketpy.ApiClient`
        """
        super().__init__(api_client, 'venues', Venue)

    def find(self, keyword=None, venue_id=None, sort=None, state_code=None,
             country_code=None, source=None, include_test=None,
             page=None, size=None, locale=None, **kwargs):
        """Search for venues matching provided parameters
        
        :param keyword: Keyword to search on (such as part of the venue name)
        :param venue_id: Venue ID 
        :param sort: Sort method for response (API default: 'name,asc')
        :param state_code: Filter by state code (ex: 'GA' not 'Georgia')
        :param country_code: Filter by country code
        :param source: Filter entities by source (['ticketmaster', 'universe', 
            'frontgate', 'tmr'])
        :param include_test: ['yes', 'no', 'only'], whether to include 
            entities flagged as test in the response (default: 'no')
        :param page: Page number (default: 0)
        :param size: Page size of the response (default: 20)
        :param locale: Locale (default: 'en')
        :return: Venues found matching criteria 
        :rtype: `ticketpy.PageIterator`fff
        """
        r = self._get(keyword, venue_id, sort, include_test, page,
                      size, locale, state_code=state_code,
                      country_code=country_code, source=source, **kwargs)
        return r

    def by_name(self, venue_name, state_code=None, **kwargs):
        """Search for a venue by name.

        :param venue_name: Venue name to search
        :param state_code: Two-letter state code to narrow results (ex 'GA')
            (default: None)
        :return: List of venues found matching search criteria
        """
        return self.find(keyword=venue_name, state_code=state_code, **kwargs)


class _EventSearch(BaseSearch):
    """Abstraction to search API for events"""
    def __init__(self, api_client):
        """Init EventSearch
        
        :param api_client: Instance of `ticketpy.ApiClient`
        """
        super().__init__(api_client, 'events', Event)

    def find(self, sort='date,asc', latlong=None, radius=None, unit=None,
             start_date_time=None, end_date_time=None,
             onsale_start_date_time=None, onsale_end_date_time=None,
             country_code=None, state_code=None, venue_id=None,
             attraction_id=None, segment_id=None, segment_name=None,
             classification_name=None, classification_id=None,
             market_id=None, promoter_id=None, dma_id=None,
             include_tba=None, include_tbd=None, client_visibility=None,
             keyword=None, event_id=None, source=None, include_test=None,
             page=None, size=None, locale=None, **kwargs):
        """Search for events matching given criteria.

        :param sort: Sorting order of search result 
            (default: *'relevance, desc'*)
        :param latlong: Latitude/longitude filter
        :param radius: Radius of area to search
        :param unit: Unit of radius, 'miles' or 'km' (default: miles)
        :param start_date_time: Filter by start date/time.
            Timestamp format: *YYYY-MM-DDTHH:MM:SSZ*
        :param end_date_time: Filter by end date/time.
            Timestamp format: *YYYY-MM-DDTHH:MM:SSZ*
        :param onsale_start_date_time: 
        :param onsale_end_date_time: 
        :param country_code: 
        :param state_code: State code (ex: 'GA' not 'Georgia')
        :param venue_id: Find events for provided venue ID
        :param attraction_id: 
        :param segment_id: 
        :param segment_name: 
        :param classification_name: Filter events by a list of 
            classification name(s) (genre/subgenre/type/subtype/segment)
        :param classification_id: 
        :param market_id: 
        :param promoter_id: 
        :param dma_id: 
        :param include_tba: True to include events with a to-be-announced 
            date (['yes', 'no', 'only'])
        :param include_tbd: True to include an event with a date to be 
            defined (['yes', 'no', 'only'])
        :param client_visibility: 
        :param keyword: 
        :param event_id: Event ID to search 
        :param source: Filter entities by source name: ['ticketmaster', 
            'universe', 'frontgate', 'tmr']
        :param include_test: 'yes' to include test entities in the 
            response. False or 'no' to exclude. 'only' to return ONLY test 
            entities. (['yes', 'no', 'only'])
        :param page: Page number to get (default: 0)
        :param size: Size of page (default: 20)
        :param locale: Locale (default: 'en')
        :return: 
        """

        # Translate parameters to API-friendly parameters
        kw_map = {
            'sort': sort,
            'latlong': latlong,
            'radius': radius,
            'unit': unit,
            'startDateTime': start_date_time,
            'endDateTime': end_date_time,
            'onsaleStartDateTime': onsale_start_date_time,
            'onsaleEndDateTime': onsale_end_date_time,
            'countryCode': country_code,
            'stateCode': state_code,
            'venueId': venue_id,
            'attractionId': attraction_id,
            'segmentId': segment_id,
            'segmentName': segment_name,
            'classificationName': classification_name,
            'classificationId': classification_id,
            'marketId': market_id,
            'promoterId': promoter_id,
            'dmaId': dma_id,
            'includeTBA': include_tba,
            'includeTBD': include_tbd,
            'clientVisibility': client_visibility,
            'keyword': keyword,
            'id': event_id,
            'source': source,
            'includeTest': include_test,
            'page': page,
            'size': size,
            'locale': locale
        }

        r = self._get(keyword, event_id, sort, include_test, page,
                      size, locale, latlong=latlong, radius=radius,
                      unit=unit, start_date_time=start_date_time,
                      end_date_time=end_date_time,
                      onsale_start_date_time=onsale_start_date_time,
                      onsale_end_date_time=onsale_end_date_time,
                      country_code=country_code, state_code=state_code,
                      venue_id=venue_id, attraction_id=attraction_id,
                      segment_id=segment_id, segment_name=segment_name,
                      classification_name=classification_name,
                      classification_id=classification_id,
                      market_id=market_id, promoter_id=promoter_id,
                      dma_id=dma_id, include_tba=include_tba,
                      include_tbd=include_tbd,
                      client_visibility=client_visibility, **kwargs)

        return r

    def by_location(self, latitude, longitude, radius='10', unit='miles',
                    sort='relevance, desc', **kwargs):
        """
        Searches events within a radius of a latitude/longitude coordinate.

        :param latitude: Latitude of radius center
        :param longitude: Longitude of radius center
        :param radius: Radius to search outside given latitude/longitude
        :param unit: Unit of radius ('miles' or 'km'),
        :param sort: Sort method. (Default: *relevance, desc*). If changed, 
            you may get wonky results (*date, asc* returns far-away events)
        :return: List of events within that area
        """
        latitude = str(latitude)
        longitude = str(longitude)
        radius = str(radius)
        latlong = "{lat},{long}".format(lat=latitude, long=longitude)
        return self.find(latlong=latlong, radius=radius, unit=unit, **kwargs)


class _AttractionSearch(BaseSearch):
    """Query class for Attractions"""

    def __init__(self, api_client):
        self.api_client = api_client
        super().__init__(api_client, 'attractions', Attraction)

    def find(self, sort=None, keyword=None, attraction_id=None,
             source=None, include_test=None, page=None, size=None,
             locale=None, **kwargs):
        """
        
        :param sort: Response sort type (API default: *name,asc*)
        :param keyword: 
        :param attraction_id: 
        :param source: 
        :param include_test: Include test attractions (['yes', 'no', 'only'])
        :param page: 
        :param size: 
        :param locale: API default: *en*
        :param kwargs: 
        :return: 
        """
        r = self._get(keyword, attraction_id, sort, include_test,
                      page, size, locale, source=source, **kwargs)
        return r


class _ClassificationSearch(BaseSearch):
    """Classification search/query class"""
    #: ``BaseQuery.by_id()`` renamed for this class, as classifications
    #: don't have IDs, but the same query will return IDs for segments,
    #: genres and subgenres (whichever matches).
    #: ``ClassificationQuery.by_id()`` will return the correct object,
    #: rather than the entire parent structure of any given ID
    query_subclass_id = BaseSearch.by_id

    def __init__(self, api_client):
        super().__init__(api_client, 'classifications', Classification)

    def find(self, sort=None, keyword=None, classification_id=None,
             source=None, include_test=None, page=None, size=None,
             locale=None, **kwargs):
        """Search classifications

        :param sort: Response sort type (API default: *name,asc*)
        :param keyword: 
        :param classification_id: 
        :param source: 
        :param include_test: Include test classifications 
            (['yes', 'no', 'only'])
        :param page: 
        :param size: 
        :param locale: API default: *en*
        :param kwargs: 
        :return: 
        """
        return self._get(keyword, classification_id, sort, include_test,
                         page, size, locale, source=source, **kwargs)

    def by_id(self, entity_id):
        """Returns a ``Segment``, ``Genre`` or ``SubGenre`` matching the 
        given entity ID. If no matching IDs are found, returns ``None``
        
        :param entity_id: Segment, genre or subgenre ID
        :return: ``Segment``, ``Genre`` or ``SubGenre``, depending which 
            matches the ID.
        """
        cl = self.query_subclass_id(entity_id)
        # No segment = no match
        if not cl.segment:
            return None
        elif cl.segment.id == entity_id:
            return cl.segment

        # Check deeper, return whatever object matches ``entity_id``
        for genre in cl.segment.genres:
            if genre.id == entity_id:
                return genre
            for subgenre in genre.subgenres:
                if subgenre.id == entity_id:
                    return subgenre

        # Return ``None`` if one still wasn't found for some reason
        return None


# API object models


def _assign_links(obj, json_obj):
    """Assigns ``links`` attribute to the given object from JSON
    
    :param obj: Model object (such as an ``Event()`` object)
    :param json_obj: JSON from API response
    :return: 
    """
    # If the structure doesn't have _links, don't bother
    json_links = json_obj.get('_links')
    if not json_links:
        obj.links = None
    else:
        obj_links = {}
        for k, v in json_links.items():
            # Normal structure with {link_name: {'href': url}}
            if 'href' in v:
                obj_links[k] = v['href']
            # Some responses add objects into the links section, leave as-is
            else:
                obj_links[k] = v
        obj.links = obj_links


class Venue:
    """A Ticketmaster venue
    
    The JSON returned from the Discovery API looks something like this 
    (*edited for brevity*):
    
    .. code-block:: json
    
        {
            "id": "KovZpaFEZe",
            "name": "The Tabernacle",
            "url": "http://www.ticketmaster.com/venue/115031",
            "timezone": "America/New_York",
            "address": {
                "line1": "152 Luckie Street"
            },
            "city": {
                "name": "Atlanta"
            },
            "postalCode": "30303",
            "state": {
                "stateCode": "GA",
                "name": "Georgia"
            },
            "country": {
                "name": "United States Of America",
                "countryCode": "US"
            },
            "location": {
                "latitude": "33.758688",
                "longitude": "-84.391449"
            },
            "social": {
                "twitter": {
                    "handle": "@TabernacleATL"
                }
            },
            "markets": [
                {
                    "id": "10"
                }
            ]
        }

    
    """
    def __init__(self, name=None, address=None, city=None, state_code=None,
                 postal_code=None, latitude=None, longitude=None,
                 markets=None, url=None, box_office_info=None,
                 dmas=None, general_info=None, venue_id=None,
                 social=None, timezone=None, images=None,
                 parking_detail=None, accessible_seating_detail=None,
                 links=None):
        self.name = name  #: Venue's name
        self.id = venue_id  #: Venue ID (use to look up events)
        self.address = address  #: Street address (first line)
        self.postal_code = postal_code  #: Zip/postal code
        self.city = city  #: City name
        self.state_code = state_code  #: State code (ex: 'GA' not 'Georgia')
        self.latitude = latitude  #: Latitude
        self.longitude = longitude  #: Longitude
        self.timezone = timezone  #: Timezone venue's located in
        self.url = url  #: Ticketmaster internal venue URL
        self.box_office_info = box_office_info
        self.dmas = dmas  # TODO what is this
        self.markets = markets  #: List of market IDs
        self.general_info = general_info  #: General info on the venue
        self.social = social  #: Social media links (Twitter, etc)
        self.images = images  #: Ticketmaster venue image links
        self.parking_detail = parking_detail  #: Parking details
        self.accessible_seating_detail = accessible_seating_detail
        self.links = links

    @property
    def location(self):
        """All location-based data (full address, lat/lon, timezone"""
        return {
            'address': self.address,
            'postal_code': self.postal_code,
            'city': self.city,
            'state_code': self.state_code,
            'timezone': self.timezone,
            'latitude': self.latitude,
            'longitude': self.longitude
        }

    def __str__(self):
        return "'{}' at {} in {} {}".format(self.name, self.address,
                                            self.city, self.state_code)

    @staticmethod
    def from_json(json_venue):
        """Create a `Venue` object from the API response's JSON data
        
        :param json_venue: Deserialized JSON from API response
        :return: `ticketpy.Venue`
        """
        v = Venue()
        v.id = json_venue['id']
        v.name = json_venue['name']
        v.url = json_venue.get('url')

        if 'markets' in json_venue:
            v.markets = [m['id'] for m in json_venue['markets']]

        # Location data
        v.postal_code = json_venue.get('postalCode')
        if 'city' in json_venue:
            v.city = json_venue['city']['name']
        if 'address' in json_venue:
            v.address = json_venue['address']['line1']
        if 'location' in json_venue:
            v.latitude = json_venue['location']['latitude']
            v.longitude = json_venue['location']['longitude']
        if 'state' in json_venue:
            v.state_code = json_venue['state']['stateCode']

        # Other general data
        v.general_info = json_venue.get('generalInfo')
        v.box_office_info = json_venue.get('boxOfficeInfo')
        v.dmas = json_venue.get('dmas')
        v.social = json_venue.get('social')
        v.timezone = json_venue.get('timezone')
        v.images = json_venue.get('images')
        v.parking_detail = json_venue.get('parkingDetail')
        v.accessible_seating_detail = json_venue.get('accessibleSeatingDetail')
        _assign_links(v, json_venue)
        return v


class Event:
    """Ticketmaster event.
    
    The JSON returned from the Discovery API (at least, as far as 
    what's being used here) looks like:
    
    .. code-block:: json
    
        {
            "name": "Event name",
            "dates": {
                "start": {
                    "localDate": "2019-04-01",
                    "localTime": "2019-04-01T23:00:00Z"
                },
                "status": {
                    "code": "onsale"
                }
            },
            "classifications": [
                {
                    "genre": {
                        "name": "Rock"
                    }
                },
                {
                    "genre": {
                        "name": "Funk"
                    }
                }
            ],
            "priceRanges": [
                {
                    "min": 10,
                    "max": 25
                }
            ],
            "_embedded": {
                "venues": [
                    {
                        "name": "The Tabernacle"
                    }
                ]
            }
        }
    """
    def __init__(self, event_id=None, name=None, start_date=None,
                 start_time=None, status=None, price_ranges=None,
                 venues=None, utc_datetime=None, classifications=None,
                 links=None):
        self.id = event_id
        self.name = name
        #: **Local** start date (*YYYY-MM-DD*)
        self.local_start_date = start_date
        #: **Local** start time (*HH:MM:SS*)
        self.local_start_time = start_time
        #: Sale status (such as *Cancelled, Offsale...*)
        self.status = status
        #: List of classifications
        self.classifications = classifications

        #: Price ranges found for tickets
        self.price_ranges = price_ranges
        #: List of ``ticketpy.Venue`` objects associated with this event
        self.venues = venues

        self.__utc_datetime = None
        if utc_datetime is not None:
            self.utc_datetime = utc_datetime

        self.links = links

    @property
    def utc_datetime(self):
        """Start date/time in UTC (Format: *YYYY-MM-DDTHH:MM:SSZ*)
        
        :return: Start date/time in UTC
        :rtype: ``datetime``
        """
        return self.__utc_datetime

    @utc_datetime.setter
    def utc_datetime(self, utc_datetime):
        if not utc_datetime:
            self.__utc_datetime = None
        else:
            ts_format = "%Y-%m-%dT%H:%M:%SZ"
            self.__utc_datetime = datetime.strptime(utc_datetime, ts_format)

    def __str__(self):
        tmpl = ("Event:        {event_name}\n"
                "Venue(s):     {venues}\n"
                "Start date:   {start_date}\n"
                "Start time:   {start_time}\n"
                "Price ranges: {ranges}\n"
                "Status:       {status}\n"
                "Genres:       {genres}\n")

        ranges = ['-'.join([str(pr['min']), str(pr['max'])])
                  for pr in self.price_ranges]

        if self.classifications:
            genres = [cl.genre.name for cl in self.classifications]

        return tmpl.format(
            event_name=self.name,
            venues=' / '.join([str(v) for v in self.venues]),
            start_date=self.local_start_date,
            start_time=self.local_start_time,
            ranges=', '.join(ranges),
            status=self.status,
            genres=', '.join(genres)
        )

    @staticmethod
    def from_json(json_event):
        """Creates an ``Event`` from API's JSON response
        
        :param json_event: Deserialized JSON object from API response
        :return: `ticketpy.Event`
        """
        e = Event()
        e.id = json_event['id']
        e.name = json_event.get('name')

        # Dates/times
        dates = json_event.get('dates')
        start_dates = dates.get('start', {})
        e.local_start_date = start_dates.get('localDate')
        e.local_start_time = start_dates.get('localTime')
        e.utc_datetime = start_dates.get('dateTime')

        # Event status (ex: 'onsale')
        status = dates.get('status', {})
        e.status = status.get('code')

        if 'classifications' in json_event:
            e.classifications = [EventClassification.from_json(cl)
                                 for cl in json_event['classifications']]

        # min/max price ranges
        price_ranges = []
        if 'priceRanges' in json_event:
            for pr in json_event['priceRanges']:
                price_ranges.append({
                    'min': pr['min'],
                    'max': pr['max']
                })
        e.price_ranges = price_ranges

        # venue list (occasionally >1 venue)
        venues = []
        if 'venues' in json_event.get('_embedded', {}):
            for v in json_event['_embedded']['venues']:
                venues.append(Venue.from_json(v))
        e.venues = venues
        _assign_links(e, json_event)
        return e


class Attraction:
    """Attraction object"""

    def __init__(self, attraction_id=None, attraction_name=None, url=None,
                 classifications=None, images=None, test=None, links=None):
        """

        :param attraction_id: Attraction ID
        :param attraction_name: Name of the attraction (ex: '*U2*'
        :param url: Ticketmaster URL
        :param classifications: Genres, subgenres, etc
        :param images: Images
        :param test: Test (bool)
        """
        self.id = attraction_id
        self.name = attraction_name
        self.url = url
        self.classifications = classifications
        self.images = images
        self.test = test
        self.links = links

    @staticmethod
    def from_json(json_obj):
        """Convert JSON object to ``Attraction`` object"""
        att = Attraction()
        att.id = json_obj.get('id')
        att.name = json_obj.get('name')
        att.url = json_obj.get('url')
        att.test = json_obj.get('test')
        att.images = json_obj.get('images')
        classifications = json_obj.get('classifications')
        att.classifications = [Classification.from_json(cl)
                               for cl in classifications]
        _assign_links(att, json_obj)
        return att

    def __str__(self):
        return self.name if self.name is not None else 'Unknown'



class EventClassification:
    """Classification as it's represented in event search results
    
    See Classification() for results from classification searches
    """
    def __init__(self, genre=None, subgenre=None, segment=None,
                 classification_type=None, classification_subtype=None,
                 primary=None, links=None):
        self.genre = genre  #: ``Genre()``
        self.subgenre = subgenre  #: ``SubGenre()``
        self.segment = segment  #: ``Segment()``
        self.type = classification_type  #: ``ClassificationType()``
        self.subtype = classification_subtype  #: ``ClassificationSubType()``
        self.primary = primary  #: Bool
        self.links = links  #: API links

    @staticmethod
    def from_json(json_obj):
        """Create/return ``EventClassification`` object from JSON"""
        ec = EventClassification()
        ec.primary = json_obj.get('primary')

        segment = json_obj.get('segment')
        if segment:
            ec.segment = Segment.from_json(segment)

        genre = json_obj.get('genre')
        if genre:
            ec.genre = Genre.from_json(genre)

        subgenre = json_obj.get('subGenre')
        if subgenre:
            ec.subgenre = SubGenre.from_json(subgenre)

        cl_t = json_obj.get('type')
        if cl_t:
            ec.type = ClassificationType(cl_t['id'], cl_t['name'])

        cl_st = json_obj.get('subType')
        if cl_st:
            ec.subtype = ClassificationSubType(cl_st['id'], cl_st['name'])

        _assign_links(ec, json_obj)
        return ec


class Classification:
    """Classification object (segment/genre/sub-genre)
    
    For the structure returned by ``EventSearch``, see ``EventClassification``
    """
    def __init__(self, segment=None, classification_type=None, subtype=None,
                 primary=None, links=None):
        self.segment = segment  #: ``Segment()``
        self.type = classification_type  #: ``ClassificationType()``
        self.subtype = subtype  #: ``ClassifictionSubType()``
        self.primary = primary  #: Boolean
        self.links = links  #: API links

    @staticmethod
    def from_json(json_obj):
        """Create/return ``Classification()`` from JSON"""
        cl = Classification()
        cl.primary = json_obj.get('primary')

        if 'segment' in json_obj:
            cl.segment = Segment.from_json(json_obj['segment'])

        if 'type' in json_obj:
            cl_t = json_obj['type']
            cl.type = ClassificationType(cl_t['id'], cl_t['name'])

        if 'subType' in json_obj:
            cl_st = json_obj['subType']
            cl.subtype = ClassificationSubType(cl_st['id'], cl_st['name'])

        _assign_links(cl, json_obj)
        return cl


class ClassificationType:
    """Type of ``Classification``"""
    def __init__(self, type_id=None, type_name=None, subtypes=None):
        self.id = type_id
        self.name = type_name
        self.subtypes = subtypes

    def __str__(self):
        return self.name if self.name is not None else 'Unknown'


class ClassificationSubType:
    """Subtype of ``ClassificationType``"""
    def __init__(self, type_id=None, type_name=None):
        self.id = type_id
        self.name = type_name

    def __str__(self):
        return self.name if self.name is not None else 'Unknown'


class Segment:
    """Segment, under ``Classification``"""
    def __init__(self, segment_id=None, segment_name=None, genres=None,
                 links=None):
        self.id = segment_id
        self.name = segment_name
        self.genres = genres  #: List of ``Genre`` objects
        self.links = links  #: API links

    @staticmethod
    def from_json(json_obj):
        """Create and return a ``Segment`` from JSON"""
        seg = Segment()
        seg.id = json_obj['id']
        seg.name = json_obj['name']

        if '_embedded' in json_obj:
            genres = json_obj['_embedded']['genres']
            seg.genres = [Genre.from_json(g) for g in genres]

        _assign_links(seg, json_obj)
        return seg

    def __str__(self):
        return self.name if self.name is not None else 'Unknown'


class Genre:
    """Genre type"""
    def __init__(self, genre_id=None, genre_name=None, subgenres=None,
                 links=None):
        self.id = genre_id
        self.name = genre_name
        self.subgenres = subgenres  #: List of ``SubGenre`` objects
        self.links = links  #: API links

    @staticmethod
    def from_json(json_obj):
        g = Genre()
        g.id = json_obj.get('id')
        g.name = json_obj.get('name')
        if '_embedded' in json_obj:
            embedded = json_obj['_embedded']
            subgenres = embedded['subgenres']
            g.subgenres = [SubGenre.from_json(sg) for sg in subgenres]

        _assign_links(g, json_obj)
        return g

    def __str__(self):
        return self.name if self.name is not None else 'Unknown'


class SubGenre:
    """SubGenre type under ``Genre``"""
    def __init__(self, subgenre_id=None, subgenre_name=None, links=None):
        self.id = subgenre_id
        self.name = subgenre_name
        self.links = links

    @staticmethod
    def from_json(json_obj):
        sg = SubGenre()
        sg.id = json_obj['id']
        sg.name = json_obj['name']
        _assign_links(sg, json_obj)
        return sg

    def __str__(self):
        return self.name if self.name is not None else 'Unknown'







