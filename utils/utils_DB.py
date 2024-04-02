class tx:
    tx_id: str
    block_id: int
    sender_address: str
    receiver_address: str
    type: str
    amount: int
    confirm_time: int
    raw_data: str


class addr:
    name: str
    addr: str
    type: str
    url: str


def add_data(conn, all_txs):
    try:
        cursor = conn.cursor()
        sql = """
        INSERT INTO transactions (Transaction_id, Block_id, Sender_address, Receiver_address, Type, Amount, Confirm_time, Raw_data)
        VALUES (%s, %s, %s, %s, %s, %s, %s,%s)
        """
        for tx in all_txs:
            # print(tx)
            data = (
                tx["tx_id"],
                tx["block_id"],
                tx["sender_address"],
                tx["receiver_address"],
                tx["type"],
                (int(tx["amount"]) / 1000000000),
                tx["confirm_time"],
                tx["raw_data"]
            )
        cursor.execute(sql, data)

        conn.commit()
        print("Data added successfully")
    except Exception as e:
        conn.rollback()
        print(f"Error adding data: {str(e)}")


def delete_data(conn, block_ids: [int]):
    for block_id in block_ids:
        try:
            cursor = conn.cursor()
            sql = "DELETE FROM transactions WHERE Block_id = %s"
            cursor.execute(sql, (block_id,))
            conn.commit()
            # print(f"Data with Block_id '{block_id}' deleted successfully")
        except Exception as e:
            conn.rollback()
            print(f"Error deleting data: {str(e)}")


def delete_duplicate_data(txs: [tx]) -> [tx]:
    seen = set()
    result: [tx] = []

    for item in txs:
        record = (
            item["block_id"],
            item["sender_address"],
            item["receiver_address"],
            item["amount"],
            item["confirm_time"],
        )

        if record not in seen:
            seen.add(record)
            result.append(item)

    return result


def get_table_data(conn) -> [tx]:
    try:
        cursor = conn.cursor()
        sql = "SELECT * FROM transactions"
        cursor.execute(sql)

        rows = cursor.fetchall()

        data_list: [tx] = []

        for row in rows:
            (
                transaction_id,
                block_id,
                sender_address,
                receiver_address,
                type,
                amount,
                confirm_time,
                raw_data
            ) = row
            data: tx = {
                "Transaction_id": transaction_id,
                "Block_id": block_id,
                "Sender_address": sender_address,
                "Receiver_address": receiver_address,
                "Type": type,
                "Amount": amount,
                "Confirm_time": confirm_time,
                "Raw_data": raw_data
            }
            data_list.append(data)

        return data_list

    except Exception as e:
        print(f"Error fetching data: {str(e)}")


def add_addr_data(conn, name, addr, type, url):
    try:
        cursor = conn.cursor()
        insert_query = """
        INSERT INTO addresses (name, addr, type, url)
        VALUES (%s, %s, %s, %s)
        """
        data = (name, addr, type, url)
        cursor.execute(insert_query, data)
        conn.commit()
        print("Data added successfully")
    except Exception as e:
        conn.rollback()
        print(f"Error adding data: {str(e)}")


def delete_addr_data(conn, name):
    try:
        cursor = conn.cursor()
        delete_query = "DELETE FROM addresses WHERE name = ?"
        cursor.execute(delete_query, (name,))
        conn.commit()
        print(f"Data for '{name}' deleted successfully")
    except Exception as e:
        conn.rollback()
        print(f"Error deleting data: {str(e)}")


def get_tx_table_rowdata_amount(conn) -> int:
    try:
        cursor = conn.cursor()
        count_query = "SELECT COUNT(*) FROM transactions"
        cursor.execute(count_query)
        count: int = cursor.fetchone()[0]
        return count

    except Exception as e:
        print(f"Error fetching data: {str(e)}")


def get_min_max_amount_data(conn) -> [tx]:
    cursor = conn.cursor()
    min_amount_query = "SELECT * FROM transactions WHERE Amount = (SELECT MIN(Amount) FROM transactions)"
    cursor.execute(min_amount_query)
    min_data = cursor.fetchone()

    max_amount_query = "SELECT * FROM transactions WHERE Amount = (SELECT MAX(Amount) FROM transactions)"
    cursor.execute(max_amount_query)
    max_data = cursor.fetchone()
    min_tx = None
    max_tx = None

    if min_data:
        min_tx = {
            "tx_id": min_data[0],
            "block_id": min_data[1],
            "sender_address": min_data[2],
            "receiver_address": min_data[3],
            "type": min_data[4],
            "amount": min_data[5],
            "confirm_time": min_data[6],
            "raw_data": min_data[7]
        }

    if max_data:
        max_tx = {
            "tx_id": max_data[0],
            "block_id": max_data[1],
            "sender_address": max_data[2],
            "receiver_address": max_data[3],
            "type": max_data[4],
            "amount": max_data[5],
            "confirm_time": max_data[6],
            "raw_data": min_data[7]
        }

    return [min_tx, max_tx]


def get_addr_data_as_dict(conn):
    cursor = conn.cursor()
    select_query = "SELECT * FROM addresses"
    cursor.execute(select_query)
    rows = cursor.fetchall()

    addr_data_dict = {}
    for row in rows:
        addr = row[1]
        name = row[0]
        addr_type = row[2]
        url = row[3]

        addr_info = {"name": name, "type": addr_type, "url": url}

        addr_data_dict[addr] = addr_info

    return addr_data_dict
