//import the JSON_KEY_TO_OPTION_NAMES from apiRoutes/api_endpoint.js
import {JSON_KEY_TO_OPTION_NAMES} from '../apiRoutes/api_endpoint.js'

/**
 * This function populates the documentation.html page.
 * @param  {object} JSON_KEY_TO_OPTION_NAMES: A Map object that contains the appropriate titles for the sections
 */
function populateEnvFeaturesDocumentation(JSON_KEY_TO_OPTION_NAMES) {
	console.log("Populating Environmental Features documentation.");
   
	var mydocumentation = document.getElementById("EnvFeatures");	
	for (let feature of JSON_KEY_TO_OPTION_NAMES) {
		let key = feature[0];
		if(!key.endsWith("_comments") && !key.startsWith("section1_time_stamp") && 
		   !key.startsWith("section1_school_name") && !key.startsWith("section1_email") &&			   				   
		   !key.startsWith("section6_enviro_awards") && !key.startsWith("section6_actions_not_mentioned") && 
		   !key.startsWith("latitude") && !key.startsWith("longitude")) {
			let columnName = feature[1][0];
			let description = feature[1][1]
			let heading = document.createElement("h5");
			let text = document.createTextNode(columnName);
			heading.appendChild(text);
			mydocumentation.appendChild(heading);
	 
			let para = document.createElement("p");
			para.className += "text-grey";
			text = document.createTextNode(description);
			para.appendChild(text);
			mydocumentation.appendChild(para);
	 
			let mybreak = document.createElement("br");
			mydocumentation.appendChild(mybreak);
		}
	}
}

/**
 * The main function that is called when the documentation.html page is loaded
 */
function mainThread(){

    populateEnvFeaturesDocumentation(JSON_KEY_TO_OPTION_NAMES)
}

window.onload=mainThread