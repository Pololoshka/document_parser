import React from "react";
import Typography from "@mui/material/Typography";
import Box from "@mui/material/Box";

function InvalidFile(props) {
  const { messageError } = props;
  return (
    <React.Fragment>
      <Typography variant="body1" noWrap align="center">
        <Box sx={{ color: "error.main" }}>{messageError}</Box>
      </Typography>
    </React.Fragment>
  );
}

export default InvalidFile;
