export interface User {
  id: number;
  email: string;
  is_active: boolean;
  is_superuser: boolean;
}

export interface CreateUserPayload {
  email: string;
  password: string;
}

export type UpdateUserPayload = Partial<CreateUserPayload>;
