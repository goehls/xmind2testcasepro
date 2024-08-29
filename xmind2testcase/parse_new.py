#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time:2023/3/1 21:00
# @Author:boyizhang
import logging

from xmind2testcase import const
from xmind2testcase.metadata import TestSuite, TestCase, TestStep, AttachedTopicAttribute
from xmind2testcase.parser_xmind import ParseXmind


class ParseNew(ParseXmind):

    def parse_testsuites(self, xmind_content_dict):
        """convert xmind file to `xmind2testcase.metadata.TestSuite` list"""
        suites = []

        for sheet in xmind_content_dict:
            logging.debug('start to parse a sheet: %s', sheet['title'])
            root_topic = AttachedTopicAttribute(sheet['rootTopic'])
            # sub_topics = AttachedTopicAttribute(root_topic.sub_attached_topics)
            suite = self.parse_sub_testsuite(root_topic)
            suites.append(suite)

        return suites

    def parse_sub_testsuite(self, root_topic: AttachedTopicAttribute):
        suite = TestSuite()
        suite.name = root_topic.title
        suite.details = root_topic.note
        suite.sub_suites = []

        for suite_dict in root_topic.sub_attached_topics:
            suite.sub_suites.append(self.parse_testsuite(suite_dict))
        return suite

    def parse_testsuite(self, suite_dict):
        testsuite = TestSuite()
        suite_attached_topic = AttachedTopicAttribute(suite_dict)
        testsuite.name = suite_attached_topic.title
        testsuite.details = suite_attached_topic.note
        testsuite.testcase_list = []
        # sub_attached_topics：层级2
        for cases_dict in suite_attached_topic.sub_attached_topics:
            for case in self.recurse_parse_testcase(cases_dict):
                testsuite.testcase_list.append(case)

        return testsuite

    def recurse_parse_testcase(self, case_dict, parent=[]):
        cur_attached_topic = AttachedTopicAttribute(case_dict)
        if cur_attached_topic.is_testcase:
            case = self.parse_a_testcase(cur_attached_topic, parent)
            yield case
        else:
            # if not parent:
            #     parent = []
            parent.append(cur_attached_topic)

            for child_dict in cur_attached_topic.sub_attached_topics:
                for case in self.recurse_parse_testcase(child_dict, parent):
                    yield case

            parent.pop()

    def parse_a_testcase(self, cur_attached_topic, parent):
        testcase = TestCase()
        attached_topics = parent + [cur_attached_topic] if parent else [cur_attached_topic]
        testcase.name = cur_attached_topic.title
        testcase.category = self.gen_testcase_category(attached_topics)
        testcase.summary = cur_attached_topic.note
        testcase.importance = cur_attached_topic.importance
        testcase.execution_type = cur_attached_topic.execution_type
        preconditions = self.gen_testcase_preconditions(cur_attached_topic.sub_attached_topics)
        testcase.preconditions = preconditions if preconditions else ''
        testcase.steps = self.parse_test_steps(cur_attached_topic.sub_attached_topics)
        return testcase

    def gen_testcase_category(self, attached_topics):
        """Link all topic's title as testcase title"""
        # 去掉testcase节点
        titles = [f"<b>{attached_topic.title}</b>" for attached_topic in attached_topics[:-1]]
        # when separator is not blank, will add space around separator, e.g. '/' will be changed to ' / '
        separator = const.config['sep']
        # logging.info(f'bseparator:{separator}')
        # if separator != ' > ':
        #     separator = ' {} > '.format(separator)
        return separator.join(titles)

    def gen_testcase_preconditions(self, attached_topics):
        preconditions = []
        for attached_topic_dict in attached_topics:
            precondition_attached_topic = AttachedTopicAttribute(attached_topic_dict)
            if precondition_attached_topic.is_precondition:
                sub_attached_topics = precondition_attached_topic.sub_attached_topics
                if sub_attached_topics or len(sub_attached_topics) > 0:
                    # 如果包含子节点，则取子节点的title
                    for sub_attached_topic_dict in sub_attached_topics:
                        sub_attached_topic = AttachedTopicAttribute(sub_attached_topic_dict)
                        preconditions.append(sub_attached_topic.title)
                else:
                    preconditions.append(precondition_attached_topic.title)
                return const.config['precondition_sep'].join(preconditions)

        return preconditions

    def parse_data_format(self, testcase_attached_topics):
        FORMATS = ["SingleStepTopic", "MutilStepTopic"]
        testcase_attached_topics = [AttachedTopicAttribute(topic) for topic in testcase_attached_topics]

        if len(testcase_attached_topics) == 3 and testcase_attached_topics[0].is_precondition\
                and testcase_attached_topics[1].is_teststep and testcase_attached_topics[2].is_expect_result:
            return FORMATS[0]
        else:
            return FORMATS[1]
    def parse_test_steps(self, testcase_attached_topics):
        steps = []
        attached_step_topics = []
        attached_expect_result_topics = []

        if self.parse_data_format(testcase_attached_topics) == "MutilStepTopic":
            for attached_topic in testcase_attached_topics:
                cur_attached_step_topic = AttachedTopicAttribute(attached_topic)
                if cur_attached_step_topic.is_teststep:
                    attached_step_topics.append(cur_attached_step_topic)
                if cur_attached_step_topic.is_expect_result:
                    attached_expect_result_topics.append(cur_attached_step_topic)

            for step_num, cur_attached_step_topic in enumerate(attached_step_topics, start=1):
                if not cur_attached_step_topic.is_teststep:
                    continue
                test_step = self.parse_a_test_step(cur_attached_step_topic)
                test_step.step_number = step_num
                steps.append(test_step)

        else:
            for attached_topic in testcase_attached_topics:
                cur_attached_step_topic = AttachedTopicAttribute(attached_topic)
                if cur_attached_step_topic.is_teststep:
                    attached_step_topics.append(cur_attached_step_topic)
                if cur_attached_step_topic.is_expect_result:
                    attached_expect_result_topics.append(cur_attached_step_topic)


            steps = self.parse_a_test_step_single(attached_step_topics[0], attached_expect_result_topics[0])


        return steps

    def parse_a_test_step(self, cur_attached_step_topic):
        test_step = TestStep()
        test_step.actions = cur_attached_step_topic.title

        expected_topics = cur_attached_step_topic.sub_attached_topics
        expected_results = []
        if expected_topics:  # have expected result
            for expected_topic_dict in expected_topics:
                expected_topic = AttachedTopicAttribute(expected_topic_dict)
                if not expected_topic.is_expect_result:
                    continue
                expected_results.append(expected_topic.title)  # one test step action, one test expected result
                # markers = expected_topic.markers

        test_step.expectedresults = expected_results

        logging.debug('finds a teststep: %s', test_step.to_dict())
        return test_step

    def parse_a_test_step_single(self, cur_attached_step_topic, cur_attached_expect_result_topic):
        steps = []
        test_steps = cur_attached_step_topic.sub_attached_topics
        expected_topics = cur_attached_expect_result_topic.sub_attached_topics
        test_steps_num = len(test_steps)
        expected_topics_num = len(expected_topics)
        for step_num, current_topic in enumerate(test_steps, start=1):
            test_step = TestStep()
            current_topic = AttachedTopicAttribute(current_topic)
            test_step.actions = current_topic.title
            test_step.step_number = step_num
            if test_steps_num == expected_topics_num:
                expected_topic = AttachedTopicAttribute(expected_topics[step_num-1])
                title = expected_topic.title
                # num, title = self.get_topic_num(title)
            else:
                # expected_topic = self.get_topic_num(expected_topic.title)
                try:
                    expected_topic = AttachedTopicAttribute(expected_topics.pop())
                    title = expected_topic.title
                    # num, title = self.get_topic_num(title)
                except Exception as e:
                    title = ''

            test_step.expectedresults = [title]
            steps.append(test_step)
        return steps

    def get_topic_num(self, topic_name):
        number = ""
        new_title = ""
        for i,char in enumerate(topic_name):
            if char.isdigit():
                number += char
            else:
                new_title = new_title[i:]
                break
        return int(number),new_title