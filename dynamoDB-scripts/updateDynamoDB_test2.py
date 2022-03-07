import re
import requests
import json
import boto3
from bs4 import BeautifulSoup 


GOOGLE_NUM_COLUMNS = 66
# MYSQL_JSON_COLUMN_NAMES contains a list of column names. These column names
# will also be the key properties is a JSON structure read by the Visualization
# app. Each row in the list contains 4 values:
# [0] The number references the question number or Google original column number.
# [1] Column Name
# [2] Column data type
MYSQL_JSON_COLUMN_NAMES = [
    [0, "section1_time_stamp", "VARCHAR(50)"],
    [1, "section1_email", "VARCHAR(100)"],
    [2, "section1_school_name", "VARCHAR(75)"],
    [3, "section1_green_school_certification", "VARCHAR(22)"],
    [4, "section1_active_garden_vegetable_garden", "VARCHAR(3)"],
    [4, "section1_active_garden_native_garden", "VARCHAR(3)"],
    [4, "section1_active_garden_butterfly_garden", "VARCHAR(3)"],
    [4, "section1_active_garden_rain_garden", "VARCHAR(3)"],
    [4, "section1_active_garden_zen_garden", "VARCHAR(3)"],
    [4, "section1_active_garden_herb_garden", "VARCHAR(3)"],
    [4, "section1_active_garden_no_gardens_on_campus", "VARCHAR(3)"],
    [4, "section1_active_garden_dont_know", "VARCHAR(3)"],
    [5, "section1_recycle_at_breakfast", "VARCHAR(3)"],
    [5, "section1_recycle_at_lunch", "VARCHAR(3)"],
    [5, "section1_recycle_in_the_classroom", "VARCHAR(3)"],
    [5, "section1_recycle_not_at_all", "VARCHAR(3)"],
    [5, "section1_recycle_dont_know", "VARCHAR(3)"],
    [6, "section1_recycling_program_ink_cartridge_recycling", "VARCHAR(3)"],
    [6, "section1_recycling_program_phones_batteries_other", "VARCHAR(3)"],
    [6, "section1_recycling_program_terra_cycling", "VARCHAR(3)"],
    [6, "section1_recycling_program_color_cycle_crayola", "VARCHAR(3)"],
    [6, "section1_recycling_program_pepsi_recycle_rally", "VARCHAR(3)"],
    [6, "section1_recycling_program_none_programs_activities", "VARCHAR(3)"],
    [6, "section1_recycling_program_dont_know", "VARCHAR(3)"],
    [7, "section1_composting_we_did_not_compost_at_our_school", "VARCHAR(3)"],
    [7, "section1_composting_vermiculture", "VARCHAR(3)"],
    [7, "section1_composting_drum_compost", "VARCHAR(3)"],
    [7, "section1_composting_open_frame", "VARCHAR(3)"],
    [7, "section1_composting_send_compost_local_facility_farm", "VARCHAR(3)"],
    [7, "section1_composting_dont_know", "VARCHAR(3)"],
    [8, "section1_cleanup_volunteer_effort", "VARCHAR(3)"],
    [9, "section1_waste_reduction_comments", "TEXT"],
    [10, "section2_reducing_water_strategy", "VARCHAR(22)"],
    [11, "section2_stream", "VARCHAR(22)"],
    [12, "section2_water_prevention_stream_bank_planting", "VARCHAR(22)"],
    [13, "section2_water_prevention_erosion_control_project", "VARCHAR(22)"],
    [14, "section2_water_prevention_painted_storm_drains", "VARCHAR(22)"],
    [15, "section2_water_prevention_raingarden_bioretention_area_planted", "VARCHAR(22)"],
    [16, "section2_water_prevention_no_mow_zone", "VARCHAR(22)"],
    [17, "section2_water_prevention_rain_barrels", "VARCHAR(22)"],
    [18, "section2_water_prevention_stream_cleaning", "VARCHAR(22)"],
    [19, "section2_water_prevention_collected_litter", "VARCHAR(22)"],
    [20, "section2_water_prevention_turf_eduction", "VARCHAR(22)"],
    [21, "section2_water_prevention_surface_reduction", "VARCHAR(22)"],
    [22, "section2_water_prevention_green_roof", "VARCHAR(22)"],
    [23, "section2_water_prevention_retrofitted_sink_toilet_showers", "VARCHAR(22)"],
    [24, "section2_runoff_strategy", "VARCHAR(22)"],
    [25, "section2_water_conservation_comments", "TEXT"],
    [26, "section3_reduce_energy_strategy", "VARCHAR(22)"],
    [27, "section3_energy_conservation_installed_efficient_lighting", "VARCHAR(22)"],
    [28, "section3_energy_conservation_use_daylighting", "VARCHAR(22)"],
    [29, "section3_energy_conservation_delamped", "VARCHAR(22)"],
    [30, "section3_energy_conservation_planted_tree_shading", "VARCHAR(22)"],
    [31, "section3_energy_conservation_use_of_blinds", "VARCHAR(22)"],
    [32, "section3_renewable_energy", "VARCHAR(22)"],
    [33, "section3_renewable_source_solar", "VARCHAR(22)"],
    [34, "section3_renewable_source_wind", "VARCHAR(22)"],
    [35, "section3_renewable_source_geothermal", "VARCHAR(22)"],
    [36, "section3_energy_conservation_comments", "TEXT"],
    [37, "section4_restore_habitat", "VARCHAR(22)"],
    [38, "section4_habitat_restoration_created_bird_houses", "VARCHAR(22)"],
    [39, "section4_habitat_restoration_planted_native_trees", "VARCHAR(22)"],
    [40, "section4_habitat_restoration_planted_native_shrubs", "VARCHAR(22)"],
    [41, "section4_habitat_restoration_removal_invasive_species", "VARCHAR(22)"],
    [42, "section4_habitat_restoration_created_native_habitat", "VARCHAR(22)"],
    [43, "section4_habit_restoration_comments", "TEXT"],
    [44, "section4_enviro_learning_structures", "VARCHAR(22)"],
    [45, "section4_env_learn_struct_interpretive_signage", "VARCHAR(22)"],
    [46, "section4_env_learn_struct_trails_pathways", "VARCHAR(22)"],
    [47, "section4_env_learn_struct_boardwalk_bridges", "VARCHAR(22)"],
    [48, "section4_env_learn_struct_tree_plant_id_tags", "VARCHAR(22)"],
    [49, "section4_env_learn_struct_outdoor_classroom", "VARCHAR(22)"],
    [50, "section4_env_learn_struct_outdoor_environmental_art", "VARCHAR(22)"],
    [51, "section4_env_learn_struct_greenhouse", "VARCHAR(22)"],
    [52, "section4_env_learn_struct_tower_garden", "VARCHAR(22)"],
    [53, "section4_env_learn_struct_weather_station", "VARCHAR(22)"],
    [54, "section4_env_learn_struct_pond", "VARCHAR(22)"],
    [55, "section4_env_learn_struct_hydroponics", "VARCHAR(22)"],
    [56, "section4_env_learn_struct_aquaponics", "VARCHAR(22)"],
    [57, "section4_enviro_structure_comments", "TEXT"],
    [58, "section5_no_idle_zone", "VARCHAR(22)"],
    [59, "section5_formal_carpooling", "VARCHAR(22)"],
    [60, "section5_electric_hybrid_parking", "VARCHAR(22)"],
    [61, "section5_grow_donate_eat_garden", "VARCHAR(22)"],
    [62, "section5_green_cleaning_products", "VARCHAR(22)"],
    [63, "section5_community_science_program", "VARCHAR(22)"],
    [64, "section6_enviro_awards", "TEXT"],
    [65, "section6_actions_not_mentioned", "TEXT"],
    [-1, "latitude", "FLOAT"],
    [-1, "longitude", "FLOAT"],
    [-1, "picture", "VARCHAR(200)"],
    [-1, "website", "VARCHAR(200)"]
]

