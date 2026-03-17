import React from 'react';
import { Document, Page, Text, View, StyleSheet, Image } from '@react-pdf/renderer';
import { useChild } from '../../contexts/ChildContext';

//this style sheet use camelCase like React Native but the same css rules apply

const styles = StyleSheet.create({
  // pdf page
  page: {
    flexDirection: 'row', //center everything vertically
    justifyContent: 'center',
    alignItems: 'center',
    textAlign: 'center',
    position: 'relative',
    padding: '15',
    border: '2 solid #D2CECE'
  },
  section: {  //text section
    margin: 10,
    flexGrow: 1,
    position: 'relative',
    padding: 20,
  },
  title: {
    fontSize: 30,
    marginBottom: 25,
  },
  title2: {
    fontSize: 20,
    marginBottom: 25,
  },
  name: {
    fontSize: 30,
    marginBottom: 25,
    textDecoration: 'underline',
  },
  milestone: {
    fontSize: 20,
    marginBottom: 10,
  },
  milestone2: {
    fontSize: 25,
    marginBottom: 5,
  },
  date: {
    fontSize: 12,
    position: 'absolute',
    bottom: 0,
    left: 5,
  },
  pageBackground: { //background image styling
    position: 'absolute',
    top: 5,
    left: 5,
    right: 5,
    bottom: 5,
    opacity: 0.5,
  }
});

const ExportCertificate = ({ data, selectedChild }) => {


  return (
    <Document>
          {/* document-container: the root container for pdf document */}
      {/* Page: represents a page within the document */}
      <Page size="A5" orientation="landscape" style={styles.page}>
        {/* Image: use to display local and network jpeg or png images into pdf */}
        <Image src="/worm.png" style={styles.pageBackground} />
         {/* View: a container component that can be used to group and style other components */}
        <View style={styles.section}>
             {/* Text: component for displaying text content */}
          <Text style={styles.title}>Certificate of Achievement</Text>
         <Text style={styles.title2}>Proudly presented to</Text>
         <Text style={styles.name}>{selectedChild.name}</Text>
         <Text style={styles.milestone}>For completing</Text>
          <Text style={styles.milestone2}>{data.milestone}!</Text>
         <Text style={styles.date}>Date {data.date}</Text>
        </View>
      </Page>
    </Document>
  );
};

export default ExportCertificate;
