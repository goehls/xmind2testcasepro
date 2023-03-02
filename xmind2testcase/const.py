#!/usr/bin/env python
# _*_ coding:utf-8 _*_


TAG_XML = 'xml'
TAG_JSON = 'json'

TAG_TESTSUITE = 'testsuite'
TAG_DETAILS = 'details'

TAG_TESTCASE = 'testcase'
TAG_VERSION = 'version'
TAG_SUMMARY = 'summary'
TAG_PRECONDITIONS = 'preconditions'
TAG_IMPORTANCE = 'importance'
TAG_ESTIMATED_EXEC_DURATION = 'estimated_exec_duration'
TAG_STATUS = 'status'
TAG_IS_OPEN = 'is_open'
TAG_ACTIVE = 'active'
TAG_STEPS = 'steps'
TAG_STEP = 'step'
TAG_STEP_NUMBER = 'step_number'
TAG_ACTIONS = 'actions'
TAG_EXPECTEDRESULTS = 'expectedresults'
TAG_EXECUTION_TYPE = 'execution_type'

ATTR_NMAE = 'name'
ATTR_ID = 'id'
ATTR_INTERNALID = 'internalid'

# -- boyi --
PRECONDITIONS_TAG = '前置条件'
TESTCASE_TAG = '测试用例'
TESTCASE_IGNORE_TAGS = ['ignore', 'skipped']
TESTSTEP_TAG = '执行步骤'
EXPECT_RESULT_TAG = '预期结果'

IMPORTANCE_TAGS = ['P[0-9]', 'priority-[0-9]']

EXECUTION_AUTO_TYPE_TAG = ['自动', 'auto', 'automate', 'automation']
EXECUTION_MANUAL_TYPE_TAG = ['手动', '手工', 'manual']
EXECUTION_MANUAL_TYPE = 1
EXECUTION_AUTO_TYPE = 2

config = {'sep': '<font color="red"> >> </font>',
          'valid_sep': '&>+/-',
          'precondition_sep': '\n----\n',
          'summary_sep': '\n----\n',
          'step': '\n#####\n',
          'ignore_char': '#!！'
          }
