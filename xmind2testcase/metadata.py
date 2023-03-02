#!/usr/bin/env python
# _*_ coding:utf-8 _*_

"""
testlink.testlink
"""
import re
from typing import Union, Match

from xmind2testcase import const


class TestSuite(object):

    def __init__(self, name='', details='', testcase_list=None, sub_suites=None, statistics=None):
        """
        TestSuite
        :param name: test suite name  > topic title
        :param details: test suite detail infomation > topic notes
        :param testcase_list: test case list
        :param sub_suites: sub test suite list
        :param statistics: testsuite statistics info {'case_num': 0, 'non_execution': 0, 'pass': 0, 'failed': 0, 'blocked': 0, 'skipped': 0}
        """
        self.name = name
        self.details = details
        self.testcase_list = testcase_list
        self.sub_suites = sub_suites  # ignore
        self.statistics = statistics  # ignore

    def to_dict(self):
        data = {
            'name': self.name,
            'details': self.details,
            'testcase_list': [],
            'sub_suites': []
        }

        if self.sub_suites:
            for suite in self.sub_suites:
                data['sub_suites'].append(suite.to_dict())

        if self.testcase_list:
            for case in self.testcase_list:
                data['testcase_list'].append(case.to_dict())

        if self.statistics:
            data['statistics'] = self.statistics

        return data


class TestCase(object):

    def __init__(self, name='', category='', version=1, summary='', preconditions='', execution_type=1, importance=2,
                 estimated_exec_duration=3, status=7, result=0, steps=None):
        """
        TestCase
        :param name: test case name  > topic title
        :param version: test case version infomation
        :param summary: test case summary infomation
        :param preconditions: test case pre condition
        :param execution_type: manual:1 or automate:2
        :param importance: high:1, middle:2, low:3
        :param estimated_exec_duration: estimated execution duration
        :param status: draft:1, ready ro review:2, review in progress:3, rework:4, obsolete:5, future:6, final:7
        :param result: non-execution:0, pass:1, failed:2, blocked:3, skipped:4
        :param steps: test case step list
        """

        self.name = name
        self.version = version
        self.category = category
        self.summary = summary
        self.preconditions = preconditions
        self.execution_type = execution_type
        self.importance = importance
        self.estimated_exec_duration = estimated_exec_duration
        self.status = status
        self.result = result
        self.steps = steps

    def to_dict(self):
        data = {
            'name': self.name,
            'version': self.version,  # TODO(devin): get version content
            'summary': self.summary,
            'category': self.category,
            'preconditions': self.preconditions,
            'execution_type': self.execution_type,
            'importance': self.importance,
            'estimated_exec_duration': self.estimated_exec_duration,  # TODO(devin): get estimated content
            'status': self.status,  # TODO(devin): get status content
            'result': self.result,
            'steps': []
        }

        if self.steps:
            for step in self.steps:
                data['steps'].append(step.to_dict())

        return data


class TestStep(object):

    def __init__(self, step_number=1, actions='', expectedresults='', execution_type=1, result=0):
        """
        TestStep
        :param step_number: test step number
        :param actions: test step actions
        :param expectedresults: test step expected results
        :param execution_type: test step execution type
        :param result: non-execution:0, pass:1, failed:2, blocked:3, skipped:4
        """
        self.step_number = step_number
        self.actions = actions
        self.expectedresults = expectedresults
        self.execution_type = execution_type  # TODO(devin): get execution type content
        self.result = result

    def to_dict(self):
        data = {
            'step_number': self.step_number,
            'actions': self.actions,
            'expectedresults': self.expectedresults,
            'execution_type': self.execution_type,
            'result': self.result
        }

        return data


