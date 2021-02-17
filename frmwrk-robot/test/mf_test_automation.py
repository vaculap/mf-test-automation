from zowe.zos_jobs_for_zowe_sdk import Jobs
from zowe.zos_files_for_zowe_sdk import Files
import os
import time
import subprocess
import json


# Check whether data set exists
# Throw an exeption if it does
def data_set_exists(zosmfProfile, dsName):
    connection = { "plugin_profile": zosmfProfile}
    files = Files(connection)
    lsDs = files.list_dsn(dsName)

    if lsDs['returnedRows'] == 0 :
        return False
    elif lsDs['items'][0]['dsname'] == dsName :
        raise AssertionError('>>> ERROR: ' + dsName + ' data set exists!')
        return True
    else:
        return False


# Create a new test data set
# Zowe Python SDK does not implement create data set yet -> using CLI command for now
def create_data_set(zosmfProfile, dsName):
    os.system('zowe zos-files create data-set-sequential ' + dsName + ' --zosmf-p ' + zosmfProfile + ' > nul')


# Upload test data into a newly clreated data set
def upload_test_data(zosmfProfile, dsName, testData):
    connection = { "plugin_profile": zosmfProfile}
    files = Files(connection)
    upDs = files.upload_file_to_dsn(testData, dsName)


# Submit job from local file
# return job response
def submit_jcl_notify(zosmfProfile, jcl):
    
    TIMEOUT = 120
    STEP = 2

    connection = { "plugin_profile": zosmfProfile}
    job = Jobs(connection)
    resp = job.submit_from_local_file(jcl)
    
    jobName = resp["jobname"]
    jobId = resp["jobid"]

    counter = 0
    while resp["status"] != 'OUTPUT':
        if counter >= TIMEOUT:
            raise TimeoutError('>>> ERROR: ' + jobName + '(' + jobId + ') exeeded time out: ' + str(counter))
            break
        time.sleep(STEP)
        counter += STEP
        resp = job.get_job_status(jobName, jobId)    
    
    return resp


# Run validation for sort job
# check RC=0 and SORTOUT is as expected
def validate_sort_job(zosmfProfile, jobResp, expectedData):
    if jobResp["retcode"] != 'CC 0000':
        raise AssertionError('>>> ERROR: ' + jobResp["jobname"] + '(' + jobResp["jobid"] + 
    ') ended with ' + jobResp["retcode"])

    jobId = jobResp["jobid"]
    
    cmd = ['zowe', 'zos-jobs', 'list', 'spool-files-by-jobid', jobId, '--rfj', '--zosmf-p', zosmfProfile]
    p = subprocess.Popen(cmd,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    stdout,stderr = p.communicate()
    outJson = json.loads(stdout)

    ddId = 0
    for item in outJson['data']:
        if item["ddname"] == 'SORTOUT':
            ddId = item["id"]
            break
    
    cmd = ['zowe', 'zos-jobs', 'view', 'spool-file-by-id', jobId, str(ddId), '--rfj']
    p = subprocess.Popen(cmd,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    stdout,stderr = p.communicate()
    outJson = json.loads(stdout)

    if outJson['stdout'] != open(expectedData).read():
        raise AssertionError(">>> ERROR: SORTOUT ouput is not as expected")


# Delete test data set
# Zowe Python SDK does not implement delete data set yet -> using CLI command for now
def delete_data_set(zosmfProfile, dsName):
    os.system('zowe zos-files delete data-set ' + dsName + ' --for-sure --zosmf-p ' + zosmfProfile + ' > nul')
    return True