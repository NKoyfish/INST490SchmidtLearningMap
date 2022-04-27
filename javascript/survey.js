//Importing the readAPI endpoint from apiRoutes/api_endpoint.js
import {readAPI} from "../apiRoutes/api_endpoint.js"

/**
 * Makes a request to the AWS DynamoDB to get the names of each school
 * @param  {string} readAPI: The url for the readAPI endpoint
 * @returns schoolNames: A string of every school name in the database
 */
async function schoolNamesDropDown(readAPI){
    const request = await fetch(readAPI)
    const response = await request.json()
    // console.log(response)
    const schoolNames = response.map((item)=>{return item.schoolName})
    // console.log(schoolNames)
    return schoolNames
    
}

/**
 * Appends the school names into the dropdown menu
 * @param  {string} schoolNames: A string of every school name in the database
 * @param  {object} dropDown: The object for the dropdown element in the survey.html file
 */


function populateDropDown(schoolNames, dropDown){
    
    schoolNames.forEach((item)=>{

        let opt = document.createElement('option')
        opt.value = item
        opt.innerHTML = item

        dropDown.appendChild(opt)
    })

}

/**
 * The function that populates the survey.html page
 * @param  {object} event: The event triggered when a school is selected in the survey.html page
 * @param  {object} section1_results: The object for the div html element with class name of section1_results
 * @param  {object} section2_results: The object for the div html element with class name of section2_results
 * @param  {object} section3_results: The object for the div html element with class name of section3_results
 * @param  {object} section4_results: The object for the div html element with class name of section4_results
 * @param  {object} section5_results: The object for the div html element with class name of section5_results
 * @async
 */
