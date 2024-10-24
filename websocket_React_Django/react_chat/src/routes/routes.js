import { Routes, Route } from "react-router-dom";
import Login from "../pages/Login";
import { Conversation } from "../pages/Conversation";
import { ChatComponent } from "../components/chatComponent";
import SignUp from "../pages/SignUp";
import { GroupChat } from "../components/groupChatComponent";
export const Router_view = () => {
    return (
        <Routes>
            <Route element={<Login />} path="/login" />
            <Route element={<Conversation />} path='/' >
                <Route element={<ChatComponent />} path="user/:conversationName" />
                <Route element={< GroupChat />} path="groups/:groupName" />
            </ Route>
            <Route element={<SignUp />} path="/signup" />
        </Routes>
    )
}