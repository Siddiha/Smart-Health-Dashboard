import axios from 'axios';

const API_BASE_URL = 'https://api.example.com'; // Replace with your actual API base URL

export const fetchHealthData = async () => {
    try {
        const response = await axios.get(`${API_BASE_URL}/health-data`);
        return response.data;
    } catch (error) {
        console.error('Error fetching health data:', error);
        throw error;
    }
};

export const updateHealthData = async (data) => {
    try {
        const response = await axios.put(`${API_BASE_URL}/health-data`, data);
        return response.data;
    } catch (error) {
        console.error('Error updating health data:', error);
        throw error;
    }
};

export const deleteHealthData = async (id) => {
    try {
        const response = await axios.delete(`${API_BASE_URL}/health-data/${id}`);
        return response.data;
    } catch (error) {
        console.error('Error deleting health data:', error);
        throw error;
    }
};