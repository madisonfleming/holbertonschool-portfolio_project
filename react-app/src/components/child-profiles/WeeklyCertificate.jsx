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
const PURPLE = '#914ebe';
const PURPLE_LIGHT = '#E8E6F8';
const PURPLE_MID = '#9a6ecd';

//this style sheet use camelCase like React Native but the same css rules apply

const styles = StyleSheet.create({
  // pdf page
  page: {
    flexDirection: 'row', //center everything vertically
    justifyContent: 'center',
    alignItems: 'center',
    textAlign: 'center',
    position: 'relative',
    padding: '20',
    border: '2 solid PURPLE_LIGHT',
    fontFamily: 'Baloo 2',
  },
  innerBorder: {
    position: 'absolute',
    top: 5,
    left: 5,
    right: 5,
    bottom: 5,
    border: `2 solid ${PURPLE_MID}`,
    borderRadius: 10,
  },
    pageBackground: { //background image styling
    position: 'absolute',
    top: 12,
    left: 85,
    right: 85,
    bottom: 12,
    opacity: 0.5,
  },
  logo: {
    position: 'absolute',
    top: 29,
    left: 24,
    height: 80,
    width: 180,
    marginBottom: 40,
  },
  section: { //text section
    margin: 10,
    flexGrow: 1,
    position: 'relative',
    paddingTop: 100,
  },
  title: {
    fontSize: 13,
    color: PURPLE_MID,
    fontWeight: 700,
    textTransform: 'uppercase',
    marginBottom: 10,
    fontFamily: 'Baloo 2',
  },
  title2: {
    color: PURPLE_MID,
    fontWeight: 600,
    fontSize: 10,
    marginBottom: 10,
  },
  divider: {
    height: 2,
    width: 100,
    alignSelf: 'center',
    backgroundColor: PURPLE_MID,
    borderRadius: 5,
    marginBottom: 10,
  },
  description: {
    fontSize: 18,
    fontWeight: 800,
    color: PURPLE,
    marginBottom: 90,
    marginLeft: 135,
    marginRight: 135,
  },
  date: {
    fontSize: 12,
    position: 'absolute',
    bottom: 0,
    right: 5,
    fontFamily: 'Baloo 2',
    fontWeight: 400,
    color: PURPLE_MID,
  },
});

const WeeklyCertificate = ({ data }) => {
  const milestone = Array.isArray(data) ? data[0] : data;

  const formattedDate = milestone?.completed_at ? new Date(milestone.completed_at).toLocaleDateString('en-AU',
    { year: 'numeric', month: 'long', day: 'numeric' }) : "";

    //FOR THE WEEKLY GOAL 

  return (
    <Document>
      {/* document-container: the root container for pdf document */}
      {/* Page: represents a page within the document */}
      <Page size="A5" orientation="landscape" style={styles.page}>
        {/* Image: use to display local and network jpeg or png images into pdf */}
        <Image src="/star_cert.png" style={styles.pageBackground} />
        {/* Logo */}
        <Image src="/logo.png" style={styles.logo} />
        {/* Inner Border: dashed line */}
        <View style={styles.innerBorder}></View>
        {/* View: a container component that can be used to group and style other components */}
        <View style={styles.section}>
          {/* Text: component for displaying text content */}
          <Text style={styles.title} hyphenationCallback={hyphenationCallback}>Certificate of Achievement</Text>
          {/* Text: component for displaying text content */}
          <Text style={styles.title2} hyphenationCallback={hyphenationCallback}>You're a star!</Text>
          {/* Divider */}
          <View style={styles.divider}></View>
          <Text style={styles.description} hyphenationCallback={hyphenationCallback}>{milestone?.description}</Text>
          <Text style={styles.date}>Date: {formattedDate}</Text>
        </View>
      </Page>
    </Document>
  );
};

export default WeeklyCertificate;
