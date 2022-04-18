/**
 * This is the Javascript file needed to make the index.html file work
 */

import {
  dropDown_query,
  JSON_KEY_TO_OPTION_NAMES,
} from "../apiRoutes/api_endpoint.js";
let lastSectionFilter = {};
let currMatches = [];
function displayCurrMatches() {
  console.log(currMatches);
}
/**
 * This function loads the leaflet map
 * @returns Returns the mymap object
 */
function loadMap() {
  const mymap = L.map("mapid").setView([38.8162729, -76.7523043], 10);
  L.tileLayer(
    "https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token={accessToken}",
    {
      attribution:
        'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, <a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
      maxZoom: 18,
      id: "mapbox/streets-v11",
      accessToken:
        "pk.eyJ1IjoiYXNhbmRpbjIxOCIsImEiOiJjazNwZm5kZDEwMm5qM3BwZTVwcmJvNGtpIn0.Omg_ZXfDgjgWA2-Lukxfow",
    }
  ).addTo(mymap);

  return mymap;
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
    if (
      !key.endsWith("_comments") &&
      !key.startsWith("section1_time_stamp") &&
      !key.startsWith("section1_school_name") &&
      !key.startsWith("section1_email") &&
      !key.startsWith("section6_enviro_awards") &&
      !key.startsWith("section6_actions_not_mentioned") &&
      !key.startsWith("latitude") &&
      !key.startsWith("longitude")
    ) {
      let opt = document.createElement("option");
      opt.appendChild(document.createTextNode(text));
      // set value property of opt
      opt.value = key;
      // add option to the end of select box
      myselect.appendChild(opt);
    }
  }
}

/**
 * This function populates the dropdown for advanced filtering (checkbox) menu in index.html by related section
 * @param  {object} JSON_KEY_TO_OPTION_NAMES : an object of the select element ,with a class name of feature_filters_drop_down, in the index.html file
 * @param  {object} myselect : selector for the tab we are inserting checkboxes into
 * @param {object} section: string of section we want to populate options
 */

function populateEnvFeaturesCheckbox(
  JSON_KEY_TO_OPTION_NAMES,
  myselect,
  section
) {
  console.log("Populating Environmental Features drop-down list.");
  let inject = "";
  // Add the options to the drop-down and build the documentation page

  for (let feature of JSON_KEY_TO_OPTION_NAMES) {
    let key = feature[0];
    let text = feature[1][0];
    if (
      !key.endsWith("_comments") &&
      !key.startsWith("section1_time_stamp") &&
      !key.startsWith("section1_school_name") &&
      !key.startsWith("section1_email") &&
      !key.startsWith("section6_enviro_awards") &&
      !key.startsWith("section6_actions_not_mentioned") &&
      !key.startsWith("latitude") &&
      !key.startsWith("longitude") &&
      key.startsWith(section)
    ) {
      //console.log("match", feature[0], section);
      let string = `<div id=labelCheck><label for="${feature[0]}">${text}<input title="checkboxClick"type="checkbox" id ="${key}" value="${text}"></label></div>`;
      let opt = document.createElement("label");
      opt.appendChild(document.createTextNode(text));
      // set value property of opt
      opt.value = key;
      // add option to the end of select box
      inject += string;
    }
  }
  myselect.innerHTML = inject;
}

/**
 * This function populates the dropdown menu in index.html by related section
 * @param  {object} JSON_KEY_TO_OPTION_NAMES : an object of the select element ,with a class name of feature_filters_drop_down, in the index.html file
 * @param  {object} myselect : a Map object created in the mainThread function
 * @param {object} section: string of section we want to populate options
 */

