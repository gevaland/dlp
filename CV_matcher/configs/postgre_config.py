posgres_DB = "cv_match_db"
posgres_user = "cv_match_user"
posgres_user_password = "cv_match_password"
sql_alchemy_engine = f"postgresql+psycopg2://{posgres_user}:{posgres_user_password}@127.0.0.1/{posgres_DB}"
