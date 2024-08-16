from flask import Flask, jsonify
import os
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/stats')
def stats():
    with open('/sys/class/thermal/thermal_zone0/temp', 'r') as f:
        cpu_temp = int(f.read()) /1000.0

    with open('/sys/devices/system/cpu/cpu0/cpufreq/scaling_cur_freq', 'r') as f:
        cpu_clock = int(f.read()) / 1000000.0
    
    with open('/proc/uptime', 'r') as f:
        uptime = float(f.read().split()[0]) / 86400  # Convert seconds to days

    meminfo = {}

    with open('/proc/meminfo') as f:
        for line in f:
            split_line = line.split(':')
            if len(split_line) == 2:
                key = split_line[0].strip()
                value = int(split_line[1].strip().split()[0])
                meminfo[key] = value

    total_ram = meminfo.get('MemTotal', 0)
    free_ram = meminfo.get('MemFree', 0)
    ram_usage = (total_ram - free_ram) * 0.000000954

    return jsonify({
        'cpuTemperature': round(cpu_temp, 1),
        'cpuClock': cpu_clock,
        'uptime': round(uptime, 2),
        'ramUsage': round(ram_usage, 3)
    })

    

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)