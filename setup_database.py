import mysql.connector
from mysql.connector import Error
import os
import sys

def setup_database():
    connection = None
    try:
        # Connect to MySQL server
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="123456789Op"
        )
        
        if connection is not None and connection.is_connected():
            cursor = connection.cursor()
            
            # Create database if it doesn't exist
            cursor.execute("CREATE DATABASE IF NOT EXISTS bincom_test")
            print("Database 'bincom_test' created successfully")
            
            # Switch to the database
            cursor.execute("USE bincom_test")
            
            # Create tables
            create_tables = [
                """
                CREATE TABLE IF NOT EXISTS states (
                    state_id INT PRIMARY KEY,
                    state_name VARCHAR(50)
                )
                """,
                """
                CREATE TABLE IF NOT EXISTS lga (
                    lga_id INT PRIMARY KEY,
                    lga_name VARCHAR(50),
                    state_id INT,
                    lga_description TEXT,
                    entered_by_user VARCHAR(50),
                    date_entered DATETIME,
                    user_ip_address VARCHAR(50),
                    FOREIGN KEY (state_id) REFERENCES states(state_id)
                )
                """,
                """
                CREATE TABLE IF NOT EXISTS ward (
                    ward_id INT PRIMARY KEY,
                    ward_name VARCHAR(50),
                    lga_id INT,
                    ward_description TEXT,
                    entered_by_user VARCHAR(50),
                    date_entered DATETIME,
                    user_ip_address VARCHAR(50),
                    FOREIGN KEY (lga_id) REFERENCES lga(lga_id)
                )
                """,
                """
                CREATE TABLE IF NOT EXISTS polling_unit (
                    polling_unit_id INT AUTO_INCREMENT PRIMARY KEY,
                    ward_id INT,
                    lga_id INT,
                    uniqueid INT UNIQUE,
                    polling_unit_number VARCHAR(50),
                    polling_unit_name VARCHAR(50),
                    polling_unit_description TEXT,
                    lat VARCHAR(255),
                    longitude VARCHAR(255),
                    entered_by_user VARCHAR(50),
                    date_entered DATETIME,
                    user_ip_address VARCHAR(50),
                    FOREIGN KEY (ward_id) REFERENCES ward(ward_id),
                    FOREIGN KEY (lga_id) REFERENCES lga(lga_id)
                )
                """,
                """
                CREATE TABLE IF NOT EXISTS announced_pu_results (
                    result_id INT AUTO_INCREMENT PRIMARY KEY,
                    polling_unit_uniqueid INT,
                    party_abbreviation VARCHAR(4),
                    party_score INT,
                    entered_by_user VARCHAR(50),
                    date_entered DATETIME,
                    user_ip_address VARCHAR(50),
                    FOREIGN KEY (polling_unit_uniqueid) REFERENCES polling_unit(uniqueid)
                )
                """,
                """
                CREATE TABLE IF NOT EXISTS announced_lga_results (
                    result_id INT AUTO_INCREMENT PRIMARY KEY,
                    lga_name VARCHAR(50),
                    party_abbreviation VARCHAR(4),
                    party_score INT,
                    entered_by_user VARCHAR(50),
                    date_entered DATETIME,
                    user_ip_address VARCHAR(50)
                )
                """
            ]
            
            for table in create_tables:
                cursor.execute(table)
                print(f"Table created successfully")
            
            connection.commit()
            print("Database setup completed successfully!")
            
    except Error as e:
        print(f"Error: {e}")
    finally:
        if connection is not None and connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection closed.")

if __name__ == "__main__":
    setup_database() 