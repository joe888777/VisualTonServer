# import pandas as pd
# from getData import getData

# def html_to_text():
#     data = create_graph()
#     return data

# def create_graph():

#     data = getData()
#     # 缩短 sender 和 receiver 地址
#     for tx in data:
#         tx['Sender_address'] = tx['Sender_address'][:6]
#         tx['Receiver_address'] = tx['Receiver_address'][:6]
#     df = pd.DataFrame(data)

#     return data
