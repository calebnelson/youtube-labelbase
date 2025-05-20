import { LLMResponse, Prompt, Video } from '@/utils/types';
import axios from 'axios';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export interface getPromptsResponse {
  prompts: Prompt[];
}

export interface getVideosResponse {
  videos: Video[];
}

export interface runPromptRequest {
  videoUrl: string;
  prompt: string;
}

export interface runPromptResponse {
  promptId: string;
  output: LLMResponse;
}

export const runPrompt = async (data: runPromptRequest): Promise<runPromptResponse> => {
  try {
    const response = await api.post<runPromptResponse>('/api/prompts/run_prompt', data);
    return response.data;
  } catch (error) {
    if (axios.isAxiosError(error)) {
      throw new Error(error.response?.data?.detail || 'Failed to run prompt');
    }
    throw error;
  }
};

export const getPrompts = async (): Promise<getPromptsResponse> => {
  try {
    const response = await api.get<Prompt[]>('/api/prompts');
    return { prompts: response.data };
  } catch (error) {
    if (axios.isAxiosError(error)) {
      throw new Error(error.response?.data?.detail || 'Failed to fetch prompts');
    }
    throw error;
  }
};

export const getVideos = async (): Promise<getVideosResponse> => {
  try {
    const response = await api.get<Video[]>('/api/videos');
    return { videos: response.data };
  } catch (error) {
    if (axios.isAxiosError(error)) {
      throw new Error(error.response?.data?.detail || 'Failed to fetch videos');
    }
    throw error;
  }
};