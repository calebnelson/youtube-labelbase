export type Video = {
  id: number;
  url: string;
}

export type LLMPrompt = {
  id: number;
  prompt: string;
  systemPrompt: string;
}

export type LLMResponse = {
  id: number;
  video: Video;
  prompt: LLMPrompt;
  response: string;
}