ACTIVE_GARDENS = [
    "Vegetable garden", "Native garden", "Butterfly garden", "Rain garden",
    "Zen garden", "Herb garden", "No gardens on campus", "I don't know"
]

RECYCLE = [
    "At breakfast", "At lunch", "In the classroom", "Not at all", "I don't know"
]

RECYCLING_PROGRAMS = [
    "Ink Cartridge Recycling", "Cell Phones, Batteries and Other Electronics",
    "Terra Cycling", "Color Cycle (Crayola)", "Pepsi Recycle Rally",
    "None of these Programs/Activities", "I don't know"
]

COMPOSTING = [
     "We did not compost at our school", "Vermiculture", "Drum compost",
     "Open frame", "Send Compost to Local Composting Facility/Farm", "I don't know"
]

KNOWN_SCHOOLS_INFO = [
    ["Andrew Jackson Academy", 38.8404724, -76.9106414,"https://www.pgcps.org/uploadedImages/Schools_and_Centers/Splash_Pages/Academies/New AJA Building pic1.png", "https://www.pgcps.org/andrewjackson/"],
    ["Annapolis Road Academy", 38.9192886, -76.7611796,"https://www.pgcps.org/uploadedImages/Schools_and_Centers/High_Schools/Annapolis_Road/Pictures/IMG_0134.jpg", "https://www.pgcps.org/annapolisroad/"],
    ["Benjamin Foulois CPAA", 38.8269309, -76.8888203,"https://www.pgcps.org/uploadedImages/Schools_and_Centers/Splash_Pages/Academies/benjamin foulois.jpg", "https://www.pgcps.org/benjaminfoulois/"],
    ["Benjamin Tasker MS", 38.9580, -76.7477,"https://www.pgcps.org/uploadedImages/Schools_and_Centers/Splash_Pages/Middle/Benjamin Tasker MS.jpg", "https://www.pgcps.org/benjamintasker/"],
    ["Berwyn Heights ES", 38.9921, -76.9114,"https://www.pgcps.org/uploadedImages/Schools_and_Centers/Splash_Pages/Elementary/berwyn.jpg?n=1766", "https://www.pgcps.org/berwynheights/"],
    ["Bladensburg HS", 38.942617, -76.9206946,"https://www.pgcps.org/uploadedImages/Schools_and_Centers/Splash_Pages/High/Bladensburg High.jpg", "https://www.pgcps.org/bladensburghs/"],
    ["Bond Mill Elementary", 39.1094, -76.8974,"https://www.pgcps.org/uploadedImages/Schools_and_Centers/Splash_Pages/Elementary/bondmill.jpg", "https://www.pgcps.org/bondmill"],
    ["Buck Lodge Middle School", 39.0108, -76.9617,"https://www.pgcps.org/uploadedImages/Schools_and_Centers/Splash_Pages/Middle/Buck Lodge.jpg", "https://www.pgcps.org/bucklodge/"],
    ["CENTRAL HS@Forestvill", 38.836129, -76.8875897,"https://www.pgcps.org/uploadedImages/Schools_and_Centers/Splash_Pages/High/Central HS.jpg", "https://www.pgcps.org/central/"],
    ["Charles Herbert Flowers High School", 38.9315768, -76.8373013,"https://www.pgcps.org/uploadedImages/Schools_and_Centers/Splash_Pages/High/Charles H. Flowers.jpg", "https://www.pgcps.org/charleshflowers/"],
    ["Cherokee Lane ES", 39.0051, -76.9656,"https://www.pgcps.org/uploadedImages/Schools_and_Centers/Splash_Pages/Elementary/IMG_4538.JPG?n=7987", "https://www.pgcps.org/cherokeelane/"],
    ["Chesapeake Math and IT - South (CMIT-South)", 38.8031642, -76.8424456,"https://www.pgcps.org/uploadedImages/Schools_and_Centers/Splash_Pages/Charter/cmite.jpg?n=7731", "https://www.pgcps.orghttp://www.cmitsouthelementary.org/"],
    ["CMIT South Public Charter School", 38.8050457,-76.8409654,"https://www.pgcps.org/uploadedImages/Schools_and_Centers/Splash_Pages/Charter/cmite.jpg?n=7731", "http://www.cmitsouthelementary.org"],
    ["Cool Spring ES", 39.0021151,-76.9759007,"https://www.pgcps.org/uploadedImages/Schools_and_Centers/Elementary_Schools/Cool_Spring/b56a4bc68bac4e11941c2644f0c71d61.jpg", "https://www.pgcps.org/coolspring/"],
    ["Concord ES", 38.8629843, -76.9101987,"https://www.pgcps.org/uploadedImages/Schools_and_Centers/Splash_Pages/Elementary/concord.jpg", "https://www.pgcps.org/concord/"],
    ["Deerfield Run ES", 39.0711, -76.8487,"https://www.pgcps.org/uploadedImages/Schools_and_Centers/Splash_Pages/Elementary/Deerfield Run.jpg", "https://www.pgcps.org/deerfieldrun/"],
    ["Dodge Park Elementary", 38.9335, -76.8779,"https://www.pgcps.org/uploadedImages/Schools_and_Centers/Splash_Pages/Elementary/dodge%20park.jpg", "https://www.pgcps.org/dodgepark/"],
    ["Dora Kennedy French Immersion", 38.9975238, -76.9046507,"https://www.pgcps.org/uploadedImages/Schools_and_Centers/Splash_Pages/Academies/dkfi-sign_1_orig.jpg", "https://www.pgcps.org/dorakennedy/"],
    ["Dr. Henry A Wise Jr. High School", 38.8337263, -76.7908283,"https://www.pgcps.org/uploadedImages/Schools_and_Centers/Splash_Pages/High/Dr. Henry A. Wise HS.jpg", "https://www.pgcps.org/drhenrywisejr/"],
    ["Eleanor Roosevelt High School", 38.9940431, -76.8716383,"https://www.pgcps.org/uploadedImages/Schools_and_Centers/Splash_Pages/High/Eleanor Roosevelt HS.jpg", "https://www.pgcps.org/eleanorroosevelt"],
    ["Ernest E. Just Middle School", 38.9072, -76.8319,"https://www.pgcps.org/uploadedImages/Schools_and_Centers/Splash_Pages/Middle/Ernest Everett Just.jpg", "https://www.pgcps.org/ernesteverettjust/"],
    ["Fairmont Heights High School", 38.9177687, -76.8966939,"https://www.pgcps.org/uploadedImages/Schools_and_Centers/Splash_Pages/High/FHHS_7551.JPG", "https://www.pgcps.org/fairmontheights/"],
    ["Fort Foote Elementary", 38.7758, -77.0070,"https://www.pgcps.org/uploadedImages/Schools_and_Centers/Splash_Pages/Elementary/fortefoote.jpg", "https://www.pgcps.org/fortfoote/"],
    ["Frederick Douglass High School", 38.7815367, -76.7838189,"https://www.pgcps.org/uploadedImages/Schools_and_Centers/Splash_Pages/High/douglass.jpg", "https://www.pgcps.org/douglass/"],
    ["Friendly High School", 38.7519549, -76.9706354,"https://www.pgcps.org/uploadedImages/Schools_and_Centers/Splash_Pages/High/Friendly HS.jpg", "https://www.pgcps.org/friendly/"],
    ["Gladys Noon Spellman Elementary", 38.9308, -76.9095,"https://www.pgcps.org/uploadedImages/Schools_and_Centers/Splash_Pages/Elementary/Gladys Noon Spellman.jpg", "https://www.pgcps.org/gladysnoonspellman/"],
    ["Glassmanor Elementary", 38.8171, -76.9924,"https://www.pgcps.org/uploadedImages/Schools_and_Centers/Splash_Pages/Elementary/Glassmanor ES.jpg", "https://www.pgcps.org/glassmanor/"],
    ["Greenbelt Elementary", 39.0123162, -76.8793746,"https://www.pgcps.org/uploadedImages/Schools_and_Centers/Splash_Pages/Elementary/Greenbelt ES.jpg", "https://www.pgcps.org/greenbeltes/"],
    ["Gwynn Park High School", 38.7017, -77.1508,"https://www.pgcps.org/uploadedImages/Schools_and_Centers/Splash_Pages/High/Gwynn Park HS.jpg", "https://www.pgcps.org/gwynnparkhs/"],
    ["Gwynn Park MS", 38.7069, -76.8709,"https://www.pgcps.org/uploadedImages/Schools_and_Centers/Middle_Schools/Gwynn_Park/Rotating_Stories/schoolphoto 2.jpg?n=9313", "https://www.pgcps.org/gwynnparkms/"],
    ["High Bridge Elementary", 38.9868884, -76.7745284,"https://www.pgcps.org/uploadedImages/Schools_and_Centers/Splash_Pages/Elementary/High Bridge ES.jpg", "https://www.pgcps.org/highbridge/"],
    ["Highland Park ES", 38.9035, -76.8960,"https://www.pgcps.org/uploadedImages/Schools_and_Centers/Splash_Pages/Elementary/Highland Park ES.jpg", "https://www.pgcps.org/highlandpark/"],
    ["Hollywood Elementary", 39.0151, -76.9250,"https://www.pgcps.org/uploadedImages/Schools_and_Centers/Splash_Pages/Elementary/Hollywood ES.jpg", "https://www.pgcps.org/hollywood/"],
    ["International High School at Largo", 38.8859, -76.8234,"https://www.pgcps.org/uploadedImages/Schools_and_Centers/Splash_Pages/High/Largo HS.jpg?n=7335", "https://www.pgcps.org/ihslargo"],
    ["Kenilworth Elementary", 38.9591, -76.7368,"https://www.pgcps.org/uploadedImages/Schools_and_Centers/Splash_Pages/Elementary/Kenilworth ES.jpg", "https://www.pgcps.org/kenilworth/"],
    ["Kingsford Elementary School", 38.9086, -76.7990,"https://www.pgcps.org/uploadedImages/Schools_and_Centers/Splash_Pages/Elementary/Kingsford ES.jpg", "https://www.pgcps.org/kingsford"],
    ["Langley Park - McCormick ES", 38.9940, -76.9831,"https://www.pgcps.org/uploadedImages/Schools_and_Centers/Splash_Pages/Elementary/Langley Park.jpg", "https://www.pgcps.org/langleyparkmccormick/"],
    ["Laurel High School", 39.0942, -76.8702,"https://www.pgcps.org/uploadedImages/Schools_and_Centers/Splash_Pages/High/Largo HS.jpg", "https://www.pgcps.org/largo/"],
    ["Magnolia ES", 38.9838055, -76.8642313,"https://www.pgcps.org/uploadedImages/Schools_and_Centers/Splash_Pages/Elementary/Magnolia ES.jpg", "https://www.pgcps.org/magnolia/"],
    ["Marlton Elementary School", 38.7725, -76.7913,"https://www.pgcps.org/uploadedImages/Schools_and_Centers/Splash_Pages/Elementary/Marlton ES.jpg", "https://www.pgcps.org/marlton/"],
    ["Melwood Elementary School", 38.7907, -76.8404,"https://www.pgcps.org/uploadedImages/Schools_and_Centers/Splash_Pages/Elementary/Melwood new front entrance pic.jpg", "https://www.pgcps.org/melwood/"],
    ["Nicholas Orem", 38.9641, -76.9621,"https://www.pgcps.org/uploadedImages/Schools_and_Centers/Splash_Pages/Middle/Nicholas Orem MS.jpg", "https://www.pgcps.org/nicholasorem/"],
    ["Northwestern HS", 38.9752874, -76.9562757,"https://www.pgcps.org/uploadedImages/Schools_and_Centers/Splash_Pages/High/Northwestern HS(1).jpg", "https://www.pgcps.org/northwestern"],
    ["Oaklands Elementary", 39.0789, -76.8512,"https://www.pgcps.org/uploadedImages/Schools_and_Centers/Splash_Pages/Elementary/Oaklands ES.jpg", "https://www.pgcps.org/oaklands/"],
    ["Paint Branch Elementary", 38.9868, -76.9285,"https://www.pgcps.org/uploadedImages/Schools_and_Centers/Splash_Pages/Elementary/Paint Branch ES.jpg", "https://www.pgcps.org/paintbranch/"],
    ["Panorama Elementary School", 38.8356, -76.9720,"https://www.pgcps.org/uploadedImages/Schools_and_Centers/Splash_Pages/Elementary/Panorama ES.jpg", "https://www.pgcps.org/panorama/"],
    ["Parkdale High School", 38.9696933, -76.9068296,"https://www.pgcps.org/uploadedImages/Schools_and_Centers/Splash_Pages/High/parkdale.jpg", "https://www.pgcps.org/parkdale/"],
    ["Patuxent Elementary", 38.8274, -76.7119,"https://www.pgcps.org/uploadedImages/Schools_and_Centers/Splash_Pages/Elementary/Patuxent ES.jpg", "https://www.pgcps.org/patuxent/"],
    ["Potomac High School", 38.8212, -76.9792,"https://www.pgcps.org/uploadedImages/Schools_and_Centers/Splash_Pages/High/Potomac HS.jpg", "https://www.pgcps.org/potomac"],
    ["Robert Godddard Montessori", 38.9883, -76.8447,"https://www.pgcps.org/uploadedImages/Schools_and_Centers/Splash_Pages/Elementary/Robert Goddard Montessori.jpg", "https://www.pgcps.org/robertgoddardmontessori/"],
    ["Robert R Gray Elementary School", 38.9088, -76.9247,"https://www.pgcps.org/uploadedImages/Schools_and_Centers/Splash_Pages/Elementary/Robert R Gray.jpg", "https://www.pgcps.org/robertrgray/"],
    ["Rogers Heights Elementary School", 38.9451163, -76.9148903,"https://www.pgcps.org/uploadedImages/Schools_and_Centers/Splash_Pages/Elementary/Rogers Heights ES.jpg", "https://www.pgcps.org/rogersheights/"],
    ["Rose Valley Elementary School", 38.7550, -76.9620,"https://www.pgcps.org/uploadedImages/Schools_and_Centers/Splash_Pages/Elementary/Rose Valley photo.jpg", "https://www.pgcps.org/rosevalley/"],
    ["Stephen Decatur Middle School", 38.7766004, -76.9106298,"https://www.pgcps.org/uploadedImages/Schools_and_Centers/Splash_Pages/Middle/Stephen Decatur MS.jpg", "https://www.pgcps.org/stephendecatur/"],
    ["Suitland Elementary School", 38.8528125, -76.9295593,"https://www.pgcps.org/uploadedImages/Schools_and_Centers/Splash_Pages/Elementary/Suitland Picture.jpg", "https://www.pgcps.org/suitlandes/"],
    ["Suitland H/S", 38.8535, -76.9198,"https://www.pgcps.org/uploadedImages/Schools_and_Centers/Splash_Pages/High/Suitland HS.jpg", "https://www.pgcps.org/suitlandhs/"],
    ["Templeton ES", 38.9525, -76.9168,"https://www.pgcps.org/uploadedImages/Schools_and_Centers/Splash_Pages/Elementary/Templeton ES.jpg", "https://www.pgcps.org/templeton/"],
    ["Thomas Johnson Middle School",  38.960509, -76.843261,"https://www.pgcps.org/uploadedImages/Schools_and_Centers/Splash_Pages/Middle/Thomas Johnson MS.jpg", "https://www.pgcps.org/thomasjohnson/"],
    ["University Park Elementary School", 38.9706181, -76.9456526,"https://www.pgcps.org/uploadedImages/Schools_and_Centers/Splash_Pages/Elementary/University Park ES.jpg", "https://www.pgcps.org/universitypark/"],
    ["Whitehall Elementary School", 38.9895601, -76.7534197,"https://www.pgcps.org/uploadedImages/Schools_and_Centers/Splash_Pages/Elementary/Whitehall ES.jpg", "https://www.pgcps.org/whitehall/"],
    ["Woodridge", 38.9507, -76.8937,"https://www.pgcps.org/uploadedImages/Schools_and_Centers/Splash_Pages/Elementary/collage (1).png", "https://www.pgcps.org/woodridge/"]
]


