import { IProfile, Session } from "@zowe/imperative";
import { ZosmfSession } from "@zowe/zosmf-for-zowe-sdk";
import { getDefaultProfile } from "@zowe/core-for-zowe-sdk";
import { List, Create, IZosFilesResponse, CreateDataSetTypeEnum, Upload, Delete } from "@zowe/zos-files-for-zowe-sdk";
import { SubmitJobs, GetJobs, IJob } from "@zowe/zos-jobs-for-zowe-sdk";
import { readFileSync } from 'fs';

let session: Session;

beforeAll(async () => {
    let defaultZosmfProfile: IProfile = await getDefaultProfile("zosmf", true);
    session = ZosmfSession.createBasicZosmfSession(defaultZosmfProfile);
})

describe("Mainframe Test Automation under Jest using Zowe Client SDK", () => {

    test('running SORT job and validate results', async () => {
        const dsName = "PUBLIC.MFTSTAUT.JEST.SORTSDK1";
        const expectedData = "test/SORTSDK1.expected.data";
        const dsInput = "test/SORTSDK1.input.data";
        const jcl = "test/SORTSDK1.jcl";

        // LIST work data set
        const lsDs: IZosFilesResponse = await List.dataSet(session, dsName, { maxLength: 1 });
        expect(Object.keys(lsDs.apiResponse.items).length).toBe(0); // ? File does not exist

        // CREATE work data set
        const crDs = await Create.dataSet(session, CreateDataSetTypeEnum.DATA_SET_SEQUENTIAL, dsName);

        // UPLOAD test data
        const upDs = await Upload.pathToDataSet(session, dsInput, dsName);

        // SUBMIT job
        const job: IJob = await SubmitJobs.submitJclNotify(session, readFileSync(jcl, 'utf8'));
        expect(job.retcode).toBe("CC 0000");    // ? Job completed successfully

        const jobLogs = await GetJobs.getSpoolFilesForJob(session, job);
        const jobFile = jobLogs.find(el => el.ddname == "SORTOUT");
        const sortOut = await GetJobs.getSpoolContent(session, jobFile);
        expect(sortOut).toBe(readFileSync(expectedData, 'utf8'));   // ? Expected SORTOUT

        // CLEANUP
        const rmDs = await Delete.dataSet(session, dsName);
    });
});