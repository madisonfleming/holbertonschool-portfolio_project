import "./Container2.css";

export const Container2 = () => {
  return (
    <div>
      <div className="suggested-books">
        {/* Suggested Books Section */}
        <p className="title">Suggested Books</p>
        {/* TO DO : Carosoul of book images */}
        <div className="row-books">
          <img className="img" src="/books/book1.jpg"></img>
          <img className="img" src="/books/book2.jpg"></img>
          <img className="img" src="/books/book3.jpg"></img>
          <img className="img" src="/books/book4.webp"></img>
          <img className="img" src="/books/book5.jpg"></img>
          <img className="img" src="/books/book6.jpg"></img>
          <img className="img" src="/books/book7.jpeg"></img>
          <img className="img" src="/books/book8.jpg"></img>
          <img className="img" src="/books/book9.jpg"></img>
          <img className="img" src="/books/book10.jpg"></img>
          <img className="img" src="/books/book11.jpeg"></img>
          <img className="img" src="/books/book12.jpg"></img>
          <img className="img" src="/books/book13.jpg"></img>
          <img className="img" src="/books/book14.jpg"></img>
          <img className="img" src="/books/book15.jpg"></img>
          <img className="img" src="/books/book16.jpg"></img>
        </div>
      </div>
      {/* Divider */}

      {/* Reading Session section */}
      <div className="reading-session">
        <div className="row-layout">
          <div className="heading">
            <p className="title">Log every reading session</p>
            <img className="book-container" src="/open-book.png?url"></img>
          </div>
        </div>
        {/* TO DO : Add Book + avatars */}
        <div className="row-avatars">
          <img src="/books/reading-popup.png" className="reading-popup"></img>
        </div>
      </div>
      {/* Divider */}

      {/* Weekly Reward section */}
      <div className="weekly-reward">
        <p className="title">
          Earn rewards for completing themed books every week
        </p>
        {/* TO DO : Add images of weekly rewards */}
        <div className="row-images">
          <img src="/themes/dinosaur.png"></img>
          <img src="/themes/Elephant.png"></img>
          <img src="/themes/rocket.png"></img>
          <img src="/themes/seahorse.png"></img>
        </div>
      </div>
    </div>
  );
};
export default Container2;
