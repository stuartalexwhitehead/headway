import initEnv from "./init/env";
import initLogging from "./init/logging";
import initServer from "./init/server";

// TODO: base HTTP request
// TODO: make getAuthToken resolver

(async function init(): Promise<void> {
    initEnv();
    initLogging();
    initServer();
})();
