"""
    Sample test case for Robot testing framework.
    author: Petr Vacula
    license: MIT
"""

*** Settings ***
Documentation    Mainframe Test Automation using Zowe Client SDK
Library          mf_test_automation.py

*** Variables ***
${zosmf_profile}    TSO1
${jcl}              test/SORTSDK1.jcl
${test_data}        test/SORTSDK1.input.data
${expected_data}    test/SORTSDK1.expected.data
${dataset_name}     PUBLIC.MFTSTAUT.ROBOT.SORTSDK1

*** Test Cases ***
Run SORT job and validate results
    Fail If Data Set Exists  ${zosmf_profile}    ${dataset_name}
    Create Data Set    ${zosmf_profile}    ${dataset_name}
    Upload Test Data   ${zosmf_profile}    ${dataset_name}    ${test_data}
    ${job_response}    Submit Jcl Notify  ${zosmf_profile}    ${jcl}
    Validate Sort Job  ${zosmf_profile}    ${job_response}    ${expected_data}
    Delete Data Set    ${zosmf_profile}    ${dataset_name}
