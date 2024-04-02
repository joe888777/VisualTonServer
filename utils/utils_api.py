import schedule
import mysql.connector
import time
import requests
import asyncio
import json
from typing import Optional

VALUE_UPPER_LIMIT = 1000000000 * 100
# 100 TON

from utils.utils_DB import delete_duplicate_data


class tx:
    tx_id: str
    block_id: int
    sender_address: str
    receiver_address: str
    transaction_type: str
    amount: int
    confirm_time: int
    raw_data: str


def create_connection():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            port=3307,
            user="root",
            password="0505jojo",
            database="example",
        )
        return conn
    except Exception as e:
        print(f"Error connecting to MySQL: {str(e)}")
        return None


async def get_request(block_url):
    response = None
    while response is None or response.status_code != 200:
        # print("trying to get request from get_request()...")
        try:
            response = requests.get(block_url)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            print("Request failed:", e)
            print("sleep a while...")
            time.sleep(2)
            continue
    if response.status_code == 200:
        return response
    else:
        print("Request failed with status code:", response.status_code)


async def analyze_tx_to_tx_info(transaction, block_id: int) -> Optional[tx]:
    transaction_type = "TON"
    if 'in_msg' in transaction and 'decoded_op_name' in transaction['in_msg']:
        if transaction['in_msg']['decoded_op_name'] == 'jetton_notify':
            transaction_type = "Jetton"
        elif transaction['in_msg']['decoded_op_name'] == 'nft_ownership_assigned':
            transaction_type = "NFT"
    transaction_json = json.dumps(transaction) 

    if "in_msg" in transaction:
        in_msg = transaction["in_msg"]
        if "source" in in_msg and "destination" in in_msg and in_msg["value"] > 0:
            res: tx = {
                "tx_id": transaction["hash"],
                "block_id": block_id,
                "sender_address": in_msg["source"]["address"],
                "receiver_address": in_msg["destination"]["address"],
                "type": transaction_type,
                "amount": in_msg["value"],
                "confirm_time": transaction["utime"],
                "raw_data": transaction_json
            }
            # print(transaction_type)
            return res

    if "out_msgs" in transaction and len(transaction["out_msgs"]) != 0:
        out_msgs = ""
        if isinstance(transaction["out_msgs"], list):
            out_msgs = transaction["out_msgs"][0]
        else:
            out_msgs = transaction["out_msgs"]

        if "source" in out_msgs and "destination" in out_msgs and out_msgs["value"] > 0:
            res: tx = {
                "tx_id": transaction["hash"],
                "block_id": block_id,
                "sender_address": out_msgs["source"]["address"],
                "receiver_address": out_msgs["destination"]["address"],
                "type": transaction_type,
                "amount": out_msgs["value"],
                "confirm_time": transaction["utime"],
                "raw_data": transaction_json
            }
            # print(transaction_type)
            return res
    tx_id = transaction["hash"]
    print(f"can't analyze tx {tx_id} !")
    # print(transaction)


async def get_txs_by_block_ids(block_ids: [int]) -> [tx]:
    all_txs: [tx] = []
    response = None
    for id in block_ids:
        # print(f"start to get block {id} tx...")

        if id % 2 == 0:
            continue
        else:
            block_url = f"https://tonapi.io/v2/blockchain/blocks/(0,8000000000000000,{id})/transactions"
            response = await get_request(block_url)
            
        block_data = response.json()

        if "transactions" in block_data:
            # lens = len(block_data["transactions"])
            # print(f"there are {lens} txs to analyze")

            for transaction in block_data["transactions"]:
                if transaction["transaction_type"] != "TransOrd":
                    print(f"the tx type is not TransOrd, just skip it")
                    print("the tx type:")
                    continue

                tmp = await analyze_tx_to_tx_info(transaction, id)

                if tmp is not None:
                    all_txs.append(tmp)
        else:
            print(f"can't find transaction in block {id}")
            continue

    print(f"total get {len(all_txs)} in {block_ids}")
    return all_txs


async def get_latest_block_id() -> int:
    # res = await get_request(f"https://tonapi.io/v2/blockchain/masterchain-head")
    # return int(res.json()["seqno"])
    paylaod = {"query": "{wcBlocks: blocks(workchain: 0, page_size: 1) { seqno }}"}
    r = requests.post("https://dton.io/graphql/", data=paylaod).json()
    return int(r["data"]["wcBlocks"][0]["seqno"])


def filter_tx(txs: [tx]) -> [tx]:
    # print(f"before filter, the total tx is {len(txs)}")
    filtered_tx_list = list(filter(lambda tx: tx["amount"] >= VALUE_UPPER_LIMIT, txs))
    filtered_tx_list = delete_duplicate_data(filtered_tx_list)
    # print(f"after filter, the total tx is {len(filtered_tx_list)}")
    return filtered_tx_list
