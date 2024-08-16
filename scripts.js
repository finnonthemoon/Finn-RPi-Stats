async function fetchStats() {
    try {
        const response = await fetch('http://192.168.1.117:5000/stats');
        const data = await response.json();

        document.getElementById('cpuTemp').textContent = data.cpuTemperature + ' °C';
        document.getElementById('cpuClock').textContent = data.cpuClock + ' GHz';
        document.getElementById('uptime').textContent = data.uptime + ' days';
        document.getElementById('ramUsage').textContent = data.ramUsage + ' GB';

    } catch (error) {
        console.error('Error fetching stats:', error);
        document.getElementById('stats').innerHTML = '<p>Error loading stats</p>';
    }
}

window.onload = function () {
    fetchStats();
    setInterval(fetchStats, 300);
}