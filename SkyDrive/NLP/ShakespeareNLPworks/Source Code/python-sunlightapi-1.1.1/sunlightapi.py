""" Python library for interacting with the Sunlight Labs API.

    The Sunlight Labs API (http://services.sunlightlabs.com/api/) provides
    basic legislator data, conversion between ids, and zipcode-district
    lookups.
"""

__author__ = "James Turk (jturk@sunlightfoundation.com)"
__version__ = "1.1.1"
__copyright__ = "Copyright (c) 2012 Sunlight Labs"
__license__ = "BSD"

import sys
import warnings

if sys.version_info[0] == 3:
    from urllib.parse import urlencode
    from urllib.request import urlopen
    from urllib.error import HTTPError
else:
    from urllib import urlencode
    from urllib2 import urlopen
    from urllib2 import HTTPError

try:
    import json
except ImportError:
    import simplejson as json

import warnings
warnings.warn('python-openstates is deprecated in favor of python-sunlight\n'
              'http://python-sunlight.readthedocs.org/', DeprecationWarning)

class SunlightApiError(Exception):
    """ Exception for Sunlight API errors """

# results #
class SunlightApiObject(object):
    def __init__(self, d):
        self.__dict__ = d

    def __repr__(self):
        return '%s(%r)' % (self.__class__.__name__, self.__dict__)


class Legislator(SunlightApiObject):
    def __str__(self):
        if self.nickname:
            fname = self.nickname
        else:
            fname = self.firstname
        return '%s. %s %s (%s-%s)' % (self.title, fname, self.lastname,
                                      self.party, self.state)

class LegislatorSearchResult(SunlightApiObject):
    def __init__(self, d):
        self.legislator = Legislator(d['legislator'])
        self.score = d['score']

    def __str__(self):
        return '%s %s' % (self.score, self.legislator)

class Committee(SunlightApiObject):
    def __init__(self, d):
        self.__dict__ = d
        self.subcommittees = [Committee(sc['committee']) for sc in getattr(self, 'subcommittees', [])]
        self.members = [Legislator(m['legislator']) for m in getattr(self, 'members', [])]

    def __str__(self):
        return '%s' % (self.name)

class District(SunlightApiObject):
    def __str__(self):
        return '%s-%s' % (self.state, self.number)

# namespaces #

class sunlight(object):

    apikey = None

    @staticmethod
    def _apicall(func, params):
        if sunlight.apikey is None:
            raise SunlightApiError('Missing sunlight apikey')

        url = 'http://services.sunlightlabs.com/api/%s.json?apikey=%s&%s' % \
              (func, sunlight.apikey, urlencode(params, True))
        try:
            response = urlopen(url).read().decode()
            return json.loads(response)['response']
        except HTTPError, e:
            raise SunlightApiError(e.read())
        except (ValueError, KeyError), e:
            raise SunlightApiError('Invalid Response')

    class legislators(object):
        @staticmethod
        def get(**kwargs):
            result = sunlight._apicall('legislators.get', kwargs)['legislator']
            return Legislator(result)

        @staticmethod
        def getList(**kwargs):
            results = sunlight._apicall('legislators.getList', kwargs)
            return [Legislator(l['legislator']) for l in results['legislators']]

        @staticmethod
        def search(name, threshold=0.9, all_legislators=False):
            params =  {'name':name, 'threshold': threshold}
            if all_legislators:
                params['all_legislators'] = 1
            results = sunlight._apicall('legislators.search', params)['results']
            return [LegislatorSearchResult(r['result']) for r in results]

        @staticmethod
        def allForZip(zipcode):
            results = sunlight._apicall('legislators.allForZip', {'zip':zipcode})
            return [Legislator(l['legislator']) for l in results['legislators']]

        @staticmethod
        def allForLatLong(latitude, longitude):
            params = {'latitude':latitude, 'longitude':longitude}
            results = sunlight._apicall('legislators.allForLatLong', params)
            return [Legislator(l['legislator']) for l in results['legislators']]

    class committees(object):
        @staticmethod
        def get(committee_id):
            results = sunlight._apicall('committees.get', {'id':committee_id})
            return Committee(results['committee'])

        @staticmethod
        def getList(chamber):
            results = sunlight._apicall('committees.getList', {'chamber':chamber})
            return [Committee(c['committee']) for c in results['committees']]

        @staticmethod
        def allForLegislator(bioguide_id):
            results = sunlight._apicall('committees.allForLegislator',
                                        {'bioguide_id': bioguide_id})
            return [Committee(c['committee']) for c in results['committees']]

    class districts(object):
        @staticmethod
        def getDistrictsFromZip(zipcode):
            results = sunlight._apicall('districts.getDistrictsFromZip', {'zip':zipcode})
            return [District(r['district']) for r in results['districts']]

        @staticmethod
        def getDistrictFromLatLong(latitude, longitude):
            params = {'latitude':latitude, 'longitude':longitude}
            result = sunlight._apicall('districts.getDistrictFromLatLong', params)
            return District(result['districts'][0]['district'])
