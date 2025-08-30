from flask import Flask, render_template, request, jsonify
import math

app = Flask(__name__)

# 송도 위험지역 좌표
coords = [
    (37.382145, 126.647382),
    (37.391245, 126.662513),
    (37.365839, 126.635281),
    (37.399128, 126.676392),
    (37.375624, 126.668417),
    (37.389513, 126.641224),
    (37.389513, 127.641224),
    (38.389513, 126.641224),
    (37.368295, 126.659283),
    (37.396427, 126.672519),
    (37.373182, 126.638514),
    (37.386291, 126.646872),
    (37.380512, 126.644921),
    (37.385721, 126.651239),
    (37.392834, 126.667812),
    (37.370152, 126.636528),
    (37.397413, 126.669847),
    (37.377845, 126.653214),
    (37.388214, 126.648932),
    (37.395621, 126.662489),
    (37.372981, 126.640185),
    (37.383472, 126.657394),
    (37.383472, 126.646489),
    (37.389757, 126.646489),
    (37.381245, 126.649372),
    (37.387451, 126.653812),
    (37.393128, 126.660291),
    (37.374512, 126.642183),
    (37.378923, 126.655732),
    (37.384672, 126.664125),
    (37.390182, 126.670892),
    (37.376281, 126.648519),
    (37.398412, 126.674231),
    (37.371892, 126.639827),
]

last_alert_zone = None

def haversine(coord1, coord2):
    lat1, lon1 = map(math.radians, coord1)
    lat2, lon2 = map(math.radians, coord2)
    dlat, dlon = lat2 - lat1, lon2 - lon1
    a = math.sin(dlat/2)**2 + math.cos(lat1)*math.cos(lat2)*math.sin(dlon/2)**2
    c = 2 * math.asin(math.sqrt(a))
    r = 6371
    return c * r  # km

@app.route('/')
def home():
    return render_template('index.html', coords=coords)

@app.route('/location', methods=['POST'])
def location():
    global last_alert_zone
    data = request.get_json()
    lat, lon = data['latitude'], data['longitude']
    inside_zones = []
    for c in coords:
        dist = haversine((lat, lon), c)
        if dist <= 0.1:
            inside_zones.append(c)
    if inside_zones and last_alert_zone is None:
        last_alert_zone = inside_zones[0]
        alert = True
    elif not inside_zones:
        last_alert_zone = None
        alert = False
    else:
        alert = False
    return jsonify({
        "inside": inside_zones,
        "alert": alert
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003, debug=True)
