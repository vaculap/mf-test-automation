const expect = require('chai').expect;
const fs = require('fs');
const { execSync } = require("child_process");

describe("Mainframe Test Automation under Mocha using Zowe CLI", function() {
    this.timeout(60000)
    
    it('should run SORT job and validate results', function() {
        const dsName = "PUBLIC.MFTSTAUT.MOCHA.SORTCLI1";
        const expectedData = "test/SORTCLI1.expected.data";
        const dsInput = "test/SORTCLI1.input.data";
        const jcl = "test/SORTCLI1.jcl";

        // LIST work data set
        const lsDs = execSync(`zowe zos-files list data-set ${dsName} --max 1`).toString().trim();
        expect(lsDs).not.to.equal(dsName); // ? File does not exist

        // CREATE work data set
        const crDs = execSync(`zowe zos-files create data-set-sequential ${dsName}`).toString();

        // UPLOAD test data
        const upDs = execSync(`zowe zos-files upload file-to-data-set ${dsInput} ${dsName}`).toString();

        // SUBMIT job
        const jobS = execSync(`zowe zos-jobs submit local-file ${jcl} --vasc --rfj`).toString();
        const resp = JSON.parse(jobS);
        expect(resp.success) // ? Job completed successfully

        const sortOut = resp.data.find(el => el.ddName == "SORTOUT").data;
        expect(sortOut).to.equal(fs.readFileSync(expectedData, 'utf8')); // ? Expected SORTOUT

        // CLEANUP
        const rmDs = execSync(`zowe zos-files delete data-set ${dsName} --for-sure`).toString();
    });
});