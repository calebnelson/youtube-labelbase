import { LLMResponse, LLMPrompt, Video } from '@/utils/types';
import axios from 'axios';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export interface getPromptsResponse {
  prompts: LLMPrompt[];
}

export interface getVideosResponse {
  videos: Video[];
}

export interface runPromptRequest {
  videoUrl: string;
  prompt: {
    id?: number;
    systemPrompt: string;
    userPrompt: string;
  }
}

export interface runPromptResponse {
  promptId: number;
  output: LLMResponse;
}

export const getPrompts = async (): Promise<getPromptsResponse> => {
  const response = await api.get<getPromptsResponse>('/api/prompts');
  return response.data;
};

export const getVideos = async (): Promise<getVideosResponse> => {
  const response = await api.get<getVideosResponse>('/api/videos');
  return response.data;
};

export const runPrompt = async (data: runPromptRequest): Promise<runPromptResponse> => {
  const response = await api.post<runPromptResponse>('/api/prompts', data);
  return response.data;
};