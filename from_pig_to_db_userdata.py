import os.path
import pymongo

demography_base_folder = os.path.join("Task1", "Task1", "trainDemography")
dem_prefix = "part-v004-o001-r-"


client = pymongo.MongoClient("localhost", 27017)
db = client.odnoklassniki
user_collection = db.user_data

start = 0
end = 16

for i in range(start, end):
    dem_filename = dem_prefix + str(i).rjust(5, "0")
    dem_path = os.path.join(demography_base_folder, dem_filename)

    dem_file = open(dem_path, 'r')
    print("Opening demography file {}".format(dem_path))

    for line in dem_file:
        (user_id, create_date, birth_date, gender, country_id, location_id, login_region,
        is_core) = map(lambda x:int(x) if x.isdigit() else x, line.strip().split('\t'))

        user = {'id': user_id,
                'create_date': create_date,
                'birth_date': birth_date,
                'gender': gender,
                'country_id': country_id,
                'location_id': location_id,
                'login_region': login_region}

        user_collection.insert(user)
