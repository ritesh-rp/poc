import React from 'react';
import conf from '../conf/config';
import { Client, Account, ID } from "appwrite";
import { useDispatch } from 'react-redux';
import { logout } from '../store/authSlice';

class AuthService {

    client = new Client()
    account;
    constructor() {
        this.client.setEndpoint(conf.appwriteUrl).setProject(conf.appwriteProjectId);
        console.log("auth account is", this.account)
        this.account = new Account(this.client)
        console.log("auth account is", this.account)
    }

    async createAccount(email, password, name) {
        try {
            console.log("creating account", email, password, name)
            const userAccount = await this.account.create(
                ID.unique(),
                email,
                password,
                name
                // ID.unique(),"abcd@abc.com","abcddf3142"
            );
            if (userAccount) {
                this.logIn(email, password)
            }
            else {
                return userAccount
            }
        }
        catch (error) {
            throw error;
        }
    }

    async logIn(email, password) {
        try {
            return await this.account.createEmailPasswordSession(email, password);
        }
        catch (error) {
            console.log(error);
            throw error
        }
    }

    async getCurrentUser() {
        try {
            return await this.account.get();
        } catch (error) {
            console.log(error);
            throw error;
        }
    }


    async logOut() {
        try {
            const user = await this.account.get();
            if (user.$id) {
                await this.account.deleteSessions();
            } else {
                console.log("User is not authenticated");
            }
        }
        catch (error) {
            console.log("logoutError.......", error);
            throw error
        }
    }
}

const authService = new AuthService()

export default authService