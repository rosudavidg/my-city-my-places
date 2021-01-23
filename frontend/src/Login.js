import './Login.css';
import { Form, Button, Spinner } from 'react-bootstrap';
import { useState } from 'react';
import { useHistory } from "react-router-dom";
import axios from "axios";

function Register({ setIsLoggedIn }) {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [animation, setAnimation] = useState('');

    const history = useHistory();

    const onChangeEmail = (event) => {
        event.preventDefault();
        setEmail(event.target.value);
    };

    const onChangePassword = (event) => {
        event.preventDefault();
        setPassword(event.target.value);
    };

    const onClickSubmit = (event) => {
        event.preventDefault()

        setAnimation("grow")
        axios
            .post('http://localhost:5000/api/login', {
                email, password
            })
            .then((res) => {
                localStorage.setItem("token", res.data.token);
                setIsLoggedIn(true)
                history.push('/')
            })
            .catch((e) => {
                setAnimation("")
                alert('Login failed.');
            });
    }

    const onClickRegister = (event) => {
        event.preventDefault()
        history.push('/register')
    }

    return (
        <div className="content">
            <Form onSubmit={onClickSubmit} className="custom-card">
                <Form.Group controlId="formGridEmail">
                    <Form.Label>Email</Form.Label>
                    <Form.Control type="email" placeholder="Enter email" onChange={onChangeEmail} value={email} />
                </Form.Group>

                <Form.Group controlId="formGridPassword">
                    <Form.Label>Password</Form.Label>
                    <Form.Control type="password" placeholder="Password" onChange={onChangePassword} value={password} />
                </Form.Group>

                <Button variant="primary" type="submit">
                    Login
                    <Spinner
                        animation={animation}
                        size="sm"
                        role="status"
                        aria-hidden="true"
                        visible="false"
                    />
                </Button>
            </Form>

            <div className="login-or-divider "> OR </div>
            <Button variant="success" type="submit" onClick={onClickRegister}>
                Register
            </Button>
        </div>
    );
}

export default Register;
