# -*- coding: utf-8 -*-

import time
from graphcompute.utils.auth import Credentials, Auth
from graphcompute.graphcompute_client import GraphCompute_Client
from graphcompute.utils.tools import BulkloadStatus


class GraphComputeExample(object):

    def __init__(self):
        access_key_id = "your access_key_id"
        access_key_secret = "your access_key_secret"
        self.cred = Credentials(access_key_id, access_key_secret)

        instance_domain = "your instance domain with port"
        remote_endpoint = "ws://%s/gremlin" % str(instance_domain)

        self.client = GraphCompute_Client(remote_endpoint, 'g', self.cred)

    def execute(self):
        pass

    def close(self):
        self.client.close();


class SchemaComputeExample(GraphComputeExample):
    def __init__(self):
        GraphComputeExample.__init__(self)

    def execute(self):
        self.create_vertex_type()
        self.create_edge_type()
        self.alter_vertex_type()
        self.get_schema_info()
        self.drop_vertex_edge_type()

    def create_vertex_type(self):
        query = "graph.createVertexType('person')" \
                ".addProperty('id','long')" \
                ".addProperty('name','string', 'comment message of name')" \
                ".addProperty('age', 'int')" \
                ".primaryKey('id')"

        result = self.client.submit(query)
        print result.one()

    def create_edge_type(self):
        query = "graph.createEdgeType('knows')" \
                ".addProperty('id', 'long')" \
                ".addProperty('weight', 'double', 'weight of knows', 1.0)" \
                ".addRelation('person', 'person')"

        result = self.client.submit(query)
        print result.one()

    def alter_vertex_type(self):
        query = "graph.alterVertexEdgeType('person')" \
                ".addProperty('age2','int', 'age2 property')" \
                ".addProperty('age3','int', 'age3 property')"

        print self.client.submit(query).one()

        query = "graph.alterVertexEdgeType('person')" \
                ".dropProperty('age2')" \
                ".dropProperty('age3')"

        print self.client.submit(query).one()

        query = "graph.alterVertexEdgeType('knows')" \
                ".addProperty('test1','int', 'age property')" \
                ".dropProperty('weight')"

        print self.client.submit(query).one()

        query = "graph.alterVertexEdgeType('knows')" \
                ".dropProperty('test1')" \
                ".addProperty('weight', 'double')"

        print self.client.submit(query).one()

        query = "graph.alterEdgeRelation('knows')" \
                ".dropRelation('person','person')"

        print self.client.submit(query).one()

        query = "graph.alterEdgeRelation('knows')" \
                ".addRelation('person','person')"

        print self.client.submit(query).one()

    def drop_vertex_edge_type(self):
        query = "graph.dropVertexEdgeType('person')"
        print self.client.submit(query).one()

        query = "graph.dropVertexEdgeType('knows')"
        print self.client.submit(query).one()

    def get_schema_info(self):
        query = "graph.schema()"
        print self.client.submit(query).one()


