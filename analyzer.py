import pandas as pd
import matplotlib.pyplot as plt

ping_data = pd.read_csv('data/ping_results.csv')
traceroute_data = pd.read_csv('data/traceroute_results.csv')

servers = ping_data['server'].unique()

for server in servers:
    server_data = ping_data[ping_data['server'] == server]

    plt.figure(figsize=(10, 6))
    plt.plot(server_data['packet_size'], server_data['rtt'], label='RTT')
    plt.xlabel('Packet Size (bytes)')
    plt.ylabel('RTT (ms)')
    plt.title(f'RTT vs Packet Size for {server}')
    plt.legend()
    plt.grid(True)
    plt.savefig(f'data/rtt_{server}.png')
    plt.close()

for server in servers:
    server_data = traceroute_data[traceroute_data['server'] == server]
    hops = server_data['hops'].values[0]
    print(f'{server}: {hops} hops')
