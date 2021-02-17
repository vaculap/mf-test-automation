# Mainframe Test Automation using Mocha.js testing framework

Sample project illustrating use of Mocha.js testing framework together with Chai assertion library to test mainframe applications. The samples use Zowe CLI to perform mainframe actions.

![Run test case](../media/frmwrk-mocha.gif)

## Prerequisites
* Node.js
* Zowe CLI with defined default z/OSMF profile for Zowe CLI samples

## Recommendations
* Visual Studio Code

## How to initialize this Mocha.js project - cloned from git repository
1. Install needed packages

    `npm install`

## Files
* `SORTCLI1.expected.data`
    * Expected data output from the Sort job. It is used for asserting the job output.
* `SORTCLI1.input.data`
    * Input data for the Sort job. It is uploaded to data set for the job to process.
* `SORTCLI1.jcl`
    * Sort job JCL.
* `SORTCLI1.test.js`
    * This is the actual Mocha.js Testing Framework test case.

## How to run test cases
If prerequisites are met, simply execute following command:

    npx mocha

Optionally use defined NPM Scripts through the VSCode Explorer