class BulkLoadExample(SchemaComputeExample):
    def __init__(self):
        SchemaComputeExample.__init__(self)

        self.odps_endpint = "http://XXXX"
        self.your_odps_access_id = "****"
        self.your_odps_access_key = "****"

        self.yourBizId = "****"
        self.your_odps_project = "****"
        self.your_odps_vertex_table = "****"
        self.your_odps_edge_table = "****"

        self.odps_person_id_field = "**"
        self.person_id_prop = "**"

        self.odps_person_name_field = "**"
        self.person_name_prop = "**"

        self.odps_person_age_field = "**"
        self.person_age_prop = "**"

        self.odps_knows_id_field = "**"
        self.knows_id_prop = "**"

        self.odps_knows_weight_field = "**"
        self.knows_weight_prop = "**"

        self.knows_src_person_id_field = "**"
        self.knows_dst_person_id_field = "**"

        self.auth = Auth(self.cred)

    def execute(self):
        self.create_vertex_type()
        self.create_edge_type()
        self.bulkload_vertex()
        self.bulkload_edge()
        self.drop_vertex_edge_type()

    def _check_bulkload_status(self, status):
        if status.status() == "RUNNING":

            check_status_query = "graph.bulkloadJobStatus(%s).signature('%s')" % \
                                 (status.job_id(), self.auth.gen_remote_credentials())

            while True:
                check_status = BulkloadStatus(self.client.submit(check_status_query).one()[0])

                if check_status.status() != "RUNNING":
                    print "bulkload job status %s  and message %s" % (status.job_id(), status.message())
                    break
                else:
                    print "bulkload job status %s  and message %s" % (status.job_id(), status.message())
                    time.sleep(2)

        elif status.status() == "SUCCESS":
            print "bulkload job has been finished"
        else:
            print "bulkload job status %s  and message %s" % (status.job_id(), status.message())

    def bulkload_vertex(self):
        query = 'graph.bulkloadVertexFromOdps("person")' \
                '.endpoint("%s")' \
                '.accessId("%s")' \
                '.accessKey("%s")' \
                '.bizOwnerId("%s")' \
                '.project("%s").table("%s")' \
                '.mappingColumn("%s", "%s")' \
                '.mappingColumn("%s", "%s")' \
                '.mappingColumn("%s", "%s")' \
                '.signature("%s")' % \
                (self.odps_endpint, self.your_odps_access_id, self.your_odps_access_key, self.yourBizId,
                 self.your_odps_project, self.your_odps_vertex_table,
                 self.odps_person_id_field, self.person_id_prop,
                 self.odps_person_name_field, self.person_name_prop,
                 self.odps_person_age_field, self.person_age_prop, self.auth.gen_remote_credentials())

        status = BulkloadStatus(self.client.submit(query).one()[0])
        self._check_bulkload_status(status)

    def bulkload_edge(self):
        query = "graph.bulkloadEdgeFromOdps('knows')" \
                ".endpoint('%s')" \
                ".accessId('%s')" \
                ".accessKey('%s')" \
                ".bizOwnerId('%s')" \
                ".project('%s')" \
                ".table('%s')" \
                ".mappingColumn('%s', '%s')" \
                ".mappingColumn('%s', '%s')" \
                ".srcVertex('person')" \
                ".mappingSrcPrimaryKey('%s','%s')" \
                ".dstVertex('person')" \
                ".mappingDstPrimaryKey('%s','%s')" \
                '.signature("%s")' % \
                (self.odps_endpint, self.your_odps_access_id, self.your_odps_access_key, self.yourBizId,
                 self.your_odps_project, self.your_odps_edge_table,
                 self.odps_knows_id_field, self.knows_id_prop,
                 self.odps_knows_weight_field, self.knows_weight_prop,
                 self.knows_src_person_id_field, self.person_id_prop,
                 self.knows_dst_person_id_field, self.person_id_prop, self.auth.gen_remote_credentials())

        status = BulkloadStatus(self.client.submit(query).one()[0])
        self._check_bulkload_status(status)


class RealTimeExample(SchemaComputeExample):

    def execute(self):
        self.create_vertex_type()
        self.create_edge_type()
        time.sleep(10)
        self.realtime_op()
        self.drop_vertex_edge_type()

    def realtime_op(self):
        query = "graph.addVertex(T.label, 'person', 'id', 1, 'name', 'tom', 'age', 20)"
        v1 = self.client.submit(query).one()[0]
        print v1

        query = "graph.addVertex(T.label, 'person', 'id', 2, 'name', 'jack', 'age', 30)"
        v2 = self.client.submit(query).one()[0]
        print v2

        query = "graph.addVertex(T.label, 'person', 'id', 3, 'name', 'tony', 'age', 25)"
        v3 = self.client.submit(query).one()[0]
        print v3

        query = "graph.addEdge('%s', '%s', T.label, 'knows', 'id', 1, 'weight', 0.5)" % (str(v1.id), str(v2.id))
        e1 = self.client.submit(query).one()[0]
        print e1

        query = "graph.addEdge('%s', '%s', T.label, 'knows', 'id', 2, 'weight', 0.8)" % (str(v1.id), str(v2.id))
        e2 = self.client.submit(query).one()[0]
        print e2

        time.sleep(10)

        query = "graph.updateVertex(T.label, 'person', 'id', 1, 'age', 25)"
        v1_update = self.client.submit(query).one()[0]
        print v1_update

        query = "graph.updateEdge('knows', %d, '%s', '%s', 'weight', 0.75)" % (
            long(e1.id.split(".")[1]), str(v1.id), str(v2.id))
        e1_update = self.client.submit(query).one()[0]
        print e1_update

        query = "graph.deleteVertex('%s')" % (str(v3.id))
        v3_delete = self.client.submit(query).one()[0]
        print v3_delete

        query = "graph.deleteEdge('knows', %d, '%s', '%s')" % (long(e1.id.split(".")[1]), str(v1.id), str(v2.id))
        e1_delete = self.client.submit(query).one()[0]
        print e1_delete


class QueryComputeExample(GraphComputeExample):

    def execute(self):
        query = "g.V().properties()"
        print self.client.submit(query).one()


if __name__ == "__main__":
    example = SchemaComputeExample()
    example.execute()
    example.close()
