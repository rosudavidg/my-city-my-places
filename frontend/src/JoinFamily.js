import { useHistory } from "react-router-dom";
import { useEffect } from 'react';
import axios from "axios"

const join = (token, history) => {
    axios
        .get(`http://localhost:5000/api/families/join/${token}`, {
            headers: {
                Authorization: `Bearer ${localStorage.getItem("token")}`,
            },
        })
        .then((res) => {
            history.push('/')
        })
        .catch((e) => {
            alert("Cannot join family")
            history.push('/')
        });
}

const JoinFamily = ({ token }) => {
    const history = useHistory();

    useEffect(() => {
        join(token, history)
    }, [])

    return <></>
}

export default JoinFamily;
