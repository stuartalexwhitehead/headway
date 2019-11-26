import { gql } from "apollo-server";

export default gql`
    type AuthToken {
        token: String
    }

    type Query {
        authToken(code: String!): AuthToken
    }
`;
