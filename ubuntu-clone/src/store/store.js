import { configureStore } from "@reduxjs/toolkit";
import authSlice from "./authSlice";
import softwares from "./softwareSlice";

const store  = configureStore({
    reducer:{
        auth : authSlice,
        softwares : softwares,
    }
});

export default store;