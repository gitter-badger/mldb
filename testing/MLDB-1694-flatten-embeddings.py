#
# MLDB-1694_flatten_embedding.py
# 2016-05-30
# This file is part of MLDB. Copyright 2016 Datacratic. All rights reserved.
#

import unittest

mldb = mldb_wrapper.wrap(mldb) # noqa

class Mldb1694(MldbUnitTest):  
    @classmethod
    def setUpClass(self):
        inceptionUrl = 'http://public.mldb.ai/models/inception_dec_2015.zip'

        mldb.put('/v1/functions/fetch', {
            "type": 'fetcher',
            "params": {}
        })

        mldb.put('/v1/functions/inception', {
            "type": 'tensorflow.graph',
            "params": {
                "modelFileUrl": 'archive+' + inceptionUrl + '#tensorflow_inception_graph.pb',
                "inputs": 'fetch({url})[content] AS "DecodeJpeg/contents"',
                "outputs": "softmax"
            }
        })

        mldb.log("pwet!")

        self.amazingGrace = "https://s3.amazonaws.com/public.mldb.ai/datasets/tensorflow-demo/grace_hopper.jpg"
 
    def test_prediction_works(self):
        self.assertTableResultEquals(
            mldb.query("""select * from transpose(
                            (
                                SELECT inception({url: '%s'}) as *
                                NAMED 'pred'
                            )
                        )
                        order by pred DESC limit 5
                """ % self.amazingGrace),
            [
                ["_rowName","pred"],
                ["softmax.0.866", 0.8080083131790161],
                ["softmax.0.794", 0.02284531109035015],
                ["softmax.0.896", 0.009539531543850899],
                ["softmax.0.849", 0.009413402527570724],
                ["softmax.0.926", 0.007742570247501135]
            ])


    def test_flattened_prediction_works(self):
        # this version does the same prediction as the test above
        # but accesses the output parameter softmax and flattens
        # the embedding
        self.assertTableResultEquals(
            mldb.query("""select * from transpose(
                            (
                                SELECT flatten(inception({url: '%s'})[softmax]) as *
                                NAMED 'pred'
                            )
                        )
                        order by pred DESC limit 5
                """ % self.amazingGrace),
            [
                ["_rowName","pred"],
                ["866", 0.8080083131790161],
                ["794", 0.02284531109035015],
                ["896", 0.009539531543850899],
                ["849", 0.009413402527570724],
                ["926", 0.007742570247501135]
            ])


mldb.run_tests()