# Function to retrieve the Google survey data in a worksheet format.
# Return a list of rows with its respective data
def getValuesFromGoogle():
    rowValues = []
    page = requests.get("https://docs.google.com/spreadsheets/d/1w1X00YL2uV_inK-l4VVbGXOXQpW1XoXlqkHFwDcJ-kc/edit#gid=487453530")

    # Call your results page through the Beautiful Soup package
    soup = BeautifulSoup(page.text, features="html.parser")
    worksheet = soup.find(name="tbody")
    for rows in worksheet.find_all(name="tr"):
        columnValues = []
        for column in rows.find_all(name="td"):
            if len(columnValues) < GOOGLE_NUM_COLUMNS:
                columnValues.append(column.text)

        rowValues.append(columnValues)

    return rowValues


# Function to retrieve the PGC Public School Info: website and picture links.
# Return a list of rows with its respective data
def getValuesFromPGCPublicSchool():
    rowValues = []
    page = requests.get("https://www.pgcps.org/schools/")

    # Call your results page through the Beautiful Soup package
    soup = BeautifulSoup(page.text, features="html.parser")
    worksheet = soup.find("table", id="table1")
    for rows in worksheet.find_all(name="tr"):
        line = ""
        a = 0
        for column in rows.find_all('td'):
            if a == 0:
                line += column.find("a").text + ","
            elif a == 1:
                line += "\"https://www.pgcps.org" + column.find("img")['src']
            elif a == 3:
                line += "\", \"https://www.pgcps.org" + column.find("a")['href'] + "\""
            a += 1
        print(line)




