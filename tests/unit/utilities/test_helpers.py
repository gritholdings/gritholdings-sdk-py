"""Helpers Test Module."""
from unittest import TestCase
from gritholdings import helpers as h


class HelpersTest(TestCase):
    def test_get_encoded_string(self):
        plain_string = 'This is a long string to test base64 encoding'
        expected = 'VGhpcyBpcyBhIGxvbmcgc3RyaW5nIHRvIHRlc3QgYmFzZTY0IGVuY29kaW5n'
        results = h.get_encoded_string(plain_string)
        self.assertEqual(results, expected)

    def test_get_decoded_string(self):
        base64_string = 'VGhpcyBpcyBhIGxvbmcgc3RyaW5nIHRvIHRlc3QgYmFzZTY0IGVuY29kaW5n'
        expected = 'This is a long string to test base64 encoding'
        results = h.get_decoded_string(base64_string)
        self.assertEqual(results, expected)

    def test_remove_duplicate_dicts(self):
        target_list = [
            {'key_1': 'value_1_1', 'key_2': 'value_1_2'},
            {'key_1': 'value_2_1', 'key_2': 'value_2_2'},
            {'key_1': 'value_3_1', 'key_2': 'value_3_2'},
            {'key_1': 'value_4_1', 'key_2': 'value_4_2'}
        ]
        # intentionally make remove_from size larger than target_list
        remove_from = [{'key_2': 'value_3_2', 'key_1': 'aaa'}, {'key_2': 'value_1_2', 'aaa': 'bbb'},
            {'key_1': 'aaa'}, {'key_1': 'bbb'}, {'key_1': 'ccc'}]
        results = h.remove_duplicate_dicts(target_list=target_list, remove_from=remove_from,
            keys=['key_2'])
        self.assertEqual(results, [
            {'key_1': 'value_2_1', 'key_2': 'value_2_2'},
            {'key_1': 'value_4_1', 'key_2': 'value_4_2'}
        ])

    def test_remove_empty_dicts(self):
        target_list = [
            {'key_1': 'value_1_1', 'key_2': '', 'key_3': ''},
            {'key_1': 'value_2_1', 'key_2': 'value_2_2', 'key_3': 'value_2_3'},
            {'key_1': 'value_3_1', 'key_2': '', 'key_3': ''},
            {'key_1': 'value_4_1', 'key_2': 'value_4_2', 'key_3': 'value_4_3'}
        ]
        results = h.remove_empty_dicts(target_list=target_list, keys=['key_2', 'key_3'])
        self.assertEqual(results, [
            {'key_1': 'value_2_1', 'key_2': 'value_2_2', 'key_3': 'value_2_3'},
            {'key_1': 'value_4_1', 'key_2': 'value_4_2', 'key_3': 'value_4_3'}
        ])

    def test_filter_keys(self):
        target_list = [
            {'key_1': 'value_1_1', 'key_2': 'value_1_2', 'key_3': 'value_1_3'},
            {'key_1': 'value_2_1', 'key_2': 'value_2_2'},
            {'key_1': 'value_3_1', 'key_2': 'value_3_2'}
        ]
        keys = ['key_2', 'key_3']
        results = h.filter_keys(target_list=target_list, keys=keys)
        self.assertEqual(results, [
            {'key_2': 'value_1_2', 'key_3': 'value_1_3'},
            {'key_2': 'value_2_2'},
            {'key_2': 'value_3_2'}
        ])

    def test_rename_keys(self):
        target_list = [
            {'key_1': 'value_1_1', 'key_2': 'value_1_2'},
            {'key_1': 'value_2_1', 'key_2': 'value_2_2'},
            {'key_1': 'value_3_1'}
        ]
        to_keys = ['key_renamed_1', 'key_renamed_2']
        from_keys = ['key_1', 'key_2']
        results = h.rename_keys(target_list=target_list, to_keys=to_keys, from_keys=from_keys)
        self.assertEqual(results, [
            {'key_renamed_1': 'value_1_1', 'key_renamed_2': 'value_1_2'},
            {'key_renamed_1': 'value_2_1', 'key_renamed_2': 'value_2_2'},
            {'key_renamed_1': 'value_3_1'}
        ])

    def test_sanitize_none_to_empty_string(self):
        target_list = [
            {'key_1': 'value_1_1', 'key_2': None},
            {'key_1': None, 'key_2': 'value_2_2'},
            {'key_1': 'value_3_1'}
        ]
        results = h.sanitize_none_to_empty_string(target_list=target_list)
        self.assertEqual(results, [
            {'key_1': 'value_1_1', 'key_2': ''},
            {'key_1': '', 'key_2': 'value_2_2'},
            {'key_1': 'value_3_1'}
        ])

    def test_sanitize_int_to_string(self):
        target_list = [
            {'key_1': 'value_1_1', 'key_2': 2},
            {'key_1': 1, 'key_2': 'value_2_2'},
            {'key_1': 'value_3_1'}
        ]
        results = h.sanitize_int_to_string(target_list=target_list)
        self.assertEqual(results, [
            {'key_1': 'value_1_1', 'key_2': '2'},
            {'key_1': '1', 'key_2': 'value_2_2'},
            {'key_1': 'value_3_1'}
        ])
