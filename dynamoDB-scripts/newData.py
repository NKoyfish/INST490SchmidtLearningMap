from datetime import date
from datetime import datetime
from datetime import timedelta
import gspread
import boto3

#create an instance of the gspread client with the credentials in keys.json
gc = gspread.service_account(filename='keys.json')

#locate the appropriate google sheet
spread = gc.open_by_key('1w1X00YL2uV_inK-l4VVbGXOXQpW1XoXlqkHFwDcJ-kc')
worksheet = spread.sheet1

#gets all of the records in the chosen sheet
res = worksheet.get_all_records()

#initializes the connection to AWS DynamoDB
client = boto3.resource('dynamodb')
table = client.Table('pgcpsdb')

#list of possible options in the active gardens section
ACTIVE_GARDENS = [
    "Vegetable garden", "Native garden", "Butterfly garden", "Rain garden", 
    "Zen garden", "Herb garden", "No gardens on campus", "I don't know"
]

#list of possible options in the recycle section
RECYCLE = [
    "At breakfast", "At lunch", "In the classroom", "Not at all", "I don't know"
]

#list of possible options in the recyling programs section
RECYCLING_PROGRAMS = [
    "Ink Cartridge Recycling", "Cell Phones, Batteries and Other Electronics", 
    "Terra Cycling", "Color Cycle (Crayola)", "Pepsi Recycle Rally", 
    "None of these Programs/Activities", "I don't know"
]

#list of possible options in the composting section
COMPOSTING = [
     "We did not compost at our school", "Vermiculture", "Drum compost", 
     "Open frame", "Send Compost to Local Composting Facility/Farm", "I don't know" 
]

