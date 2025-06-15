import re
import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter

# Load log files
with open("access.log") as f:
    apache_logs = f.readlines()

with open("auth.log") as f:
    ssh_logs = f.readlines()

# Apache DoS detection
ip_counts = Counter()
for line in apache_logs:
    match = re.search(r'^(\d+\.\d+\.\d+\.\d+)', line)
    if match:
        ip = match.group(1)
        ip_counts[ip] += 1

# Flag IPs with high requests
dos_ips = {ip: count for ip, count in ip_counts.items() if count > 10}
pd.DataFrame(list(dos_ips.items()), columns=["IP", "Request Count"]).to_csv("dos_report.csv", index=False)

# SSH Brute-force detection
ssh_failures = []
for line in ssh_logs:
    match = re.search(r'Failed password.*from (\d+\.\d+\.\d+\.\d+)', line)
    if match:
        ssh_failures.append(match.group(1))

brute_force_ips = Counter(ssh_failures)
brute_force_report = {ip: count for ip, count in brute_force_ips.items() if count > 5}
pd.DataFrame(list(brute_force_report.items()), columns=["IP", "Failed Logins"]).to_csv("brute_force_report.csv", index=False)

# Visualization
top_ips = ip_counts.most_common(5)
ips, counts = zip(*top_ips)
plt.bar(ips, counts)
plt.title("Top 5 IPs by Request Count")
plt.xlabel("IP Address")
plt.ylabel("Number of Requests")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("access_patterns.png")
plt.show()

print("Analysis Complete. Reports generated.")
