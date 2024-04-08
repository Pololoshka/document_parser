import React from "react";
import Button from "@mui/material/Button";
import Typography from "@mui/material/Typography";
import FileUploadIcon from "@mui/icons-material/FileUpload";
import Card from "@mui/material/Card";
import CardContent from "@mui/material/CardContent";

function FieldUpload(props) {
  const { handleFileUpload } = props;
  return (
    <React.Fragment>
      <Card variant="outlined" sx={{ mx: 5, backgroundColor: "#ffa0a0" }}>
        <CardContent>
          <Typography variant="h6" sx={{ mb: 2 }}>
            Restrictions
          </Typography>

          <Typography variant="body1">
            The application only processes files with the .TXT extension and
            UTF-8 encoding. The file size must not exceed 1 MB. The application
            processes words from a file consisting only of letters of the
            English alphabet.
          </Typography>
        </CardContent>
      </Card>
      <Typography
        variant="h5"
        noWrap
        align="center"
        sx={{
          mt: 5,
          mx: 5,
        }}
      >
        Upload a file with the extension .TXT
      </Typography>
      <Button
        variant="contained"
        component="label"
        startIcon={<FileUploadIcon />}
        sx={{ m: 5, typography: "h6" }}
        size="large"
      >
        Upload File
        <input type="file" hidden onChange={handleFileUpload} />
      </Button>
    </React.Fragment>
  );
}
export default FieldUpload;
