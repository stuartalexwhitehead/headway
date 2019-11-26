import * as nconf from 'nconf';
import * as winston from 'winston';

export default (): void => {
    const level = nconf.get('log_level');
    const silent = nconf.get('log_silent');

    winston.configure({
        transports: [
          new winston.transports.Console({
              level,
              silent,
          }),
        ],
    });
};
