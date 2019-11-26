import * as nconf from 'nconf';

export default (): void => {
    nconf.env({ lowerCase: true, parseValues: true });
    nconf.required([
        'core_url',
        'port',
        'log_level',
        'log_silent',
    ]);
}
