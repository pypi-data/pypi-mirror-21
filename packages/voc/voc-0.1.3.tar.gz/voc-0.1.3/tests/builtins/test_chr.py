from .. utils import TranspileTestCase, BuiltinFunctionTestCase


class ChrTests(TranspileTestCase):
    pass


class BuiltinChrFunctionTests(BuiltinFunctionTestCase, TranspileTestCase):
    functions = ["chr"]

    not_implemented = [
        'test_class',
        'test_complex',
        'test_frozenset',
    ]
