/* eslint-disable @typescript-eslint/no-explicit-any */

export type Video = {
  id: number;
  youtube_id: string;
  title: string;
  description: string;
  video_metadata: any;
  created_at: string;
  updated_at: string | null;
  user_id: number;
}

export interface Output {
  id: string;
  video_id: number;
  prompt_id: string;
  llm_output: string;
  run_date: string;
  time_to_generate: number;
}

export interface Prompt {
  id: string;
  user_id: number;
  system_prompt?: string;
  user_prompt: string;
  created_at: string;
  updated_at?: string;
  outputs: Output[];
}

export type LLMResponse = {
  content: string;
  model: string;
  usage: {
    prompt_tokens: number;
    completion_tokens: number;
    total_tokens: number;
  }
}
