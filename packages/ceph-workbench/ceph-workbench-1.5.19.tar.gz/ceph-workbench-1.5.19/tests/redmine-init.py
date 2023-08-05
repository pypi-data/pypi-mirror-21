import re
import requests
import sys


def params(page):
    def lookup(*regexps):
        for regexp in regexps:
            matches = re.findall(regexp, page.text)
            if matches:
                return matches[0]
    csrf_token = lookup(r'meta content="(.*?)" name="csrf-token"',
                        r'meta name="csrf-token" content="(.*?)"')
    csrf_param = lookup(r'meta content="(.*?)" name="csrf-param"',
                        r'meta name="csrf-param" content="(.*?)"')
    return {csrf_param: csrf_token}


def init(url, user, password):
    s = requests.Session()

    p = params(s.get(url + '/login'))
    p.update({"username": user, "password": password})
    s.post(url + '/login', params=p).raise_for_status()

    p = params(s.get(url + '/settings?tab=authentication'))
    p.update({'settings[rest_api_enabled]': '1'})
    s.post(url + '/settings/edit?tab=authentication',
           params=p).raise_for_status()

    p = params(s.get(url + '/admin'))
    p.update({'lang': 'en'})
    s.post(url + '/admin/default_configuration', params=p).raise_for_status()

    p = params(s.get(url + '/custom_fields/new?type=IssueCustomField'))
    p.update({
        'custom_field[name]': 'Backport',
        'custom_field[tracker_ids][]': "1",
        'custom_field[visible]': "1",
        'custom_field[field_format]': "string",
        'custom_field[is_filter]': "0",
        'custom_field[is_for_all]': "0",
        'custom_field[is_required]': "0",
        'custom_field[searchable]': "0",
        'type': 'IssueCustomField',
    })
    s.post(url + '/custom_fields', params=p).raise_for_status()

    p = params(s.get(url + '/trackers/new'))
    p.update({
        'tracker[name]': 'Backport',
        'tracker[default_status_id]': '1',
        'copy_workflow_from': '1',
    })
    s.post(url + '/trackers', params=p).raise_for_status()

    p = params(s.get(url + '/custom_fields/new?type=IssueCustomField'))
    p.update({
        'custom_field[name]': 'Release',
        'custom_field[tracker_ids][]': "4",  # Backport
        'custom_field[visible]': "1",
        'custom_field[field_format]': "list",
        'custom_field[multiple]': "1",
        'custom_field[possible_values]':
            "cuttlefish\ndumpling\nemperor\nfirefly\ngiant\nhammer",
        'custom_field[is_filter]': "1",
        'custom_field[is_for_all]': "1",
        'custom_field[is_required]': "0",
        'custom_field[searchable]': "1",
        'type': 'IssueCustomField',
    })
    s.post(url + '/custom_fields', params=p).raise_for_status()

init(*sys.argv[1:])
