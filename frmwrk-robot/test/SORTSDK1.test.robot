*** Settings ***
Documentation    Mainframe Test Automation using Zowe Client SDK
Library          mf_test_automation.py

*** Variables ***
${zosmfProfile}    TSO1
${jcl}             SORTSDK1.jcl
${testData}        SORTSDK1.input.data
${expectedData}    SORTSDK1.expected.data
${dsName}          PUBLIC.MFTSTAUT.ROBOT.SORTSDK1

*** Test Cases ***
Run SORT job and validate results
    Data Set Exists    ${zosmfProfile}    ${dsName}
    Create Data Set    ${zosmfProfile}    ${dsName}
    Upload Test Data   ${zosmfProfile}    ${dsName}    ${testData}
    ${jobResp}    Submit Jcl Notify  ${zosmfProfile}    ${jcl}
    Validate Sort Job  ${zosmfProfile}    ${jobResp}    ${expectedData}
    Delete Data Set    ${zosmfProfile}    ${dsName}




