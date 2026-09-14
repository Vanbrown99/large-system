import os
import time

import mysql.connector


def enabled() -> bool:
    return bool(os.getenv("DB_HOST"))


def connection():
    last_error = None
    for _ in range(15):
        try:
            return mysql.connector.connect(
                host=os.getenv("DB_HOST", "mysql"),
                port=int(os.getenv("DB_PORT", "3306")),
                database=os.getenv("DB_NAME", "school_erp"),
                user=os.getenv("DB_USER", "erp_user"),
                password=os.getenv("DB_PASSWORD", "erp_password_change_me"),
            )
        except mysql.connector.Error as error:
            last_error = error
            time.sleep(2)
    raise RuntimeError("HR database is unavailable") from last_error