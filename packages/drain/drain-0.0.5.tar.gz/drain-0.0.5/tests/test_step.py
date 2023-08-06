from drain.step import *
from drain import step
import numpy as np
import tempfile

def test_run(drain_setup):
    s = Add(inputs = [Scalar(value=value) for value in range(1,10)])
    s.execute()
    assert s.get_result() == 45

def test_run_inputs_mapping():
    s = Divide(inputs = [Scalar(value=1), Scalar(value=2)], 
            inputs_mapping=['denominator', 'numerator'])
    s.execute()
    assert s.get_result() == 2

def test_inputs_mapping():
    a = Scalar(1)
    b = Scalar(2)

    a.execute()
    b.execute()

    assert Step(inputs=[a,b], inputs_mapping=['a','b']).map_inputs() == ([], {'a':1, 'b':2})

def test_inputs_mapping_dict():
    a = Scalar(1)
    b = Scalar(2)

    a.execute()
    b.execute()

    assert Step(inputs=[a,b], inputs_mapping=['a','b']).map_inputs() == ([], {'a':1, 'b':2})

def test_inputs_mapping_list():
    a = Scalar([1,2])
    a.execute()

    assert Step(inputs=[a], inputs_mapping=[['a','b']]).map_inputs() == ([], {'a':1, 'b':2})



class DumpStep(Step):
    def __init__(self, n, n_df, return_list):
        # number of objects to return and number of them to be dataframes
        # and whether to use a list or dict
        if n_df == None:
            n_df = n

        Step.__init__(self, n=n, n_df=n_df, return_list=return_list)
        self.target = True

    def run(self):
        l = ['a']*self.n + [pd.DataFrame(np.arange(5))]*self.n_df
        if len(l) == 1:
            return l[0]

        if self.return_list:
            return l
        else:
            d = {'k'+str(k):v for k,v in zip(range(len(l)), l)}
            return d

def test_dump_joblib():
    t = DumpStep(n=10, n_df=0, return_list=False)

    t.execute()
    r = t.get_result()
    t.dump()
    t.load()
    assert r == t.get_result()

def test_dump_hdf_single():
    t = DumpStep(n=0, n_df=1, return_list=False)

    t.execute()
    r = t.get_result()
    t.dump()
    t.load()
    assert r.equals(t.get_result())

def test_dump_hdf_list():
    t = DumpStep(n=0, n_df=5, return_list=True)

    t.execute()
    r = t.get_result()
    t.dump()
    t.load()

    for a,b in zip(r,t.get_result()):
        assert a.equals(b)

def test_dump_hdf_dict():
    t = DumpStep(n=0, n_df=5, return_list=False)

    t.execute()
    r = t.get_result()
    t.dump()
    t.load()

    for k in r:
        assert r[k].equals(t.get_result()[k])
