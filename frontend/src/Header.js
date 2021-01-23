import 'bootstrap/dist/css/bootstrap.css';
import './Header.css';

import { useHistory } from "react-router-dom";

function Header() {
    const history = useHistory();

    const onClickHeader = (e) => {
        history.push("/");
    }

    return (
        <div className="header" onClick={onClickHeader}>My City - My Places</div>
    );
}

export default Header;
