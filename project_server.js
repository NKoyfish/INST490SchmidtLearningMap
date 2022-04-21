// import express JS module into app and creates its variable.
import express from "express";

const app = express();
const port = process.env.PORT || 80;
import { join } from "path";
import { spawn } from "child_process";
// var spawn = require("child_process").spawnSync

app.use(express.urlencoded({ extended: true }));
app.use(express.json());
app.use(express.static("./"));

// Creates a server which runs on port 3000 and
// can be accessed through localhost:3000
app.listen(port, () => console.log(`Server app listening on port ${port}!`));

// API to update the local database with Google data
app.get("/pythonTest", async (req, res) => {
  console.log("python");
  const python = spawn("python", [
    "./dynamoDB-scripts/test.py",
    "node.js",
    "python",
  ]);
  let dataToSend = "testttt";
  python.stdout.on("data", function (data) {
    console.log("Pipe data from python script ...");
    dataToSend = data.toString();
  });
  await python.on("close", (code) => {
    console.log(`child process close all stdio with code ${code}`);
    // send data to browser
    console.log(dataToSend);
    res.send(`<p>Updated?${dataToSend}</p>`);
  });
});
app.get("/updateDatabase", async (req, res) => {
  console.log("updateDatabase called");
  // Parameters passed in spawn -
  // 1. type_of_script
  // 2. list containing Path of the script and arguments for the script
  // code 0 is success
  // var spawn = require("child_process").spawnSync;

  try {
    // Parameters passed in spawn -
    // 1. type_of_script
    // 2. list containing Path of the script and arguments for the script
    // var spawn = require("child_process").spawnSync;
    var process = spawn("python", [
      "./dynamoDB-scripts/updateDynamoDB_test2.py",
    ]);
    let dataToSend = "";
    process.stdout.on("data", (data) => {
      dataToSend += data.toString();
    });
    process.stdout.on("end", (code) => {
      console.log(`child process close all stdio with code ${code}`);
      //console.log(dataToSend);
      res.json({ data: dataToSend });
    });
  } catch (err) {
    res.send(err);
  }
});

// API to get ALL data from database and return it in JSON format.
app.get("/getAllData", async (req, res) => {
  console.log("getAllData called");
  try {
    // Parameters passed in spawn -
    // 1. type_of_script
    // 2. list containing Path of the script and arguments for the script
    // var spawn = require("child_process").spawnSync;
    var process = spawn("python", ["./dynamoDB-scripts/readDynamoDB.py"]);
    let dataToSend = "";
    process.stdout.on("data", (data) => {
      dataToSend += data.toString();
    });
    process.stdout.on("end", (code) => {
      console.log(`child process close all stdio with code ${code}`);
      //console.log(dataToSend);
      res.json({ data: dataToSend });
    });
  } catch (err) {
    res.send(err);
  }
});

// API to get some data from database and return it in JSON format.
// It expects 2 parameters: columnName and value.
app.get("/getDataByColumnName", (req, res) => {
  console.log(
    "getDataByColumnName called. ColumnName=" +
      req.query.columnName +
      "; Value=" +
      req.query.value
  );

  // Parameters passed in spawn -
  // 1. type_of_script
  // 2. list containing Path of the script and arguments for the script
  // var spawn = require("child_process").spawnSync;
  var process = spawn("python", [
    "./query_database.py",
    req.query.columnName,
    req.query.value,
  ]);
  // console.log(process.stdout.toString())
  res.send(JSON.parse(process.stdout.toString()));
});

//API to get ALL data from database and return it in JSON format.
app.get("/getDuplicateSchools", (req, res) => {
  console.log("getDuplicateSchools called");

  // Parameters passed in spawn -
  // 1. type_of_script
  // 2. list containing Path of the script and arguments for the script
  // var spawn = require("child_process").spawnSync;
  var process = spawn("python", ["./query_duplicates_database.py"]);
  res.send(JSON.parse(process.stdout.toString()));
});

// This is in case someone tries to use a PUT command
app.put("/", (req, res) => {
  res.sendFile(join(__dirname + "/index.html"));
});

// This is in case someone tries to use a POST command
app.post("/", (req, res) => {
  res.sendFile(join(__dirname + "/index.html"));
});
