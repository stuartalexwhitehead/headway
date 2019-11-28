# Headway
## _In 33 seconds or less_
I’ve been exploring the topic of ‘feedback’ for the last few months. What makes for good feedback; when is the best time for it and how should it be delivered?

The more I explore, the clearer my opinions have become and the more I’ve realised there are patterns and principles to define.

That curiosity has led to Headway. Is it possible to codify the process of giving and receiving feedback?

Bonus points: I don’t get to code much at work these days, so Headway has been an opportunity to scratch that coding itch.

### Feedback modes
I’ve been synthesising my ideas down into what I’ve called Feedback Modes. These are the reasons or methods to give and receive feedback:

1. Request specific feedback from an individual (response may not be anonymous)
2. Request specific feedback from a group (responses may be anonymous)
3. Scheduled speculative feedback on conclusion of a project
4. Scheduled speculative feedback for a ritual (i.e. an Annual Review)
5. Unsolicited feedback from an individual
6. Feedback from yourself (i.e. self-reflection)

### The technology
I’m still experimenting :)

There are three main system components:

1. [`core`](./core) – A headless Django app. It uses Django Rest Framework and authentication via OpenID Connect with Google.
2. [`middleware`](./middleware) – A stateless GraphQL server (built with apollo-server). Queries resolve to the `core` APIs.
3. [`webapp`](./webapp) – A Single-Page Application built with create-react-app (is the plan, at least). Not yet started.

Some things I’ve found interesting so far:

- [multi-stage](./core/Dockerfile) Docker builds
- [federated authentication](https://github.com/st4lk/django-rest-social-auth) with Python/Django (lots of similar packages)
- [approaches to TypeScript](https://www.npmjs.com/package/ts-node) with Node.js
- linting/formatting comparison between Python and JavaScript (flake8/black vs eslint/prettier)
- [GraphQL Subscriptions](https://www.apollographql.com/docs/apollo-server/data/subscriptions/) (the plan is to send events with Redis pubsub between `core` and `middleware`)

Lots of ideas still to explore!