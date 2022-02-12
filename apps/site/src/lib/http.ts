import axios from 'axios';
import { variables } from '$lib/environment';

export const httpService = axios.create({
  baseURL: variables.basePath,
});
