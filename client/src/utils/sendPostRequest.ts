export const sendPostRequest = async ({
  url,
  data,
  baseUrl = "http://127.0.0.1:8000",
}: {
  url: string;
  data: object;
  baseUrl?: string;
}) => {
  const requestOptions = {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  };
  const resp = await fetch(baseUrl + url, requestOptions);
  if (!resp.ok) {
    throw new Error(`HTTP error! status: ${resp.status}`);
  }
  return await resp.json();
};
