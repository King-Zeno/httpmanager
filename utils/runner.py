# 生成测试用例并执行
import datetime
import io
import json
from manager.models.project import Project
import os
import shutil
import time
from httprunner import report

import requests
from config import LOG_DIR, Config
from hrunmanage import settings
from httprunner import logger
from httprunner.api import HttpRunner
from httprunner.report import gen_html_report
from celery import shared_task
from manager.models.api import Api, APICate
from manager.models.case import TestCase
from manager.models.env import EnvParam
from manager.models.report import Report
from manager.models.plan import Plan, PlanCase
from manager.serializers.case import TestCaseListSerializer


class RunApi(object):

    def run(self, env, api_id):
        api_obj = Api.objects.get(pk=api_id)
        env_obj = EnvParam.objects.get(pk=env)
        url = '%s%s' % (env_obj.base_url, api_obj.url)
        method = api_obj.method
        headers = {**dict(env_obj.headers), **dict(api_obj.headers)}
        headers["Content-Type"] = "application/json"
        
        if method == 'get':
            params = api_obj.body
        else:
            params = {}
        # params = api_obj.body['params']
        data = api_obj.body

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

    def json_format(self, env, case_id):
        """ 格式化成 testcase json格式 """

        instance = TestCase.objects.get(pk=case_id)
        serializer = TestCaseListSerializer(instance=instance)
        project = instance.project.name

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

            # 用例引用
            if step['testcase']:
                case_id = step['testcase']
                data = self.json_format(env, case_id)
                testcase_path, json_file = self.dump_json_file(project, data)

                step['testcase'] = json_file

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

        json_file = os.path.join(testcase_path, data['config']['name'] + "-" + time.strftime("%Y%m%d") + ".json")

        with io.open(json_file, 'w', encoding='utf-8') as stream:
            json.dump(data, stream, indent=4, separators=(
                ',', ': '), ensure_ascii=False)

        return testcase_path, json_file

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

    def run_case(self, env, case_id):
        """ 
        执行用例
        """
        case_obj = TestCase.objects.get(pk=case_id)
        project = case_obj.project.name

        testcase = self.json_format(env, case_id)
        testcase_path, json_file = self.dump_json_file(project, testcase)

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

        report_path = self.add_test_reports(summary, report_name=case_obj.name)
        report_path = report_path.replace('\\','/')

        # 保存到数据库
        report_obj = Report.objects.filter(case=case_obj, path=report_path).first()
        if report_obj:
            report_obj.path = report_path
            report_obj.save()
        else:
            Report.objects.create(
                name = case_obj.name,
                path = report_path,
                case = case_obj
            )
            

        # 删除生成的工程目录
        shutil.rmtree(testcase_path)

        return report_path


@shared_task()
def run_plan(plan_id, env):
    """ 
    异步执行计划 
        plan_id    计划ID
        env        ENV ID
    """

    log_path = LOG_DIR
    log_level = Config.LEVEL
    log_file = os.path.join(log_path, "runner.log")

    plan_obj = Plan.objects.get(pk=plan_id)
    plan_case= PlanCase.objects.filter(plan=plan_id)
    project = plan_obj.project.name

    for case in plan_case:
        testcase = RunTestCase().json_format(env, case.id)
        testcase_path, json_file = RunTestCase().dump_json_file(project, testcase)
    
    logger.setup_logger(log_level, log_file)

    kwargs = {
        "failfast": False,
        "log_level": log_level,
        "log_file": log_file
    }
    runner = HttpRunner(**kwargs)
    summary = runner.run_path(testcase_path)

    # 删除生成的工程目录
    shutil.rmtree(testcase_path)
    report_path = RunTestCase().add_test_reports(summary, report_name=plan_obj.name)
    report_path = report_path.replace('\\','/')

    # 保存到数据库
    report_obj = Report.objects.filter(plan=plan_id, path=report_path).first()
    
    if  report_obj:
        report_obj.path = report_path
        report_obj.save()
    else:
        Report.objects.create(
            name = plan_obj.name,
            path = report_path,
            plan = plan_obj
        )

    return report_path


# 导入接口数据
def import_api(project_id, file_obj, author):
    json_file = json.load(file_obj)
    project = Project.objects.get(pk=project_id)
    for cate in json_file:
        cate_obj = APICate.objects.create(project=project, name=cate['name'])
        for i in cate['list']:
            Api.objects.create(
                project = project,
                cate = cate_obj,
                name = i['title'],
                method = i['method'].lower(),
                url = i['path'],
                author = author
            )