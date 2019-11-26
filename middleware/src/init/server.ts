import * as logger from "winston"
import { ApolloServer } from 'apollo-server';
import typeDefs from '../typeDefs';
import resolvers from '../resolvers';

export default (): void => {
  const server = new ApolloServer({ typeDefs, resolvers });

  server.listen().then(({ url }) => {
    logger.info(`🚀 Server ready at ${url}`);
  });
}