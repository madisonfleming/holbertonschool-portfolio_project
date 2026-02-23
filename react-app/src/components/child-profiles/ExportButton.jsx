import React, { useState, useCallback } from 'react';
import { pdf } from '@react-pdf/renderer';
import ExportCertificate from './ExportCertificate'; // PDF component
import './ExportButton.css'

const ExportButton = ({ certificateData }) => {
    // certificateData saved in child-profiles

    const [isLoading, setIsLoading] = useState(false);

    const generatePdf = useCallback(async () => {
        if (certificateData) {
            setIsLoading(true);

            try {
                const pdfBlob = await pdf(
                    <ExportCertificate data={certificateData} />
                ).toBlob();

                const pdfBlobUrl = URL.createObjectURL(pdfBlob);

                return pdfBlobUrl;
            } finally {
                setIsLoading(false);
            }
        }
        return null;
    }, [certificateData]);

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

    const previewPdf = async () => {
        const pdfBlobUrl = await generatePdf();

        if (pdfBlobUrl) {
            window.open(pdfBlobUrl, '_blank');
        }
    };
    return (
        <div>
            <button className="export-btn" onClick={previewPdf} disabled={isLoading}>
                Preview Reward in another tab
            </button>
            <button className="export-btn" onClick={downloadPdf} disabled={isLoading}>
                Download Reward
            </button>
        </div>
    );
}
export default ExportButton;
