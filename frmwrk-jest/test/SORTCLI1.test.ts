import { execSync } from "child_process";

interface cmdResponse {
    success: boolean;
    data: jobLog[];
}

interface jobLog {
    ddName: string;
    data: string;
}

describe("Mainframe Test Automation under Jest using Zowe CLI", () => {

    test('running SORT job and validate results', () => {
        const dsName = "PUBLIC.MFTSTAUT.JEST.SORTCLI1";
        const expectedData = "test/SORTCLI1.expected.data";
        const dsInput = "test/SORTCLI1.input.data";
        const jcl = "test/SORTCLI1.jcl";

        // LIST work data set
        const lsDs = execSync(`zowe zos-files list data-set ${dsName} --max 1`).toString().trim();
        expect(lsDs).not.toBe(dsName);  // ? File does not exist

        // CREATE work data set
        const crDs = execSync(`zowe zos-files create data-set-sequential ${dsName}`).toString();

        // UPLOAD test data
        const upDs = execSync(`zowe zos-files upload file-to-data-set ${dsInput} ${dsName}`).toString();

        // SUBMIT job
        const jobS = execSync(`zowe zos-jobs submit local-file ${jcl} --vasc --rfj`).toString();
        const resp: cmdResponse = JSON.parse(jobS);
        expect(resp.success)    // ? Job completed successfully

        const sortOut = resp.data.find(el => el.ddName == "SORTOUT").data;
        var fs = require('fs');
        expect(sortOut).toBe(fs.readFileSync(expectedData, 'utf8'));   // ? Expected SORTOUT

        // CLEANUP
        const rmDs = execSync(`zowe zos-files delete data-set ${dsName} --for-sure`).toString();
    });
});