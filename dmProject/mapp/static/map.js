
var map = L.map('map').setView([11, 79], 10);
data = {};
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="https://osm.org/copyright">OpenStreetMap</a>contributors'
}).addTo(map);
var gcs = L.esri.Geocoding.geocodeService();
var count = 0;

map.on('click', (e) => {
    count += 1;
    gcs.reverse().latlng(e.latlng).run((err, res) => {
        if (err) return;

        L.marker(res.latlng).addTo(map).bindPopup(res.address.Match_addr).openPopup();
        k = count.toString();
        data[k + 'lat'] = res.latlng['lat'];
        data[k + 'lon'] = res.latlng['lng'];

        if (count == 1) {
            $('#lat11').val(res.latlng['lat']);
            $('#lon11').val(res.latlng['lng']);
        }

        if (count == 2) {
            $('#lat22').val(res.latlng['lat']);
            $('#lon22').val(res.latlng['lng']);

            var lat11 = document.getElementById('lat11').value;
            var lon11 = document.getElementById('lon11').value;
            var lat22 = document.getElementById('lat22').value;
            var lon22 = document.getElementById('lon22').value;
            var baseurl = "{% url 'mapp:showroute' 1.01 1.11 2.01 2.11 %}";

            window.location.replace(baseurl.substring(0, 6) + lat11 + '/' + lon11 + '/' + lat22 + '/' + lon22);
            count = 0;
        }
    });
});
