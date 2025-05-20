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

export type Prompt = {
  id: string;
  video_id: number;
  user_id: number | null;
  system_prompt: string | null;
  user_prompt: string;
  output: any | null;
  created_at: string;
  updated_at: string | null;
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
