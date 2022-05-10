<p>Title of Project: Prince George County Public School - Literacy 490</p>
<p>Description of Project: Helps visually represent how environment-friendly schools are throughout PGC</p>
<p>Link to App: http://localhost/</p>
<p>Target Browsers: Google Chrome, Mozilla Firefox, Safari, Microsoft Edge</p>
<p>Link to User Manual: https://github.com/asandin218/pgcps_enviro_literacy490/README.md</p><br/>
<p>Link to Developer Manual: See below. </p><br/>

# Developer Manual
<h1>How to install application and all dependencies</h1>
  <ol>
    <li>Download the source code from GitHub</li>
      <ul>git clone "https://github.com/NKoyfish/INST490SchmidtLearningMap.git</ul>
    <li>Install npm for your specific OS</li>
      <ul> https://nodejs.org/en/download/ </ul>
    <li>Execute 'npm install' command</li>
    <li>Execute 'pip install wheel' command</li>
    <li>Execute 'python -m pip install --upgrade pip' command</li>
    <li>Execute 'pip install express requests bs4 pymysql' command</li>
    <li>If there were any dependencies that we failed to mention 'pip install' those as well.
  </ol>
<h1>How to run application on a server </h1>
  <ol>
    <li>Execute 'npm start' command</li>
    <li>Open browser and connect to the local host</li>
    <li>http://localhost</li>
  </ol>
<h1>The API for the server application in case AWS Lambda is hard to use</h1>
  <h2>You will need to download the keys.json file from AWS to run some of the scripts locally</h2>
  <p>Some of the api routes weren't fully set up since it appears that it was deprecated when we (2022 Spring Semester) took a look at it. We gathered this after seeing the api routes referring to incorrect python scripts paths. A guide on how to update the database should be provided via Donald or a google drive link</p>
  <ol>
    <li>To return all of the survey data</li>
      <ul> http://localhost/getAllData</ul>
    <li>To update database with all data from Google surveys</li>
      <ul> http://localhost/updateDatabase </ul>
    <li>To return records that match the query; when calumnName equals value</li>
      <ul> http://localhost/getDataByColumnName?columnName=<column name>&value=<value to query></ul>
    <li>To return records of schools that have the same name</li>
      <ul> http://localhost/getDuplicateSchools</ul>
  </ol>
<h1>Any expectations around known bugs and road-map for future development </h1>
  <ol>
    <li>Better Marker icons</li>
    <li>Click through the school result list to pan to that specific school</li>
    <li>Allow for authentication for schools to upload pictures</li>
    <li>Add more details to map pane</li>
    <li>Add a legend for leaflet</li>
    <li>Remove old code that no longer is needed</li>
    <li>Redeploy app to AWS</li>
  </ol>
