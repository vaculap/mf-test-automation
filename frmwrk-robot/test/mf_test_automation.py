"""
    Sample test case for Robot testing framework.
    author: Petr Vacula
    license: MIT
"""

from zowe.zos_jobs_for_zowe_sdk import Jobs
from zowe.zos_files_for_zowe_sdk import Files
import time
import subprocess
import json


def fail_if_data_set_exists(zosmf_profile, dataset_name):
    """
    Check whether data set exists and throw and exception if it does
    """
    connection = {'plugin_profile': zosmf_profile}
    files = Files(connection)
    list_dsn = files.list_dsn(dataset_name)

    if list_dsn['returnedRows'] == 0 :
        return False
    elif list_dsn['items'][0]['dsname'] == dataset_name :
        raise AssertionError('>>> ERROR: %s data set exists!' % (dataset_name))
    else:
        return False


def create_data_set(zosmf_profile, dataset_name):
    """
    Create a new sequential data set
    Zowe Python SDK does not implement create data set yet -> using CLI command for now
    OPPORTUNITY: implement the data set create functionality under Python SDK
    """
    cmd = 'zowe zos-files create data-set-sequential %s --zosmf-p %s' % (dataset_name, zosmf_profile)
    subprocess.run(cmd, capture_output=True, shell=True)


def upload_test_data(zosmf_profile, dataset_name, test_data):
    """
    Upload test data into a newly created data set
    """
    connection = {'plugin_profile': zosmf_profile}
    files = Files(connection)
    files.upload_file_to_dsn(test_data, dataset_name)


def submit_jcl_notify(zosmf_profile, jcl):
    """
    Submit job from local file
    Return job response
    """
    
    TIMEOUT = 120
    STEP = 2

    connection = {'plugin_profile': zosmf_profile}
    job = Jobs(connection)
    response = job.submit_from_local_file(jcl)

    job_name = response['jobname']
    job_id = response['jobid']

    timeout = time.time() + TIMEOUT
    while response['status'] != 'OUTPUT':
        if time.time() > timeout:
            raise TimeoutError('>>> ERROR: Job %s(%s) exceeded timeout of %s secs' % (job_name, job_id, TIMEOUT))
        time.sleep(STEP)
        response = job.get_job_status(job_name, job_id)    
    
    return response


def validate_sort_job(zosmf_profile, job_response, expected_data):
    """
    Run validation for sort job
    check RC=0 and SORTOUT is as expected
    """
    if job_response['retcode'] != 'CC 0000':
        raise AssertionError('>>> ERROR: %s(%s) ended with %s' 
    % (job_response['jobname'], job_response['jobid'], job_response['retcode']))

    job_id = job_response['jobid']
    
    cmd = 'zowe zos-jobs list spool-files-by-jobid %s --rfj --zosmf-p %s' % (job_id, zosmf_profile)
    result = subprocess.run(cmd, capture_output=True, shell=True)
    output_json = json.loads(result.stdout)

    dd_id = 0
    for item in output_json['data']:
        if item['ddname'] == 'SORTOUT':
            dd_id = item['id']
            break
    
    cmd = 'zowe zos-jobs view spool-file-by-id %s %s --rfj --zosmf-p %s' % (job_id, dd_id, zosmf_profile)
    result = subprocess.run(cmd, capture_output=True, shell=True)
    output_json = json.loads(result.stdout)

    if output_json['stdout'] != open(expected_data).read():
        raise AssertionError('>>> ERROR: SORTOUT output is not as expected')


def delete_data_set(zosmf_profile, dataset_name):
    """
    Delete test data set
    Zowe Python SDK does not implement delete data set yet -> using CLI command for now
    OPPORTUNITY: implement the data set create functionality under Python SDK
    """
    cmd = 'zowe zos-files delete data-set %s --for-sure --zosmf-p %s' % (dataset_name, zosmf_profile)
    subprocess.run(cmd, capture_output=True, shell=True)
