import React from 'react';
import { Document, Page, Text, View, StyleSheet, Image } from '@react-pdf/renderer';
import { useChild } from '../../contexts/ChildContext';
/* document-container: the root container for pdf document
page: represents a apge within the document
view: a container component that can be used to group and style other components
text: component for display text content
Image: use to display local and network jpeg or png images into pdf
PDFDownloadLink: anchor tag to enable generating and downloading pdf documents
*/

const styles = StyleSheet.create({
  page: {
    flexDirection: 'row',
    justifyContent: 'center',
    alignItems: 'center',
    textAlign: 'center',
    position: 'relative',
    padding: '15',
    border: '2 solid #D2CECE'
  },
  section: {
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
  pageBackground: {
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
      <Page size="A5" orientation="landscape" style={styles.page}>
        <Image src="/worm.png" style={styles.pageBackground} />
        <View style={styles.section}>
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
