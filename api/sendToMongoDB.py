def push_to_mongo(data, user_email):
    from pymongo import MongoClient
    from datetime import datetime
    import heartpy as hp

    # Collect User Email
    user = user_email['localEmail']

    today_date = datetime.utcnow().strftime('%Y-%m-%d')
    sample_rate = 250

    # Collect Voltage Values
    voltage = data['voltage']

    # Filter and remove noise using heartpy library
    filtered = hp.remove_baseline_wander(voltage, sample_rate)
    filtered_voltage = filtered[1250:1750].tolist()

    # Calculate Heart Rate
    working_data, measures = hp.process(filtered, 250, report_time=True)
    heart_rate=round(measures['bpm'])

    # Calculate Breathing Rate
    breathing_rate=round(measures['breathingrate'], 3)

    data_to_send_to_mongo = {'timestamp': today_date, 'voltage': filtered_voltage, 'heartRate': heart_rate, 'breathingRate': breathing_rate}

    # Connect to the MongoDB Client
    client = MongoClient(
        "mongodb+srv://ecg:ecg@cluster0.9vq9f.mongodb.net/<dbname>?retryWrites=true&w=majority")

    # Access the database
    db = client["<dbname>"]

    # Access the collection
    collection = db["users"]

    # Add ecg data into the database based on the unique user email
    collection.update_one(
            {'email': user}, {'$push': {'data': data_to_send_to_mongo}})