import urllib

import requests
from flarecast.utils.rest_exception import RestException


class PropertyServiceClient(object):
    __ADD_PROPERTY = '/property/%s'
    __ADD_PROPERTY_BY_DATASET = '/property/%s/%s'

    __INSERT_PROPERTIES = '/property/bulk'
    __INSERT_PROPERTIES_BY_DATASET = '/property/%s/bulk'

    __ADD_DATASET = '/dataset'
    __INSERT_DATASET = '/dataset/bulk'
    __GET_DATASET = '/dataset/%s'
    __GET_DATASETS = '/dataset/list'

    __ADD_REGION = '/region/%s'
    __INSERT_REGIONS = '/region/%s/bulk'
    __DELETE_REGIONS = '/region/%s/bulk%s'

    __QUERY_PROPERTIES = '/property/%s/list%s'
    __QUERY_PROPERTIES_BY_OBS_DATE = '/property/%s/%s/list%s'
    __QUERY_PROPERTIES_EVOLUTION = '/property/%s/%s/%s/list%s'

    __INSERT_LINK_URL = '/link/bulk'
    __QUERY_LINKS_BY_TIME_RANGE = '/link/%s/%s/%s/list%s'
    __QUERY_LINKS_BY_FC_ID = '/link/%s/%s/list'
    __QUERY_LINK_GRAPH = '/link/%s/%s/graph'

    def __init__(self, property_db_url):
        self.property_db_url = property_db_url

    # -- delete --

    def delete_regions(self, dataset, sirql_arguments=''):
        if sirql_arguments != '':
            sirql_arguments = '?' + sirql_arguments

        url = self.property_db_url + self.__DELETE_REGIONS % (
            dataset,
            sirql_arguments)
        return self.__delete_request(url)

    # -- inserts --

    def insert_regions(self, dataset, property_groups):
        url = self.property_db_url + self.__INSERT_REGIONS % (
            dataset)
        return self.__post_request(url, property_groups)

    def insert_properties(self, properties):
        url = self.property_db_url + self.__INSERT_PROPERTIES
        return self.__post_request(url, properties)

    # todo: name this properly
    def insert_properties_as_dataset(self, dataset, properties):
        url = self.property_db_url + \
            self.__INSERT_PROPERTIES_BY_DATASET % \
            dataset
        return self.__post_request(url, properties)

    def insert_datasets(self, dataset_list):
        url = self.property_db_url + self.__INSERT_DATASET
        return self.__post_request(url, dataset_list)

    def insert_links(self, link_list):
        url = self.property_db_url + self.__INSERT_LINK_URL
        return self.__post_request(url, link_list)

    # -- add --

    def add_dataset(self, name):
        url = self.property_db_url + self.__ADD_DATASET
        return self.__post_request(url, name)

    def add_region(self, dataset, time_start, **attributes):
        group = {'time_start': time_start}
        group.update(attributes)

        url = self.property_db_url + self.__ADD_REGION % dataset
        return self.__post_request(url, group)

    def add_properties(self, region_fc_id, dataset=None,
                       **properties):
        props = {region_fc_id: properties}

        if dataset is None:
            return self.insert_properties(props)

        url = self.property_db_url + self.__ADD_PROPERTY_BY_DATASET % (
            dataset, urllib.quote(region_fc_id, safe=''))
        return self.__post_request(url, properties)

    def add_link(self, source, target, link_type, description=''):
        link = {'source': source,
                'target': target,
                'type': link_type,
                'description': description}
        return self.insert_links([link])

    # -- get --

    def get_properties(self, dataset, sirql_arguments=''):
        if sirql_arguments != '':
            sirql_arguments = '?' + sirql_arguments

        url = self.property_db_url + self.__QUERY_PROPERTIES % (
            dataset,
            sirql_arguments)

        return self.__get_request(url)

    def get_properties_by_obs_date(self, dataset, obs_date,
                                   sirql_arguments=''):
        if sirql_arguments != '':
            sirql_arguments = '?' + sirql_arguments

        query_str = self.__QUERY_PROPERTIES_BY_OBS_DATE % (
            dataset, obs_date, sirql_arguments
        )
        url = self.property_db_url + query_str
        return self.__get_request(url)

    def get_properties_by_time_range(self,
                                     dataset,
                                     from_date,
                                     to_date,
                                     sirql_arguments=''):

        # add time-range query
        range_query = 'time_start=between("%s", "%s")' % (from_date, to_date)
        sirql_arguments = '&'.join([sirql_arguments, range_query])

        if sirql_arguments != '':
            sirql_arguments = '?' + sirql_arguments

        query_str = self.__QUERY_PROPERTIES % (
            dataset, sirql_arguments
        )
        url = self.property_db_url + query_str
        return self.__get_request(url)

    def get_property_evolution(self,
                               dataset,
                               from_date,
                               to_date,
                               property_name,
                               sirql_arguments=''):
        if sirql_arguments != '':
            sirql_arguments = '?' + sirql_arguments

        # add query

        query_str = self.__QUERY_PROPERTIES_EVOLUTION % (
            dataset, from_date, to_date, sirql_arguments
        )
        url = self.property_db_url + query_str
        return self.__get_request(url)

    def get_dataset(self, dataset):
        url = self.property_db_url + self.__GET_DATASET % dataset
        return self.__get_request(url)

    def get_datasets(self):
        url = self.property_db_url + self.__GET_DATASETS
        return self.__get_request(url)

    def get_links_by_time_range(self, link_type, from_date, to_date,
                                sirql_arguments=''):
        if sirql_arguments != '':
            sirql_arguments = '?' + sirql_arguments
        query_str = self.__QUERY_LINKS_BY_TIME_RANGE % (
            link_type, from_date, to_date, sirql_arguments
        )
        url = self.property_db_url + query_str
        return self.__get_request(url)

    def get_links(self, fc_id, link_type):
        url = self.property_db_url + self.__QUERY_LINKS_BY_FC_ID % (
            fc_id, link_type)
        return self.__get_request(url)

    def get_link_graph(self, fc_id, link_type):
        url = self.property_db_url + self.__QUERY_LINK_GRAPH % (
            fc_id, link_type)
        return self.__get_request(url)

    @staticmethod
    def __post_request(url, payload):
        headers = {'Content-Type': 'application/json'}
        r = requests.post(url, json=payload, headers=headers)

        if r.status_code != 200:
            raise RestException(r)

        return r.json()

    @staticmethod
    def __delete_request(url):
        r = requests.delete(url)

        if r.status_code != 200:
            raise RestException(r)

        return r.text

    @staticmethod
    def __get_request(url):
        r = requests.get(url)

        if r.status_code != 200:
            raise RestException(r)

        return r.json()
