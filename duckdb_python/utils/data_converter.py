import duckdb
import glob
from duckdb_python.config import settings

# produces a parquet file in settings.parquet_data_path for each file in settings.csv_data_path
def generate_parquet_from_csv():
  conn = duckdb.connect(database=settings.db_path, read_only=False)
  for filename in glob.iglob(f'{settings.csv_data_path}/*.csv'):
    output_path = f'{settings.parquet_data_path}/{filename.split("/")[-1][:-4]}.parquet'
    conn.execute(f"""
    COPY (SELECT * FROM read_csv('{filename}', header=True, timestampformat='%m/%d/%Y %H:%M:%S %p', columns={{'SRNumber': 'VARCHAR(255)','CreatedDate': 'TIMESTAMP','UpdatedDate': 'TIMESTAMP','ActionTaken': 'VARCHAR(255)','Owner': "VARCHAR(255)",'RequestType': 'VARCHAR(255)','Status': 'VARCHAR(255)','RequestSource': 'VARCHAR(255)','CreatedByUserOrganization': 'VARCHAR(255)','MobileOS': 'VARCHAR(255)','Anonymous': 'VARCHAR(255)','AssignTo': 'VARCHAR(255)','ServiceDate': 'TIMESTAMP','ClosedDate': 'TIMESTAMP','AddressVerified': 'VARCHAR(255)','ApproximateAddress': 'VARCHAR(255)','Address': 'VARCHAR(255)','HouseNumber': 'INTEGER','Direction': 'VARCHAR(255)','StreetName': 'VARCHAR(255)','Suffix': 'VARCHAR(255)','ZipCode': 'INTEGER','Latitude': 'DECIMAL(8,6)','Longitude': 'DECIMAL(9,6)','Location': 'VARCHAR(255)','TBMPage': 'INTEGER','TBMColumn': 'VARCHAR(255)','TBMRow': 'INTEGER','APC': 'VARCHAR(255)','CD': 'INTEGER','CDMember': 'VARCHAR(255)','NC': 'INTEGER','NCName': 'VARCHAR(255)','PolicePrecinct': 'VARCHAR(255)'}}, filename=True, ignore_errors=True)) 
    TO '{output_path}' (FORMAT 'parquet')""")