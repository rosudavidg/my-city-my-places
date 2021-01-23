import "./Map.css"
import GoogleMapReact from 'google-map-react';
import { useState } from "react";
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faMapMarkerAlt } from '@fortawesome/free-solid-svg-icons'
import { Toast, Button, Form } from 'react-bootstrap';
import axios from "axios";

const createLocation = (lat, lng, name, locations, setLocations, setFocusLocationCoords, setFocusLocation) => {
    axios
        .post('http://localhost:5000/api/locations', {
            name, lat, lng
        }, {
            headers: {
                Authorization: `Bearer ${localStorage.getItem("token")}`,
            },
        })
        .then((res) => {
            let locationsClone = { ...locations }
            let newLocation = {
                id: res.data.id, lat, lng, name
            }

            locationsClone.own.push(newLocation)
            setLocations(locationsClone)
            setFocusLocationCoords(false)
            setFocusLocation(newLocation)
        })
        .catch((e) => {
            alert("Cannot create location")
        });
}

const deleteLocation = (id, locations, setLocations, setFocusLocation) => {
    axios
        .delete(`http://localhost:5000/api/locations/${id}`, {
            headers: {
                Authorization: `Bearer ${localStorage.getItem("token")}`,
            },
        })
        .then((res) => {
            let locationsClone = { ...locations }
            let newOwnLocation = locationsClone.own.filter(e => e.id !== id)

            setLocations({
                family: locationsClone.family,
                own: newOwnLocation
            })

            setFocusLocation(undefined)
        })
        .catch((e) => {
            alert("Cannot delete location")
        });
}

const setCurrentLocation = (setCoords) => {
    navigator.geolocation.getCurrentPosition(function (position) {
        setCoords(
            {
                center: {
                    lat: position.coords.latitude,
                    lng: position.coords.longitude
                },
                zoom: 14
            }
        )
    })
}

const InfoLocation = ({ id, locations, setLocations, title, name, setFocusLocation, owned }) => {
    const onClickClose = (e) => {
        e.preventDefault();
        e.stopPropagation();
        setFocusLocation(undefined);
    }

    const onClickDelete = (e) => {
        e.preventDefault();
        e.stopPropagation();

        deleteLocation(id, locations, setLocations, setFocusLocation);
    }

    return <Toast onClose={onClickClose}>
        <Toast.Header>
            <strong className="mr-auto">{title}</strong>
            {owned &&
                <Button variant="danger" size="sm" onClick={onClickDelete}>
                    delete
                </Button>
            }
        </Toast.Header>
        <Toast.Body>
            <div>{name}</div>
        </Toast.Body>
    </Toast>
}

const OwnLocation = ({ location, focusLocation, setFocusLocation, setFocusLocationCoords, locations, setLocations, focusLocationCoords }) => {
    let infoLocation = <></>

    const onClickPin = (e) => {
        e.preventDefault();
        e.stopPropagation();
        setFocusLocationCoords(false)
        setFocusLocation(location)
    }

    if (focusLocation === location) {
        infoLocation = <InfoLocation locations={locations} setLocations={setLocations} id={location.id} title="Your location" name={location.name} setFocusLocation={setFocusLocation} owned={true} />
    }

    if (focusLocation === location || (focusLocation === undefined && focusLocationCoords === false)) {
        return <div className="location">
            {infoLocation}
            <FontAwesomeIcon icon={faMapMarkerAlt} color="red" size="3x" onClick={onClickPin} />
        </div>
    } else {
        return <></>
    }
}


const NewLocation = ({ newLocationCoords, setFocusLocationCoords, locations, setLocations, setFocusLocation }) => {
    const [name, setname] = useState("")
    const onClickClose = (e) => {
        e.preventDefault();
        e.stopPropagation();
        setFocusLocationCoords(false);
    }

    const onChangeName = (e) => {
        e.preventDefault();
        setname(e.target.value);
    }

    const onClickName = (e) => {
        e.stopPropagation();
    }

    const onClickSubmit = (e) => {
        e.preventDefault();
        e.stopPropagation();

        createLocation(newLocationCoords.lat, newLocationCoords.lng, name, locations, setLocations, setFocusLocationCoords, setFocusLocation);
    }

    return <div className="location">
        <Toast onClose={onClickClose}>
            <Toast.Header>
                <strong className="mr-auto">New location</strong>
                <Button variant="success" size="sm" onClick={onClickSubmit}>
                    create
            </Button>
            </Toast.Header>
            <Toast.Body>
                <Form.Group controlId="formGridName">
                    <Form.Control type="text" placeholder="Enter name" onClick={onClickName} onChange={onChangeName} value={name} />
                </Form.Group>
            </Toast.Body>
        </Toast>
        <FontAwesomeIcon icon={faMapMarkerAlt} color="green" size="3x" />
    </div>
}


const SharedLocation = ({ location, focusLocation, setFocusLocation, setFocusLocationCoords, focusLocationCoords }) => {
    let infoLocation = <></>

    const onClickPin = (e) => {
        e.preventDefault();
        e.stopPropagation();
        setFocusLocation(location)
        setFocusLocationCoords(false)
    }

    if (focusLocation === location) {
        infoLocation = <InfoLocation title={`${location.user_nickname}'s location`} name={location.name} setFocusLocation={setFocusLocation} />
    }

    if (focusLocation === location || (focusLocation === undefined && focusLocationCoords === false)) {
        return <div className="location">
            {infoLocation}
            <FontAwesomeIcon icon={faMapMarkerAlt} color="blue" size="3x" onClick={onClickPin} />
        </div>
    } else {
        return <></>
    }
}

const Map = ({ locations, setLocations, focusLocation, newLocationCoords, focusLocationCoords, setNewLocationCoords, setFocusLocationCoords, setFocusLocation, coords, setCoords }) => {
    setCurrentLocation(setCoords);

    const onClickMap = (e) => {
        setNewLocationCoords({ lat: e.lat, lng: e.lng })
        setFocusLocationCoords(true)
        setFocusLocation(undefined);
    }

    return (
        <div className="map">
            < GoogleMapReact
                bootstrapURLKeys={{ key: process.env.REACT_APP_GOOGLE_MAPS_API }}
                center={coords.center}
                zoom={coords.zoom}
                onClick={onClickMap}
                onChildMouseDown={() => { }}
            >
                {
                    focusLocationCoords && <NewLocation
                        lat={newLocationCoords.lat}
                        lng={newLocationCoords.lng}
                        newLocationCoords={newLocationCoords}
                        setFocusLocationCoords={setFocusLocationCoords}
                        locations={locations}
                        setLocations={setLocations}
                        setFocusLocation={setFocusLocation}
                    />
                }
                {
                    locations.own.map((location, id) => {
                        return <OwnLocation key={`location-${id}`}
                            lat={location.lat}
                            lng={location.lng}
                            location={location}
                            focusLocation={focusLocation}
                            setFocusLocation={setFocusLocation}
                            setFocusLocationCoords={setFocusLocationCoords}
                            locations={locations}
                            setLocations={setLocations}
                            focusLocationCoords={focusLocationCoords}
                        />
                    })
                }
                {
                    locations.family.map((location, id) => {
                        return <SharedLocation key={`location-${id}`}
                            lat={location.lat}
                            lng={location.lng}
                            location={location}
                            focusLocation={focusLocation}
                            setFocusLocation={setFocusLocation}
                            setFocusLocationCoords={setFocusLocationCoords}
                            focusLocationCoords={focusLocationCoords}
                        />
                    })
                }
            </GoogleMapReact >
        </div >
    );
}

export default Map;
