import os
import pandas as pd
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

class Database:
    """Class to handle all database operations."""
    
    def __init__(self):
        """Initialize the database connection."""
        self.mongo_uri = os.getenv('MONGO_URI')
        if not self.mongo_uri:
            raise ValueError("MONGO_URI environment variable not set")
        
        self.client = MongoClient(self.mongo_uri)
        self.db = self.client.health_db
        
    def import_csv_to_mongodb(self, csv_file, collection_name):
        """Import data from a CSV file into MongoDB."""
        df = pd.read_csv(csv_file)
        
        # Convert dates to proper format
        if 'date' in df.columns:
            df['date'] = pd.to_datetime(df['date'])
        
        # Convert DataFrame to list of dictionaries
        records = df.to_dict('records')
        
        # Insert into MongoDB
        collection = self.db[collection_name]
        result = collection.insert_many(records)
        
        return len(result.inserted_ids)
    
    def get_all_data(self, collection_name):
        """Get all data from a collection."""
        collection = self.db[collection_name]
        return list(collection.find({}, {'_id': 0}))
    
    def get_data_by_country(self, collection_name, country):
        """Get data for a specific country."""
        collection = self.db[collection_name]
        return list(collection.find({'country': country}, {'_id': 0}))
    
    def get_data_by_disease(self, collection_name, disease):
        """Get data for a specific disease."""
        collection = self.db[collection_name]
        return list(collection.find({'disease': disease}, {'_id': 0}))
    
    def get_unique_countries(self, collection_name):
        """Get a list of unique countries in the dataset."""
        collection = self.db[collection_name]
        return collection.distinct('country')
    
    def get_unique_diseases(self, collection_name):
        """Get a list of unique diseases in the dataset."""
        collection = self.db[collection_name]
        return collection.distinct('disease')
    
    def get_summary_stats(self, collection_name):
        """Get summary statistics from the data."""
        collection = self.db[collection_name]
        pipeline = [
            {
                '$group': {
                    '_id': '$disease',
                    'total_cases': {'$sum': '$cases'},
                    'total_deaths': {'$sum': '$deaths'},
                    'total_recovered': {'$sum': '$recovered'},
                    'avg_cases': {'$avg': '$cases'},
                    'avg_deaths': {'$avg': '$deaths'},
                    'avg_recovered': {'$avg': '$recovered'}
                }
            }
        ]
        return list(collection.aggregate(pipeline))