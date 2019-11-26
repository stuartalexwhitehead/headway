import * as nconf from 'nconf';
import * as rp from 'request-promise';

export default (): rp.RequestPromiseAPI => rp.defaults({
    json: true,
    simple: false,
    resolveWithFullResponse: true,
    baseUrl: nconf.get('core_url'),
});