#list of information about the schools in the survey data. Includes names, latitude and logitude coordinates, url for school image and their website
KNOWN_SCHOOLS_INFO = [
    ["Andrew Jackson Academy", '38.8404724', '-76.9106414',"https://schools.pgcps.org/uploadedImages/Schools_and_Centers/Splash_Pages/Academies/New%20AJA%20Building%20pic1.png", "https://www.pgcps.org/andrewjackson/"],
    ["Annapolis Road Academy", '38.9192886', '-76.7611796',"https://schools.pgcps.org/uploadedImages/Schools_and_Centers/High_Schools/Annapolis_Road/Pictures/IMG_0134.jpg", "https://www.pgcps.org/annapolisroad/"],
    ["Benjamin Foulois CPAA", '38.8269309', '-76.8888203',"https://schools.pgcps.org/uploadedImages/Schools_and_Centers/Splash_Pages/Academies/benjamin%20foulois.jpg", "https://www.pgcps.org/benjaminfoulois/"],
    ["Benjamin Tasker MS", '38.9580', '-76.7477',"https://schools.pgcps.org/uploadedImages/Schools_and_Centers/Splash_Pages/Middle/Benjamin%20Tasker%20MS.jpg", "https://www.pgcps.org/benjamintasker/"],
    ["Berwyn Heights ES", '38.9921', '-76.9114',"https://schools.pgcps.org/uploadedImages/Schools_and_Centers/Splash_Pages/Elementary/berwyn.jpg?n=1766", "https://www.pgcps.org/berwynheights/"],
    ["Bladensburg HS", '38.942617', '-76.9206946',"https://schools.pgcps.org/uploadedImages/Schools_and_Centers/Splash_Pages/High/Bladensburg%20High.jpg", "https://www.pgcps.org/bladensburghs/"],
    ["Bond Mill", '39.1094', '-76.8974',"https://schools.pgcps.org/uploadedImages/Schools_and_Centers/Splash_Pages/Elementary/bondmill.jpg", "https://www.pgcps.org/bondmill"],
    ["Bond Mill Elementary", '39.1094', '-76.8974',"https://schools.pgcps.org/uploadedImages/Schools_and_Centers/Splash_Pages/Elementary/bondmill.jpg", "https://www.pgcps.org/bondmill"],
    ["Buck Lodge Middle School", '39.0108', '-76.9617',"https://schools.pgcps.org/uploadedImages/Schools_and_Centers/Splash_Pages/Middle/Buck%20Lodge.jpg", "https://www.pgcps.org/bucklodge/"],
    ["CENTRAL HS@Forestvill", '38.836129', '-76.8875897',"https://schools.pgcps.org/uploadedImages/Schools_and_Centers/Splash_Pages/High/Central%20HS.jpg", "https://www.pgcps.org/central/"],
    ["Charles Herbert Flowers High School", '38.9315768', '-76.8373013',"https://schools.pgcps.org/uploadedImages/Schools_and_Centers/Splash_Pages/High/Charles%20H.%20Flowers.jpg", "https://www.pgcps.org/charleshflowers/"],
    ["Cherokee Lane ES", '39.0051', '-76.9656',"https://schools.pgcps.org/uploadedImages/Schools_and_Centers/Splash_Pages/Elementary/IMG_4538.JPG?n=7987", "https://www.pgcps.org/cherokeelane/"],
    ["Chesapeake Math and IT - South (CMIT-South)", '38.8031642', '-76.8424456',"https://www.pgcps.org/uploadedImages/Schools_and_Centers/Splash_Pages/Charter/cmite.jpg?n=7731", "https://www.pgcps.orghttp://www.cmitsouthelementary.org/"],
    ["CMIT South Public Charter School", '38.8050457','-76.8409654',"https://schools.pgcps.org/uploadedImages/Schools_and_Centers/Splash_Pages/Charter/cmit_ms.png?n=3662", "http://www.cmitsouthelementary.org"],
    ["Cool Spring ES", '39.0021151','-76.9759007',"https://schools.pgcps.org/uploadedImages/Schools_and_Centers/Elementary_Schools/Cool_Spring/b56a4bc68bac4e11941c2644f0c71d61.jpg", "https://www.pgcps.org/coolspring/"],
    ["Concord ES", '38.8629843', '-76.9101987',"https://schools.pgcps.org/uploadedImages/Schools_and_Centers/Splash_Pages/Elementary/concord.jpg", "https://www.pgcps.org/concord/"],
    ["Deerfield Run ES",' 39.0711', '-76.8487',"https://schools.pgcps.org/uploadedImages/Schools_and_Centers/Splash_Pages/Elementary/Deerfield%20Run.jpg", "https://www.pgcps.org/deerfieldrun/"],
    ["Dodge Park Elementary", '38.9335', '-76.8779',"https://schools.pgcps.org/uploadedImages/Schools_and_Centers/Splash_Pages/Elementary/dodge%20park.jpg", "https://www.pgcps.org/dodgepark/"],
    ["Dora Kennedy French Immersion", '38.9975238', '-76.9046507',"https://schools.pgcps.org/uploadedImages/Schools_and_Centers/Splash_Pages/Academies/dkfi-sign_1_orig.jpg", "https://www.pgcps.org/dorakennedy/"],
    ["Dr. Henry A Wise Jr. High School", '38.8337263', '-76.7908283',"https://schools.pgcps.org/uploadedImages/Schools_and_Centers/Splash_Pages/High/Dr.%20Henry%20A.%20Wise%20HS.jpg", "https://www.pgcps.org/drhenrywisejr/"],
    ["Eleanor Roosevelt High School", '38.9940431', '-76.8716383',"https://schools.pgcps.org/uploadedImages/Schools_and_Centers/Splash_Pages/High/Eleanor%20Roosevelt%20HS.jpg", "https://www.pgcps.org/eleanorroosevelt"],
    ["Ernest E. Just Middle School", '38.9072', '-76.8319',"https://schools.pgcps.org/uploadedImages/Schools_and_Centers/Splash_Pages/Middle/Ernest%20Everett%20Just.jpg", "https://www.pgcps.org/ernesteverettjust/"],
    ["Fairmont Heights High School", '38.9177687', '-76.8966939',"https://schools.pgcps.org/uploadedImages/Schools_and_Centers/Splash_Pages/High/FHHS_7551.JPG", "https://www.pgcps.org/fairmontheights/"],
    ["Fort Foote Elementary", '38.7758', '-77.0070',"https://schools.pgcps.org/uploadedImages/Schools_and_Centers/Splash_Pages/Elementary/fortefoote.jpg", "https://www.pgcps.org/fortfoote/"],
    ["Frederick Douglass High School", '38.7815367', '-76.7838189',"https://schools.pgcps.org/uploadedImages/Schools_and_Centers/Splash_Pages/High/douglass.jpg", "https://www.pgcps.org/douglass/"],
    ["Friendly High School", '38.7519549', '-76.9706354',"https://schools.pgcps.org/uploadedImages/Schools_and_Centers/Splash_Pages/High/Friendly%20HS.jpg", "https://www.pgcps.org/friendly/"],
    ["Gladys Noon Spellman Elementary", '38.9308', '-76.9095',"https://schools.pgcps.org/uploadedImages/Schools_and_Centers/Splash_Pages/Elementary/Gladys%20Noon%20Spellman.jpg", "https://www.pgcps.org/gladysnoonspellman/"],
    ["Glassmanor Elementary", '38.8171', '-76.9924',"https://schools.pgcps.org/uploadedImages/Schools_and_Centers/Splash_Pages/Elementary/Glassmanor%20ES.jpg", "https://www.pgcps.org/glassmanor/"],
    ["Greenbelt Elementary", '39.0123162', '-76.8793746',"https://schools.pgcps.org/uploadedImages/Schools_and_Centers/Splash_Pages/Elementary/Greenbelt%20ES.jpg", "https://www.pgcps.org/greenbeltes/"],
    ["Gwynn Park High School", '38.7016', '-76.8697',"https://schools.pgcps.org/uploadedImages/Schools_and_Centers/Splash_Pages/High/Gwynn%20Park%20HS.jpg", "https://www.pgcps.org/gwynnparkhs/"],
    ["Gwynn Park MS", '38.7069', '-76.8709',"https://schools.pgcps.org/uploadedImages/Schools_and_Centers/Middle_Schools/Gwynn_Park/Rotating_Stories/schoolphoto%202.jpg?n=9313", "https://www.pgcps.org/gwynnparkms/"],
    ["High Bridge Elementary", '38.9868884', '-76.7745284',"https://schools.pgcps.org/uploadedImages/Schools_and_Centers/Splash_Pages/Elementary/High%20Bridge%20ES.jpg", "https://www.pgcps.org/highbridge/"],
    ["Highland Park ES", '38.9035', '-76.8960',"https://schools.pgcps.org/uploadedImages/Schools_and_Centers/Splash_Pages/Elementary/Highland%20Park%20ES.jpg", "https://www.pgcps.org/highlandpark/"],
    ["Hollywood Elementary", '39.0151', '-76.9250',"https://schools.pgcps.org/uploadedImages/Schools_and_Centers/Splash_Pages/Elementary/Hollywood%20ES.jpg", "https://www.pgcps.org/hollywood/"],
    ["International High School at Largo", '38.8859', '-76.8234',"https://schools.pgcps.org/uploadedImages/Schools_and_Centers/Splash_Pages/High/Largo%20HS.jpg?n=7335", "https://www.pgcps.org/ihslargo"],
    ["Kenilworth Elementary", '38.9591', '-76.7368',"https://schools.pgcps.org/uploadedImages/Schools_and_Centers/Splash_Pages/Elementary/Kenilworth%20ES.jpg", "https://www.pgcps.org/kenilworth/"],
    ["Kingsford Elementary School", '38.9086', '-76.7990',"https://schools.pgcps.org/uploadedImages/Schools_and_Centers/Splash_Pages/Elementary/Kingsford%20ES.jpg", "https://www.pgcps.org/kingsford"],
    ["Langley Park - McCormick ES", '38.9940', '-76.9831',"https://schools.pgcps.org/uploadedImages/Schools_and_Centers/Splash_Pages/Elementary/Langley%20Park.jpg", "https://www.pgcps.org/langleyparkmccormick/"],
    ["Laurel High School", '39.0942', '-76.8702',"https://schools.pgcps.org/uploadedImages/Schools_and_Centers/Splash_Pages/High/Laurel%20HS.jpg", "https://www.pgcps.org/largo/"],
    ["Laurel High", '39.0942', '-76.8702',"https://schools.pgcps.org/uploadedImages/Schools_and_Centers/Splash_Pages/High/Laurel%20HS.jpg", "https://www.pgcps.org/largo/"],
    ["Magnolia ES", '38.9838055', '-76.8642313',"https://schools.pgcps.org/uploadedImages/Schools_and_Centers/Splash_Pages/Elementary/Magnolia%20ES.jpg", "https://www.pgcps.org/magnolia/"],
    ["Marlton Elementary School", '38.7725', '-76.7913',"https://schools.pgcps.org/uploadedImages/Schools_and_Centers/Splash_Pages/Elementary/Marlton%20ES.jpg", "https://www.pgcps.org/marlton/"],
    ["Melwood Elementary School", '38.7907', '-76.8404',"https://schools.pgcps.org/uploadedImages/Schools_and_Centers/Splash_Pages/Elementary/Melwood%20new%20front%20entrance%20pic.jpg", "https://www.pgcps.org/melwood/"],
    ["Nicholas Orem", '38.9641', '-76.9621',"https://schools.pgcps.org/uploadedImages/Schools_and_Centers/Splash_Pages/Middle/Nicholas%20Orem%20MS.jpg", "https://www.pgcps.org/nicholasorem/"],
    ["Northwestern HS", '38.9752874', '-76.9562757',"https://schools.pgcps.org/uploadedImages/Schools_and_Centers/Splash_Pages/High/Northwestern%20HS(1).jpg", "https://www.pgcps.org/northwestern"],
    ["Oaklands Elementary", '39.0789', '-76.8512',"https://schools.pgcps.org/uploadedImages/Schools_and_Centers/Splash_Pages/Elementary/Oaklands%20ES.jpg", "https://www.pgcps.org/oaklands/"],
    ["Paint Branch Elementary", '38.9868', '-76.9285',"https://schools.pgcps.org/uploadedImages/Schools_and_Centers/Splash_Pages/Elementary/Paint%20Branch%20ES.jpg", "https://www.pgcps.org/paintbranch/"],
    ["Panorama Elementary School", '38.8356', '-76.9720',"https://schools.pgcps.org/uploadedImages/Schools_and_Centers/Splash_Pages/Elementary/Panorama%20ES.jpg", "https://www.pgcps.org/panorama/"],
    ["Parkdale High School", '38.9696933', '-76.9068296',"https://schools.pgcps.org/uploadedImages/Schools_and_Centers/Splash_Pages/High/parkdale.jpg", "https://www.pgcps.org/parkdale/"],
    ["Patuxent Elementary", '38.8274', '-76.7119',"https://schools.pgcps.org/uploadedImages/Schools_and_Centers/Splash_Pages/Elementary/Patuxent%20ES.jpg", "https://www.pgcps.org/patuxent/"],
    ["Potomac High School", '38.8212', '-76.9792',"https://schools.pgcps.org/uploadedImages/Schools_and_Centers/Splash_Pages/High/Potomac%20HS.jpg", "https://www.pgcps.org/potomac"],
    ["Robert Goddard Montessori", '38.9883', '-76.8447',"https://schools.pgcps.org/uploadedImages/Schools_and_Centers/Splash_Pages/Elementary/Robert%20Goddard%20Montessori.jpg", "https://www.pgcps.org/robertgoddardmontessori/"],
    ["Robert R Gray Elementary School", '38.9088', '-76.9247',"https://schools.pgcps.org/uploadedImages/Schools_and_Centers/Splash_Pages/Elementary/Robert%20R%20Gray.jpg", "https://www.pgcps.org/robertrgray/"],
    ["Rogers Heights Elementary School", '38.9451163', '-76.9148903',"https://schools.pgcps.org/uploadedImages/Schools_and_Centers/Splash_Pages/Elementary/Rogers%20Heights%20ES.jpg", "https://www.pgcps.org/rogersheights/"],
    ["Rose Valley Elementary School", '38.7550', '-76.9620',"https://schools.pgcps.org/uploadedImages/Schools_and_Centers/Splash_Pages/Elementary/Rose%20Valley%20photo.jpg", "https://www.pgcps.org/rosevalley/"],
    ["Stephen Decatur Middle School", '38.7766004', '-76.9106298',"https://schools.pgcps.org/uploadedImages/Schools_and_Centers/Splash_Pages/Middle/Stephen%20Decatur%20MS.jpg", "https://www.pgcps.org/stephendecatur/"],
    ["Suitland Elementary School", '38.8528125', '-76.9295593',"https://schools.pgcps.org/uploadedImages/Schools_and_Centers/Splash_Pages/Elementary/Suitland%20Picture.jpg", "https://www.pgcps.org/suitlandes/"],
    ["Suitland HS", '38.8535', '-76.9198',"https://schools.pgcps.org/uploadedImages/Schools_and_Centers/Splash_Pages/High/Suitland%20HS.jpg", "https://www.pgcps.org/suitlandhs/"],
    ["Templeton ES", '38.9525', '-76.9168',"https://schools.pgcps.org/uploadedImages/Schools_and_Centers/Splash_Pages/Elementary/Templeton%20ES.jpg", "https://www.pgcps.org/templeton/"],
    ["Thomas Johnson Middle School",  '38.960509', '-76.843261',"https://schools.pgcps.org/uploadedImages/Schools_and_Centers/Splash_Pages/Middle/Thomas%20Johnson%20MS.jpg", "https://www.pgcps.org/thomasjohnson/"],
    ["University Park Elementary School", '38.9706181', '-76.9456526',"https://schools.pgcps.org/uploadedImages/Schools_and_Centers/Splash_Pages/Elementary/University%20Park%20ES.jpg", "https://www.pgcps.org/universitypark/"],
    ["Whitehall Elementary School", '38.9895601', '-76.7534197',"https://schools.pgcps.org/uploadedImages/Schools_and_Centers/Splash_Pages/Elementary/Whitehall%20ES.jpg", "https://www.pgcps.org/whitehall/"],
    ["Woodridge", '38.9507', '-76.8937',"https://schools.pgcps.org/uploadedImages/Schools_and_Centers/Splash_Pages/Elementary/collage%20(1).png", "https://www.pgcps.org/woodridge/"]
]

