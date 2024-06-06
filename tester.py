import subprocess
import re
import csv
import concurrent.futures

# Configuration
servers = [
    "atl.speedtest.clouvider.net",
    "nyc.speedtest.clouvider.net",
    "lon.speedtest.clouvider.net",
    "la.speedtest.clouvider.net",
    "paris.testdebit.info",
    "lyon.testdebit.info",
    "aix-marseille.testdebit.info",
    "1.1.1.1"
]

packet_count = 4
payload_sizes = range(10, 1473, 10)
rtt_csv_filename = 'RTT.csv'
hops_csv_filename = 'hops.csv'


def execute_command(command):
    """Run a shell command and return its output."""
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    return result.stdout.decode('utf-8')


def ping(server, packet_size, packet_count=4):
    """Ping a server with a specified packet size and count."""
    command = f'ping {server} -n {packet_count} -l {packet_size}'
    return execute_command(command)


def tracert(server):
    """Run tracert to a server."""
    command = f'tracert {server}'
    return execute_command(command)


def parse_ping_rtt(ping_output):
    """Extract RTT values from ping output."""
    match = re.search(r'Medio =\s+(\d+)ms', ping_output)
    if match:
        avg_rtt = float(match.group(1))
        return avg_rtt
    return None


def calculate_hops(traceroute_output):
    """Calculate the number of hops from traceroute output."""
    hops = len(re.findall(r'^\s*\d+', traceroute_output, re.MULTILINE))
    if hops > 0:
        return hops - 1
    return hops


def process_server(server):
    """Process each server by performing traceroute and ping."""
    print(f"Processing {server}...")
    traceroute_result = tracert(server)
    hops = calculate_hops(traceroute_result)
    print(f"Traceroute to {server} completed with {hops} hops. Output:\n{traceroute_result}")

    rtt_results = []
    for payload_size in payload_sizes:
        ping_result = ping(server, payload_size, packet_count)
        avg_rtt = parse_ping_rtt(ping_result)
        if avg_rtt is not None:
            rtt_results.append((server, payload_size, avg_rtt))
            print(f"Ping to {server} with payload size {payload_size} bytes: avg RTT = {avg_rtt} ms")
        else:
            print(
                f"Failed to parse RTT from ping to {server} with payload size {payload_size} bytes. Output:\n{ping_result}")
    return server, hops, rtt_results


def main():
    results = []
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future_to_server = {executor.submit(process_server, server): server for server in servers}
        for future in concurrent.futures.as_completed(future_to_server):
            server = future_to_server[future]
            try:
                result = future.result()
                results.append(result)
            except Exception as exc:
                print(f"{server} generated an exception: {exc}")

    with open(rtt_csv_filename, mode='w', newline='') as rtt_file, open(hops_csv_filename, mode='w',
                                                                        newline='') as hops_file:
        rtt_writer = csv.writer(rtt_file)
        hops_writer = csv.writer(hops_file)

        rtt_writer.writerow(['server', 'payload_size', 'avg_rtt'])
        hops_writer.writerow(['server', 'hops'])

        for server, hops, rtt_results in results:
            hops_writer.writerow([server, hops])
            for rtt_result in rtt_results:
                rtt_writer.writerow(rtt_result)

    print("Results saved to CSV files.")


if __name__ == "__main__":
    main()