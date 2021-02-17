# Sample test cases for Jest testing framework.

Sample project ilustrating use of Jest Testing Framework to test mainframe applications. Sample test cases cover the use Zowe CLI as well as Zowe Node.js SDK.

## Prerequisities
* Node.js
* Zowe CLI with defined default z/OSMF profile for Zowe CLI samples

## Recomendations
* Visual Studio Code
* Jest Runner VSCode extension

## How to initialize this Jest project - cloned from git repository
1. Install needed packages

    `npm install`

## How to initialize your Jest project - when starting completely from scratch

1. Initialize package.json

    `npm init -y`

2. Install needed packages

    `npm install -D jest typescript ts-jest @types/jest @zowe/imperative @zowe/cli`

3. Create ts-jest configuration to use typescript with Jest

    `npx ts-jest config:init`

## Files
* `SORTCLI1.expected.data`
    * Expected data output from the Sort job. It is used for asserting the job output.
* `SORTCLI1.input.data`
    * Input data for the Sort job. It is uploaded to data set for the job to process.
* `SORTCLI1.jcl`
    * Sort job JCL.
* `SORTCLI1.test.ts`
    * This is the actual Jest Testing Framework test case using Zowe CLI to communicate with mainframe.

* `SORTSDK1.expected.data`
    * Expected data output from the Sort job. It is used for asserting the job output.
* `SORTSDK1.input.data`
    * Input data for the Sort job. It is uploaded to data set for the job to process.
* `SORTSDK1.jcl`
    * Sort job JCL.
* `SORTSDK1.test.ts`
    * This is the actual Jest Testing Framework test case using Zowe Node.js SDK to communicate with mainframe.

## How to run test cases
If prerequisities are met, simply execute following command:

    npm run test

Optionaly use defined NPM Scripts through the VSCode Explorer
* test
    * to run all test cases
* testCLI
    * to run only CLI test case
* test SDK
    * to run only SKD test case

Yet another option is using Jest Runner in VSCode. It adds run | debug buttons in front of every test case and test suite.