class AttachedTopicAttribute:
    def __init__(self, attached_topic):
        self.id: str = attached_topic.get('id', '')
        self.title: str = attached_topic.get('title', '')
        self.note: str = self.get_notes(attached_topic.get('notes', ''))
        self.href: str = attached_topic.get('href', '')
        self.markers: list = self.get_markers(attached_topic.get('markers', ''))
        self.labels: list = attached_topic.get('labels', [])
        self.image: list = self.get_image(attached_topic.get('image', ''))
        self.sub_attached_topics: list = self.get_sub_attached_topics(attached_topic.get('children', {}))
        self.execution_type: int = self.get_execution_type(self.labels, self.markers)
        self.is_ignore: bool = self.get_attached_topic_type_by_labels(const.TESTCASE_IGNORE_TAGS, self.labels)
        # 测试用例 执行步骤 预期结果 前置条件 不允许同时关联同一节点
        self.is_valid: bool = self.get_valid_testcase_attached_topic(self.labels)
        self.is_testcase: bool = self.get_attached_topic_type_by_labels(const.TESTCASE_TAG, self.labels)
        self.is_precondition: bool = self.get_attached_topic_type_by_labels(const.PRECONDITIONS_TAG, self.labels)
        self.is_teststep: bool = self.get_attached_topic_type_by_labels(const.TESTSTEP_TAG, self.labels)
        self.is_expect_result: bool = self.get_attached_topic_type_by_labels(const.EXPECT_RESULT_TAG, self.labels)
        self.importance: int = self.get_importance_by_labels(const.IMPORTANCE_TAGS, self.labels, self.markers)

    def get_notes(self, notes):
        notes_content = ''
        if notes:
            notes_content = notes.get('plain').get('content')
        return notes_content

    def get_image(self, image):
        src = ''
        if image:
            src = image.get('src', '')
        return src

    def get_valid_testcase_attached_topic(self, labels):
        cou = 0
        labels = [label.lower() for label in labels]
        if const.TESTCASE_TAG.lower() in labels:
            cou += 1
        if const.TESTSTEP_TAG.lower() in labels:
            cou += 1
        if const.EXPECT_RESULT_TAG.lower() in labels:
            cou += 1
        if const.PRECONDITIONS_TAG.lower() in labels:
            cou += 1

        return cou <= 1

    def get_sub_attached_topics(self, children):
        cur_attached_topics = []
        if children:
            cur_attached_topics = children.get('attached', [])
        return cur_attached_topics

    def get_markers(self, markers):
        cur_markers = []
        if markers:
            cur_markers = [marker.get('markerId', '') for marker in markers]
        return cur_markers

    def get_attached_topic_type_by_labels(self, tag, labels):
        tags = []
        if isinstance(tag, list):
            tags.extend(tag)
        else:
            tags.append(tag)
        return self.match_tags(tags, labels)
        # if tag in labels:
        #     return True
        # return False

    def get_importance_by_labels(self, tags, labels, makers=list()) -> int:
        importance = 2
        labels.extend(makers)
        # logging.info(f'AAAAAA-labels:{labels}')
        match = self.match_tags(tags, labels, makers, is_regex=True)
        if match:
            importance = int(re.findall('[0-9]', match.string)[0])
        return importance

    def get_execution_type(self, labels=[], markers=[]):
        execution_type = const.EXECUTION_MANUAL_TYPE
        is_match = self.match_tags(const.EXECUTION_AUTO_TYPE_TAG, labels, markers)
        if is_match:
            execution_type = const.EXECUTION_AUTO_TYPE
        return execution_type

    def match_tags(self, tags, labels=[], markers=[], is_regex=False) -> Union[Match[str], None, bool]:
        labels.extend(markers)
        labels = [label.lower() for label in labels]
        tags = [tag.lower() for tag in tags]
        if is_regex:
            for label in labels:
                for tag in tags:
                    match = re.match(tag, label)
                    if match:
                        return match
            return None
        else:
            for tag in tags:
                if tag in labels:
                    return True
            return False

    def get_preconditions(self):
        preconditions = []
        if not self.is_precondition:
            return preconditions

        if not self.sub_attached_topics:
            preconditions.append(self.title)

        else:
            for sub_attached_topic in self.sub_attached_topics:
                sub_attached_topic = AttachedTopicAttribute(sub_attached_topic)
                preconditions.append(sub_attached_topic.title)

        return preconditions
