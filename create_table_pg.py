import psycopg2
from db import conn


def create_table():
    command = (
            """
            CREATE TABLE meta (
                FILENAME TEXT NOT NULL,
                WELL_ID VARCHAR(20) NOT NULL,
                PLATE_ID TEXT NOT NULL,
                STAIN_DATE TEXT NOT NULL,
                PLATE_ROW CHAR(10) NOT NULL,
                PLATE_COLUMN INT NOT NULL,
                CONTROL_ROW CHAR(20),
                TARGET_SPECIES VARCHAR(30),
                SPECIFICITY_CD VARCHAR(40),
                SPECIFICITY_NON_CD VARCHAR(50),
                ISOTYPE_HOST_SPECIES VARCHAR(30),
                CLONE VARCHAR(40),
                FLUOROCHROME VARCHAR(50),
                PARAMETER VARCHAR(50),
                BATCH_NUMBER TEXT,
                UG_TEST REAL,
                UNITS VARCHAR(40),
                SAMPLE_TYPE VARCHAR(30),
                SAMPLE_SPECIES VARCHAR(30),
                SAMPLE_STRAIN TEXT,
                DONOR_ID VARCHAR(40),
                SPEC1_RANGE TEXT,
                SPEC2_RANGE TEXT,
                SPEC3_RANGE TEXT,
                GATING_METHOD VARCHAR(20),
                GATING_ARGUMENT INT
                )
            """)
    try:
        cur = conn.cursor()
        print('running commands..')
        # for cmd in command:
        cur.execute(command)
        cur.close()
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as e:
        print(e)
    finally:
        if conn is not None:
            conn.close()

if __name__ == "__main__":
    create_table()
