import "./Panel.css"
import { Tabs, Tab, Button } from 'react-bootstrap';
import Locations from "./Locations"
import Family from "./Family"
import Export from "./Export"
import { useHistory } from "react-router-dom";

const Panel = ({ locations, setFocusLocationCoords, setFocusLocation, setCoords }) => {
    const history = useHistory();

    const onClickLogout = (event) => {
        event.preventDefault()
        localStorage.removeItem('token')
        history.go(0)
    }

    return <div className="panel">
        <Button variant="dark" type="submit" onClick={onClickLogout}>
            Log out
        </Button>
        <Tabs defaultActiveKey="locations" className="tab">
            <Tab eventKey="locations" title="Locations">
                <Locations locations={locations} setFocusLocationCoords={setFocusLocationCoords} setFocusLocation={setFocusLocation} setCoords={setCoords} />
            </Tab>
            <Tab eventKey="family" title="Family">
                <Family />
            </Tab>
            <Tab eventKey="export" title="Export">
                <Export />
            </Tab>
        </Tabs>
    </div >
}

export default Panel;