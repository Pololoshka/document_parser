import * as React from "react";
import { Typography } from "@mui/material";
import AppBar from "@mui/material/AppBar";
import Box from "@mui/material/Box";
import Toolbar from "@mui/material/Toolbar";
import MenuBookIcon from "@mui/icons-material/MenuBook";

function Bar(props) {
  const { content } = props;
  return (
    <React.Fragment>
      <AppBar
        position="fixed"
        sx={{ bgcolor: "#61dafb", color: "#000000", zIndex: "tooltip" }}
      >
        <Toolbar disableGutters>
          <Box sx={{ mr: 2, ml: 5 }}>
            <MenuBookIcon fontSize="large" />
          </Box>

          <Typography
            variant="h5"
            sx={{
              fontFamily: "monospace",
              fontWeight: 500,
              flexGrow: 1,
            }}
          >
            Assessing the importance of words in the context of a document
          </Typography>
        </Toolbar>
      </AppBar>
      <React.Fragment>{content}</React.Fragment>
    </React.Fragment>
  );
}

export default Bar;
