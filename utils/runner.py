# 生成测试用例并执行
import datetime
import io
import json
import os
import shutil
import time

import requests
from config import LOG_DIR, Config
from hrunmanage import settings
from httprunner import logger
from httprunner.api import HttpRunner
from httprunner.report import gen_html_report, get_summary
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

    log_path = LOG_DIR
    log_level = Config.LEVEL

    def json_fromat(self, env, case_id):
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

    def dump_json_file(self, project, data):
        """ 写入json 文件，返回用例路径 """

        path = os.path.join(settings.BASE_DIR, "testcase")
        testcase_path = os.path.join(path, str(project))

        if not os.path.exists(testcase_path):
            os.mkdir(testcase_path)

        json_file = os.path.join(testcase_path, time.strftime("%Y%m%d") + ".json")

        with io.open(json_file, 'w', encoding='utf-8') as stream:
            json.dump(data, stream, indent=4, separators=(
                ',', ': '), ensure_ascii=False)

        return testcase_path

    def add_test_reports(self, summary, report_name=None):
        """
        生成 html 报告
        """

        time_stamp = int(summary["time"]["start_at"])
        summary['time']['start_datetime'] = datetime.datetime.fromtimestamp(
            time_stamp).strftime('%Y-%m-%d %H:%M:%S')
        summary['html_report_name'] = report_name

        report_dir = "report"

        if not os.path.exists(report_dir):
            os.mkdir(report_dir)

        if report_name:
            report_file = os.path.join(report_dir, "%s%s.html" % (
                report_name, time.strftime("%Y%m%d")))
        else:
            report_file = os.path.join(
                report_dir, "%s.html" % time.strftime("%Y%m%d"))

        gen_html_report(summary, report_file=report_file)

        return report_file

    def run_case(self, project, env, case_id):
        """ 
        执行用例
        """

        testcase = self.json_fromat(env, case_id)
        testcase_path = self.dump_json_file(project, testcase)

        if not os.path.exists(self.log_path):
            os.mkdir(self.log_path)
        log_file = os.path.join(self.log_path, "runner.log")

        logger.setup_logger(self.log_level, log_file=log_file)

        kwargs = {
            "failfast": False,
            "log_level": self.log_level,
            "log_file": log_file
        }
        runner = HttpRunner(**kwargs)
        summary = runner.run(testcase_path)

        # 删除生成的工程目录
        shutil.rmtree(testcase_path)
        report_path = self.add_test_reports(summary, report_name=project)

        return report_path
