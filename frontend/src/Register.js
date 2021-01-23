import './Register.css';
import { Form, Button, Spinner } from 'react-bootstrap';
import { useState } from 'react';
import axios from "axios";
import { useHistory } from "react-router-dom";

function Register() {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [nickname, setNickname] = useState('');
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

    const onChangeNickname = (event) => {
        event.preventDefault();
        setNickname(event.target.value);
    };

    const onClickSubmit = (event) => {
        event.preventDefault()

        setAnimation("grow")
        axios
            .post('http://localhost:5000/api/users', {
                email, password, nickname
            })
            .then((res) => {
                alert('Successfully registered.');
                history.push('/login')
            })
            .catch((e) => {
                setAnimation("")
                alert('Register failed.');
            });
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

                <Form.Group controlId="formGridNickname">
                    <Form.Label>Nickname</Form.Label>
                    <Form.Control placeholder="Vasile Nebunu" onChange={onChangeNickname} value={nickname} />
                </Form.Group>

                <Button variant="primary" type="submit">
                    Register
                    <Spinner
                        animation={animation}
                        size="sm"
                        role="status"
                        aria-hidden="true"
                        visible="false"
                    />
                </Button>
            </Form>
        </div>
    );
}

export default Register;
