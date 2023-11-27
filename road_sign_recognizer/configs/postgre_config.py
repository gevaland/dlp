posgres_DB = "road_sign_detection_db"
posgres_user = "road_sign_detection_user"
posgres_user_password = "rsdpassword"
sql_alchemy_engine = f"postgresql+psycopg2://{posgres_user}:{posgres_user_password}@127.0.0.1/{posgres_DB}"
