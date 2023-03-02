#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time:2023/3/1 19:07
# @Author:boyizhang
import json
import logging
import os

from xmind2testcase import const
from xmind2testcase.parse_new import ParseNew
from xmind2testcase.parse_old import ParseOld
# from xmind2testcase.parser_v1 import xmind_to_testsuites
from xmind2testcase.utils import get_absolute_path, parser_xmind_to_dict


def get_raw_testsuites(xmind_file):
    """Load the XMind file and parse to `xmind2testcase.metadata.TestSuite` list"""
    xmind_file = get_absolute_path(xmind_file)
    # 根据解析对象使用指定的入口函数解析
    parser_type, xmind_content_dict = parser_xmind_to_dict(xmind_file)
    if parser_type == const.TAG_JSON:
        parse = ParseNew()
        logging.info('parser new version xmind')
    else:
        logging.info('parser old version xmind')
        parse = ParseOld()

    logging.info(f"xmind_content_dict:{json.dumps(xmind_content_dict)}")

    if xmind_content_dict:
        try:
            testsuites = parse.parse_testsuites(xmind_content_dict)
            return testsuites
        except Exception as e:
            logging.exception(f"e:{e}")

    else:
        logging.error('Invalid XMind file(%s): it is empty!', xmind_file)
        return []

def count_testsuits(xmind_file):
    testsuites = get_raw_testsuites(xmind_file)
    suite_count = 0
    for suite in testsuites:
        suite_count += len(suite.sub_suites)

    return suite_count

def get_testsuite_list(xmind_file):
    """Load the XMind file and get all testsuite in it

    :param xmind_file: the target XMind file
    :return: a list of testsuite data
    """
    xmind_file = get_absolute_path(xmind_file)
    logging.info('Start converting XMind file(%s) to testsuite data list...', xmind_file)
    testsuite_list = get_raw_testsuites(xmind_file)
    suite_data_list = []

    for testsuite in testsuite_list:
        # product_statistics = {'case_num': 0, 'non_execution': 0, 'pass': 0, 'failed': 0, 'blocked': 0, 'skipped': 0}
        # for sub_suite in testsuite.sub_suites:
        #     suite_statistics = {'case_num': len(sub_suite.testcase_list), 'non_execution': 0, 'pass': 0, 'failed': 0,
        #                         'blocked': 0, 'skipped': 0}
        #     for case in sub_suite.testcase_list:
        #         if case.result == 0:
        #             suite_statistics['non_execution'] += 1
        #         elif case.result == 1:
        #             suite_statistics['pass'] += 1
        #         elif case.result == 2:
        #             suite_statistics['failed'] += 1
        #         elif case.result == 3:
        #             suite_statistics['blocked'] += 1
        #         elif case.result == 4:
        #             suite_statistics['skipped'] += 1
        #         else:
        #             logging.warning('This testcase result is abnormal: %s, please check it: %s', case.result,
        #                             case.to_dict())
        #     sub_suite.statistics = suite_statistics
        #     for item in product_statistics:
        #         product_statistics[item] += suite_statistics[item]
        #
        # testsuite.statistics = product_statistics
        suite_data = testsuite.to_dict()
        suite_data_list.append(suite_data)

    logging.info('Convert XMind file(%s) to testsuite data list successfully!', xmind_file)
    return suite_data_list


def get_testcase_list(xmind_file):
    """Load the XMind file and get all testcase in it

    :param xmind_file: the target XMind file
    :return: a list of testcase data
    """
    xmind_file = get_absolute_path(xmind_file)
    logging.info('Start converting XMind file(%s) to testcases dict data...', xmind_file)
    testsuites = get_raw_testsuites(xmind_file)
    testcases = []

    for testsuite in testsuites:
        product = testsuite.name
        for suite in testsuite.sub_suites:
            for case in suite.testcase_list:
                case_data = case.to_dict()
                case_data['product'] = product
                case_data['suite'] = f"{product}::{suite.name}"
                testcases.append(case_data)

    logging.info('Convert XMind file(%s) to testcases dict data successfully!', xmind_file)
    return testcases


def gen_testsuite_to_json_file(xmind_file):
    """Convert XMind file to a testsuite json file"""
    xmind_file = get_absolute_path(xmind_file)
    logging.info('Start converting XMind file(%s) to testsuites json file...', xmind_file)
    testsuites = get_testsuite_list(xmind_file)
    testsuite_json_file = xmind_file[:-6] + '_testsuite.json'

    if os.path.exists(testsuite_json_file):
        os.remove(testsuite_json_file)
        # logging.info('The testsuite json file already exists, return it directly: %s', testsuite_json_file)
        # return testsuite_json_file

    with open(testsuite_json_file, 'w', encoding='utf8') as f:
        f.write(json.dumps(testsuites, indent=4, separators=(',', ': '), ensure_ascii=False))
        logging.info('Convert XMind file(%s) to a testsuite json file(%s) successfully!', xmind_file,
                     testsuite_json_file)

    return testsuite_json_file


def gen_testcase_to_json_file(xmind_file):
    """Convert XMind file to a testcase json file"""
    xmind_file = get_absolute_path(xmind_file)
    logging.info('Start converting XMind file(%s) to testcases json file...', xmind_file)
    testcases = get_testcase_list(xmind_file)
    testcase_json_file = xmind_file[:-6] + '.json'
    logging.info(f"testcase_json_file:{testcase_json_file}")
    if os.path.exists(testcase_json_file):
        os.remove(testcase_json_file)
        logging.info('The testcase json file already exists, return it directly: %s', testcase_json_file)
        # return testcase_json_file

    with open(testcase_json_file, 'w', encoding='utf8') as f:
        f.write(json.dumps(testcases, indent=4, separators=(',', ': '), ensure_ascii=False))
        logging.info('Convert XMind file(%s) to a testcase json file(%s) successfully!', xmind_file, testcase_json_file)

    return testcase_json_file

if __name__ == '__main__':
    # gen_testcase_to_json_file('/Users/boyizhang/Downloads/new-[SPSOB-2252][Package] BP V3.4.1 Auto-pricing for special discount.xmind')
    gen_testsuite_to_json_file('/Users/boyizhang/Downloads/new-[SPSOB-2252][Package] BP V3.4.1 Auto-pricing for special discount.xmind')