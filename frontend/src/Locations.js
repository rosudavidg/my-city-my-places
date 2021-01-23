import "./Locations.css"
import { Card, Button } from 'react-bootstrap';

const Location = ({ location, owned, setFocusLocationCoords, setFocusLocation, setCoords }) => {
    const title = owned ? `${location.user_nickname}'s location` : 'Your location'

    const onClickView = (e) => {
        e.preventDefault();
        setFocusLocationCoords(false)
        setFocusLocation(location)

        setCoords({
            center: {
                lat: location.lat,
                lng: location.lng
            },
            zoom: 14
        })
    }

    return <div className="location-card">
        <Card
            style={{ width: '18rem' }}
            className="mb-2"
        >
            <Card.Header>
                <div className='locations-card-header'>
                    <div className='locations-card-header-title'>
                        {title}
                    </div>

                    <div className='locations-card-header-button'>
                        <Button variant="info" size="sm" onClick={onClickView}>
                            view
                    </Button>
                    </div>
                </div>
            </Card.Header>
            <Card.Body>
                <Card.Title>{location.name}</Card.Title>
            </Card.Body>
        </Card>
    </div>
}

const Locations = ({ locations, setFocusLocationCoords, setFocusLocation, setCoords }) => {
    return <>
        <div className="locations">
            {locations.own.map((location, id) => {
                return <Location key={`location-${id}`} location={location} setFocusLocationCoords={setFocusLocationCoords} setFocusLocation={setFocusLocation} setCoords={setCoords} />
            })}
            {locations.family.map((location, id) => {
                return <Location key={`location-${id}`} location={location} setFocusLocationCoords={setFocusLocationCoords} setFocusLocation={setFocusLocation} setCoords={setCoords} owned />
            })}
        </div >
        <div className="locations-line"></div>
    </>
}

export default Locations;