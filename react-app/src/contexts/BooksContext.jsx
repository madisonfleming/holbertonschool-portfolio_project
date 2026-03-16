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

  const [readingSessions, setReadingSessions] = useState([]);
  // load the current state of reading sessions
  const [loading, setLoading] = useState(true);

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
  async function loadData() {
    try {
      const token = await currentUser.getIdToken();
      /* reading-session endpoint  */
      const response = await fetch(
        `http://127.0.0.1:8000/api/children/${selectedChild.id}/reading-sessions`,
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        },
      );

      const data = await response.json();
      /* we need to add an if in case the data is error  */
      console.log("READING SESSION DATA from Backend:", data);

      if (!data) return;

      const formatted = data.map((session) => ({
        //mapping each session to display
        id: session.session_id,
        childId: session.child_id,
        bookId: session.book_id,
        title: session.book_title,
        img: session.cover_url,
      }));
      setReadingSessions(formatted);
      //set loading false
      //setLoading(false);
    } catch (error) {
      console.error("Error getting reading sessions", error);
      //setLoading(false);
      return [];
    }
  }

  //UPDATE READING SESSIONS
  async function updateReadingSessions(session_id, updatedData) {
    //show session_id in console
    console.log("session_id data:", session_id);
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

      //using set function to map and to update UI immediately
      setReadingSessions((prev) => {
        const updatedList = prev.map((item) => {
          if (item.id === session_id) {
            //search for the session to update
            // ... copy all the properties into a new object
            return {
              ...item,
              ...data,
              // if updated has a valid url use it, otherwise use old data
              img: data.cover_url ?? item.img,
            };
          } else {
            // item new data is not new, stay with old data
            return item;
          }
        });
        return updatedList;
      });

      //show fail error
      if (!response.ok) {
        console.error("Update fail", data);
      }
    } catch (error) {
      console.error("Error updating reading sessions", error);
      return [];
    }
  }

  //ENDPOINT TO CREATE A READING SESSION
  async function createReadingSession(readingSessionData) {
    if (!currentUser) return;

    const token = await currentUser.getIdToken();
    const response = await fetch("http://127.0.0.1:8000/api/reading-sessions", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
      },
      body: JSON.stringify(readingSessionData),
    });
    if (!response.ok) {
      console.error("Error creating reading session");
      return;
    }
    const newReadingSession = await response.json();
    // we received fron BE
    console.log(
      "Answer from BE of creating new reading session:",
      newReadingSession,
    );
    //mapping new reading session. ...prev means copy object and new data to new object
    setReadingSessions((prev) => [
      ...prev,
      {
        id: newReadingSession.session_id,
        childId: newReadingSession.child_id,
        bookId: newReadingSession.book_id,
        title: newReadingSession.title,
        img: newReadingSession.cover_url,
      },
    ]);
  }

  useEffect(() => {
    if (currentUser) loadData();
  }, [currentUser]);

  //use effect for no child selected yet
  useEffect(() => {
    if (!selectedChild) return;

    loadData(selectedChild);
  }, [selectedChild]);

  return (
    <BooksContext.Provider
      value={{
        searchBooks,
        loadData,
        BooksList,
        setBooksList,
        updateReadingSessions,
        readingSessions,
        setReadingSessions,
        createReadingSession,
      }}
    >
      {children}
    </BooksContext.Provider>
  );
}
