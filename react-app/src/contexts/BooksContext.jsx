import React, { useState, useEffect, useContext } from "react";
import { useAuth } from "./AuthContext";

const BooksContext = React.createContext();

export function useBooks() {
  return useContext(BooksContext);
}

export function BooksProvider({ children }) {
  const [BooksList, setBooksList] = useState([]);
  const { currentUser } = useAuth();

  //ENDPOIN TO LOAD ALL THE BOOKS (not implemented yet is for show reading history)
  async function loadBooks() {
    try {
      const token = await currentUser.getIdToken();
      const respBooks = await fetch(
        "http://127.0.0.1:8000/api/books/search?q=a",
        {
          headers: { Authorization: `Bearer ${token}` },
        },
      );

      const BooksData = await respBooks.json();
      const formatted = BooksData.map((book) => ({
        id: book.book_id,
        title: book.title,
        img: book.cover_url,
      }));

      setBooksList(formatted);
    } catch (error) {
      console.error("Error fetch book", error);
    }
  }

  //ENDPOINT TO SEARCH FOR BOOK BY QUERY the str required frm the BE
  async function searchBooks(q) {
    try {
      const token = await currentUser.getIdToken();

      const resp = await fetch(
        `http://127.0.0.1:8000/api/books/search?q=${encodeURIComponent(q)}`,
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        },
      );

      const data = await resp.json();
      /* we need to add an if in case the data is error so map is not going to work but works good is just best */
      console.log("DATA FROM BACKEND BOOKS:", data);
      return data.map((book) => ({
        id: book.book_id,
        title: book.title,
        img: book.cover_url,
      }));
    } catch (error) {
      console.error("Error searching books", error);
      return [];
    }
  }

  return (
    <BooksContext.Provider value={{ BooksList, searchBooks }}>
      {children}
    </BooksContext.Provider>
  );
}
