type Tokens = {
  access_token: string;
  refresh_token: string;
};
type LoginParams = {
  login: string;
  password: string;
};
export const sendLoginData = async ({
  login,
  password,
}: LoginParams): Promise<Tokens> => {
  const response = await fetch("http://127.0.0.1:8000/user/login", {
    method: "POST",
    headers: {
      "Content-Type": "application/x-www-form-urlencoded",
    },
    body: new URLSearchParams({
      username: login,
      password: password,
    }),
  });
  if (response.status >= 400) {
    throw new Error("Failed to login");
  }
  return await response.json();
};
