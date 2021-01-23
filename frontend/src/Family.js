import './Family.css';
import { useState, useEffect } from "react"
import { Form, Card, Button } from 'react-bootstrap';
import axios from "axios";
import { useHistory } from "react-router-dom";

const loadFamily = (setFamily) => {
    axios
        .get('http://localhost:5000/api/families', {
            headers: {
                Authorization: `Bearer ${localStorage.getItem("token")}`,
            },
        })
        .then((res) => {
            setFamily(res.data)
        })
        .catch((e) => {
            alert("Cannot get family")
        });
}

const inviteMember = (email, history) => {
    axios
        .post('http://localhost:5000/api/families/invitations', { email }, {
            headers: {
                Authorization: `Bearer ${localStorage.getItem("token")}`,
            },
        })
        .then((res) => {
            history.go(0)
        })
        .catch((e) => {
            alert("Cannot send invitation")
        });
}

const leaveFamily = (history) => {
    axios
        .get('http://localhost:5000/api/families/leave', {
            headers: {
                Authorization: `Bearer ${localStorage.getItem("token")}`,
            },
        })
        .then((res) => {
            history.go(0)
        })
        .catch((e) => {
            alert("Cannot leave family")
        });
}


const deleteFamily = (history) => {
    axios
        .delete('http://localhost:5000/api/families', {
            headers: {
                Authorization: `Bearer ${localStorage.getItem("token")}`,
            },
        })
        .then((res) => {
            history.go(0)
        })
        .catch((e) => {
            alert("Cannot delete family")
        });
}

const createFamily = (history) => {
    axios
        .post('http://localhost:5000/api/families', {}, {
            headers: {
                Authorization: `Bearer ${localStorage.getItem("token")}`,
            },
        })
        .then((res) => {
            history.go(0)
        })
        .catch((e) => {
            alert("Cannot create family")
        });
}

const CreateFamily = () => {
    const history = useHistory();

    const onClickCreate = () => {
        createFamily(history);
    }

    return <div className="family">
        <Button variant="success" onClick={onClickCreate}>
            Create family
        </Button>
    </div>
}

const FamilyMembers = ({ family }) => {
    return <div className="family-members">
        {family.members.map((member, id) => {
            return <div key={`member-${id}`} className="family-member">
                <Card
                    style={{ width: '18rem' }}
                    className="mb-2"
                >
                    <Card.Header>
                        Member
                    </Card.Header>
                    <Card.Body>
                        <Card.Title>{member.nickname}</Card.Title>
                    </Card.Body>
                </Card>
            </div>
        })}
    </div>
}

const FamilyOwner = () => {
    const [email, setEmail] = useState('');
    const history = useHistory();

    const onChangeEmail = (e) => {
        e.preventDefault();
        setEmail(e.target.value)
    }

    const onClickInvite = (e) => {
        e.preventDefault();

        inviteMember(email, history);
    }

    const onClickDelete = (e) => {
        e.preventDefault();
        deleteFamily(history);
    }

    return <div className="family-button">
        <Form.Group controlId="formGridEmail">
            <Form.Control type="email" placeholder="Enter email" onChange={onChangeEmail} value={email} />
        </Form.Group>

        <Button variant="primary" type="submit" onClick={onClickInvite}>
            Invite
        </Button>

        <Button variant="danger" className="offset" onClick={onClickDelete}>
            Delete family
        </Button>
    </div>
}

const FamilyMember = () => {
    const history = useHistory();

    const onClickLeave = (e) => {
        e.preventDefault();
        leaveFamily(history);
    }
    return <div className="family-button">
        <Button variant="danger" onClick={onClickLeave}>
            Leave family
        </Button>
    </div>
}

function Family() {
    const [family, setFamily] = useState({
        'family_id': null
    })

    useEffect(() => {
        loadFamily(setFamily)
    }, [])

    if (family['family_id'] === null) {
        return <CreateFamily />
    } else {
        if (family['is_owner']) {
            return <>
                <FamilyOwner />
                <FamilyMembers family={family} />
            </>
        } else {
            return <>
                <FamilyMember />
                <FamilyMembers family={family} />
            </>
        }
    }
}

export default Family;
