/**
 * This is the Javascript file needed to make the index.html file work
 */

import {dropDown_query, JSON_KEY_TO_OPTION_NAMES} from '../apiRoutes/api_endpoint.js'

/**
 * This function loads the leaflet map
 * @returns Returns the mymap object
 */
function loadMap() {

    const mymap = L.map('mapid').setView([38.8162729,-76.7523043], 10);   
    L.tileLayer('https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token={accessToken}', {
        attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, <a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
        maxZoom: 18,
        id: 'mapbox/streets-v11',
        accessToken: 'pk.eyJ1IjoiYXNhbmRpbjIxOCIsImEiOiJjazNwZm5kZDEwMm5qM3BwZTVwcmJvNGtpIn0.Omg_ZXfDgjgWA2-Lukxfow'
    }).addTo(mymap);
    
    
    return mymap
}
/**
 * This function populates the dropdown menu in index.html
 * @param  {object} JSON_KEY_TO_OPTION_NAMES : an object of the select element ,with a class name of feature_filters_drop_down, in the index.html file
 * @param  {object} myselect : a Map object created in the mainThread function
 */

function populateEnvFeaturesDropDown(JSON_KEY_TO_OPTION_NAMES, myselect) {

    console.log("Populating Environmental Features drop-down list.");
    
    // Add the options to the drop-down and build the documentation page
    
    for (let feature of JSON_KEY_TO_OPTION_NAMES) {
        let key = feature[0];
        let text = feature[1][0];
        if(!key.endsWith("_comments") && !key.startsWith("section1_time_stamp") && 
            !key.startsWith("section1_school_name") && !key.startsWith("section1_email") &&			   				   
            !key.startsWith("section6_enviro_awards") && !key.startsWith("section6_actions_not_mentioned") && 
            !key.startsWith("latitude") && !key.startsWith("longitude")) {
            let opt = document.createElement('option');
            opt.appendChild(document.createTextNode(text));
            // set value property of opt
            opt.value = key;
            // add option to the end of select box
            myselect.appendChild(opt);
        }
    }
}
/**
 * The displayMarkersByFeature function obtains the latitude and longitude of the schools, and displays them on the map as markers
 * @param  {object} myselect : an object of the select element ,with a class name of feature_filters_drop_down, in the index.html file
 * @param  {object} mymap : The map object from the loadMap function
 * @param  {object} markersLayer : A layer object related to the map. The markers are added to this layer, then the layer is added to the map for the markers to be visible
 * @async
 */

async function displayMarkersByFeature(myselect, mymap, markersLayer) {

    let feature = myselect.options[myselect.selectedIndex].value;
    // const dropDown_query = 'https://voyn795bv9.execute-api.us-east-1.amazonaws.com/Dev/getDataByColumnName?columnName='
    console.log("Displaying markers for: " + feature);
    
    // NOTE: The first thing we do here is clear the markers from the layer.
    markersLayer.clearLayers();

    const request = await fetch(dropDown_query + feature + "&value=Yes");
    let response = await request.json()
    console.log(response)
    response.forEach((item) => {
        const latitude = item.latitude;
            const longitude = item.longitude;    		  
                
            if(feature.toLowerCase().length > 0) {
                    if(item[feature].toLowerCase() == "yes") {
                        // Create a marker
                        const marker = L.marker([latitude, longitude]);
                        // Add a popup to the marker
                        marker.bindPopup(
                        "<b>" + item['schoolName'] + "</b><br>" +
                        "Website: <a target='_blank' href='" + item.website + "'>" + item.website + "</a><br>" +
                        "<img src='" + item.picture + "' style='width: 200px; height: 150px' /><br>"
                        ).openPopup();
                        // Add marker to the layer. Not displayed yet.
                        markersLayer.addLayer(marker);
                    }
            }
            // Display all the markers.
            markersLayer.addTo(mymap);
        }); 
}

/**
 * @param  {object} mymap : The map object from the loadMap function
 * @param  {object} perimLayer : The layer object that contains the Prince George's county perimeter polygon
 * @param  {object} countyPerimeter : An object that allows us to test if the toggle button is on or off
 */
