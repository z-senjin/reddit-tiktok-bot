//redditbotfortiktok@zach.com

import fetch from 'node-fetch';

const REDDIT_KEY = 'CdJbv_SlW4K_JvMmC3Zl_waKVt7Glg';
const RESPONSE_TYPE = 'code';
const RANDOM_STRING = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789';
const REDIRECT_URI = 'https://www.senjinsolutions.com';
const DURATION = 'permanent';
const SCOPE = 'identity';
const AUTH_URL = `https://www.reddit.com/api/v1/authorize?client_id=${REDDIT_KEY}&response_type=${RESPONSE_TYPE}&state=${RANDOM_STRING}&redirect_uri=${REDIRECT_URI}&duration=${DURATION}&scope=${SCOPE}`;

console.log(AUTH_URL);

const response = await fetch(AUTH_URL);

const body = await response;

console.log(body);