async function populateSurvey(event, section1_results,section2_results,section3_results,section4_results,section5_results){
    console.log(event.target.value)
    const name = event.target.value
    const dropDown_query = 'https://voyn795bv9.execute-api.us-east-1.amazonaws.com/Dev/getDataByColumnName?columnName='
    const request = await fetch(dropDown_query + 'schoolName' + '&value='+name)
    let response = await request.json()
    response = response[0]
    
    // res_arr = Object.entries(response)
    // console.log(Object.entries(response))
    const db_columnNames = [
            "schoolName",
            "section1_time_stamp",
            "section1_email",
            "section1_green_school_certification",
            "section1_active_garden_vegetable_garden",
            "section1_active_garden_native_garden",
            "section1_active_garden_butterfly_garden",
            "section1_active_garden_rain_garden",
            "section1_active_garden_zen_garden",
            "section1_active_garden_herb_garden",
            "section1_active_garden_no_gardens_on_campus",
            "section1_active_garden_dont_know",
            "section1_recycle_at_breakfast",
            "section1_recycle_at_lunch",
            "section1_recycle_in_the_classroom",
            "section1_recycle_not_at_all",
            "section1_recycle_dont_know",
            "section1_recycling_program_ink_cartridge_recycling",
            "section1_recycling_program_phones_batteries_other",
            "section1_recycling_program_terra_cycling",
            "section1_recycling_program_color_cycle_crayola",
            "section1_recycling_program_pepsi_recycle_rally",
            "section1_recycling_program_none_programs_activities",
            "section1_recycling_program_dont_know",
            "section1_composting_we_did_not_compost_at_our_school",
            "section1_composting_vermiculture",
            "section1_composting_drum_compost",
            "section1_composting_open_frame",
            "section1_composting_send_compost_local_facility_farm",
            "section1_composting_dont_know",
            "section1_cleanup_volunteer_effort",
            "section1_waste_reduction_comments",
            "section2_reducing_water_strategy",
            "section2_stream",
            "section2_water_prevention_stream_bank_planting",
            "section2_water_prevention_erosion_control_project",
            "section2_water_prevention_painted_storm_drains",
            "section2_water_prevention_raingarden_bioretention_area_planted",
            "section2_water_prevention_no_mow_zone",
            "section2_water_prevention_rain_barrels",
            "section2_water_prevention_stream_cleaning",
            "section2_water_prevention_collected_litter",
            "section2_water_prevention_turf_eduction",
            "section2_water_prevention_surface_reduction",
            "section2_water_prevention_green_roof",
            "section2_water_prevention_retrofitted_sink_toilet_showers",
            "section2_runoff_strategy",
            "section2_water_conservation_comments",
            "section3_reduce_energy_strategy",
            "section3_energy_conservation_installed_efficient_lighting",
            "section3_energy_conservation_use_daylighting",
            "section3_energy_conservation_delamped",
            "section3_energy_conservation_planted_tree_shading",
            "section3_energy_conservation_use_of_blinds",
            "section3_renewable_energy",
            "section3_renewable_source_solar",
            "section3_renewable_source_wind",
            "section3_renewable_source_geothermal",
            "section3_energy_conservation_comments",
            "section4_restore_habitat",
            "section4_habitat_restoration_created_bird_houses",
            "section4_habitat_restoration_planted_native_trees",
            "section4_habitat_restoration_planted_native_shrubs",
            "section4_habitat_restoration_removal_invasive_species",
            "section4_habitat_restoration_created_native_habitat",
            "section4_habit_restoration_comments",
            "section4_enviro_learning_structures",
            "section4_env_learn_struct_interpretive_signage",
            "section4_env_learn_struct_trails_pathways",
            "section4_env_learn_struct_boardwalk_bridges",
            "section4_env_learn_struct_tree_plant_id_tags",
            "section4_env_learn_struct_outdoor_classroom",
            "section4_env_learn_struct_outdoor_environmental_art",
            "section4_env_learn_struct_greenhouse",
            "section4_env_learn_struct_tower_garden",
            "section4_env_learn_struct_weather_station",
            "section4_env_learn_struct_pond",
            "section4_env_learn_struct_hydroponics",
            "section4_env_learn_struct_aquaponics",
            "section4_enviro_structure_comments",
            "section5_no_idle_zone",
            "section5_formal_carpooling",
            "section5_electric_hybrid_parking",
            "section5_grow_donate_eat_garden",
            "section5_green_cleaning_products",
            "section5_community_science_program",
            "section6_enviro_awards",
            "section6_actions_not_mentioned",
            "latitude",
            "longitude",
            "picture",
            "website"
    ]
    console.log(response[db_columnNames[1]])
    const html1 = `
    
    <div class="box">         
        <h1><strong>Section 1 Answers</strong></h1><br>            
        <p><strong>Section 1: School Name - </strong></strong>${response[db_columnNames[0]]}</p><br>
        <p><strong>Section 1: Time Stamp - </strong>${response[db_columnNames[1]]}</p><br>
        <p><strong>Section 1: Email - </strong>${response[db_columnNames[2]]}</p><br>
        <p><strong>Section 1: Green School Certification - </strong>${response[db_columnNames[3]]}</p><br>
        <p><strong>Section 1: Active Gardens: Vegetable Garden - </strong>${response[db_columnNames[4]]}</p><br>
        <p><strong>Section 1: Active Gardens: Native Garden - </strong>${response[db_columnNames[5]]}</p><br>
        <p><strong>Section 1: Active Gardens: Butterfly Garden - </strong>${response[db_columnNames[6]]}</p><br>
        <p><strong>Section 1: Active Gardens: Rain Garden - </strong>${response[db_columnNames[7]]}</p><br>
        <p><strong>Section 1: Active Gardens: Zen Garden - </strong>${response[db_columnNames[8]]}</p><br>
        <p><strong>Section 1: Active Gardens: Herb Garden - </strong>${response[db_columnNames[9]]}</p><br>
        <p><strong>Section 1: Active Gardens: No gardens on campus - </strong>${response[db_columnNames[10]]}</p><br>
        <p><strong>Section 1: Active Gardens: I don't know - </strong>${response[db_columnNames[11]]}</p><br>
        <p><strong>Section 1: Recycle: At Breakfast - </strong>${response[db_columnNames[12]]}</p><br>
        <p><strong>Section 1: Recycle: At Lunch - </strong>${response[db_columnNames[13]]}</p><br>
        <p><strong>Section 1: Recycle: In the classroom - </strong>${response[db_columnNames[14]]}</p><br>
        <p><strong>Section 1: Recycle: Not at all - </strong>${response[db_columnNames[15]]}</p><br>
        <p><strong>Section 1: Recycle: I don't know - </strong>${response[db_columnNames[16]]}</p><br>
        <p><strong>Section 1: Recycling Program: Ink Cartridge Recycling - </strong>${response[db_columnNames[17]]}</p><br>
        <p><strong>Section 1: Recycling Program: Cellphones, Batteries, Others - </strong>${response[db_columnNames[18]]}</p><br>
        <p><strong>Section 1: Recycling Program: Terra Cycling - </strong>${response[db_columnNames[19]]}</p><br>
        <p><strong>Section 1: Recycling Program: Color Cycle (Crayola) - </strong>${response[db_columnNames[20]]}</p><br>
        <p><strong>Section 1: Recycling Program: Pepsi Recycle Rally - </strong>${response[db_columnNames[21]]}</p><br>
        <p><strong>Section 1: Recycling Program: No Programs/Activities - </strong>${response[db_columnNames[22]]}</p><br>
        <p><strong>Section 1: Recycling Program: I don't know - </strong>${response[db_columnNames[23]]}</p><br>
        <p><strong>Section 1: Composting: No compost at school - </strong>${response[db_columnNames[24]]}</p><br>
        <p><strong>Section 1: Composting: Vermiculture - </strong>${response[db_columnNames[25]]}</p><br>
        <p><strong>Section 1: Composting: Drum Compost - </strong>${response[db_columnNames[26]]}</p><br>
        <p><strong>Section 1: Composting: Open Frame - </strong>${response[db_columnNames[27]]}</p><br>
        <p><strong>Section 1: Composting: Send to Local Facility/Farm - </strong>${response[db_columnNames[28]]}</p><br>
        <p><strong>Section 1: Composting: I don't know - </strong>${response[db_columnNames[29]]}</p><br>
        <p><strong>Section 1: Cleanup Volunteer Effort - </strong>${response[db_columnNames[30]]}</p><br>
        <p><strong>Section 1: Waste Reduction Comments - </strong>${response[db_columnNames[31]]}</p><br>
    </div>`

    
    section1_results.innerHTML=html1

    const html2 = `
    <div class="box">
    <h1><strong>Section 2 Answers</strong></h1><br>
    <p><strong>Section 2: Reducing Water Strategy - </strong>${response[db_columnNames[32]]}</p><br>
    <p><strong>Section 2: Stream - </strong>${response[db_columnNames[33]]}</p><br>
    <p><strong>Section 2: Water Prevention: Stream Bank Planting - </strong>${response[db_columnNames[34]]}</p><br>
    <p><strong>Section 2: Water Prevention: Erosion Control Project other than Stream Bank Planting - </strong>${response[db_columnNames[35]]}</p><br>
    <p><strong>Section 2: Water Prevention: Painted Storm Drains - </strong>${response[db_columnNames[36]]}</p><br>
    <p><strong>Section 2: Water Prevention: Raingarden/bioretention area planted - </strong>${response[db_columnNames[37]]}</p><br>
    <p><strong>Section 2: Water Prevention: No-mow zone installed  - </strong>${response[db_columnNames[38]]}</p><br>
    <p><strong>Section 2: Water Prevention: Rain barrels installed - </strong>${response[db_columnNames[39]]}</p><br>
    <p><strong>Section 2: Water Prevention: Stream Cleaning - </strong>${response[db_columnNames[40]]}</p><br>
    <p><strong>Section 2: Water Prevention: Collected litter to prevent water pollution - </strong>${response[db_columnNames[41]]}</p><br>
    <p><strong>Section 2: Water Prevention: Turf Eduction - </strong>${response[db_columnNames[42]]}</p><br>
    <p><strong>Section 2: Water Prevention: Impervious surface reduction - </strong>${response[db_columnNames[43]]}</p><br>
    <p><strong>Section 2: Water Prevention: Green Roof - </strong>${response[db_columnNames[44]]}</p><br>
    <p><strong>Section 2: Water Prevention: Retrofitted sinks, toilets, showers - </strong>${response[db_columnNames[45]]}</p><br>
    <p><strong>Section 2: Runoff Strategy - </strong>${response[db_columnNames[46]]}</p><br>
    <p><strong>Section 2: Water Conservation Comments - </strong>${response[db_columnNames[47]]}</p><br>

    </div>`
    
    section2_results.innerHTML= html2

    const html3=`
    <div class="box">
    <h1><strong>Section 3 Answers</strong></h1><br>
    <p><strong>Section 3: Reduce Energy Strategy - </strong>${response[db_columnNames[48]]}</p><br>
    <p><strong>Section 3: Energy Conservation: Installed efficient lighting - </strong>${response[db_columnNames[49]]}</p><br>
    <p><strong>Section 3: Energy Conservation: Use Daylighting most of the day - </strong>${response[db_columnNames[50]]}</p><br>
    <p><strong>Section 3: Energy Conservation: Delamped - </strong>${response[db_columnNames[51]]}</p><br>
    <p><strong>Section 3: Energy Conservation: Planted trees to shade building - </strong>${response[db_columnNames[52]]}</p><br>
    <p><strong>Section 3: Energy Conservation: Use of blinds in the classroom - </strong>${response[db_columnNames[53]]}</p><br>
    <p><strong>Section 3: Renewable Energy - </strong>${response[db_columnNames[54]]}</p><br>
    <p><strong>Section 3: Renewable Source: Solar - </strong>${response[db_columnNames[55]]}</p><br>
    <p><strong>Section 3: Renewable Source: Wind - </strong>${response[db_columnNames[56]]}</p><br>
    <p><strong>Section 3: Renewable Source: Geothermal - </strong>${response[db_columnNames[57]]}</p><br>
    <p><strong>Section 3: Energy Conservation Comments - </strong>${response[db_columnNames[58]]}</p><br>

    </div>`
    section3_results.innerHTML = html3

    const html4=`
    <div class="box">
    <h1><strong>Section 4 Answers</strong></h1><br>
    <p><strong>Section 4: Restore Habitat - </strong>${response[db_columnNames[59]]}</p><br>
    <p><strong>Section 4: Habitat Restoration: Created/Installed bird houses - </strong>${response[db_columnNames[60]]}</p><br>
    <p><strong>Section 4: Habitat Restoration: Planted Native Trees - </strong>${response[db_columnNames[61]]}</p><br>
    <p><strong>Section 4: Habitat Restoration: Planted Native Shrubs - </strong>${response[db_columnNames[62]]}</p><br>
    <p><strong>Section 4: Habitat Restoration: Removal of invasive species - </strong>${response[db_columnNames[63]]}</p><br>
    <p><strong>Section 4: Habitat Restoration: Native habitat - meadows, wetlands or forests - </strong>${response[db_columnNames[64]]}</p><br>
    <p><strong>Section 4: Habit Restoration Comments - </strong>${response[db_columnNames[65]]}</p><br>
    <p><strong>Section 4: Environmental Learning Structures - </strong>${response[db_columnNames[66]]}</p><br>
    <p><strong>Section 4: Env. Learning Struct.: Interpretive signage - </strong>${response[db_columnNames[67]]}</p><br>
    <p><strong>Section 4: Env. Learning Struct.: Trails, pathways - </strong>${response[db_columnNames[68]]}</p><br>
    <p><strong>Section 4: Env. Learning Struct.: Boardwalk, bridges - </strong>${response[db_columnNames[69]]}</p><br>
    <p><strong>Section 4: Env. Learning Struct.: Tree/Plant ID Tags - </strong>${response[db_columnNames[70]]}</p><br>
    <p><strong>Section 4: Env. Learning Struct.: Outdoor Classroom - </strong>${response[db_columnNames[71]]}</p><br>
    <p><strong>Section 4: Env. Learning Struct.: Outdoor environmental art - </strong>${response[db_columnNames[72]]}</p><br>
    <p><strong>Section 4: Env. Learning Struct.: Greenhouse - </strong>${response[db_columnNames[73]]}</p><br>
    <p><strong>Section 4: Env. Learning Struct.: Tower garden - </strong>${response[db_columnNames[74]]}</p><br>
    <p><strong>Section 4: Env. Learning Struct.: Weather Station - </strong>${response[db_columnNames[75]]}</p><br>
    <p><strong>Section 4: Env. Learning Struct.: Pond - </strong>${response[db_columnNames[76]]}</p><br>
    <p><strong>Section 4: Env. Learning Struct.: Hydroponics - </strong>${response[db_columnNames[77]]}</p><br>
    <p><strong>Section 4: Env. Learning Struct.: Aquaponics - </strong>${response[db_columnNames[78]]}</p><br>
    <p><strong>Section 4: Environmental Structure Comments - </strong>${response[db_columnNames[79]]}</p><br>
    </div>`

    section4_results.innerHTML = html4

    const html5 = `
    <div class="box">
    <h1><strong>Section 5 Answers</strong></h1><br>
    <p><strong>Section 5: No Idle Zone - </strong>${response[db_columnNames[80]]}</p><br>
    <p><strong>Section 5: Formal Carpooling Program - </strong>${response[db_columnNames[81]]}</p><br>
    <p><strong>Section 5: Parking for Electric, Hybrid Vehicle - </strong>${response[db_columnNames[82]]}</p><br>
    <p><strong>Section 5: Grow/Donate Eat Food in Garden - </strong>${response[db_columnNames[83]]}</p><br>
    <p><strong>Section 5: Green Cleaning Products - </strong>${response[db_columnNames[84]]}</p><br>
    <p><strong>Section 5: Community Science Program - </strong>${response[db_columnNames[85]]}</p><br>
    <p><strong>Section 6: Environmental Awards - </strong>${response[db_columnNames[86]]}</p><br>
    <p><strong>Section 6: Actions Not Mentioned - </strong>${response[db_columnNames[87]]}</p><br>
    <p><strong>Latitude - </strong>${response[db_columnNames[88]]}</p><br>
    <p><strong>Longitude - </strong>${response[db_columnNames[89]]}</p><br>
    <a href="</strong>${response[db_columnNames[90]]}">Picture</a><br>
    <p>Website - </strong>${response[db_columnNames[91]]}</p><br>
    </div>`

    section5_results.innerHTML = html5


}

