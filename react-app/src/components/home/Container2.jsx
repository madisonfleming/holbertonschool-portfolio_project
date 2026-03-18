import './Container2.css'

export const Container2 = () => {

    return (
        <div>
            <div className="suggested-books">
                {/* Suggested Books Section */}
                <p className='title'>Suggested Books</p>
                {/* TO DO : Carosoul of book images */}
            </div>
            {/* Divider */}
            <div className="divider"></div>

            {/* Reading Session section */}
            <div className='reading-session'>
                <p className='title'>Log every reading session</p>
                {/* TO DO : Add Book + avatars */}
                <div>
                    <img className='book-container' src='/open-book.png?url'></img>
                </div>
                <div className="row-avatars">
                    <img src='/avatars/mlb-avatar-apple.svg'></img>
                    <img src='/avatars/mlb-avatar-bee.svg'></img>
                    <img src='/avatars/mlb-avatar-robot.svg'></img>
                    <img src='/avatars/mlb-avatar-sun.svg'></img>
                </div>
            </div>
            {/* Divider */}
            <div className="divider"></div>

            {/* Weekly Reward section */}
            <div className="weekly-reward">
                <p className="title">Earn rewards for completing themed books every week</p>
                {/* TO DO : Add images of weekly rewards */}
                <div className='row-images'>
                    <img src='/themes/dinosaur.png'></img>
                    <img src='/themes/Elephant.png'></img>
                    <img src='/themes/rocket.png'></img>
                    <img src='/themes/seahorse.png'></img>
                </div>
            </div>
        </div>
    )
};
export default Container2;