function populateEnvFeaturesDropDownSection(
  JSON_KEY_TO_OPTION_NAMES,
  myselect,
  section
) {
  console.log("Populating Environmental Features drop-down list.");

  // Add the options to the drop-down and build the documentation page

  for (let feature of JSON_KEY_TO_OPTION_NAMES) {
    let key = feature[0];
    let text = feature[1][0];
    if (
      !key.endsWith("_comments") &&
      !key.startsWith("section1_time_stamp") &&
      !key.startsWith("section1_school_name") &&
      !key.startsWith("section1_email") &&
      !key.startsWith("section6_enviro_awards") &&
      !key.startsWith("section6_actions_not_mentioned") &&
      !key.startsWith("latitude") &&
      !key.startsWith("longitude") &&
      key.startsWith(section)
    ) {
      //console.log("match", feature[0], section);
      let opt = document.createElement("option");
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
 * @param {object} filterVal: string of last used filter
 * @async
 */
async function updateLast(key, filterVal) {
  lastSectionFilter[key] = filterVal;
}
async function displayMarkersByFeature(
  myselect,
  mymap,
  markersLayer,
  filterVal
) {
  //await updateLast(myselect.className, filterVal);
  //await updateLast("2", "hello");
  let feature = myselect.options[myselect.selectedIndex].value;
  // const dropDown_query = 'https://voyn795bv9.execute-api.us-east-1.amazonaws.com/Dev/getDataByColumnName?columnName='
  //console.log("Displaying markers for: " + feature);

  // NOTE: The first thing we do here is clear the markers from the layer.
  markersLayer.clearLayers();

  const request = await fetch(dropDown_query + feature + "&value=Yes");
  let response = await request.json();
  let markerGroup = [];
  console.log(response);
  response.forEach((item) => {
    const latitude = item.latitude;
    const longitude = item.longitude;
    currMatches.push(item);

    if (feature.toLowerCase().length > 0) {
      if (item[feature].toLowerCase() == "yes") {
        // Create a marker
        const marker = L.marker([latitude, longitude]);
        // Add a popup to the marker
        marker
          .bindPopup(
            "<b>" +
              item["schoolName"] +
              "</b><br>" +
              "Website: <a target='_blank' href='" +
              item.website +
              "'>" +
              item.website +
              "</a><br>" +
              "<img src='" +
              item.picture +
              "' style='width: 200px; height: 150px' /><br>"
          )
          .openPopup();
        // Add marker to the layer. Not displayed yet.
        markersLayer.addLayer(marker);
        markerGroup.push(marker);
      }
    }
    // Display all the markers.
    markersLayer.addTo(mymap);
  });
  //pan and set zoom to fit everything
  let featureGroup = L.featureGroup(markerGroup).addTo(mymap);
  mymap.fitBounds(featureGroup.getBounds());
}

/**
 * @param  {object} mymap : The map object from the loadMap function
 * @param  {object} perimLayer : The layer object that contains the Prince George's county perimeter polygon
 * @param  {object} countyPerimeter : An object that allows us to test if the toggle button is on or off
 */
function displayAreaCovered(mymap, perimLayer, countyPerimeter) {
  countyPerimeter.classList.toggle("active");
  if (countyPerimeter.classList[1]) {
    var polygon = L.polygon([
      [39.1297476, -76.887847],
      [38.9658582, -77.0028848],
      [38.89241, -76.9101263],
      [38.8040671, -77.022392],
      [38.7084377, -77.0373222],
      [38.6892932, -77.0766706],
      [38.6165086, -77.0482834],
      [38.660321, -76.9853651],
      [38.6516428, -76.9011842],
      [38.6608615, -76.8657629],
      [38.6168659, -76.7494621],
      [38.5582369, -76.741024],
      [38.540197, -76.6813885],
      [38.7833602, -76.7141972],
      [38.9053952, -76.6694931],
      [38.9900079, -76.7046728],
      [39.0766305, -76.8341119],
      [39.1025425, -76.835635],
    ]);

    perimLayer.addLayer(polygon);
    // Display all the markers.
    perimLayer.addTo(mymap);
    // console.log(markersLayer._layers)
  } else {
    // console.log(markersLayer)
    perimLayer.clearLayers(polygon);
  }
}

/**
 * @param  {Array} sectionDropdown
 * @param  {object} markersLayer: A layer object related to the map. The markers are added to this layer, then the layer is added to the map for the markers to be visible
 * @param  {object} mymap : The map object from the loadMap function
 * @async
 */
async function displayMarkersBySectionRating(
  sectionDropdown,
  markersLayer,
  mymap
) {
  console.log(sectionDropdown);
  const section = sectionDropdown.options[sectionDropdown.selectedIndex].value;
  const readAPI =
    "https://voyn795bv9.execute-api.us-east-1.amazonaws.com/Dev/read_all_dynamodb";
  console.log("Displaying markers for school rating section: " + section);

  // NOTE: The first thing we do here is clear the markers from the layer.
  markersLayer.clearLayers();
  const request = await fetch(readAPI);
  let response = await request.json();

  response.forEach((item) => {
    let numberYes = countYesForSection(item, section);
    let latitude = item.latitude;
    let longitude = item.longitude;

    let circle = L.circle([latitude, longitude], {
      color: "red",
      fillColor: "#f03",
      fillOpacity: 0.5,
      radius: numberYes * (section === "srf_all" ? 50 : 100),
    });

    // Add a popup to the circle
    circle
      .bindPopup(
        "<b>" +
          item["schoolName"] +
          "</b><br>" +
          "Total Yes: " +
          numberYes +
          "<br>" +
          "Website: <a target='_blank' href='" +
          item.website +
          "'>" +
          item.website +
          "</a><br>" +
          "<img src='" +
          item.picture +
          "' style='width: 100%; height: 150px' /><br>"
      )
      .openPopup();

    // Add marker to the layer. Not displayed yet.
    markersLayer.addLayer(circle);

    // Display all the markers.
    markersLayer.addTo(mymap);
    // return res;
  });
}
/**
 * @param  {object} schoolData : An object of information about each school, sent from displayMarkersBySectionRating function
 * @param  {string} section : A string of chosen section
 */
function countYesForSection(schoolData, section) {
  var counter = 0;
  Object.entries(schoolData).forEach(([key, value]) => {
    if (typeof value === "string" && value.toLowerCase() === "yes") {
      switch (section) {
        case "srf_all":
          counter++;
          break;
        case "srf_section1":
          if (key.startsWith("section1_")) counter++;
          break;
        case "srf_section2":
          if (key.startsWith("section2_")) counter++;
          break;
        case "srf_section3":
          if (key.startsWith("section3_")) counter++;
          break;
        case "srf_section4":
          if (key.startsWith("section4_")) counter++;
          break;
        case "srf_section5":
          if (key.startsWith("section5_")) counter++;
          break;
      }
    }
  });
  return counter;
}
/**
 * The main function that runs first when the index.html page is loaded.
 */
async function mainThread() {
  const mymap = loadMap();
  let markersLayer = new L.LayerGroup();
  let perimLayer = new L.LayerGroup();
  const myselect = document.querySelector(".feature_filters_drop_down");
  const sectionDropdown1 = document.querySelector(".section1");
  const sectionDropdown2 = document.querySelector(".section2");
  const sectionDropdown3 = document.querySelector(".section3");
  const sectionDropdown4 = document.querySelector(".section4");
  const sectionDropdown5 = document.querySelector(".section5");
  const advSec1 = document.querySelector(".content-inner");
  populateEnvFeaturesCheckbox(JSON_KEY_TO_OPTION_NAMES, advSec1, "section1");
  const advSec2 = document.querySelector(".content-inner2");
  populateEnvFeaturesCheckbox(JSON_KEY_TO_OPTION_NAMES, advSec2, "section2");
  const advSec3 = document.querySelector(".content-inner3");
  populateEnvFeaturesCheckbox(JSON_KEY_TO_OPTION_NAMES, advSec3, "section3");
  const advSec4 = document.querySelector(".content-inner4");
  populateEnvFeaturesCheckbox(JSON_KEY_TO_OPTION_NAMES, advSec4, "section4");
  const advSec5 = document.querySelector(".content-inner5");
  populateEnvFeaturesCheckbox(JSON_KEY_TO_OPTION_NAMES, advSec5, "section5");
  //grab all advanced filter checkboxes so we can add an eventlistener on click
  const allCheckboxes = document.querySelectorAll('[title*="checkboxClick"]');
  let filterList = [];
  let filterData = [];
  let data = await fetch(
    "https://voyn795bv9.execute-api.us-east-1.amazonaws.com/Dev/read_all_dynamodb"
  );
  data = await data.json();
  allCheckboxes.forEach((item) => {
    item.addEventListener("click", () => {
      //initialize the filter
      if (filterList.length < 1) {
        if (item.checked) {
          filterList.push(item.id);
          //console.log("adding " + `${item.id} to filter`);
        }
      } else {
        //filter already established
        if (item.checked) {
          filterList.push(item.id);
          //console.log("adding " + `${item.id} to filter`);
          //console.log(filterList.length);
        } else {
          let filterout = filterList.filter((elm) => elm != item.id);
          //console.log("removing " + `${item.id} from filter`);
          filterList = filterout;
          //console.log(filterList);
        }
      }
      let filteredData = [];
      filterList.forEach((filter, index) => {
        if (index === 0) {
          data.forEach((school) => {
            if (school[filter].toLowerCase() === "yes") {
              filteredData.push(school);
            }
          });
          //console.log("starting filter", filteredData, `filter`);
        } else {
          //console.log("now filtering", filter);

          let newfiltered = filteredData.filter(
            (elm) => elm[filter].toLowerCase() === "yes"
          );
          filteredData = newfiltered;
          //console.log(filteredData);
          filterData = filteredData;
        }
      });
      markersLayer.clearLayers();
      let markerGroup = [];
      if (filterList.length < 1) {
        data.forEach((school) => {
          const latitude = school.latitude;
          const longitude = school.longitude;
          const marker = L.marker([latitude, longitude]);
          // Add a popup to the marker
          marker
            .bindPopup(
              "<b>" +
                school["schoolName"] +
                "</b><br>" +
                "Website: <a target='_blank' href='" +
                school.website +
                "'>" +
                school.website +
                "</a><br>" +
                "<img src='" +
                school.picture +
                "' style='width: 200px; height: 150px' /><br>"
            )
            .openPopup();
          // Add marker to the layer. Not displayed yet.
          markersLayer.addLayer(marker);
          markerGroup.push(marker);

          // Display all the markers.
          markersLayer.addTo(mymap);
        });
      }
      filteredData.forEach((school) => {
        const latitude = school.latitude;
        const longitude = school.longitude;
        const marker = L.marker([latitude, longitude]);
        // Add a popup to the marker
        marker
          .bindPopup(
            "<b>" +
              school["schoolName"] +
              "</b><br>" +
              "Website: <a target='_blank' href='" +
              school.website +
              "'>" +
              school.website +
              "</a><br>" +
              "<img src='" +
              school.picture +
              "' style='width: 200px; height: 150px' /><br>"
          )
          .openPopup();
        // Add marker to the layer. Not displayed yet.
        markersLayer.addLayer(marker);
        markerGroup.push(marker);

        // Display all the markers.
        markersLayer.addTo(mymap);
      });
    });
  });

  let lastSectionFilter = {};

  populateEnvFeaturesDropDownSection(
    JSON_KEY_TO_OPTION_NAMES,
    sectionDropdown1,
    "section1"
  );
  populateEnvFeaturesDropDownSection(
    JSON_KEY_TO_OPTION_NAMES,
    sectionDropdown2,
    "section2"
  );
  populateEnvFeaturesDropDownSection(
    JSON_KEY_TO_OPTION_NAMES,
    sectionDropdown3,
    "section3"
  );
  populateEnvFeaturesDropDownSection(
    JSON_KEY_TO_OPTION_NAMES,
    sectionDropdown4,
    "section4"
  );
  populateEnvFeaturesDropDownSection(
    JSON_KEY_TO_OPTION_NAMES,
    sectionDropdown5,
    "section5"
  );

  sectionDropdown1.addEventListener("change", (event) => {
    sectionDropdown2.value = "None";
    sectionDropdown3.value = "None";
    sectionDropdown4.value = "None";
    sectionDropdown5.value = "None";

    displayMarkersByFeature(
      sectionDropdown1,
      mymap,
      markersLayer,
      event.target.value
    );

    console.log(event.target.value, lastSectionFilter);
  });
  sectionDropdown2.addEventListener("change", (event) => {
    sectionDropdown1.value = "None";
    sectionDropdown3.value = "None";
    sectionDropdown4.value = "None";
    sectionDropdown5.value = "None";
    displayMarkersByFeature(
      sectionDropdown2,
      mymap,
      markersLayer,
      event.target.value
    );
  });
  sectionDropdown3.addEventListener("change", (event) => {
    sectionDropdown1.value = "None";
    sectionDropdown2.value = "None";
    sectionDropdown4.value = "None";
    sectionDropdown5.value = "None";
    displayMarkersByFeature(
      sectionDropdown3,
      mymap,
      markersLayer,
      event.target.value
    );
  });
  sectionDropdown4.addEventListener("change", (event) => {
    sectionDropdown1.value = "None";
    sectionDropdown2.value = "None";
    sectionDropdown3.value = "None";
    sectionDropdown5.value = "None";
    displayMarkersByFeature(
      sectionDropdown4,
      mymap,
      markersLayer,
      event.target.value
    );
  });
  sectionDropdown5.addEventListener("change", (event) => {
    sectionDropdown1.value = "None";
    sectionDropdown2.value = "None";
    sectionDropdown3.value = "None";
    sectionDropdown4.value = "None";
    displayMarkersByFeature(
      sectionDropdown5,
      mymap,
      markersLayer,
      event.target.value
    );
  });
  let advancedtabFilter = document.querySelector(".advancedfiltertab");
  let simpleFilter = document.querySelector(".toggleShow");
  const multiFilter = document.querySelector("#multfilter");
  multiFilter.addEventListener("click", (evt) => {
    multiFilter.classList.toggle("active");
    if (advancedtabFilter.style.display === "none") {
      advancedtabFilter.style.display = "block";
      simpleFilter.style.display = "none";
    } else {
      advancedtabFilter.style.display = "none";
      simpleFilter.style.display = "block";
    }
  });
  const countyPerimeter = document.querySelector(".toggle-btn");
  const sectionSelect = document.querySelector(".section_filters_drop_down");
  //populateEnvFeaturesDropDown(JSON_KEY_TO_OPTION_NAMES, myselect);

  countyPerimeter.addEventListener("click", (event) => {
    displayAreaCovered(mymap, perimLayer, countyPerimeter);
  });

  sectionSelect.addEventListener("change", (event) => {
    displayMarkersBySectionRating(sectionSelect, markersLayer, mymap);
    displayCurrMatches();
    console.log(lastSectionFilter);
  });
}

window.onload = mainThread;
