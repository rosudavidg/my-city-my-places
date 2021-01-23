import "./Home.css"
import Map from "./Map"
import Panel from "./Panel"
import { useState, useEffect } from "react"
import axios from "axios";

const loadLocations = (setLocations) => {
    axios
        .get('http://localhost:5000/api/locations', {
            headers: {
                Authorization: `Bearer ${localStorage.getItem("token")}`,
            },
        })
        .then((res) => {
            setLocations(res.data)
        })
        .catch((e) => {
            alert("Cannot get locations")
        });
}

const Home = () => {
    const [coords, setCoords] = useState({
        center: {
            lat: 0,
            lng: 0
        },
        zoom: 14
    });

    const [locations, setLocations] = useState({ 'family': [], 'own': [] });
    const [focusLocation, setFocusLocation] = useState(undefined)
    const [newLocationCoords, setNewLocationCoords] = useState({ lat: 0, lng: 0 })
    const [focusLocationCoords, setFocusLocationCoords] = useState(false)

    useEffect(() => {
        loadLocations(setLocations);
    }, [])

    return <div className="home">
        <div className="left">
            <Map locations={locations}
                coords={coords}
                setCoords={setCoords}
                setLocations={setLocations}
                focusLocation={focusLocation}
                newLocationCoords={newLocationCoords}
                focusLocationCoords={focusLocationCoords}
                setFocusLocation={setFocusLocation}
                setNewLocationCoords={setNewLocationCoords}
                setFocusLocationCoords={setFocusLocationCoords}
            />
        </div>
        <div className="right"><Panel locations={locations} setFocusLocationCoords={setFocusLocationCoords} setFocusLocation={setFocusLocation} setCoords={setCoords} /></div>
    </div>
}

export default Home;