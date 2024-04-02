from utils.utils_api import (
    create_connection
)
from utils.utils_DB import get_table_data ,get_addr_data_as_dict

def dbconnect():
    conn = create_connection()
    return conn

def getData():
    conn = dbconnect()
    tableData = get_table_data(conn)
    # print("tableData",tableData)
    return tableData

def ShortData():
    data = getData()
    for tx in data:
        tx['Sender_address'] = tx['Sender_address'][:6]
        tx['Receiver_address'] = tx['Receiver_address'][:6]
    return data


def getFilterData(amount:int):
    tx_list = getData()
    # print(tx_list)
    filter_list = []
    for tx in tx_list:
        if tx['Amount'] >= amount:
            filter_list.append(tx)
    # print(filter_list)
    return filter_list

def getJettonData():
    tx_list = getData()
    jetton_list = []
    for tx in tx_list:
        if tx['Type'] == 'Jetton':
            jetton_list.append(tx)
    return jetton_list

def getNFTData():
    tx_list = getData()
    nft_list = []
    for tx in tx_list:
        if tx['transaction_type'] == 'NFT':
            nft_list.append(tx)
    return nft_list


def getAddressTable()->dict:
    conn = dbconnect()
    add_data = get_addr_data_as_dict(conn)
    return add_data

getFilterData(1)



