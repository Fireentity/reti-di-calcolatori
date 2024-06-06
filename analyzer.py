import csv
import matplotlib.pyplot as plt

def calculate_metrics(times):
    if not times:
        return 0, 0, 0, 0
    minimum = min(times)
    maximum = max(times)
    average = sum(times) / len(times)
    variance = sum((x - average) ** 2 for x in times) / len(times)
    return minimum, average, maximum, variance ** 0.5


def main():
    with open('RTT.csv', 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        data = {}
        for row in reader:
            server = row['server']

            if server not in data:
                data[server] = []
            data[server].append(row)

        for server, data in data.items():

            packet_size = [point['payload_size'] for point in data]
            avg_rtt = [point['avg_rtt'] for point in data]
            min_rtt = [point['min_rtt'] for point in data]
            max_rtt = [point['max_rtt'] for point in data]
            plt.figure(figsize=(10, 6))
            plt.plot(packet_size, avg_rtt, color='red', marker='o', label=f'{server} - Average RTT')
            plt.plot(packet_size, min_rtt, color='blue', marker='o', label=f'{server} - Minimum RTT')
            plt.plot(packet_size, max_rtt, color='green', marker='o', label=f'{server} - Maximum RTT')
            plt.xlabel('Packet Size (bytes)')
            plt.ylabel('RTT (ms)')
            plt.title(f'RTT vs Packet Size - {server}')
            plt.tight_layout()
            plt.legend()
            plt.grid(True)
            plt.savefig(f'rtt_graph_{server}.png')
            plt.close()

            std_rtt = [point['std_rtt'] for point in data]
            plt.figure(figsize=(10, 6))
            plt.plot(packet_size, std_rtt, marker='o', label=f'{server} - Standard deviation RTT')
            plt.xlabel('Packet Size (bytes)')
            plt.ylabel('RTT (ms)')
            plt.title(f'RTT vs Packet Size - {server}')
            plt.tight_layout()
            plt.legend()
            plt.grid(True)
            plt.savefig(f'rtt_std_graph_{server}.png')
            plt.close()


if __name__ == "__main__":
    main()