//Get button:
let topButton = document.getElementById("topBtn");

// at 50px of scroll display button
window.onscroll = function() {scrollFunction()};

function scrollFunction() {
  if (document.body.scrollTop > 50 || document.documentElement.scrollTop > 50) {
    topButton.style.display = "block";
  } else {
    topButton.style.display = "none";
  }
}

// Scroll to the top when clicked
 function topFunction() {
	console.log('hello')
  document.body.scrollTop = 0; // For Safari
  document.documentElement.scrollTop = 0; // For Chrome, Firefox, IE and Opera
}

topButton.addEventListener('click', topFunction)

//get section buttons
let sone = document.getElementById("one");
let stwo = document.getElementById("two");
let sthree = document.getElementById("three");
let sfour = document.getElementById("four");
let sfive = document.getElementById("five");
let ssix = document.getElementById("viewAll");

//get sections
let secOne = document.getElementById("secOne");
let secTwo = document.getElementById("secTwo");
let secThree = document.getElementById("secThree");
let secFour = document.getElementById("secFour");
let secFive = document.getElementById("secFive");

//onclick 
sone.addEventListener('click', () =>
sectionVisibility(1))
stwo.addEventListener('click', () =>
sectionVisibility(2))
sthree.addEventListener('click', () =>
sectionVisibility(3))
sfour.addEventListener('click', () =>
sectionVisibility(4))
sfive.addEventListener('click', () =>
sectionVisibility(5))
ssix.addEventListener('click', () =>
sectionVisibility(6))

