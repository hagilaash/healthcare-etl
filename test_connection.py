from src.database.connection import test_database_connection


if __name__ == "__main__":
    try:
        if test_database_connection():
            print("SUCCESS: Connected to healthcare_etl_db!")
        else:
            print("FAILED: Database returned an unexpected result.")
    except Exception as error:
        print(f"FAILED: {type(error).__name__}: {error}")
