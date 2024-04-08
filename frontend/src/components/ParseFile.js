import React from "react";
import { useMemo } from "react";
import Box from "@mui/material/Box";
import { MaterialReactTable } from "material-react-table";
import Typography from "@mui/material/Typography";
import Card from "@mui/material/Card";
import CardContent from "@mui/material/CardContent";

function ParseFile(props) {
  const { myData } = props;
  const columns = useMemo(
    () => [
      {
        accessorKey: "name",
        header: "Word",
        size: 150,
      },
      {
        accessorKey: "tf",
        header: "TF",
        size: 150,
      },
      {
        accessorKey: "idf",
        header: "IDF",
        size: 200,
      },
    ],
    []
  );
  return (
    <React.Fragment>
      <Card variant="outlined" sx={{ mx: 5, backgroundColor: "#c1faf5" }}>
        <CardContent>
          <Typography variant="body1">
            TF is the ratio of the number of occurrences of a certain word to
            the total number of words in the document.
          </Typography>
          <Typography variant="body1">
            IDF is the inverse of the frequency with which a certain word occurs
            in documents in a database collection. The resulting table is sorted
            by IDF.
          </Typography>
        </CardContent>
      </Card>
      <Box
        sx={{
          mt: 5,
          mx: 10,
        }}
      >
        <MaterialReactTable columns={columns} data={myData} />
      </Box>
    </React.Fragment>
  );
}

export default ParseFile;
