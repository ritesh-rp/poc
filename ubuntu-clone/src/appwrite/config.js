import conf from '../conf/config';
import { Client, Databases,Storage, ID, Query,Account } from "appwrite";


class Service{
    client = new Client()
    databases;
    bucket;
    constructor() {
        this.client.setEndpoint(conf.appwriteUrl).setProject(conf.appwriteProjectId);
        this.account = new Account(this.client)
        this.databases = new Databases(this.client)
        this.bucket = new Storage(this.client)
    }

    async createPost({title,slug,content,status,featuredImage,userId}){
        try{
            return await this.databases.createDocument(
                conf.appwriteDatabaseId,conf.appwriteCollectionId,slug,
                {
                    title,
                    content,
                    status,
                    userId,
                    featuredImage
                }
            )
        }
        catch(error){
            throw error
        }
    }

    async updatePost(slug,{title,content,status,featuredImage}){
        try{
            return await this.databases.updateDocument(
                conf.appwriteDatabaseId,conf.appwriteCollectionId,slug,
                {
                    title,
                    content,
                    status,
                    featuredImage
                }
            )
        }
        catch(error){
            throw error
        }
    }

    async deletePost(slug){
        try{
            return await this.databases.deleteDocument(conf.appwriteDatabaseId,conf.appwriteCollectionId,slug)
        }
        catch(error){
            throw error
        }
    }

    async getPost(slug){
        try{
            return await this.databases.getDocument(conf.appwriteDatabaseId,conf.appwriteCollectionId,slug)
        }
        catch(error){
            throw error
        }
    }


    async getPosts(queries = [Query.equal("status","active")]){
        try{
            return await this.databases.listDocuments(conf.appwriteDatabaseId,conf.appwriteCollectionId,queries)
        }
        catch(error){
            throw error
        }
    }

    async uploadFile(file){
        try{
            return await this.bucket.createFile(conf.appwriteBucketId,ID.unique(),file)
        }
        catch(error){
            throw error
        }
    }

    async deleteFile(fileId){
        try{
            return await this.bucket.deleteFile(conf.appwriteBucketId,fileId)
        }
        catch(error){
            throw error
        }
    }

    getFilePreview(fileId){
        try{
            return this.bucket.getFilePreview(conf.appwriteBucketId,fileId)
        }
        catch(error){
            throw error
        }
    }
}


const service = new Service()
export default service