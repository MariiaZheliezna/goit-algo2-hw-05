import json
import time
import hyperloglog

def load_log_file(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
        ip_addresses = [json.loads(line)["remote_addr"] for line in lines]
    return ip_addresses

def exact_unique_ips(ip_addresses):
    start_time = time.time()
    unique_ips = set(ip_addresses)
    unique_count = len(unique_ips)
    end_time = time.time()
    return unique_count, end_time - start_time

def approximate_unique_ips(ip_addresses, precision=0.01):
    start_time = time.time()
    hll = hyperloglog.HyperLogLog(precision)
    for ip in ip_addresses:
        hll.add(ip)
    unique_count = len(hll)
    end_time = time.time()
    return unique_count, end_time - start_time

if __name__ == "__main__":
    log_file_path = "lms-stage-access.log"  # Замість цього шляху вкажіть реальний шлях до лог-файлу
    ip_addresses = load_log_file(log_file_path)

    exact_count, exact_time = exact_unique_ips(ip_addresses)
    approx_count, approx_time = approximate_unique_ips(ip_addresses)

    print("Результати порівняння:")
    print("                       Точний підрахунок   HyperLogLog")
    print(f"Унікальні елементи               {exact_count:.0f}           {approx_count:.0f}")
    print(f"Час виконання (сек.)             {exact_time:.4f}       {approx_time:.4f}")