//section Visibility function
function sectionVisibility(sectionNumber) {
    secOne.style.display = "none";
    secTwo.style.display = "none";
    secThree.style.display = "none";
    secFour.style.display = "none";
    secFive.style.display = "none";
    if (sectionNumber == 1){
        secOne.style.display = "block";
    }else if(sectionNumber == 2){
        secTwo.style.display = "block";
    }else if(sectionNumber == 3){
        secThree.style.display = "block";    
    }else if(sectionNumber == 4){
        secFour.style.display = "block";      
    }else if(sectionNumber == 5){
        secFive.style.display = "block";       
    }else if(sectionNumber == 6){
        console.log(sectionNumber)
        secOne.style.display = "block";
        secTwo.style.display = "block";
        secThree.style.display = "block";
        secFour.style.display = "block";
        secFive.style.display = "block";
    }else{
        console.log("Error in sectionVisibility")
        console.log(sectionNumber)
    }
    console.log(sectionNumber)
  }

/**
 * The main function that is called when the survey.html page is loaded
 */

async function mainThread(){
    
    let schoolNames = await schoolNamesDropDown(readAPI)
    let dropDown = document.querySelector('.survey-dropDown')
    let section1_results = document.querySelector('.section1_results')
    let section2_results = document.querySelector('.section2_results')
    let section3_results = document.querySelector('.section3_results')
    let section4_results = document.querySelector('.section4_results')
    let section5_results = document.querySelector('.section5_results')
    const selection = document.addEventListener('change',event =>{
        populateSurvey(event, section1_results,section2_results,section3_results,section4_results,section5_results)
    })

    populateDropDown(schoolNames, dropDown)
}

window.onload=mainThread

