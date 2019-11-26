import * as status from 'http-status-codes';
import { ForbiddenError, ApolloError } from 'apollo-server';
import request from '../utils/http';

interface AuthToken {
    token: string,
}

export default async function getAuthToken(parent, args): Promise<AuthToken> {
    const res = await request()({
        method: 'POST',
        uri: '/api/login/social/token/',
        body: {
            provider: "google-oauth2",
            code: args.code,
         },
    });

    if (res.statusCode !== status.OK) {
        throw new ForbiddenError('Token could not be retrieved');
    }

    if (!res.body.token) {
        throw new ApolloError('Token was not on response');
    }

    return { token: res.body.token };
};
