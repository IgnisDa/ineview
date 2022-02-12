import axios from 'axios';
import { variables } from './environment';

export const httpService = axios.create({
  baseURL: variables.basePath,
});
