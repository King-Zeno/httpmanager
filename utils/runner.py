# 生成测试用例并执行
import io
import json
import os
import re
import time

import requests
from httprunner import Config, HttpRunner, RunRequest, RunTestCase, Step
from manager.models.api import Api
from manager.models.case import TestCase, TestStep
from manager.models.env import EnvParam
from manager.serializers.case import TestCaseListSerializer


class RunApi(object):

    def run(self, env, api_id):
        api_obj = Api.objects.get(pk=api_id)
        env_obj = EnvParam.objects.get(pk=env)
        url = '%s%s' % (env_obj.base_url, api_obj.url)
        method = api_obj.method
        headers = env_obj.headers
        headers['Content-Type'] = 'application/json'
        params = api_obj.body['params']
        data = api_obj.body['data']

        r = requests.request(method, url, headers=headers,
                             params=params, json=data, timeout=5)

        if r.status_code in (200, 201, 203, 204):
            data = r.json()
        else:
            data = r

        return data


class RunTestCase(object):
    """
        生成可执行的 json 格式用例，并运行生成报告
    """

    def json_fromat(env, case_id):
        """ 格式化成 testcase json格式 """

        instance = TestCase.objects.get(pk=case_id)
        serializer = TestCaseListSerializer(instance=instance)

        test_case = {}
        test_case['config'] = {}
        test_case['teststeps'] = []
        env_obj = EnvParam.objects.get(pk=env)
        test_case['config']['name'] = serializer.data['name']
        test_case['config']['variables'] = serializer.data['variables']
        test_case['config']['base_url'] = env_obj.base_url
        test_case['config']['export'] = serializer.data['export']
        test_case['config']['parameters'] = serializer.data['parameters']

        for key in list(test_case['config'].keys()):
            if not test_case['config'].get(key):
                del test_case['config'][key]

        for step in serializer.data['case_step']:
            del step['id']
            del step['sort']
            del step['case']

            for key in list(step.keys()):
                if not step.get(key):
                    del step[key]
            test_case['teststeps'].append(step)

        return test_case

    def dump_json_file(project, data):
        """ 写入json 文件 """

        path = "testcase"
        testcase_dir_path = os.path.join(path, str(project))

        if not os.path.exists(testcase_dir_path):
            os.mkdir(testcase_dir_path)

        json_file = "%s/%s.json" % (testcase_dir_path, time.strftime("%Y%m%d"))
        with io.open(json_file, 'w', encoding='utf-8') as stream:
            json.dump(data, stream, indent=4, separators=(
                ',', ': '), ensure_ascii=False)

        return json_file


