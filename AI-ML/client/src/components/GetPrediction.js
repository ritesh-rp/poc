import { Box, Button, Typography, capitalize } from "@mui/material";
import AddSymptoms from "./AddSymptoms";

import { useEffect, useState } from "react";
import { allSymptomsList, sampleSymptomData } from "../symptomsData";
import { ReactComponent as Logo } from '../assets/logo.svg'

export default function GetPrediction() {
  const [selectedSymptoms, setSelectedSymptoms] = useState([]);
  const [prognosis, setPrognosis] = useState("");
  const [certainity, setCertainity] = useState(0);

  console.log({ sampleSymptomData });

  const handleSelectedSymptoms = (selectedItem) => {
    setSelectedSymptoms([...selectedItem]);
    setPrognosis("");
    setCertainity(0);
  };

  const fetchPrediction = async () => {
    const payload = createPayload(allSymptomsList, selectedSymptoms);

    console.log({ payload });

    const predictionReport = await postData(payload);
    setPrognosis(predictionReport?.predicted_prognosis);
    setCertainity(predictionReport?.certainty);

    console.log(predictionReport);
  };
  useEffect(() => {
    console.log("from main app", selectedSymptoms);
    if (!selectedSymptoms.length) {
      setPrognosis("");
      setCertainity(0);
    }
  }, [selectedSymptoms]);
  return (
    <Box
      width={"800px"}
      height={"90%"}
      border={"2px solid"}
      display={"flex"}
      flexDirection={"column"}
      padding={"1em"}
      borderRadius={"50px"}
      sx={{
        background: "white",
      }}
    >
       <Box display={"flex"} justifyContent={"center"} mb={2}>
        <Logo  />
      </Box>

      <Box
        border={"1px solid"}
        borderRadius={"10px"}
        padding={"5px"}
        mb={"1rem"}
        width={"fit-content"}
        display={"flex"}
        alignSelf={"center"}
        backgroundColor={"#1976d2"}

      >
        <Typography
          component={"h1"}
          color={"white"}
          textAlign={"center"}
          fontSize={"2rem"}
          fontWeight={"bold"}
          mb={1}
          margin={"10px"}
        >
          Prognosis By AI
        </Typography>
      </Box>
      <Box>
        <Box display={"flex"} justifyContent={"center"} mb={2}>
          <AddSymptoms
            selectedSymptoms={selectedSymptoms}
            setSelectedSymptoms={setSelectedSymptoms}
            allSymptoms={allSymptomsList}
          />
        </Box>
        <Typography fontWeight={"bold"}>
          Predicted Disease:{" "}
          <Typography component={"span"} color={"secondary"}>
            {" "}
            {prognosis || "none"}{" "}
          </Typography>
        </Typography>
        <Typography fontWeight={"bold"}>
          Certainity:{" "}
          <Typography component={"span"} color={"secondary"}>
            {" "}
            {`${Math.floor(certainity * 100)}%`}{" "}
          </Typography>
        </Typography>
        <Box display={"flex"} justifyContent={"center"} width={"100%"}>
          <Button variant="contained" size="small" onClick={fetchPrediction}>
            Get Prediction
          </Button>
        </Box>
        {sampleSymptomData?.map((item) => {
          return (
            <AddSymptomDataSample
              key={item?.prognosis}
              prognosis={item?.prognosis}
              selectedSymptoms={item.selectedItem}
              handleSelectedSymptoms={handleSelectedSymptoms}
            />
          );
        })}
      </Box>

      {/* <Stack direction="row" spacing={1} width={"fit-content"} flexWrap={"wrap"} justifyContent={"center"}>
        <Chip label="Custom delete icon" variant="outlined" style={{justifyContent:"start", width:"fit-content"}} />
        <Chip label="Custom delete icon" variant="outlined" />
        <Chip label="Custom delete icon" variant="outlined" />
        <Chip label="Custom delete icon" variant="outlined" />
        <Chip label="Custom delete icon" variant="outlined" />
        <Chip label="Custom delete icon" variant="outlined" />
        <Chip label="Custom delete icon" variant="outlined" />
        <Chip label="Custom delete icon" variant="outlined" />

      </Stack> */}
    </Box>
  );
}

function createPayload(allSymptomsList = [], selectedSymptoms = []) {
  const payload = {};
  allSymptomsList.forEach((item) => {
    payload[item.symptom] = 0;
  });
  selectedSymptoms.forEach((item) => {
    payload[item.symptom] = 1;
  });

  return payload;
}

async function postData(data = {}) {
  const url = "http://localhost:5000/predict";
  // Default options are marked with *
  const response = await fetch(url, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(data),
  });
  return response.json();
}

function AddSymptomDataSample({
  prognosis,
  selectedSymptoms,
  handleSelectedSymptoms,
}) {
  const updateSelectedSymptoms = () => {
    handleSelectedSymptoms(selectedSymptoms);
  };
  return (
    <Box mt={2}>
      <Box
        display={"flex"}
        alignItems={"center"}
        justifyContent={"space-between"}
      >
        <Typography color={"secondary"}>
          Sample Symptom Data For: {prognosis}
        </Typography>
        <Button
          variant="contained"
          size={"small"}
          onClick={updateSelectedSymptoms}
        >
          {" "}
          Add{" "}
        </Button>
      </Box>
    </Box>
  );
}
