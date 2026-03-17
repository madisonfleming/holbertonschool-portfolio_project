import React, { useState, useCallback, useEffect } from 'react';
import { pdf } from '@react-pdf/renderer';
import ExportCertificate from './WeeklyCertificate'; // PDF component
import './ExportButton.css'
import { useChild } from '../../contexts/ChildContext';
import { useMilestones } from '../../contexts/MilestonesContext';
import { previewPdf } from '../../utils/certificatePdf';

export const ExportButton = ({ selectedChild }) => {

    const [isLoading, setIsLoading] = useState(false);
    //get single reward from endpoint
    const { getSingleWeeklyReward } = useMilestones();
    const [certificateData, setCertificateData] = useState([]);

    //get the reward data
    useEffect(() => {
        if (!selectedChild?.id) return;

        async function fetchSingleReward() {
            const singleReward = await getSingleWeeklyReward(selectedChild.id);
            console.log("getSingleWeeklyReward returns:", singleReward)

        setCertificateData(singleReward);
    }
    fetchSingleReward();
}, [selectedChild]);

    //Generate PDF from ExportCertificate
    // link the data to receive
    // link the child
    const generatePdf = useCallback(async () => {
        if (certificateData) {
            setIsLoading(true);

            try {
                const pdfBlob = await pdf(
                    <ExportCertificate data={certificateData} selectedChild={selectedChild} />
                ).toBlob();

                const pdfBlobUrl = URL.createObjectURL(pdfBlob);

                return pdfBlobUrl;
            } finally {
                setIsLoading(false);
            }
        }
        return null;
    }, [certificateData], [selectedChild]);

    //DOWNLOAD CERTIFICATE
    const downloadPdf = async () => {
        const pdfBlobUrl = await generatePdf();

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
    const previewPdf = async () => {
        const pdfBlobUrl = await generatePdf();

        if (pdfBlobUrl) {
            window.open(pdfBlobUrl, '_blank');
        }
    };
    //Just render Preview reward in a div rather than btn.
    //style when you call the func
    return (
            <div>
                <button onClick={(previewPdf)}>Preview</button>
                <button onClick={(downloadPdf)}>Download</button>
        </div>
    );
}
export default ExportButton;
