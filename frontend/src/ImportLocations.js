import { useHistory } from "react-router-dom";
import { useEffect } from 'react';
import axios from "axios"

const importLocations = (id, history) => {
    axios
        .get(`http://localhost:5000/api/exports/${id}`, {
            headers: {
                Authorization: `Bearer ${localStorage.getItem("token")}`,
            },
        })
        .then((res) => {
            history.push('/')
        })
        .catch((e) => {
            alert("Cannot import")
            history.push('/')
        });
}

const ImportLocations = ({ id }) => {
    const history = useHistory();

    useEffect(() => {
        importLocations(id, history)
    }, [])

    return <></>
}

export default ImportLocations;
