"""
Copyright 2012-2017 Ministerie van Sociale Zaken en Werkgelegenheid

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""


from ast import literal_eval
import datetime
import functools
import io
import logging

from .. import domain


class History(domain.MetricSource):
    """ Class representing the history file. """
    metric_source_name = 'Measurement history file'

    def __init__(self, history_filename, recent_history=250, file_=None):
        self.__history_filename = history_filename
        self.__recent_history = recent_history
        self.__file = file_ if file_ else open
        super().__init__(url=history_filename)

    def filename(self):
        """ Return the history filename """
        return self.__history_filename

    def recent_history(self, *metric_ids):
        """ Retrieve the recent history for the metric_ids. """
        values = []
        for measurement in self.__historic_values():
            for metric_id in metric_ids:
                if metric_id in measurement:
                    values.append(measurement[metric_id])
                    break  # inner loop
        return values

    def complete_history(self):
        """ Return the complete history. """
        return self.__historic_values(recent_only=False)

    def status_start_date(self, metric_id, current_status, now=datetime.datetime.now):
        """ Return the start date of the current status of the metric. """
        last_status, date = self.__last_status(metric_id)
        return date if last_status == current_status else now()

    def statuses(self):
        """ Return the statuses for each measurement. """
        measurements = self.__load_history(recent_only=False)
        statuses = []
        for measurement in measurements:
            measurement_statuses = dict(date=measurement['date'])
            for measurement_data in list(measurement.values()):
                if isinstance(measurement_data, tuple):
                    status = measurement_data[1]
                    measurement_statuses[status] = measurement_statuses.get(status, 0) + 1
            statuses.append(measurement_statuses)
        return statuses

    def __last_status(self, metric_id):
        """ Return the last recorded status of the metric and the date that the metric first had that status. """
        try:
            last_measurement = self.__load_history()[-1][metric_id]
        except (IndexError, KeyError):
            last_measurement = None
        if isinstance(last_measurement, tuple) and len(last_measurement) >= 3:
            last_status = last_measurement[1]
            time_stamp = last_measurement[2]
            time_stamp_format = '%Y-%m-%d %H:%M:%S'
            if '.' in time_stamp:
                time_stamp_format += '.%f'
            date = datetime.datetime.strptime(time_stamp, time_stamp_format)
            return last_status, date
        else:
            return '', datetime.datetime.min

    @functools.lru_cache(maxsize=1024)
    def __historic_values(self, recent_only=True):
        """ Return only the historic values from the history file, so without the status and status date. """
        measurements = self.__load_history(recent_only)
        value_only_measurements = []
        for measurement in measurements:
            values_only_measurement = dict()
            for metric_id, measurement_data in list(measurement.items()):
                value = measurement_data[0] if isinstance(measurement_data, tuple) else measurement_data
                values_only_measurement[metric_id] = value
            value_only_measurements.append(values_only_measurement)
        return value_only_measurements

    def __load_history(self, recent_only=True):
        """ Load measurements from the history file. """
        lines = self.__load_complete_history()
        return lines[-self.__recent_history:] if recent_only else lines

    @functools.lru_cache(maxsize=1024)
    def __load_complete_history(self):
        """ Load all measurements from the history file. """
        try:
            history_file = self.__file(self.__history_filename)
        except IOError:
            logging.warning('Could not open %s', self.__history_filename)
            history_file = io.StringIO()  # Fake an empty file
        lines = [literal_eval(line) for line in history_file if line.strip()]
        history_file.close()
        lines = [line for line in lines if len(line) > 6]  # Weed out lines with meta metrics only
        logging.info('Read %d lines from %s', len(lines), self.__history_filename)
        return lines
