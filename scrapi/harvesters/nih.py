"""
Harvester for NIH.gov Research Portal Online Reporting Tools (RePORTER) for the SHARE Notification Service

Getting weekly summary from ExPORTER on nih.gov, parse XML and normalize the data
An example file: http://exporter.nih.gov/XMLData/final/RePORTER_PRJ_X_FY2015_035.zip

Note: This harvester assigns incorrect dates to some xml files due to an inconsistency in the numbering of week of the
month in the project file names. It is guaranteed that all data are harvested in a sufficiently long time frame
(>1 month).
"""

from __future__ import unicode_literals


import logging
import re

from bs4 import BeautifulSoup
from datetime import date, timedelta
from dateutil.parser import parse
from io import BytesIO
from lxml import etree
from zipfile import ZipFile

from scrapi import requests
from scrapi import settings
from scrapi.base import XMLHarvester
from scrapi.util import copy_to_unicode
from scrapi.linter.document import RawDocument
from scrapi.base.helpers import (
    compose,
    single_result,
    build_properties,
    datetime_formatter,
    default_name_parser
)


logger = logging.getLogger(__name__)


def daterange(start_date, end_date):
    """
    Get all the dates between the start_date and the end_date
    """
    pass


def get_days_of_week(start_date, end_date, day_of_week):
    """
    First convert start_date and end_date to have the day of week we require.
    Then get all the dates of the specified day of week between the start_date and end_date.
    """
    start_date = start_date - timedelta(days=(start_date.weekday() - day_of_week))
    end_date = end_date - timedelta(days=(end_date.weekday() - day_of_week))

    for ordinal in range(start_date.toordinal(), end_date.toordinal() + 1):
        if date.fromordinal(ordinal).weekday() == day_of_week:
            yield date.fromordinal(ordinal)


def get_fiscal_year(mydate=date.today()):
    """
    Return the current fiscal year. Each fiscal year starts on October 1
    """
    pass


def get_fiscal_years(dates):
    """
    Given a range of dates, get unique fiscal years
    """
    return tuple(set(map(get_fiscal_year, dates)))


def parse_month_column(month_column, day_of_week):
    """
    Given a month column string, return the date of a day (Monday by default) of that week
    An example of a month column string: September, 2015 - WEEK 1
    """
    month_year, week = iter(map(lambda x: x.strip(), month_column.split('-')))
    first_day = parse('1 ' + month_year)
    first_day -= timedelta(days=(first_day.weekday() - day_of_week + 7 * (1 if first_day.weekday() - day_of_week <= 0 else 0)))
    week = int(re.search('.*([0-9]{1,2})', week).group(1))
    mydate = first_day + timedelta(week * 7)
    return mydate.date()


def parse_row(row, day_of_week):
    """
    Get a row of the ExPORTER table, return the date of a day (Monday by default) of that week, the fiscal year,
    and the url of the xml file
    To keep the format consistent, if the record is from previous fiscal years, None is returned
    """
    row_text = list(map(lambda x: x.text.strip('\t').strip('\n').strip('\r').strip('<td>').strip('</td>'), row))
    row_text = list(map(lambda x: x.strip(), row_text))
    month_column = row_text[1]
    fiscal_year = int(row_text[2])
    url = row[3].find('a').get('href')

    if month_column.lower() == u"all":
        return (None, fiscal_year, url)
    elif re.match('[A-Za-z]*, [0-9]{4} - .*', month_column):
        date = parse_month_column(month_column, day_of_week)
        return (date, fiscal_year, url)


def parse_rows(rows, day_of_week):
    """
    A generator to parse all the rows
    """
    for row in rows:
        yield parse_row(row('td'), day_of_week)


def construct_urls(base_url, start_date, end_date, rows, day_of_week=0):
    """
    Given date range, constructs urls of corresponded XML files.
    """
    dates = [i for i in get_days_of_week(start_date, end_date, day_of_week)]
    fiscal_years = get_fiscal_years(dates)
    for data in parse_rows(rows, day_of_week):
        if data[0] in dates or (data[0] is None and data[1] in fiscal_years):
            yield "".join([base_url, data[2]])


def get_xml_files(urls):
    for zip_url in urls:
            data = requests.get(zip_url)
            zipfile = ZipFile(BytesIO(data.content))
            with zipfile.open(zipfile.namelist()[0], 'r') as f:
                yield f.read()


def xml_records(files):
    for xml_file in files:
        records = etree.XML(xml_file).xpath('row')
        for record in records:
            yield record




def nih_name_parser(names, org_name):
    """
    Takes a list of names and organization names, and attempts to parse them
    """
    pass


class NIHHarvesters(XMLHarvester):

    short_name = 'nih'
    long_name = 'NIH Research Portal Online Reporting Tools'
    url = 'http://exporter.nih.gov/ExPORTER_Catalog.aspx/'
    project_base_url = 'https://projectreporter.nih.gov/project_info_description.cfm?aid={}'
    foa_base_url = 'http://grants.nih.gov/grants/guide/pa-files/{}.html'
    DEFAULT_ENCODING = 'UTF-8'
    record_encoding = None




    namespaces = {'xsi': "http://www.w3.org/2001/XMLSchema-instance"}

    def harvest(self, start_date=None, end_date=None):
        """
        Return a list of RawDocuments
        """
        start_date = start_date or date.today() - timedelta(settings.DAYS_BACK)
        end_date = end_date or date.today()

        base_url = 'http://exporter.nih.gov/'
        table_url = 'http://exporter.nih.gov/ExPORTER_Catalog.aspx/'

        # get ExPORTER page html and rows storing records
        html = requests.get(table_url).content
        soup = BeautifulSoup(html, 'lxml')
        table = soup.find('table', id="ContentPlaceHolder1_ProjectData_dgProjectData")
        rows = table.find_all('tr', class_="row_bg")
        urls = [i for i in construct_urls(base_url, start_date, end_date, rows)]

        return [
            RawDocument({
                'doc': etree.tostring(record, encoding=self.DEFAULT_ENCODING),
                'source': self.short_name,
                'docID': copy_to_unicode(record.xpath('.//APPLICATION_ID/node()', namespaces=self.namespaces)[0]),
                'filetype': 'xml'
            }) for record in xml_records(get_xml_files(urls))
        ]
