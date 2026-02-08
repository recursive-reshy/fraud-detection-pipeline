# System imports
import logging
# Database
from sqlalchemy import Engine, text

logging.basicConfig( 
  level = logging.INFO,
  format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger( __name__ )

def populate_fact_transactions( engine: Engine ) -> int:

  logger.info( "Clearing existing data..." )

  with engine.connect() as connection:
    # connection.execute( text( "TRUNCATE TABLE fact_transactions" ) )
    # connection.commit()

    logger.info( "Inserting data into fact_transactions..." )

    # Insert data into fact_transactions
    sql = """
      INSERT INTO fact_transactions (
        time_key,
        type_key,
        origin_account_key,
        destination_account_key,
        amount,
        old_balance_orig,
        new_balance_orig,
        old_balance_dest,
        new_balance_dest,
        is_fraud,
        is_flagged_fraud
      ) 
      SELECT 
        dt.id,
        tt.id,
        da_orig.id,
        da_dest.id,
        st.amount,
        st.oldbalanceOrg,
        st.newbalanceOrig,
        st.oldbalanceDest,
        st.newbalanceDest,
        st.isFraud,
        st.isFlaggedFraud
      FROM staging_transactions st 
      INNER JOIN dim_time dt ON st.step = dt.step 
      INNER JOIN dim_transaction_type tt ON st.type = tt.type_name 
      INNER JOIN dim_account da_orig ON st.nameOrig = da_orig.account_id 
      INNER JOIN dim_account da_dest ON st.nameDest = da_dest.account_id
    """

    connection.execute( text( sql ) )
    connection.commit()

    # Verify
    count_result = connection.execute( text( "SELECT COUNT(*) FROM fact_transactions" ) )
    count = count_result.fetchone()[ 0 ]

    logger.info( f"Fact transactions inserted: { count }" )

  return count

"""
Helper function that ensures that the relationships between your tables remain consistent
and that we don't end up with orphaned data
"""
def verify_referential_integrity( engine: Engine ) -> bool:
  logger.info( "Verifying referential integrity..." )

  sql = """
    SELECT COUNT(*) as orphaned_records 
    FROM fact_transactions ft 
    LEFT JOIN dim_time dt ON ft.time_key = dt.id 
    LEFT JOIN dim_transaction_type tt ON ft.type_key = tt.id 
    LEFT JOIN dim_account da_orig ON ft.origin_account_key = da_orig.id 
    LEFT JOIN dim_account da_dest ON ft.destination_account_key = da_dest.id 
    WHERE dt.id is NULL 
      OR tt.id is NULL 
      OR da_orig.id is NULL 
      OR da_dest.id is NULL
  """

  with engine.connect() as connection:
    result = connection.execute( text( sql ) )

    orphaned_records = result.fetchone()[ 0 ]

    if orphaned_records > 0:
      logger.info( f"Found { orphaned_records } orphaned records" )
    else:
      logger.info( "No orphaned records found" )
    
    return orphaned_records == 0

def show_fraud_distribution( engine: Engine ) -> None:
  logger.info( "Showing fraud distribution..." )

  sql = """
    SELECT is_fraud, COUNT(*) as count 
    FROM fact_transactions 
    GROUP BY is_fraud
  """

  with engine.connect() as connection:
    fraud_distribution = connection.execute( text( sql ) )

  for row in fraud_distribution:
    fraud_label = "fraudulent" if row[ 0 ] == 1 else "not fraudulent"
    logger.info( f"{ fraud_label }: { row[ 1 ] } rows" )