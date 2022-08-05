# Implementing OAuth 2.0

OAuth2 is an authentication protocol that is used to authenticate and authorize users in an application by using another service provider.

There are three parties in any OAuth mechanism:

The client - The person, or user who is trying to log in
The consumer - The application that the client wants to log into (which is Gitlab in this example)
The service provider - The external application that authenticates the users identity. (which is Github in this example)
In this post, we’ll create a Node.js HTTP server (consumer) that uses Github’s OAuth2 API (service provider) to authenticate the user (client).

Let’s look at an overview of how this would work in practice.

<img src="./node-oauth.svg">

## Requirements

Create a basic client / server application using Oauth 2.0 to register a user and login to an application