#column names for the database
db_columnNames = [
    "section1_school_name",
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


def getValuesForActiveGargen(googleValue, gardenType):
    """ Checks to see if any of the garden types in ACTIVE_GARDENS is in the schools survey response
    
    Args:
        googleValue (str): The garden tye the school reported to have in their survy response
        gardenType (str): A value from the ACTIVE_GARDENS list
        
    Returns:
        A string of 'Yes' or 'No' depending on if the gardenType is in the school or not
    """
    if googleValue.find(gardenType) != -1:
        return 'Yes'    
    return 'No'

def getValuesForRecycle(googleValue, recycle):
    """ Checks to see if any of the recycle types in RECYCLE is in the schools survey response
    
    Args:
        googleValue (str): The garden tye the school reported to have in their survy response
        recycle (str): A value from the RECYCLE list
        
    Returns:
        A string of 'Yes' or 'No' depending on if the recycle type is in the school or not
    """
    if googleValue.find(recycle) != -1:
        return 'Yes'    
    return 'No'

def getValuesForRecyclingProgram(googleValue, recyclingProgram):
    """ Checks to see if any of the recyclingPrograms in RECYCLING_PROGRAMS is in the schools survey response
    
    Args:
        googleValue (str): The garden tye the school reported to have in their survy response
        recyclingProgram (str): A value from the RECYCLING_PROGRAMS list
        
    Returns:
        A string of 'Yes' or 'No' depending on if the recycling program is in the school or not
    """
    if googleValue.find(recyclingProgram) != -1:
        return 'Yes'    
    return 'No'

def getValuesForComposting(googleValue, composting):
    """ Checks to see if any of the composting types in COMPOSTING is in the schools survey response
    
    Args:
        googleValue (str): The garden tye the school reported to have in their survy response
        composting (str): A value from the COMPOSTING list
        
    Returns:
        A string of 'Yes' or 'No' depending on if the composting type is in the school or not
    """
    if googleValue.find(composting) != -1:
        return 'Yes'    
    return 'No'

def getSchoolAdditionalInfo(schoolName, add_info):
    """ Finds the appropriate info from the KNOWN_SCHOOLS_INFO
    
    Args:
        schoolName (str): The name of a school
        add_info (str): an argument used to find the appropriate info
        
    Returns:
        A string of either latitude/longitude coordinates, url for school picture or school webiste url
    """
    for schoolInfo in KNOWN_SCHOOLS_INFO:
        if schoolInfo[0] == schoolName:

            if add_info == 'latitude':

                return schoolInfo[1]

            elif add_info == 'longitude':
                return schoolInfo[2]
            
            elif add_info == 'picture':
                return schoolInfo[3]
            
            elif add_info == 'website':
                return schoolInfo[4]

#The datetime module is used to obtain new survey data


today=datetime.today()

yesterday = today-timedelta(days=1)

#loops through each row in the survey response
for i in range(len(res)):
    
    #gets the time of the latest update
    latest_update=res[i]['Timestamp']

    #changing the latest_update datetime to the right format
    latest_update=datetime.strptime(latest_update, '%m/%d/%Y %H:%M:%S').strftime('%Y-%m-%d')
    latest_update = datetime.strptime(latest_update, '%Y-%m-%d')
    
    #checks if the latest_update is more recent than yesterday, i.e has there been an update to the survey since yesterday
    #if there was a new update, thy database is updated with the new data
    if latest_update > yesterday:
        for i in range(len(res)):
            input = {  "pkey":i+1,
                        "schoolName":res[i]['What is the name of your school? '],
                        db_columnNames[1]: res[i]['Timestamp'],
                        db_columnNames[2]:res[i]['Email Address'],
                        db_columnNames[3]:res[i]['Does your school have a MD Green School Certification?'],
                        db_columnNames[4]:getValuesForActiveGargen(res[i]['Does your school have an active garden? (Check all that apply)'], ACTIVE_GARDENS[0]),
                        db_columnNames[5]:getValuesForActiveGargen(res[i]['Does your school have an active garden? (Check all that apply)'], ACTIVE_GARDENS[1]),
                        db_columnNames[6]:getValuesForActiveGargen(res[i]['Does your school have an active garden? (Check all that apply)'], ACTIVE_GARDENS[2]),
                        db_columnNames[7]:getValuesForActiveGargen(res[i]['Does your school have an active garden? (Check all that apply)'], ACTIVE_GARDENS[3]),
                        db_columnNames[8]:getValuesForActiveGargen(res[i]['Does your school have an active garden? (Check all that apply)'], ACTIVE_GARDENS[4]),
                        db_columnNames[9]:getValuesForActiveGargen(res[i]['Does your school have an active garden? (Check all that apply)'], ACTIVE_GARDENS[5]),
                        db_columnNames[10]:getValuesForActiveGargen(res[i]['Does your school have an active garden? (Check all that apply)'], ACTIVE_GARDENS[6]),
                        db_columnNames[11]:getValuesForActiveGargen(res[i]['Does your school have an active garden? (Check all that apply)'], ACTIVE_GARDENS[7]),
                        db_columnNames[12]:getValuesForRecycle(res[i]['Does your school actively recycle? (Check all that apply)'], RECYCLE[0]),
                        db_columnNames[13]:getValuesForRecycle(res[i]['Does your school actively recycle? (Check all that apply)'], RECYCLE[1]),
                        db_columnNames[14]:getValuesForRecycle(res[i]['Does your school actively recycle? (Check all that apply)'], RECYCLE[2]),
                        db_columnNames[15]:getValuesForRecycle(res[i]['Does your school actively recycle? (Check all that apply)'], RECYCLE[3]),
                        db_columnNames[16]:getValuesForRecycle(res[i]['Does your school actively recycle? (Check all that apply)'], RECYCLE[4]),
                        db_columnNames[17]:getValuesForRecyclingProgram(res[i]['Does your school participate in any of the following Recycling Programs/Activities? (Check all that apply)'],RECYCLING_PROGRAMS[0]),
                        db_columnNames[18]:getValuesForRecyclingProgram(res[i]['Does your school participate in any of the following Recycling Programs/Activities? (Check all that apply)'],RECYCLING_PROGRAMS[1]),
                        db_columnNames[19]:getValuesForRecyclingProgram(res[i]['Does your school participate in any of the following Recycling Programs/Activities? (Check all that apply)'],RECYCLING_PROGRAMS[2]),
                        db_columnNames[20]:getValuesForRecyclingProgram(res[i]['Does your school participate in any of the following Recycling Programs/Activities? (Check all that apply)'],RECYCLING_PROGRAMS[3]),
                        db_columnNames[21]:getValuesForRecyclingProgram(res[i]['Does your school participate in any of the following Recycling Programs/Activities? (Check all that apply)'],RECYCLING_PROGRAMS[4]),
                        db_columnNames[22]:getValuesForRecyclingProgram(res[i]['Does your school participate in any of the following Recycling Programs/Activities? (Check all that apply)'],RECYCLING_PROGRAMS[5]),
                        db_columnNames[23]:getValuesForRecyclingProgram(res[i]['Does your school participate in any of the following Recycling Programs/Activities? (Check all that apply)'],RECYCLING_PROGRAMS[6]),
                        db_columnNames[24]:getValuesForComposting(res[i]['What type of composting is implemented at your school? '],COMPOSTING[0]),
                        db_columnNames[25]:getValuesForComposting(res[i]['What type of composting is implemented at your school? '],COMPOSTING[1]),
                        db_columnNames[26]:getValuesForComposting(res[i]['What type of composting is implemented at your school? '],COMPOSTING[2]),
                        db_columnNames[27]:getValuesForComposting(res[i]['What type of composting is implemented at your school? '],COMPOSTING[3]),
                        db_columnNames[28]:getValuesForComposting(res[i]['What type of composting is implemented at your school? '],COMPOSTING[4]),
                        db_columnNames[29]:getValuesForComposting(res[i]['What type of composting is implemented at your school? '],COMPOSTING[5]),
                        db_columnNames[30]:res[i]['Does your school participate in environmental cleanup volunteer efforts?'],
                        db_columnNames[31]:res[i]['Waste Reduction:  Other and Comments, also please explain if your school participates in other waste reduction efforts. '],
                        db_columnNames[32]:res[i]['Are strategies implemented to reduce water use in your school? '],
                        db_columnNames[33]:res[i]['Do you have a stream located on your school grounds? '],
                        db_columnNames[34]:res[i]['Has your school completed any of the following Water Conservation/Water Pollution Prevention actions? Please provide an answer in each row.  [Stream Bank Planting (Riparian Buffer)]'],
                        db_columnNames[35]:res[i]['Has your school completed any of the following Water Conservation/Water Pollution Prevention actions? Please provide an answer in each row.  [Erosion Control Project other than Stream Bank Planting]'],
                        db_columnNames[36]:res[i]['Has your school completed any of the following Water Conservation/Water Pollution Prevention actions? Please provide an answer in each row.  [Painted Storm Drains]'],
                        db_columnNames[37]:res[i]['Has your school completed any of the following Water Conservation/Water Pollution Prevention actions? Please provide an answer in each row.  [Raingarden/bioretention area planted]'],
                        db_columnNames[38]:res[i]['Has your school completed any of the following Water Conservation/Water Pollution Prevention actions? Please provide an answer in each row.  [No-mow zone installed ]'],
                        db_columnNames[39]:res[i]['Has your school completed any of the following Water Conservation/Water Pollution Prevention actions? Please provide an answer in each row.  [Rain barrels installed]'],
                        db_columnNames[40]:res[i]['Has your school completed any of the following Water Conservation/Water Pollution Prevention actions? Please provide an answer in each row.  [Stream Cleaning (at your school or in the community)]'],
                        db_columnNames[41]:res[i]['Has your school completed any of the following Water Conservation/Water Pollution Prevention actions? Please provide an answer in each row.  [Collected litter to prevent water pollution]'],
                        db_columnNames[42]:res[i]['Has your school completed any of the following Water Conservation/Water Pollution Prevention actions? Please provide an answer in each row.  [Turf Eduction]'],
                        db_columnNames[43]:res[i]['Has your school completed any of the following Water Conservation/Water Pollution Prevention actions? Please provide an answer in each row.  [Impervious surface reduction]'],
                        db_columnNames[44]:res[i]['Has your school completed any of the following Water Conservation/Water Pollution Prevention actions? Please provide an answer in each row.  [Green Roof]'],
                        db_columnNames[45]:res[i]['Has your school completed any of the following Water Conservation/Water Pollution Prevention actions? Please provide an answer in each row.  [Retrofitted sinks, toilets, showers]'],
                        db_columnNames[46]:res[i]['Does your school implement strategies to reduce or improve runoff from the school grounds?'],
                        db_columnNames[47]:res[i]['Water Conservation:  Other and Comments, also please indicate if storm water management has been done or is taking place at your school on what has been/is being done.'],
                        db_columnNames[48]:res[i]['Does your school implement strategies to reduce energy use?'],
                        db_columnNames[49]:res[i]['Has your school completed the following Energy Conservation actions? Please provide an answer in each row.  [Installed efficient lighting]'],
                        db_columnNames[50]:res[i]['Has your school completed the following Energy Conservation actions? Please provide an answer in each row.  [Use Daylighting most of the day]'],
                        db_columnNames[51]:res[i]['Has your school completed the following Energy Conservation actions? Please provide an answer in each row.  [Delamped]'],
                        db_columnNames[52]:res[i]['Has your school completed the following Energy Conservation actions? Please provide an answer in each row.  [Planted trees to shade building]'],
                        db_columnNames[53]:res[i]['Has your school completed the following Energy Conservation actions? Please provide an answer in each row.  [Use of blinds in the classroom to control daylight and temperature]'],
                        db_columnNames[54]:res[i]['Does your school use renewable energy sources?'],
                        db_columnNames[55]:res[i]['Please indicate the renewable energy sources that your school uses? Please provide an answer for each row.  [Solar]'],
                        db_columnNames[56]:res[i]['Please indicate the renewable energy sources that your school uses? Please provide an answer for each row.  [Wind]'],
                        db_columnNames[57]:res[i]['Please indicate the renewable energy sources that your school uses? Please provide an answer for each row.  [Geothermal]'],
                        db_columnNames[58]:res[i]['Energy Conservation:  Other and Comments, also please indicate if additional energy conservation practices or renewable energy sources are being implemented at your school. '],
                        db_columnNames[59]:res[i]['Did you restore habitat on your school grounds? '],
                        db_columnNames[60]:res[i]['Please indicate the habitat restoration actions that your school has implemented? Please provide an answer for each row.  [Created/Installed bird houses]'],
                        db_columnNames[61]:res[i]['Please indicate the habitat restoration actions that your school has implemented? Please provide an answer for each row.  [Planted Native Trees]'],
                        db_columnNames[62]:res[i]['Please indicate the habitat restoration actions that your school has implemented? Please provide an answer for each row.  [Planted Native Shrubs]'],
                        db_columnNames[63]:res[i]['Please indicate the habitat restoration actions that your school has implemented? Please provide an answer for each row.  [Removal of invasive species]'],
                        db_columnNames[64]:res[i]['Please indicate the habitat restoration actions that your school has implemented? Please provide an answer for each row.  [Created native habitat - meadows, wetlands or forests]'],
                        db_columnNames[65]:res[i]['Habitat Restoration:  Other and Comments, please describe other habitat restoration efforts at your school or that your school has done in the community. '],
                        db_columnNames[66]:res[i]['Does your school have structures for environmental learning on the school grounds? '],
                        db_columnNames[67]:res[i]['Please indicate the structures for environmental learning located on your school grounds. Please provide an answer for each row.  [Interpretive signage]'],
                        db_columnNames[68]:res[i]['Please indicate the structures for environmental learning located on your school grounds. Please provide an answer for each row.  [Trails, pathways]'],
                        db_columnNames[69]:res[i]['Please indicate the structures for environmental learning located on your school grounds. Please provide an answer for each row.  [Boardwalk, bridges]'],
                        db_columnNames[70]:res[i]['Please indicate the structures for environmental learning located on your school grounds. Please provide an answer for each row.  [Tree/Plant ID Tags]'],
                        db_columnNames[71]:res[i]['Please indicate the structures for environmental learning located on your school grounds. Please provide an answer for each row.  [Outdoor Classroom]'],
                        db_columnNames[72]:res[i]['Please indicate the structures for environmental learning located on your school grounds. Please provide an answer for each row.  [Outdoor environmental art]'],
                        db_columnNames[73]:res[i]['Please indicate the structures for environmental learning located on your school grounds. Please provide an answer for each row.  [Greenhouse]'],
                        db_columnNames[74]:res[i]['Please indicate the structures for environmental learning located on your school grounds. Please provide an answer for each row.  [Tower garden]'],
                        db_columnNames[75]:res[i]['Please indicate the structures for environmental learning located on your school grounds. Please provide an answer for each row.  [Weather Station]'],
                        db_columnNames[76]:res[i]['Please indicate the structures for environmental learning located on your school grounds. Please provide an answer for each row.  [Pond]'],
                        db_columnNames[77]:res[i]['Please indicate the structures for environmental learning located on your school grounds. Please provide an answer for each row.  [Hydroponics ]'],
                        db_columnNames[78]:res[i]['Please indicate the structures for environmental learning located on your school grounds. Please provide an answer for each row.  [Aquaponics]'],
                        db_columnNames[79]:res[i]['Structures for Environmental Learning:  Other and Comments, please describe other structures for environmental learning located on your school campus. '],
                        db_columnNames[80]:res[i]['Does your school have a No Idle Zone?'],
                        db_columnNames[81]:res[i]['Does your school have a formal carpooling program? '],
                        db_columnNames[82]:res[i]['Does your school have parking spaces designated for electric, hybrid, or energy efficient vehicles? '],
                        db_columnNames[83]:res[i]['Does your school grow and donate and/or eat healthy food in school gardens?'],
                        db_columnNames[84]:res[i]['Does your school utilize green cleaning products?'],
                        db_columnNames[85]:res[i]['Does your school participate in one or more Citizen Science/Community Science programs such as GLOBE, GLOBE Observer, iTree, iNaturalist or other citizen science/ community science protocol to better understand the school environment and how citizen science/community science is used?'],
                        db_columnNames[86]:res[i]['Has your school received any awards or special recognition based on your enviornmental actions or instruction? '],
                        db_columnNames[87]:res[i]['Are there any other environmentally friendly actions your school takes that have not been mentioned in this survey?'],
                        db_columnNames[88]:getSchoolAdditionalInfo(res[i]['What is the name of your school? '],'latitude'),
                        db_columnNames[89]:getSchoolAdditionalInfo(res[i]['What is the name of your school? '],'longitude'),
                        db_columnNames[90]:getSchoolAdditionalInfo(res[i]['What is the name of your school? '],'picture'),
                        db_columnNames[91]:getSchoolAdditionalInfo(res[i]['What is the name of your school? '],'website')
                }
        table.put_item(Item=input)
    else:
        response = ('[{"status":"No New Data."}]')
return response
# print(latest_update)
# today=datetime.datetime.strftime(today, '%m/%d/%Y')