def getValuesForActiveGargen(googleValue, gardenType):
    if googleValue.find(gardenType) != -1:
        return "Yes"
    return "No"

def getValuesForRecycle(googleValue, recycle):
    if googleValue.find(recycle) != -1:
        return "Yes"
    return "No"

def getValuesForRecyclingProgram(googleValue, recyclingProgram):
    if googleValue.find(recyclingProgram) != -1:
        return "Yes"
    return "No"

def getValuesForComposting(googleValue, composting):
    if googleValue.find(composting) != -1:
        return "Yes"
    return "No"

def getSchoolAdditionalInfo(schoolName, item):
    for schoolInfo in KNOWN_SCHOOLS_INFO:
        if schoolInfo[0].find(schoolName) != -1:
            item['latitude'] = str(schoolInfo[1])
            item['longitude'] = str(schoolInfo[2])
            item['picture'] = str(schoolInfo[3])
            item['website'] = str(schoolInfo[4])
            return

    ## Default value if we don't find the school
    item['latitude'] = "38.7849"
    item['longitude'] = "-76.8721"
    item['picture'] = 'Data Not Available'
    item['website'] = 'Data Not Available'

# Function to delete previous table and create a new one
# Some data has double-quotes (") so I had to escape the
# character (\") so it does not interfere with the MYSQL
# statement.
def populateDatabase(rows):
    client = boto3.resource('dynamodb')
    table = client.Table('dbtest2')
    pk_count = 1 

    for row in rows:
        if len(row[0]) > 0:  ## row[0] is the timestamp field. If it is empty, don't do anything. Go to next row
            # column[0] Contains the index for the question number or Google original column number.
            # column[1] Column Name
            # column[2] Column data type
            activeGardenCounter = 0
            recycleCounter = 0
            recyclingProgramCounter = 0
            compostingCounter = 0
            #creating item to put in dynamodb
            item = {}
            item["pk_num"] = pk_count
            pk_count = pk_count + 1 

            for column in MYSQL_JSON_COLUMN_NAMES:
                #column[1] is the column name
                if column[0] != -1:
                    googleValue = row[column[0]].strip()
                    if column[0] == 4:
                        item[column[1]] = getValuesForActiveGargen(googleValue, ACTIVE_GARDENS[activeGardenCounter])
                        activeGardenCounter += 1
                    elif column[0] == 5:
                        item[column[1]] = getValuesForRecycle(googleValue, RECYCLE[recycleCounter])
                        recycleCounter += 1
                    elif column[0] == 6:
                        item[column[1]] = getValuesForRecyclingProgram(googleValue, RECYCLING_PROGRAMS[recyclingProgramCounter])
                        recyclingProgramCounter += 1
                    elif column[0] == 7:
                        item[column[1]] = getValuesForComposting(googleValue, COMPOSTING[compostingCounter])
                        compostingCounter += 1
                    else:
                        item[column[1]] =  googleValue.replace("\"", "\\\"")


            #pass in item to fill in remaining values
            getSchoolAdditionalInfo(row[2].strip(), item)  # row[2] is the school name
            
            res = table.put_item(Item=item)
            # print(res)

            #print("NEW-ROW#############################################################")
            #for k, v in item.items():
                #print(k + "->" + v)  


   
            
          


################
## MAIN PROGRAM
################
rowValues = getValuesFromGoogle()
#getValuesFromPGCPublicSchool()



# Skip row 0 because that is only the column headings
# Skip row 1 because that is only and empty row
populateDatabase(rowValues[2:])

print('[{"status":"Database updated."}]')
