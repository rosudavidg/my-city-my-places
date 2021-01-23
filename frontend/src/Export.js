import './Export.css';
import { useState } from "react"
import { Form, Button } from 'react-bootstrap';
import axios from "axios";
import { useHistory } from "react-router-dom";

const exportTo = (email, history) => {
    axios
        .post('http://localhost:5000/api/exports', { email }, {
            headers: {
                Authorization: `Bearer ${localStorage.getItem("token")}`,
            },
        })
        .then((res) => {
            history.go(0)
        })
        .catch((e) => {
            alert("Cannot export")
        });
}

function Export() {
    const [email, setEmail] = useState('');
    const history = useHistory();

    const onChangeEmail = (e) => {
        e.preventDefault();
        setEmail(e.target.value)
    }

    const onClickExport = (e) => {
        e.preventDefault();

        exportTo(email, history);
    }

    return <div className="export-button">
        <Form.Group controlId="formGridEmail">
            <Form.Control type="email" placeholder="Enter email" onChange={onChangeEmail} value={email} />
        </Form.Group>
        <Button variant="primary" type="submit" onClick={onClickExport}>
            Export
        </Button>
    </div>
}

export default Export;
