#
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
#

import os
import urllib2

from ocw.esgf.constants import DEFAULT_ESGF_SEARCH
from ocw.esgf.download import download
from ocw.esgf.logon import logon
from ocw.esgf.search import SearchClient
import ocw.data_source.local as local

from bs4 import BeautifulSoup
import requests


def load_dataset(dataset_id,
                 variable_name,
                 esgf_username,
                 esgf_password,
                 search_url=DEFAULT_ESGF_SEARCH,
                 elevation_index=0,
                 name='',
                 save_path='/tmp',
                 **additional_constraints):
    ''' Load an ESGF dataset.

    :param dataset_id: The ESGF ID of the dataset to load.
    :type dataset_id: :mod:`string`

    :param variable_name: The variable to load.
    :type variable_name: :mod:`string`

    :param esgf_username: ESGF OpenID value to use for authentication.
    :type esgf_username: :mod:`string`

    :param esgf_password: ESGF Password to use for authentication.
    :type esgf_password: :mod:`string`

    :param search_url: (Optional) The ESGF node to use for searching. Defaults
        to the Jet Propulsion Laboratory node.
    :type search_url: :mod:`string`

    :param elevation_index: (Optional) The elevation level to strip out when
        loading the dataset using ocw.data_source.local.
    :type elevation_index: :class:`int`

    :param name: (Optional) A name for the loaded dataset.
    :type name: :mod:`string`

    :param save_path: (Optional) Path to where downloaded files should be saved.
    :type save_path: :mod:`string`

    :param additional_constraints: (Optional) Additional key,value pairs to
        pass as constraints to the search wrapper. These can be anything found
        on the ESGF metadata page for a dataset.

    :returns: A :class:`list` of :class:`dataset.Dataset` contained the
        requested dataset. If the dataset is stored in multiple files each will
        be loaded into a separate :class:`dataset.Dataset`.

    :raises ValueError: If no dataset can be found for the supplied ID and
        variable, or if the requested dataset is a multi-file dataset.
    '''
    download_data = _get_file_download_data(url=search_url,
                                            dataset_id=dataset_id,
                                            variable=variable_name)

    datasets = []
    for url, var in download_data:
        _download_files([url],
                        esgf_username,
                        esgf_password,
                        download_directory=save_path)

        file_save_path = os.path.join(save_path, url.split('/')[-1])
        datasets.append(local.load_file(file_save_path,
                                        var,
                                        name=name,
                                        elevation_index=elevation_index))

    origin = {
        'source': 'esgf',
        'dataset_id': dataset_id,
        'variable': variable_name
    }
    for ds in datasets:
        ds.origin = origin

    return datasets


def _get_file_download_data(dataset_id, variable, url=DEFAULT_ESGF_SEARCH):
    ''''''
    url += '?type=File&dataset_id={}&variable={}'
    url = url.format(dataset_id, variable)

    r = requests.get(url)
    xml = BeautifulSoup(r.content, "html.parser")

    dont_have_results = not bool(xml.response.result['numfound'])

    if dont_have_results:
        err = "esgf.load_dataset: No files found for specified dataset."
        raise ValueError(err)

    # Split out URLs for dataset download along with variable names for each
    # of those files.
    url_groups = xml.response.result.findAll('arr', {'name': 'url'})
    variable_groups = xml.response.result.findAll('arr', {'name': 'variable'})

    urls = [group.findAll('str')[0].string.split('|')[0]
            for group in url_groups]
    variables = [group.findAll('str')[0].string
                 for group in variable_groups]

    return zip(urls, variables)


def _download_files(file_urls, username, password, download_directory='/tmp'):
    ''''''
    try:
        logon(username, password)
    except urllib2.HTTPError:
        raise ValueError('esgf._download_files: Invalid login credentials')

    for url in file_urls:
        download(url, toDirectory=download_directory)
