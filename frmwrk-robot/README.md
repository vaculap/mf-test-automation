# Mainframe Test Automation using Robot testing framework

Sample project ilustrating use of Robot Testing Framework together with Zowe Python Client SDK to test mainframe applications.

## Prerequisities
* python (python.org)
* robot framework (python -m pip install robotframework)

## Recomendations
* Visual Studio Code
* Python VSCode extension
* Pylance VSCode extension
* Robot Framework Language Server VSCode extension

## Files
* `mf_test_automation.py`
    * Python library defining Robot keywords specific to Mainframe Testing. It uses Zowe Python library to perform mainframe actions.
* `SORTSDK1.expected.data`
    * Expected data output from the Sort job. It is used for asserting the job output.
* `SORTSDK1.input.data`
    * Input data for the Sort job. It is uploaded to data set for the job to process.
* `SORTSDK1.jcl`
    * Sort job JCL.
* `SORTSDK1.test.robot`
    * This is the actual Robot Testing Framework test case.

## How to run the test case
If prerequisities are met, simply run:

`robot SORTSDK1.test.robot`