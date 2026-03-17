import React, { useState, useCallback, useEffect } from 'react';
import { pdf } from '@react-pdf/renderer';
import ExportCertificate from './ExportCertificate'; // PDF component
import './ExportButton.css'
import { useChild } from '../../contexts/ChildContext';
import { useMilestones } from '../../contexts/MilestonesContext';

export const ExportButton = ({ selectedChild, data }) => {

    const [isLoading, setIsLoading] = useState(false);

    console.log("data received in export btn:", data)
    console.log("selectedChild in export btn:", selectedChild)

    //Generate PDF from ExportCertificate
    // link the data to receive
    // link the child
    const generating = useCallback(async () => {
        if (data) {
            setIsLoading(true);

            try {
                const pdfBlob = await pdf(
                    <ExportCertificate data={data} selectedChild={selectedChild}/>
                ).toBlob();

                const pdfBlobUrl = URL.createObjectURL(pdfBlob);

                return pdfBlobUrl;
            } finally {
                setIsLoading(false);
            }
        }
        return null;
    }, [data, selectedChild]);

    //DOWNLOAD CERTIFICATE
    const downloading = async () => {
        const pdfBlobUrl = await generating();

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
    //change to previewing for books read cert
    const previewing = async () => {
        const pdfBlobUrl = await generating();

        if (pdfBlobUrl) {
            window.open(pdfBlobUrl, '_blank');
        }
    };
    //Just render Preview reward in a div rather than btn.
    //style when you call the func
    return (
            <div>
                <button className="export-btn" onClick={(previewing)} data={data} selectedChild={selectedChild} >Preview Reward</button>
                <button className="export-btn" onClick={(downloading)} data={data} selectedChild={selectedChild} >Download Reward</button>
        </div>
    );
}
export default ExportButton;
