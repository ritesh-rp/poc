import { Box } from "@mui/material";
import GetPrediction from "./components/GetPrediction";

function App() {
  return (
     <Box display={"flex"} justifyContent={"center"} alignItems={"center"} height={"100vh"} sx={{
      background:"blue"
     }}>
      <GetPrediction/>
     </Box>
  );
}

export default App;
