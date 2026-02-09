import { Link } from 'react-router-dom'

const Header = () => {
    return (
        <nav>
        <Link to={'/home'}>Home</Link>
        <Link to={'/login'}>Login</Link>
        </nav>
    )
}

export default Header