# JWT Authentication

JWT, an acronym for JSON Web Token, is an open standard that allows developers to verify the authenticity of pieces of information called claims via a signature. This signature can either be a secret or a public/private key pair. Together with the header and the payload, they can be used to generate or construct a JWT, as we will get to see later.

JWTs are commonly used for authentication or to safely transmit information across different parties. Here’s a common flow for JWT-based authentication systems: once a user has logged into an app, a JWT is created on the server and returned back to the calling client.

Each subsequent request will include the JWT as an authorization header, allowing access to protected routes and resources. Also, once the backend server verifies the signature is valid, it extracts the user data from the token as required. Note that in order to ensure a JWT is valid, only the party holding the keys or secret is responsible for signing the information.

### How JWT authentication works

In JWT authentication-based systems, when a user successfully logs in using their credentials, a JSON Web Token will be returned back to the calling client. Whenever the user wants to access a protected route or resource, the user agent sends the same JWT, typically in the Authorization header using the Bearer schema.

The content of the header should look like this:

```
Authorization: Bearer <token>
```

For a user to be granted access to a protected resource, the server routes will have to check for the presence of a valid JWT in the Authorization header. As a bonus, sending JWTs in the Authorization header also solves some issues related to CORS. This applies even if the app is served from an entirely different domain.

Note: Even if JWTs are signed, the information is still exposed to users or other parties because the data are unencrypted. Therefore, users are encouraged not to include sensitive information like credentials within a JWT payload. Additionally, tokens should always have an expiry.

### Token and refresh token

Tokens give users access to protected resources. They are usually short-lived and may have an expiration date attached to their headers. They may also contain additional information about the user.

Refresh tokens, on the other hand, allow users request new tokens. For example, after a token has expired, a client may perform a request for a new token to be generated by the backend server. For this to happen, a refresh token is required. In contrast to access tokens, refresh tokens are usually long-lived.

## Requirements

Create a basic client / server authentication process using JWT with a refresh token strategy.