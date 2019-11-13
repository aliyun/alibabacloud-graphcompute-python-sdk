# -*- coding: utf-8 -*-

import json
from collections import namedtuple


class BulkloadStatus(object):
    # Format of json_string should be like: "data":XX,"message":"XX XX","status":"XX"
    def __init__(self, json_string):
        self.bulkload_status = json.loads(json_string, object_hook=lambda d: namedtuple('X', d.keys())(*d.values()))

    def job_id(self):
        return self.bulkload_status.data

    def message(self):
        return self.bulkload_status.message

    def status(self):
        return self.bulkload_status.status


class CompositeID(object):
    def __init__(self, composite_id):
        (self.type_id, self.id) = composite_id.split(".")

    def id(self):
        return self.id

    def type_id(self):
        return self.type_id()