function displayAreaCovered(mymap, perimLayer, countyPerimeter) {
    countyPerimeter.classList.toggle('active')
    if(countyPerimeter.classList[1]){  

        var polygon = L.polygon([
            [39.1297476, -76.8878470],
            [38.9658582, -77.0028848],
            [38.8924100, -76.9101263],
            [38.8040671, -77.0223920],
            [38.7084377, -77.0373222],
            [38.6892932, -77.0766706],
            [38.6165086, -77.0482834],
            [38.6603210, -76.9853651],
            [38.6516428, -76.9011842],
            [38.6608615, -76.8657629],
            [38.6168659, -76.7494621],
            [38.5582369, -76.7410240],
            [38.5401970, -76.6813885],
            [38.7833602, -76.7141972],
            [38.9053952, -76.6694931],
            [38.9900079, -76.7046728],
            [39.0766305, -76.8341119],
            [39.1025425, -76.8356350] 
            ]);
        
        perimLayer.addLayer(polygon);
        // Display all the markers.
        perimLayer.addTo(mymap);
        // console.log(markersLayer._layers)
    } 
    else{
        // console.log(markersLayer)
        perimLayer.clearLayers(polygon)
    }
}; 
 

/**
 * @param  {Array} sectionDropdown
 * @param  {object} markersLayer: A layer object related to the map. The markers are added to this layer, then the layer is added to the map for the markers to be visible
 * @param  {object} mymap : The map object from the loadMap function
 * @async
 */
async function displayMarkersBySectionRating(sectionDropdown,markersLayer,mymap) {
    console.log(sectionDropdown)
    const section = sectionDropdown.options[sectionDropdown.selectedIndex].value;
    const readAPI = 'https://voyn795bv9.execute-api.us-east-1.amazonaws.com/Dev/read_all_dynamodb';
    console.log("Displaying markers for school rating section: " + section);

    // NOTE: The first thing we do here is clear the markers from the layer.
    markersLayer.clearLayers();
    const request = await fetch(readAPI)
    let response = await request.json()
 
    response.forEach((item) =>{
       let numberYes = countYesForSection(item, section);	 
              let latitude = item.latitude;
              let longitude = item.longitude;
 
              let circle = L.circle([latitude, longitude], {
                  color: 'red',
                  fillColor: '#f03',
                  fillOpacity: 0.5,
                  radius: numberYes * (section === 'srf_all' ? 50 : 100)
              });
               
              // Add a popup to the circle
              circle.bindPopup(
                      "<b>" + item['schoolName'] + "</b><br>" +
                      "Total Yes: " + numberYes + "<br>" +
                      "Website: <a target='_blank' href='" + item.website + "'>" + item.website + "</a><br>" +
                      "<img src='" + item.picture + "' style='width: 200px; height: 150px' /><br>"		                
              ).openPopup();
               
              // Add marker to the layer. Not displayed yet.
              markersLayer.addLayer(circle);             
          
          // Display all the markers.
          markersLayer.addTo(mymap);
          // return res;
    })
}
/**
 * @param  {object} schoolData : An object of information about each school, sent from displayMarkersBySectionRating function
 * @param  {string} section : A string of chosen section
 */
function countYesForSection(schoolData, section) {
	var counter = 0;
	Object.entries(schoolData).forEach(([key, value]) => {
		if(typeof value === 'string' && value.toLowerCase() === "yes") {
			switch(section) {
			case "srf_all":
				counter++;
				break;
			case "srf_section1":
				if(key.startsWith("section1_")) counter++;
				break;
			case "srf_section2":
				if(key.startsWith("section2_")) counter++;
				break;
			case "srf_section3":
				if(key.startsWith("section3_")) counter++;
				break;
			case "srf_section4":
				if(key.startsWith("section4_")) counter++;
				break;
			case "srf_section5":
				if(key.startsWith("section5_")) counter++;
				break;
			}
		}
	});	
	return counter;
}
/**
 * The main function that runs first when the index.html page is loaded. 
 */
function mainThread(){
    
    const mymap = loadMap()
    let markersLayer = new L.LayerGroup();
    let perimLayer = new L.LayerGroup();
    const myselect = document.querySelector(".feature_filters_drop_down");
    const countyPerimeter = document.querySelector(".toggle-btn")
    const sectionSelect = document.querySelector(".section_filters_drop_down")
    populateEnvFeaturesDropDown(JSON_KEY_TO_OPTION_NAMES, myselect)
    myselect.addEventListener('change', (event) => {
        displayMarkersByFeature(myselect, mymap, markersLayer)
    });

    countyPerimeter.addEventListener('click', (event)=>{
        displayAreaCovered(mymap, perimLayer, countyPerimeter)
    })


    sectionSelect.addEventListener('change', (event) => {
        displayMarkersBySectionRating(sectionSelect,markersLayer,mymap)
    })
}

window.onload = mainThread