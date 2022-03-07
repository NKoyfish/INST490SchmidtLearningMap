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
      <ul>git clone "https://github.com/asandin218/pgcps_enviro_literacy490.git</ul>
    <li>Install npm for your specific OS</li>
      <ul> https://nodejs.org/en/download/ </ul>
    <li>Execute 'npm install' command</li>
    <li>Execute 'pip install wheel' command</li>
    <li>Execute 'python -m pip install --upgrade pip' command</li>
    <li>Execute 'pip install express requests bs4 pymysql' command</li>
  </ol>
<h1>How to run application on a server </h1>
  <ol>
    <li>Execute 'npm start' command</li>
    <li>Open browser and connect to the local host</li>
    <li>http://localhost</li>
  </ol>
<h1>How to run tests </h1>
  <ol>
    <li>Executing npm start will test the application and return back any errors before launching it</li>
  </ol>
<h1>The API for the server application </h1>  
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
  <p>There are no known bugs right now. Future development would spread our map to other counties, which may cause a bug
  if the map becomes too large. It would be bad if the map was so big that the user could not distinguish any of the school points. </p>
