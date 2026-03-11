import React, { useState, useEffect, useContext } from "react";
import { useAuth } from "./AuthContext";
import { useChild } from "./ChildContext";

const BooksContext = React.createContext();

export function useBooks() {
  return useContext(BooksContext);
}

export function BooksProvider({ children }) {
  const [BooksList, setBooksList] = useState([]);
  const { currentUser } = useAuth();
  const { selectedChild } = useChild();

  const [readingSession, setReadingSession] = useState([]);

  //ENDPOIN TO LOAD ALL THE BOOKS (not implemented yet is for show reading history)
  async function loadBooks(q) {
    try {
      const token = await currentUser.getIdToken();
      const response = await fetch(`http://127.0.0.1:8000/api/books/search?q=${q}/limit=30`,
        {
          headers: { Authorization: `Bearer ${token}` },
        },
      );

      const BooksData = await response.json();
      console.log("this is book data:", BooksData)
      const formatted = BooksData.map((book) => ({
        id: book.book_id,
        title: book.title,
        img: book.cover_url,
      }));

      setBooksList(formatted);
      console.log("Books list is:", setBooksList);
    } catch (error) {
      console.error("Error fetch book", error);
      return BooksList;
    }
  }


  //ENDPOINT TO SEARCH FOR BOOK BY QUERY the str required frm the BE
  async function searchBooks(q) {
    try {
      const token = await currentUser.getIdToken();
      /* encodeURIComponent converts the quary (q) like cat into something the URL can take, I delete to test and work without it lol  */
      const resp = await fetch(
        `http://127.0.0.1:8000/api/books/search?q=${q}`,
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        },
      );

      const data = await resp.json();
      /*in case we get an error and not an array  */
      if (!Array.isArray(data)) {
        console.error("Expected an array but got:", data);
        return [];
      }
      /* we need to add an if in case the data is error so map is not going to work but works good is just best */
      console.log("DATA FROM BACKEND BOOKS:", data);
      return data.map((book) => ({
        id: book.book_id,
        title: book.title,
        img: book.cover_url,
        external_id: book.external_id,
        source: book.source,
        author: book.author,
      }));
    } catch (error) {
      console.error("Error searching books", error);
      return [];
    }
  }


  //GET READING SESSIONS

  // To display as reading activity on figma we need the cover URL. data is not working
  // To display EDIT reading sessions we also need BOOK TITLE in payload
    async function readingSessions(id) {
      console.log("child_id data:", id)
      
    try {
      const token = await currentUser.getIdToken();
      //const child = useState(selectedChild);
      /* reading-session endpoint  */
      const response = await fetch(
        `http://127.0.0.1:8000/api/children/${id}/reading-sessions`,
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        },
      );

      const data = await response.json();
      /* we need to add an if in case the data is error  */
      console.log("READING SESSION DATA from BACKEND:", data);
      return data.map((readingSession) => ({
        id: readingSession.session_id,
        childId: readingSession.child_id,
        bookId: readingSession.book_id
      }));

    } catch (error) {
      console.error("Error getting reading sessions", error);
      return [];
    }
    
  }

  //UPDATE READING SESSIONS
      async function updateReadingSessions(session_id, updatedData) {
        console.log("id data:", session_id)
        console.log("PUT payload:", updatedData);
    try {
      const token = await currentUser.getIdToken();
  
      /* update-reading-session endpoint  */
      const response = await fetch(
        `http://127.0.0.1:8000/api/reading-sessions/${session_id}`,
        {
          method: "PUT",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${token}`,
          },
          body: JSON.stringify(updatedData),
        },
      );

      const data = await response.json();
      /* we need to add an if in case the data is error  */
      console.log("Answer from BE of Updating Reading Session:", data);

      setReadingSession(data)

    } catch (error) {
      console.error("Error updating reading sessions", error);
      return [];
    }
    
  }


  return (
    <BooksContext.Provider value={{ searchBooks, loadBooks, BooksList, readingSessions, updateReadingSessions }}>
      {children}
    </BooksContext.Provider>
  );
}
