import AxiosInstance from "./Axios";
import { React, useState } from "react";
import Button from "@mui/material/Button";
import Box from "@mui/material/Box";
import FileUploadIcon from "@mui/icons-material/FileUpload";
import InvalidFile from "./InvalidFile";
import ParseFile from "./ParseFile";
import FieldUpload from "./FieldUpload";

function Home() {
  const [myData, setMydata] = useState([]);
  const [downloadFIle, setDownloadFile] = useState(false);
  const [validFile, setValidFile] = useState(true);
  const [messageError, setMessageError] = useState("");

  function handleFileUpload(event) {
    const file = event.target.files[0];
    console.log(file)
    const formData = new FormData();
    formData.append("file", file);
    AxiosInstance.post(`api/documents/`, formData, {
      headers: {
        "Content-Type": "multipart/form-data",
        "x-rapidapi-host": "file-upload8.p.rapidapi.com",
        "x-rapidapi-key": "your-rapidapi-key-here",
      },
    })
      .then((response) => {
        setMydata(response.data);
        setDownloadFile(true);
        setValidFile(true);

        console.log(response);
      })
      .catch((error) => {
        console.log(error.response.data.detail);
        setMessageError(error.response.data.detail);
        setValidFile(false);
        setDownloadFile(false);
      });
  }

  return (
    <div>
      <Box>
        {!downloadFIle && (
          <Box sx={{ mt: 15 }}>
            <FieldUpload handleFileUpload={handleFileUpload} />
          </Box>
        )}

        {downloadFIle && (
          <Box sx={{ mt: 15 }}>
            <ParseFile myData={myData} />
            <Box sx={{ display: "flex", justifyContent: "end" }}>
              <Button
                variant="contained"
                component="label"
                startIcon={<FileUploadIcon />}
                sx={{ mt: 2, mr: 10, mb: 5 }}
                size="large"
              >
                Upload More
                <input type="file" hidden onChange={handleFileUpload} />
              </Button>
            </Box>
          </Box>
        )}
        {!validFile && (
          <Box>
            <InvalidFile messageError={messageError} />
          </Box>
        )}
      </Box>
    </div>
  );
}
export default Home;
