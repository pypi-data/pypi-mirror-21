from .. utils import TranspileTestCase, BuiltinTwoargFunctionTestCase

from unittest import expectedFailure


class MapTests(TranspileTestCase):
    base_code = """
        iterable = %s
        def testish(x):
            return %s
        it = map(testish, iterable)
        print(it)
        print(next(it))
        print(next(it))
        print(next(it))
        try:
            print(next(it))
        except StopIteration:
            pass
    """

    def test_bool(self):
        self.assertCodeExecution(self.base_code % ("[True, False, True]", "bool(x)"))

    @expectedFailure
    def test_bytearray(self):
        self.assertCodeExecution(self.base_code % ("b'123'", "x"))

    def test_float(self):
        self.assertCodeExecution(self.base_code % ("[3.14, 2.17, 1.0]", "x > 1"))

    def test_int(self):
        self.assertCodeExecution(self.base_code % ("[1, 2, 3]", "x * 2"))


class BuiltinMapFunctionTests(BuiltinTwoargFunctionTestCase, TranspileTestCase):
    functions = ["map"]

    not_implemented = [
        'test_bool_bytearray',
        'test_bool_bytes',
        'test_bool_class',
        'test_bool_dict',
        'test_bool_frozenset',
        'test_bool_set',
        'test_bool_str',

        'test_bytearray_bytearray',
        'test_bytearray_bytes',
        'test_bytearray_class',
        'test_bytearray_dict',
        'test_bytearray_frozenset',
        'test_bytearray_set',
        'test_bytearray_str',

        'test_bytes_bytearray',
        'test_bytes_bytes',
        'test_bytes_class',
        'test_bytes_dict',
        'test_bytes_frozenset',
        'test_bytes_set',
        'test_bytes_str',

        'test_class_bool',
        'test_class_bytearray',
        'test_class_bytes',
        'test_class_class',
        'test_class_complex',
        'test_class_dict',
        'test_class_float',
        'test_class_frozenset',
        'test_class_int',
        'test_class_list',
        'test_class_None',
        'test_class_NotImplemented',
        'test_class_range',
        'test_class_set',
        'test_class_slice',
        'test_class_str',
        'test_class_tuple',

        'test_complex_bytearray',
        'test_complex_bytes',
        'test_complex_class',
        'test_complex_dict',
        'test_complex_frozenset',
        'test_complex_set',
        'test_complex_str',

        'test_dict_bytearray',
        'test_dict_bytes',
        'test_dict_class',
        'test_dict_dict',
        'test_dict_frozenset',
        'test_dict_set',
        'test_dict_str',

        'test_float_bytearray',
        'test_float_bytes',
        'test_float_class',
        'test_float_dict',
        'test_float_frozenset',
        'test_float_set',
        'test_float_str',

        'test_frozenset_bool',
        'test_frozenset_bytearray',
        'test_frozenset_bytes',
        'test_frozenset_class',
        'test_frozenset_complex',
        'test_frozenset_dict',
        'test_frozenset_float',
        'test_frozenset_frozenset',
        'test_frozenset_int',
        'test_frozenset_list',
        'test_frozenset_None',
        'test_frozenset_NotImplemented',
        'test_frozenset_range',
        'test_frozenset_set',
        'test_frozenset_slice',
        'test_frozenset_str',
        'test_frozenset_tuple',

        'test_int_bytearray',
        'test_int_bytes',
        'test_int_class',
        'test_int_dict',
        'test_int_frozenset',
        'test_int_set',
        'test_int_str',

        'test_list_bytearray',
        'test_list_bytes',
        'test_list_class',
        'test_list_dict',
        'test_list_frozenset',
        'test_list_set',
        'test_list_str',

        'test_None_bytearray',
        'test_None_bytes',
        'test_None_class',
        'test_None_dict',
        'test_None_frozenset',
        'test_None_set',
        'test_None_str',

        'test_NotImplemented_bytearray',
        'test_NotImplemented_bytes',
        'test_NotImplemented_class',
        'test_NotImplemented_dict',
        'test_NotImplemented_frozenset',
        'test_NotImplemented_set',
        'test_NotImplemented_str',

        'test_range_bytearray',
        'test_range_bytes',
        'test_range_class',
        'test_range_dict',
        'test_range_frozenset',
        'test_range_set',
        'test_range_str',

        'test_set_bytearray',
        'test_set_bytes',
        'test_set_class',
        'test_set_dict',
        'test_set_frozenset',
        'test_set_set',
        'test_set_str',

        'test_slice_bytearray',
        'test_slice_bytes',
        'test_slice_class',
        'test_slice_dict',
        'test_slice_frozenset',
        'test_slice_set',
        'test_slice_str',

        'test_str_bytearray',
        'test_str_bytes',
        'test_str_class',
        'test_str_dict',
        'test_str_frozenset',
        'test_str_set',
        'test_str_str',

        'test_tuple_bytearray',
        'test_tuple_bytes',
        'test_tuple_class',
        'test_tuple_dict',
        'test_tuple_frozenset',
        'test_tuple_set',
        'test_tuple_str',
    ]
