import { useHistory } from "react-router-dom";
import { useEffect } from 'react';
import axios from "axios"

const activate = (token, history) => {
    axios
        .get(`http://localhost:5000/api/users/activate/${token}`)
        .then((res) => {
            history.push('/')
        })
        .catch((e) => {
            alert("Cannot activate")
            history.push('/')
        });
}

const Activate = ({ token }) => {
    const history = useHistory();

    useEffect(() => {
        activate(token, history)
    }, [])

    return <></>
}

export default Activate;
