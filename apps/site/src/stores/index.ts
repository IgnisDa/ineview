import { localStorage, persist } from '@macfja/svelte-persistent-store';
import { writable } from 'svelte/store';

export const questions = persist<number[]>(
  writable(),
  localStorage(),
  'questions'
);

export const questions_set = persist<number>(
  writable(),
  localStorage(),
  'questions_set'
);

export const attempt_set = persist<number>(
  writable(),
  localStorage(),
  'attempt_set'
);
