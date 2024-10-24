const fs = require("fs");
const csvParser = require("csv-parser");

const result = [];

fs.createReadStream("./Testing.csv")
  .pipe(csvParser())
  .on("data", (data) => {
    result.push(data);
  })
  .on("end", () => {
    console.log(result);
    createSampleJsonTestData(result)
  });



function createSampleJsonTestData (data) {
  const path = './samplTestData.js';
  const line = `const data = ${JSON.stringify(data)}`
  fs.writeFile(path, line, (error) => {
    if (error) {
      console.log('An error has occurred ', error);
      return;
    }
    console.log('Data written successfully to disk');
  });

}