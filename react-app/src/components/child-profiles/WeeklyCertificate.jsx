import React from 'react';
import { Document, Page, Text, View, StyleSheet, Image, Font } from '@react-pdf/renderer';
import Baloo2Regular from "../../assets/fonts/Baloo2-Regular.ttf";
import Baloo2SemiBold from "../../assets/fonts/Baloo2-SemiBold.ttf";


//register font family from google fonts
//font files saved in assets/fonts
Font.register({
  family: 'Baloo 2',
  fonts: [
    { src: Baloo2Regular, fontWeight: 'normal' },
    { src: Baloo2SemiBold, fontWeight: 'bold' },
  ]
});

//prevent hyphen mid-word
const hyphenationCallback = (word) => [word];

//create colour theme:
const PURPLE = '#995ac3';
const PURPLE_LIGHT = '#E8E6F8';
const PURPLE_MID = '#926ecd';

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
    border: '2 solid PURPLE_LIGHT',
    fontFamily: 'Baloo 2',
  }, 
  section: { //text section
    margin: 10,
    flexGrow: 1,
    position: 'relative',
    padding: 20,
  },
  title: {
    fontSize: 20,
    color: PURPLE_MID,
    fontWeight: 700,
    textTransform: 'uppercase',
    marginBottom: 40,
    fontFamily: 'Baloo 2',
    fontWeight: 'bold',
  },
  description: {
    fontSize: 35,
    fontWeight: 800,
    color: PURPLE,
    marginBottom: 40,
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
    opacity: 0.35,
  }
});

const WeeklyCertificate = ({ data }) => {
  const milestone = Array.isArray(data) ? data[0] : data;

  const formattedDate = milestone?.completed_at ? new Date(milestone.completed_at).toLocaleDateString('en-AU', 
    { year: 'numeric', month: 'long', day: 'numeric' }) : "";

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
          <Text style={styles.title} hyphenationCallback={hyphenationCallback}>Certificate of Achievement</Text>
          <Text style={styles.description} hyphenationCallback={hyphenationCallback}>{milestone?.description}</Text>
         <Text style={styles.date}>Date: {formattedDate}</Text>
        </View>
      </Page>
    </Document>
  );
};

export default WeeklyCertificate;
