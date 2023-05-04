import axios from 'axios'

export const API_URL = 'http://127.0.0.1:5000'
export const client = axios.create({
  baseURL: API_URL,
  headers: {'Content-Type': 'application/json'}
})