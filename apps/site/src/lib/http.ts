import axios from 'axios';
import { variables } from '$lib/environment';
import { AUTH_TOKEN_KEY } from './constants';

export const httpService = axios.create({
  baseURL: variables.basePath,
  headers: { authorization: `Bearer ${localStorage?.getItem(AUTH_TOKEN_KEY)}` },
});
