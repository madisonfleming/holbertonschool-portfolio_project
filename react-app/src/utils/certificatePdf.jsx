import { pdf } from '@react-pdf/renderer';
import WeeklyCertificate from '../components/child-profiles/WeeklyCertificate'; // PDF component

//Generate PDF from WeeklyCertificate
// link the data to receive
// link the child
export const generatePdf = async (certificateData, selectedChildData) => {
    if (!certificateData) return null;

    const pdfBlob = await pdf(
        <WeeklyCertificate data={certificateData} selectedChild={selectedChildData} />
    ).toBlob();

    const pdfBlobUrl = URL.createObjectURL(pdfBlob);

    return pdfBlobUrl;
}


//DOWNLOAD CERTIFICATE
export const downloadPdf = async (certificateData, selectedChildData) => {
    const pdfBlobUrl = await generatePdf(certificateData, selectedChildData);

    if (pdfBlobUrl) {
        const downloadLink = document.createElement('a');
        downloadLink.href = pdfBlobUrl;
        downloadLink.download = `certificate${Date.now()}.pdf`;
        document.body.appendChild(downloadLink);
        downloadLink.click();
        document.body.removeChild(downloadLink);

        //clean memory so i can download multiple times
        URL.revokeObjectURL(pdfBlobUrl);
    }
};

//PREVIEW CERTIFICATE in new window
export const previewPdf = async (certificateData, selectedChildData) => {
    const pdfBlobUrl = await generatePdf(certificateData, selectedChildData);

    if (pdfBlobUrl) {
        window.open(pdfBlobUrl, '_blank');
    }
};
